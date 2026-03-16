"""
SQLite Loader - Swimm-Style Knowledge Base
Loads ProLeap-parsed COBOL data into SQLite with full statement-level detail.
Implements graph-based module detection.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console(force_terminal=True, highlight=False)


class SQLiteLoader:
    """Loads parsed and enriched COBOL data into SQLite knowledge base."""

    def __init__(self, db_path: str, schema_path: str = None):
        self.db_path = db_path
        self.schema_path = schema_path or "schemas/cobol_knowledge.sql"
        self.conn = None

    def connect(self):
        """Connect to the database and initialize schema."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

        if os.path.exists(self.schema_path):
            console.print(f"[cyan]Initializing database schema...[/cyan]")
            with open(self.schema_path, 'r') as f:
                schema_sql = f.read()
            self.conn.executescript(schema_sql)
            self.conn.commit()

        # Apply any schema migrations for columns added after initial release
        self._apply_migrations()

        console.print(f"[green]OK - Connected to {self.db_path}[/green]")

    def _apply_migrations(self):
        """Add new columns to existing tables — safe to run on any DB version."""
        new_columns = [
            ("programs", "migration_complexity",          "INTEGER"),
            ("programs", "complexity_reason",             "TEXT"),
            ("programs", "modern_equivalent",             "TEXT"),
            ("programs", "suggested_service",             "TEXT"),
            ("programs", "migration_approach",            "TEXT"),
            ("programs", "data_contracts",                "TEXT"),
            ("programs", "migration_risks",               "TEXT"),
            ("programs", "dependencies_to_migrate_first", "TEXT"),
        ]
        cursor = self.conn.cursor()
        for table, col, coltype in new_columns:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}")
            except Exception:
                pass  # Column already exists — that's fine
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    # ================================================================
    # Internal Helpers
    # ================================================================

    def _recreate_fts_triggers(self, cursor):
        """Re-create FTS sync triggers after bulk load."""
        triggers = [
            """CREATE TRIGGER IF NOT EXISTS programs_ai AFTER INSERT ON programs BEGIN
                INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
                VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
            END""",
            """CREATE TRIGGER IF NOT EXISTS programs_ad AFTER DELETE ON programs BEGIN
                INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
                VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
            END""",
            """CREATE TRIGGER IF NOT EXISTS programs_au AFTER UPDATE ON programs BEGIN
                INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
                VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
                INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
                VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
            END""",
            """CREATE TRIGGER IF NOT EXISTS data_items_ai AFTER INSERT ON data_items BEGIN
                INSERT INTO data_items_fts(rowid, name, business_name, description)
                VALUES (NEW.id, NEW.name, NEW.business_name, NEW.description);
            END""",
            """CREATE TRIGGER IF NOT EXISTS business_rules_ai AFTER INSERT ON business_rules BEGIN
                INSERT INTO business_rules_fts(rowid, rule_name, rule_statement, condition_text, action_text)
                VALUES (NEW.id, NEW.rule_name, NEW.rule_statement, NEW.condition_text, NEW.action_text);
            END""",
        ]
        for sql in triggers:
            try:
                cursor.execute(sql)
            except:
                pass

    # ================================================================
    # Loading Methods
    # ================================================================

    def update_business_context(self, program_id, data):
        """Specifically update business context fields for a program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE programs SET
                business_name = ?,
                business_purpose = ?,
                user_role = ?,
                business_process = ?
            WHERE program_id = ?
        """, (
            data.get("business_name"),
            data.get("business_purpose"),
            data.get("user_role"),
            data.get("business_process"),
            program_id
        ))
        self.conn.commit()

    def update_paragraph_narratives(self, program_id, paragraphs):
        """Specifically update narrative fields for paragraphs."""
        cursor = self.conn.cursor()
        for p in paragraphs:
            cursor.execute("""
                UPDATE paragraphs SET
                    business_name = ?,
                    narrative = ?,
                    purpose = ?
                WHERE program_id = ? AND paragraph_name = ?
            """, (
                p.get("business_name"),
                p.get("narrative"),
                p.get("purpose"),
                program_id,
                p.get("name")
            ))
        self.conn.commit()

    def load_programs(self, programs: List[Dict]):
        """Load program data including statements, calls, performs, CICS."""
        cursor = self.conn.cursor()

        # Drop FTS triggers temporarily for bulk load performance
        for trig in ["programs_ai", "programs_ad", "programs_au",
                      "data_items_ai", "business_rules_ai"]:
            try:
                cursor.execute(f"DROP TRIGGER IF EXISTS {trig}")
            except:
                pass
        # Disable foreign keys during bulk load for performance
        cursor.execute("PRAGMA foreign_keys = OFF")
        self.conn.commit()

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Loading programs...", total=len(programs))

            for program in programs:
                try:
                    program_id = program.get("program_id")

                    # Serialize list/dict fields to JSON text for storage
                    def _to_str(val):
                        if val is None:
                            return None
                        if isinstance(val, (list, dict)):
                            return json.dumps(val)
                        return val
                    deps_json = json.dumps(program.get("dependencies_to_migrate_first") or [])
                    data_contracts = _to_str(program.get("data_contracts"))
                    migration_risks = _to_str(program.get("migration_risks"))
                    migration_approach = _to_str(program.get("migration_approach"))

                    # Insert/replace program
                    cursor.execute("""
                        INSERT OR REPLACE INTO programs (
                            program_id, file_path, file_hash, program_type, line_count,
                            business_name, business_purpose, user_role, business_process,
                            migration_complexity, complexity_reason, modern_equivalent,
                            suggested_service, migration_approach, data_contracts,
                            migration_risks, dependencies_to_migrate_first,
                            updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        program_id,
                        program.get("file_path"),
                        program.get("file_hash"),
                        program.get("program_type"),
                        program.get("line_count"),
                        program.get("business_name"),
                        program.get("business_purpose"),
                        program.get("user_role"),
                        program.get("business_process"),
                        program.get("migration_complexity"),
                        program.get("complexity_reason"),
                        program.get("modern_equivalent"),
                        program.get("suggested_service"),
                        migration_approach,
                        data_contracts,
                        migration_risks,
                        deps_json,
                        datetime.now().isoformat()
                    ))

                    # Clear old data for this program
                    for table in ["paragraphs", "data_items", "files", "statements",
                                  "performs", "copybook_usage"]:
                        cursor.execute(f"DELETE FROM {table} WHERE program_id = ?", (program_id,))
                    # program_calls uses caller_program, not program_id
                    cursor.execute("DELETE FROM program_calls WHERE caller_program = ?", (program_id,))

                    # Insert paragraphs
                    for para in program.get("paragraphs", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO paragraphs (
                                program_id, paragraph_name, line_start, line_end,
                                business_name, narrative, purpose
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            para.get("name"),
                            para.get("line_start"),
                            para.get("line_end"),
                            para.get("business_name"),
                            para.get("narrative"),
                            para.get("purpose")
                        ))

                    # Insert data items
                    for item in program.get("data_items", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO data_items (
                                program_id, name, level_number, picture, usage, value,
                                section, parent_name, line_number,
                                business_name, description, data_type_description
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            item.get("name"),
                            item.get("level_number"),
                            item.get("picture"),
                            item.get("usage"),
                            item.get("value"),
                            item.get("section"),
                            item.get("parent_name"),
                            item.get("line_number"),
                            item.get("business_name"),
                            item.get("description"),
                            item.get("data_type_description")
                        ))

                    # Insert files
                    for f in program.get("files", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO files (
                                program_id, file_name, file_type, organization,
                                access_mode, record_name, business_name, description
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            program_id, f.get("file_name"), f.get("file_type"),
                            f.get("organization"), f.get("access_mode"),
                            f.get("record_name"), f.get("business_name"), f.get("description")
                        ))

                    # Insert ALL statements (new: this was empty before)
                    for stmt in program.get("statements", []):
                        details = {k: v for k, v in stmt.items()
                                   if k not in ("type", "line", "line_end", "paragraph", "raw_text")}
                        cursor.execute("""
                            INSERT OR REPLACE INTO statements (
                                program_id, paragraph_name, statement_type,
                                line_number, details_json
                            ) VALUES (?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            stmt.get("paragraph"),
                            stmt.get("type"),
                            stmt.get("line"),
                            json.dumps(details) if details else None
                        ))

                    # Insert calls
                    for call in program.get("calls", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO program_calls (
                                caller_program, called_program, call_location, line_number
                            ) VALUES (?, ?, ?, ?)
                        """, (
                            program_id,
                            call.get("called_program"),
                            call.get("call_location"),
                            call.get("line_number")
                        ))

                    # Insert performs
                    for perf in program.get("performs", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO performs (
                                program_id, source_paragraph, target_paragraph,
                                perform_type, line_number, condition
                            ) VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            perf.get("source_paragraph", "MAIN"),
                            perf.get("target_paragraph"),
                            perf.get("perform_type", "SIMPLE"),
                            perf.get("line_number"),
                            perf.get("condition")
                        ))

                    # Insert copybook usage
                    for cb in program.get("copybooks", []):
                        cursor.execute("INSERT OR IGNORE INTO copybooks (copybook_name) VALUES (?)", (cb,))
                        cursor.execute("""
                            INSERT OR REPLACE INTO copybook_usage (program_id, copybook_name) VALUES (?, ?)
                        """, (program_id, cb))

                except Exception as e:
                    import traceback
                    console.print(f"[yellow]Warning: Error loading {program.get('program_id')}: {e}[/yellow]")
                    traceback.print_exc()

                progress.advance(task)

        # Re-enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

        # Rebuild FTS indexes from content tables
        try:
            cursor.execute("INSERT INTO programs_fts(programs_fts) VALUES('rebuild')")
            cursor.execute("INSERT INTO data_items_fts(data_items_fts) VALUES('rebuild')")
            cursor.execute("INSERT INTO business_rules_fts(business_rules_fts) VALUES('rebuild')")
            self.conn.commit()
        except Exception as e:
            console.print(f"[yellow]Warning: FTS rebuild: {e}[/yellow]")

        # Re-create FTS triggers from schema
        try:
            self._recreate_fts_triggers(cursor)
            self.conn.commit()
        except Exception as e:
            console.print(f"[yellow]Warning: FTS trigger re-creation: {e}[/yellow]")

        console.print(f"[green]OK - Loaded {len(programs)} programs[/green]")

    def load_screens(self, screens: List[Dict]):
        """Load BMS screen definitions."""
        cursor = self.conn.cursor()
        for screen_data in screens:
            mapset = screen_data.get("mapset_name", "")
            for map_info in screen_data.get("maps", []):
                map_name = map_info.get("map_name", "")
                # Try to find associated program (skip FK if not found)
                prog = None
                for suffix in ["C", ""]:
                    candidate = mapset + suffix
                    cursor.execute("SELECT program_id FROM programs WHERE program_id = ?", (candidate,))
                    if cursor.fetchone():
                        prog = candidate
                        break

                cursor.execute("""
                    INSERT OR REPLACE INTO screens (
                        screen_name, map_name, mapset_name, file_path,
                        associated_program, business_name
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    map_name, map_name, mapset,
                    screen_data.get("file_path"),
                    prog, map_name
                ))

                screen_id = cursor.lastrowid

                 # Insert fields
                for fld in map_info.get("fields", []):
                    cursor.execute("""
                        INSERT OR REPLACE INTO screen_fields (
                            screen_id, field_name, field_type, length,
                            row_position, col_position, attributes,
                            business_name, description
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        screen_id,
                        fld.get("field_name"),
                        fld.get("field_type"),
                        fld.get("length"),
                        fld.get("row_position"),
                        fld.get("col_position"),
                        fld.get("attributes"),
                        fld.get("field_name"),
                        fld.get("initial_value", "")
                    ))

        self.conn.commit()
        console.print(f"[green]OK - Loaded {len(screens)} screens[/green]")

    def load_business_rules(self, rules: List[Dict]):
        """Load business rules into the database."""
        cursor = self.conn.cursor()
        for rule in rules:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO business_rules (
                        rule_id, rule_name, rule_statement, category,
                        program_id, paragraph_name, line_start, line_end,
                        condition_text, action_text, source_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rule.get("rule_id"), rule.get("rule_name"),
                    rule.get("rule_statement"), rule.get("category"),
                    rule.get("program_id"), rule.get("paragraph_name"),
                    rule.get("line_start"), rule.get("line_end"),
                    rule.get("condition"), rule.get("action"),
                    rule.get("source_code")
                ))
            except Exception as e:
                pass

        self.conn.commit()
        console.print(f"[green]OK - Loaded {len(rules)} business rules[/green]")

    def load_from_json(self, programs_json=None, rules_json=None,
                       enriched_json=None, screens_json=None):
        """Load data from JSON files."""
        if enriched_json:
            enriched_path = Path(enriched_json)
            if (enriched_path / "enriched_programs.json").exists():
                programs_json = str(enriched_path / "enriched_programs.json")
            if (enriched_path / "business_rules.json").exists():
                rules_json = str(enriched_path / "business_rules.json")

        if programs_json and Path(programs_json).exists():
            with open(programs_json, 'r') as f:
                raw = json.load(f)
            # Deduplicate: keep the entry with the most enrichment (has business_purpose)
            seen = {}
            for p in raw:
                pid = p.get("program_id", "")
                if pid not in seen or (p.get("business_purpose") and not seen[pid].get("business_purpose")):
                    seen[pid] = p
            self.load_programs(list(seen.values()))

        if rules_json and Path(rules_json).exists():
            with open(rules_json, 'r') as f:
                self.load_business_rules(json.load(f))

        if screens_json and Path(screens_json).exists():
            with open(screens_json, 'r') as f:
                self.load_screens(json.load(f))

    # ================================================================
    # Query Methods
    # ================================================================

    def get_all_programs(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT program_id, file_path, program_type, line_count,
                   business_name, business_purpose, user_role, business_process,
                   migration_complexity, complexity_reason, modern_equivalent,
                   suggested_service, migration_approach, data_contracts, migration_risks
            FROM programs ORDER BY program_id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_program_details(self, program_id: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM programs WHERE program_id = ?", (program_id,))
        program = cursor.fetchone()
        if not program:
            return None
        result = dict(program)

        for key, query in [
            ("paragraphs", "SELECT * FROM paragraphs WHERE program_id = ? ORDER BY line_start"),
            ("data_items", "SELECT * FROM data_items WHERE program_id = ? ORDER BY line_number"),
            ("files", "SELECT * FROM files WHERE program_id = ?"),
            ("statements", "SELECT * FROM statements WHERE program_id = ? ORDER BY line_number"),
            ("calls", "SELECT * FROM program_calls WHERE caller_program = ?"),
            ("called_by", "SELECT * FROM program_calls WHERE called_program = ?"),
            ("performs", "SELECT * FROM performs WHERE program_id = ?"),
            ("business_rules", "SELECT * FROM business_rules WHERE program_id = ?"),
        ]:
            cursor.execute(query, (program_id,))
            result[key] = [dict(row) for row in cursor.fetchall()]

        return result

    def get_call_graph(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT pc.caller_program, p1.business_name as caller_name,
                   pc.called_program, p2.business_name as called_name, pc.line_number
            FROM program_calls pc
            LEFT JOIN programs p1 ON pc.caller_program = p1.program_id
            LEFT JOIN programs p2 ON pc.called_program = p2.program_id
            ORDER BY pc.caller_program
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_all_business_rules(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT br.*, p.business_name as program_business_name
            FROM business_rules br
            LEFT JOIN programs p ON br.program_id = p.program_id
            ORDER BY br.category, br.rule_id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_data_dictionary(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT di.name, di.picture, di.section, di.level_number,
                   di.parent_name, di.business_name, di.description,
                   di.program_id, p.business_name as program_business_name
            FROM data_items di
            LEFT JOIN programs p ON di.program_id = p.program_id
            ORDER BY di.name
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_all_screens(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.*, GROUP_CONCAT(sf.field_name, ', ') as field_names
            FROM screens s
            LEFT JOIN screen_fields sf ON s.id = sf.screen_id
            GROUP BY s.id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_screen_details(self, screen_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM screens WHERE id = ?", (screen_id,))
        screen = cursor.fetchone()
        if not screen:
            return None
        result = dict(screen)
        cursor.execute("SELECT * FROM screen_fields WHERE screen_id = ? ORDER BY row_position, col_position",
                       (screen_id,))
        result["fields"] = [dict(row) for row in cursor.fetchall()]
        return result

    def get_program_statements(self, program_id: str, stmt_type: str = None) -> List[Dict]:
        """Get statements for a program, optionally filtered by type."""
        cursor = self.conn.cursor()
        if stmt_type:
            cursor.execute("""
                SELECT * FROM statements WHERE program_id = ? AND statement_type = ?
                ORDER BY line_number
            """, (program_id, stmt_type))
        else:
            cursor.execute("""
                SELECT * FROM statements WHERE program_id = ? ORDER BY line_number
            """, (program_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_all_modules(self) -> List[Dict]:
        """Get all modules with their programs."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT m.id, m.module_name, m.business_name, m.description, m.business_purpose
            FROM modules m ORDER BY m.module_name
        """)
        modules = []
        for row in cursor.fetchall():
            mod = dict(row)
            cursor.execute("""
                SELECT mp.program_id, p.program_type, p.line_count,
                       p.business_name, p.business_purpose
                FROM module_programs mp
                LEFT JOIN programs p ON mp.program_id = p.program_id
                WHERE mp.module_id = ?
                ORDER BY mp.program_id
            """, (mod["id"],))
            mod["programs"] = [dict(r) for r in cursor.fetchall()]
            modules.append(mod)
        return modules

    def get_module_details(self, module_id: int) -> Optional[Dict]:
        """Get full module details including programs, calls, files."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
        row = cursor.fetchone()
        if not row:
            return None
        mod = dict(row)

        # Get programs in module
        cursor.execute("""
            SELECT mp.program_id, p.program_type, p.line_count, p.file_path,
                   p.business_name, p.business_purpose, p.user_role
            FROM module_programs mp
            LEFT JOIN programs p ON mp.program_id = p.program_id
            WHERE mp.module_id = ?
            ORDER BY mp.program_id
        """, (module_id,))
        mod["programs"] = [dict(r) for r in cursor.fetchall()]

        # Get inter-module calls (calls from programs in this module)
        prog_ids = [p["program_id"] for p in mod["programs"]]
        if prog_ids:
            placeholders = ",".join("?" * len(prog_ids))
            cursor.execute(f"""
                SELECT DISTINCT pc.caller_program, pc.called_program, pc.line_number
                FROM program_calls pc
                WHERE pc.caller_program IN ({placeholders})
                ORDER BY pc.caller_program, pc.called_program
            """, prog_ids)
            mod["calls"] = [dict(r) for r in cursor.fetchall()]

            # Files used by module programs
            cursor.execute(f"""
                SELECT DISTINCT f.file_name, f.file_type, f.access_mode, f.program_id
                FROM files f
                WHERE f.program_id IN ({placeholders})
                ORDER BY f.file_name
            """, prog_ids)
            mod["files"] = [dict(r) for r in cursor.fetchall()]

            # Screens associated with module programs
            cursor.execute(f"""
                SELECT s.id, s.screen_name, s.map_name, s.mapset_name,
                       s.associated_program, s.business_name
                FROM screens s
                WHERE s.associated_program IN ({placeholders})
            """, prog_ids)
            mod["screens"] = [dict(r) for r in cursor.fetchall()]
        else:
            mod["calls"] = []
            mod["files"] = []
            mod["screens"] = []

        return mod

    def get_copybooks(self) -> List[Dict]:
        """Get all copybooks with usage info."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.copybook_name, c.file_path, c.business_name, c.description,
                   GROUP_CONCAT(cu.program_id, ', ') as used_by
            FROM copybooks c
            LEFT JOIN copybook_usage cu ON c.copybook_name = cu.copybook_name
            GROUP BY c.copybook_name
            ORDER BY c.copybook_name
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_statement_summary(self, program_id: str) -> Dict[str, int]:
        """Get summary counts of statement types for a program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT statement_type, COUNT(*) as cnt
            FROM statements WHERE program_id = ?
            GROUP BY statement_type ORDER BY cnt DESC
        """, (program_id,))
        return {row[0]: row[1] for row in cursor.fetchall()}

    # ================================================================
    # Graph-Based Module Detection (Swimm-style)
    # ================================================================

    def detect_modules(self) -> List[Dict]:
        """
        Detect logical modules using call graph analysis, naming patterns,
        and data access similarity -- not just 2-char prefix matching.
        """
        cursor = self.conn.cursor()

        # Ensure module tables exist even if the database was created
        # with an older schema that didn't include them.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_name TEXT NOT NULL,
                business_name TEXT,
                description TEXT,
                business_purpose TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS module_programs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id INTEGER NOT NULL,
                program_id TEXT NOT NULL,
                FOREIGN KEY(module_id) REFERENCES modules(id) ON DELETE CASCADE,
                FOREIGN KEY(program_id) REFERENCES programs(program_id) ON DELETE CASCADE
            )
        """)

        # Get all programs
        cursor.execute("SELECT program_id, program_type, file_path FROM programs")
        all_programs = {row[0]: {"type": row[1], "path": row[2]} for row in cursor.fetchall()}

        # Get call graph
        cursor.execute("SELECT caller_program, called_program FROM program_calls")
        calls = cursor.fetchall()

        # Get file usage
        cursor.execute("SELECT program_id, file_name FROM files")
        file_usage = defaultdict(set)
        for row in cursor.fetchall():
            file_usage[row[0]].add(row[1])

        # Build adjacency for clustering
        connected = defaultdict(set)
        for caller, called in calls:
            connected[caller].add(called)
            connected[called].add(caller)

        # Strategy 1: Name-based functional grouping
        func_groups = defaultdict(list)
        for pid in all_programs:
            # CardDemo naming: CO* = Common Online, CB* = Credit Card Batch
            # More specific: COSGN = Sign-on, COMEN = Menu, COTRN = Transaction
            # CBACT = Account, CBTRN = Transaction, COCRD = Credit Card
            if len(pid) >= 5:
                prefix4 = pid[:4]  # e.g., COSG, COME, COTR, CBAC, CBTR
                prefix5 = pid[:5]  # e.g., COSGN, COMEN, COTRN

                # Specific functional groupings
                if pid.startswith("COSGN"):
                    func_groups["AUTHENTICATION"].append(pid)
                elif pid.startswith("COMEN"):
                    func_groups["NAVIGATION"].append(pid)
                elif pid.startswith("COADM"):
                    func_groups["ADMINISTRATION"].append(pid)
                elif pid.startswith("COUSR"):
                    func_groups["USER_MANAGEMENT"].append(pid)
                elif pid.startswith("COTRN"):
                    func_groups["TRANSACTION_ONLINE"].append(pid)
                elif pid.startswith("COCRD"):
                    func_groups["CREDIT_CARD_MGMT"].append(pid)
                elif pid.startswith("COBIL"):
                    func_groups["BILLING"].append(pid)
                elif pid.startswith("CORPT"):
                    func_groups["REPORTING"].append(pid)
                elif pid.startswith("COACTU") or pid.startswith("COACTV"):
                    func_groups["ACCOUNT_MGMT_ONLINE"].append(pid)
                elif pid.startswith("CBACT"):
                    func_groups["ACCOUNT_BATCH"].append(pid)
                elif pid.startswith("CBTRN"):
                    func_groups["TRANSACTION_BATCH"].append(pid)
                elif pid.startswith("CBCUS"):
                    func_groups["CUSTOMER_BATCH"].append(pid)
                elif pid.startswith("CBEXPO") or pid.startswith("CBIMPO"):
                    func_groups["DATA_EXCHANGE"].append(pid)
                elif pid.startswith("CBSTM"):
                    func_groups["STATEMENT_PROCESSING"].append(pid)
                elif pid.startswith("CSUTL") or pid.startswith("COBSW"):
                    func_groups["UTILITIES"].append(pid)
                else:
                    # Classify by 2-char prefix with a meaningful fallback name
                    prefix2 = pid[:2].upper()
                    group_key = {
                        "CB": "BATCH_PROCESSING",
                        "CO": "ONLINE_PROCESSING",
                        "CS": "SHARED_SERVICES",
                        "DB": "DATABASE_OPERATIONS",
                        "PA": "PAYMENT_PROCESSING",
                    }.get(prefix2, f"MODULE_{prefix2}")
                    func_groups[group_key].append(pid)
            else:
                func_groups["OTHER"].append(pid)

        # Strategy 2: Merge small groups into neighbors via call graph
        module_names = {
            "AUTHENTICATION":       "Authentication & Sign-On",
            "NAVIGATION":           "Menu Navigation",
            "ADMINISTRATION":       "System Administration",
            "USER_MANAGEMENT":      "User Management",
            "TRANSACTION_ONLINE":   "Online Transaction Processing",
            "TRANSACTION_BATCH":    "Batch Transaction Processing",
            "CREDIT_CARD_MGMT":     "Credit Card Management",
            "BILLING":              "Billing & Statements",
            "REPORTING":            "Reports & Analytics",
            "ACCOUNT_MGMT_ONLINE":  "Online Account Management",
            "ACCOUNT_BATCH":        "Batch Account Processing",
            "CUSTOMER_BATCH":       "Customer Data Processing",
            "DATA_EXCHANGE":        "Data Import/Export",
            "STATEMENT_PROCESSING": "Statement Generation",
            "UTILITIES":            "Shared Utilities",
            "BATCH_PROCESSING":     "Batch Processing (Uncategorised)",
            "ONLINE_PROCESSING":    "Online Processing (Uncategorised)",
            "SHARED_SERVICES":      "Shared Services",
            "DATABASE_OPERATIONS":  "Database Operations",
            "PAYMENT_PROCESSING":   "Payment Processing",
            "OTHER":                "Other Programs",
        }

        # Build result
        modules = []
        for mod_id, progs in sorted(func_groups.items()):
            if not progs:
                continue
            modules.append({
                "module_id": mod_id,
                "module_name": module_names.get(mod_id, f"Module: {mod_id}"),
                "programs": sorted(progs),
                "program_count": len(progs),
            })

        # Save to DB (tables might not exist in very old DBs)
        try:
            cursor.execute("DELETE FROM modules")
        except Exception:
            pass
        try:
            cursor.execute("DELETE FROM module_programs")
        except Exception:
            pass
        # Best-effort persistence of detected modules.
        # If the schema doesn't match (older DB), skip writing but still
        # return the in-memory modules list so callers can proceed.
        try:
            for mod in modules:
                cursor.execute("""
                    INSERT INTO modules (module_name, business_name, description, business_purpose)
                    VALUES (?, ?, ?, ?)
                """, (mod["module_id"], mod["module_name"], "", mod["module_name"]))
                mod_db_id = cursor.lastrowid
                for pid in mod["programs"]:
                    try:
                        cursor.execute(
                            "INSERT INTO module_programs (module_id, program_id) VALUES (?, ?)",
                            (mod_db_id, pid),
                        )
                    except Exception:
                        # Ignore individual mapping failures
                        pass
            self.conn.commit()
        except Exception as e:
            # Log and continue without failing module detection
            console.print(f"[yellow]Warning: module persistence skipped due to schema issue: {e}[/yellow]")

        return modules

    # ================================================================
    # Full-Text Search
    # ================================================================

    def full_text_search(self, query: str) -> Dict[str, List]:
        cursor = self.conn.cursor()
        results = {}
        for table, fields in [
            ("programs_fts", "program_id, business_name, business_purpose"),
            ("data_items_fts", "name, business_name, description"),
            ("business_rules_fts", "rule_name, rule_statement"),
        ]:
            try:
                cursor.execute(f"SELECT {fields} FROM {table} WHERE {table} MATCH ?", (query,))
                results[table.replace("_fts", "")] = [dict(row) for row in cursor.fetchall()]
            except:
                results[table.replace("_fts", "")] = []
        return results

    # ================================================================
    # Dependency & Impact Analysis (for doc generation)
    # ================================================================

    def get_program_dependencies(self, program_id: str) -> Dict:
        """Get direct callers and callees with business context."""
        cursor = self.conn.cursor()

        # Direct callers
        cursor.execute("""
            SELECT pc.caller_program, pc.call_location, pc.line_number,
                   p.business_name, p.program_type, p.business_purpose
            FROM program_calls pc
            LEFT JOIN programs p ON pc.caller_program = p.program_id
            WHERE pc.called_program = ?
            ORDER BY pc.caller_program
        """, (program_id,))
        callers = [dict(r) for r in cursor.fetchall()]

        # Direct callees
        cursor.execute("""
            SELECT pc.called_program, pc.call_location, pc.line_number,
                   p.business_name, p.program_type, p.business_purpose
            FROM program_calls pc
            LEFT JOIN programs p ON pc.called_program = p.program_id
            WHERE pc.caller_program = ?
            ORDER BY pc.called_program
        """, (program_id,))
        callees = [dict(r) for r in cursor.fetchall()]

        return {"callers": callers, "callees": callees}

    def get_shared_data_context(self, program_id: str) -> Dict:
        """Get copybooks and files used by this program with co-users."""
        cursor = self.conn.cursor()

        # Copybooks used by this program + other programs sharing them
        cursor.execute("""
            SELECT cu.copybook_name
            FROM copybook_usage cu
            WHERE cu.program_id = ?
            ORDER BY cu.copybook_name
        """, (program_id,))
        my_copybooks = [row[0] for row in cursor.fetchall()]

        shared_copybooks = []
        for cb in my_copybooks:
            cursor.execute("""
                SELECT cu.program_id, p.business_name
                FROM copybook_usage cu
                LEFT JOIN programs p ON cu.program_id = p.program_id
                WHERE cu.copybook_name = ? AND cu.program_id != ?
                ORDER BY cu.program_id
            """, (cb, program_id))
            co_users = [dict(r) for r in cursor.fetchall()]
            shared_copybooks.append({
                "copybook_name": cb,
                "co_users": co_users,
                "co_user_count": len(co_users),
            })

        # Files used by this program + other programs sharing them
        cursor.execute("""
            SELECT f.file_name, f.file_type, f.access_mode
            FROM files f
            WHERE f.program_id = ?
            ORDER BY f.file_name
        """, (program_id,))
        my_files = [dict(r) for r in cursor.fetchall()]

        shared_files = []
        for f in my_files:
            cursor.execute("""
                SELECT f2.program_id, p.business_name, f2.access_mode
                FROM files f2
                LEFT JOIN programs p ON f2.program_id = p.program_id
                WHERE f2.file_name = ? AND f2.program_id != ?
                ORDER BY f2.program_id
            """, (f["file_name"], program_id))
            co_users = [dict(r) for r in cursor.fetchall()]
            shared_files.append({
                **f,
                "co_users": co_users,
                "co_user_count": len(co_users),
            })

        return {"shared_copybooks": shared_copybooks, "shared_files": shared_files}

    def get_impact_analysis(self, program_id: str) -> Dict:
        """Compute transitive impact: what breaks if this program changes."""
        cursor = self.conn.cursor()

        # Build full adjacency from DB
        cursor.execute("SELECT caller_program, called_program FROM program_calls")
        calls_out = defaultdict(set)
        called_by = defaultdict(set)
        for row in cursor.fetchall():
            calls_out[row[0]].add(row[1])
            called_by[row[1]].add(row[0])

        # Build copybook coupling
        cursor.execute("SELECT copybook_name, program_id FROM copybook_usage")
        cb_to_progs = defaultdict(set)
        prog_to_cbs = defaultdict(set)
        for row in cursor.fetchall():
            cb_to_progs[row[0]].add(row[1])
            prog_to_cbs[row[1]].add(row[0])

        # All known programs
        cursor.execute("SELECT program_id FROM programs")
        all_programs = set(row[0] for row in cursor.fetchall())

        def transitive(pid, graph):
            visited = set()
            stack = list(graph.get(pid, set()))
            while stack:
                nxt = stack.pop()
                if nxt not in visited and nxt in all_programs:
                    visited.add(nxt)
                    stack.extend(graph.get(nxt, set()) - visited)
            return visited

        def cb_impact(pid):
            affected = set()
            for cb in prog_to_cbs.get(pid, set()):
                affected.update(cb_to_progs.get(cb, set()))
            affected.discard(pid)
            return affected

        direct_callers = called_by.get(program_id, set()) & all_programs
        trans_callers = transitive(program_id, called_by)
        direct_callees = calls_out.get(program_id, set()) & all_programs
        trans_callees = transitive(program_id, calls_out)
        coupling = cb_impact(program_id)
        total_impact = len(trans_callers | coupling)

        if total_impact >= 10:
            risk = "HIGH"
        elif total_impact >= 5:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return {
            "direct_callers": sorted(direct_callers),
            "transitive_callers": sorted(trans_callers),
            "direct_callees": sorted(direct_callees),
            "transitive_callees": sorted(trans_callees),
            "copybook_coupling": sorted(coupling),
            "total_impact": total_impact,
            "risk": risk,
        }

    def get_linked_clusters(self) -> List[Dict]:
        """Find connected components in the call + copybook graph."""
        cursor = self.conn.cursor()

        cursor.execute("SELECT program_id, business_name, program_type FROM programs")
        all_programs = {row[0]: {"business_name": row[1], "program_type": row[2]}
                        for row in cursor.fetchall()}

        # Build undirected adjacency from calls
        adj = defaultdict(set)
        cursor.execute("SELECT caller_program, called_program FROM program_calls")
        for row in cursor.fetchall():
            if row[0] in all_programs and row[1] in all_programs:
                adj[row[0]].add(row[1])
                adj[row[1]].add(row[0])

        # Add copybook coupling edges
        cursor.execute("SELECT copybook_name, program_id FROM copybook_usage")
        cb_map = defaultdict(set)
        for row in cursor.fetchall():
            if row[1] in all_programs:
                cb_map[row[0]].add(row[1])
        for cb, progs in cb_map.items():
            prog_list = list(progs)
            for i in range(len(prog_list)):
                for j in range(i + 1, len(prog_list)):
                    adj[prog_list[i]].add(prog_list[j])
                    adj[prog_list[j]].add(prog_list[i])

        # BFS to find connected components
        visited = set()
        clusters = []
        for pid in sorted(all_programs.keys()):
            if pid in visited:
                continue
            component = set()
            queue = [pid]
            while queue:
                node = queue.pop(0)
                if node in visited:
                    continue
                visited.add(node)
                component.add(node)
                queue.extend(adj.get(node, set()) - visited)
            clusters.append(sorted(component))

        # Build cluster details
        result = []
        for idx, members in enumerate(clusters, 1):
            # Gather inter-cluster calls
            member_set = set(members)
            cursor.execute(
                "SELECT caller_program, called_program, line_number FROM program_calls "
                "WHERE caller_program IN ({seq}) AND called_program IN ({seq})".format(
                    seq=",".join("?" * len(members))),
                members + members)
            internal_calls = [dict(r) for r in cursor.fetchall()]

            # Shared copybooks within cluster
            if members:
                cursor.execute(
                    "SELECT copybook_name, GROUP_CONCAT(program_id) as programs "
                    "FROM copybook_usage WHERE program_id IN ({seq}) "
                    "GROUP BY copybook_name HAVING COUNT(DISTINCT program_id) > 1".format(
                        seq=",".join("?" * len(members))),
                    members)
                shared_cbs = [dict(r) for r in cursor.fetchall()]
            else:
                shared_cbs = []

            result.append({
                "cluster_id": idx,
                "members": members,
                "member_details": [
                    {"program_id": m, **all_programs.get(m, {})} for m in members
                ],
                "size": len(members),
                "internal_calls": internal_calls,
                "shared_copybooks": shared_cbs,
                "is_standalone": len(members) == 1,
            })

        # Sort: largest clusters first, standalones last
        result.sort(key=lambda c: (-c["size"], c["cluster_id"]))
        return result


    # ================================================================
    # JCL Loading & Queries
    # ================================================================

    def load_jcl(self, jcl_jobs: List[Dict]):
        """Load parsed JCL jobs, steps, and datasets into SQLite."""
        if not jcl_jobs:
            return
        cursor = self.conn.cursor()

        # Ensure JCL tables exist (schema may have been created before JCL support)
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS jcl_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT UNIQUE NOT NULL,
                file_name TEXT, file_path TEXT, file_hash TEXT,
                job_description TEXT, job_class TEXT, msg_class TEXT,
                header_comments TEXT, programs_called TEXT,
                input_datasets TEXT, output_datasets TEXT,
                step_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS jcl_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL, step_name TEXT NOT NULL, step_order INTEGER,
                program TEXT, proc TEXT, step_type TEXT,
                step_comments TEXT, cond TEXT, line_number INTEGER, sysin_data TEXT,
                UNIQUE(job_name, step_name)
            );
            CREATE TABLE IF NOT EXISTS jcl_datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL, step_name TEXT NOT NULL, dd_name TEXT,
                dsn TEXT, disp TEXT, disposition_normal TEXT, disposition_abnormal TEXT,
                direction TEXT, recfm TEXT, lrecl TEXT, unit TEXT, space TEXT,
                is_inline INTEGER DEFAULT 0
            );
        """)
        self.conn.commit()

        for job in jcl_jobs:
            job_name = job.get("job_name", "")
            if not job_name:
                continue

            # Upsert job row
            cursor.execute("DELETE FROM jcl_datasets WHERE job_name = ?", (job_name,))
            cursor.execute("DELETE FROM jcl_steps    WHERE job_name = ?", (job_name,))
            cursor.execute("DELETE FROM jcl_jobs     WHERE job_name = ?", (job_name,))

            steps = job.get("steps") or []
            cursor.execute("""
                INSERT INTO jcl_jobs (
                    job_name, file_name, file_path, file_hash,
                    job_description, job_class, msg_class, header_comments,
                    programs_called, input_datasets, output_datasets, step_count
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                job_name,
                job.get("file_name"), job.get("file_path"), job.get("file_hash"),
                job.get("job_description"), job.get("job_class"), job.get("msg_class"),
                "\n".join(job.get("comment_lines") or []),
                json.dumps(job.get("programs_called") or []),
                json.dumps(job.get("input_datasets") or []),
                json.dumps(job.get("output_datasets") or []),
                len(steps),
            ))

            for order, step in enumerate(steps, 1):
                step_name = step.get("step_name", f"STEP{order}")
                cursor.execute("""
                    INSERT OR REPLACE INTO jcl_steps (
                        job_name, step_name, step_order, program, proc,
                        step_type, step_comments, cond, line_number, sysin_data
                    ) VALUES (?,?,?,?,?,?,?,?,?,?)
                """, (
                    job_name, step_name, order,
                    step.get("program"), step.get("proc"),
                    step.get("step_type"),
                    "\n".join(step.get("comment_lines") or []),
                    step.get("cond"), step.get("line_number"),
                    json.dumps(step.get("sysin_data") or []),
                ))

                for ds in (step.get("datasets") or []):
                    cursor.execute("""
                        INSERT INTO jcl_datasets (
                            job_name, step_name, dd_name, dsn, disp,
                            disposition_normal, disposition_abnormal, direction,
                            recfm, lrecl, unit, space, is_inline
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        job_name, step_name,
                        ds.get("dd_name"), ds.get("dsn"), ds.get("disp"),
                        ds.get("disposition_normal"), ds.get("disposition_abnormal"),
                        ds.get("direction"), ds.get("recfm"), ds.get("lrecl"),
                        ds.get("unit"), ds.get("space"),
                        1 if ds.get("is_inline") else 0,
                    ))

        self.conn.commit()
        console.print(f"[green]OK - Loaded {len(jcl_jobs)} JCL jobs into database[/green]")

    def get_all_jcl_jobs(self) -> List[Dict]:
        """Return all JCL jobs with their parsed programs_called / datasets."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT job_name, file_name, file_path, job_description,
                       job_class, msg_class, header_comments,
                       programs_called, input_datasets, output_datasets, step_count
                FROM jcl_jobs ORDER BY job_name
            """)
            rows = [dict(r) for r in cursor.fetchall()]
            for row in rows:
                for f in ("programs_called", "input_datasets", "output_datasets"):
                    try:
                        row[f] = json.loads(row[f] or "[]")
                    except Exception:
                        row[f] = []
            return rows
        except Exception:
            return []

    def get_jcl_job_details(self, job_name: str) -> Optional[Dict]:
        """Return a JCL job with all its steps and datasets."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM jcl_jobs WHERE job_name = ?", (job_name,))
            row = cursor.fetchone()
            if not row:
                return None
            job = dict(row)
            for f in ("programs_called", "input_datasets", "output_datasets"):
                try:
                    job[f] = json.loads(job.get(f) or "[]")
                except Exception:
                    job[f] = []

            cursor.execute("""
                SELECT * FROM jcl_steps WHERE job_name = ? ORDER BY step_order
            """, (job_name,))
            steps = [dict(r) for r in cursor.fetchall()]
            for step in steps:
                try:
                    step["sysin_data"] = json.loads(step.get("sysin_data") or "[]")
                except Exception:
                    step["sysin_data"] = []
                cursor.execute("""
                    SELECT * FROM jcl_datasets
                    WHERE job_name = ? AND step_name = ? ORDER BY id
                """, (job_name, step["step_name"]))
                step["datasets"] = [dict(r) for r in cursor.fetchall()]
            job["steps"] = steps
            return job
        except Exception:
            return None

    def get_program_jcl_jobs(self, program_id: str) -> List[Dict]:
        """Return all JCL jobs that execute a given COBOL program."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT j.job_name, j.file_name, j.job_description,
                                s.step_name, s.step_order, s.step_comments
                FROM jcl_jobs j
                JOIN jcl_steps s ON j.job_name = s.job_name
                WHERE UPPER(s.program) = UPPER(?)
                ORDER BY j.job_name, s.step_order
            """, (program_id,))
            return [dict(r) for r in cursor.fetchall()]
        except Exception:
            return []


# CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load COBOL data into SQLite")
    parser.add_argument("--db", default="data/cobol_knowledge.db")
    parser.add_argument("--schema", default="schemas/cobol_knowledge.sql")
    parser.add_argument("--programs", help="programs.json path")
    parser.add_argument("--screens", help="screens.json path")
    parser.add_argument("--rules", help="business_rules.json path")
    parser.add_argument("--enriched", help="enriched output directory")
    args = parser.parse_args()

    loader = SQLiteLoader(args.db, args.schema)
    loader.connect()
    loader.load_from_json(programs_json=args.programs, rules_json=args.rules,
                          enriched_json=args.enriched, screens_json=args.screens)
    if args.programs:
        modules = loader.detect_modules()
        print(f"Detected {len(modules)} modules")
    loader.close()
