-- COBOL Knowledge Database Schema
-- SQLite schema for storing parsed COBOL analysis

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================
-- Table: programs
-- Core COBOL program information
-- ============================================
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    file_hash TEXT,  -- For incremental updates
    program_type TEXT,  -- ONLINE, BATCH, UTILITY
    line_count INTEGER,
    
    -- LLM Enriched fields
    business_name TEXT,
    business_purpose TEXT,
    user_role TEXT,
    business_process TEXT,

    -- Migration fields (LLM enriched)
    migration_complexity INTEGER,           -- 1-5 score
    complexity_reason TEXT,
    modern_equivalent TEXT,
    suggested_service TEXT,
    migration_approach TEXT,
    data_contracts TEXT,
    migration_risks TEXT,
    dependencies_to_migrate_first TEXT,     -- JSON array of program IDs

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_programs_type ON programs(program_type);

-- ============================================
-- Table: paragraphs
-- Executable sections within programs
-- ============================================
CREATE TABLE IF NOT EXISTS paragraphs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    paragraph_name TEXT NOT NULL,
    line_start INTEGER,
    line_end INTEGER,
    
    -- LLM Enriched fields
    business_name TEXT,
    narrative TEXT,
    purpose TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    UNIQUE(program_id, paragraph_name)
);

CREATE INDEX IF NOT EXISTS idx_paragraphs_program ON paragraphs(program_id);

-- ============================================
-- Table: data_items
-- Variables (Working-Storage, Linkage, File Section)
-- ============================================
CREATE TABLE IF NOT EXISTS data_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    name TEXT NOT NULL,
    level_number INTEGER,
    picture TEXT,
    usage TEXT,
    value TEXT,
    section TEXT,  -- WORKING-STORAGE, LINKAGE, FILE
    parent_name TEXT,  -- For hierarchical structures
    line_number INTEGER,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    data_type_description TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_data_items_program ON data_items(program_id);
CREATE INDEX IF NOT EXISTS idx_data_items_name ON data_items(name);

-- ============================================
-- Table: files
-- VSAM/Sequential files used by programs
-- ============================================
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT,  -- VSAM, SEQUENTIAL, INDEXED
    organization TEXT,
    access_mode TEXT,
    record_name TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_files_program ON files(program_id);

-- ============================================
-- Table: statements
-- Every executable statement
-- ============================================
CREATE TABLE IF NOT EXISTS statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    paragraph_name TEXT,
    statement_type TEXT NOT NULL,  -- CALL, PERFORM, IF, MOVE, READ, WRITE, EVALUATE
    line_number INTEGER,
    details_json TEXT,  -- JSON with condition, parameters, etc.
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_statements_program ON statements(program_id);
CREATE INDEX IF NOT EXISTS idx_statements_type ON statements(statement_type);
CREATE INDEX IF NOT EXISTS idx_statements_paragraph ON statements(paragraph_name);

-- ============================================
-- Table: program_calls
-- Inter-program dependencies (CALL statements)
-- ============================================
CREATE TABLE IF NOT EXISTS program_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caller_program TEXT NOT NULL,
    called_program TEXT NOT NULL,
    call_location TEXT,  -- Paragraph where call occurs
    line_number INTEGER,
    parameters_json TEXT,
    
    FOREIGN KEY (caller_program) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_calls_caller ON program_calls(caller_program);
CREATE INDEX IF NOT EXISTS idx_calls_called ON program_calls(called_program);

-- ============================================
-- Table: performs
-- Intra-program control flow (PERFORM statements)
-- ============================================
CREATE TABLE IF NOT EXISTS performs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    source_paragraph TEXT NOT NULL,
    target_paragraph TEXT NOT NULL,
    perform_type TEXT,  -- SIMPLE, THRU, UNTIL, TIMES, VARYING
    line_number INTEGER,
    condition TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_performs_program ON performs(program_id);
CREATE INDEX IF NOT EXISTS idx_performs_source ON performs(source_paragraph);
CREATE INDEX IF NOT EXISTS idx_performs_target ON performs(target_paragraph);

-- ============================================
-- Table: copybooks
-- Shared data structures
-- ============================================
CREATE TABLE IF NOT EXISTS copybooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    copybook_name TEXT UNIQUE NOT NULL,
    file_path TEXT,
    file_hash TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_copybooks_name ON copybooks(copybook_name);

-- ============================================
-- Table: copybook_usage
-- Which programs include which copybooks
-- ============================================
CREATE TABLE IF NOT EXISTS copybook_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    copybook_name TEXT NOT NULL,
    line_number INTEGER,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    FOREIGN KEY (copybook_name) REFERENCES copybooks(copybook_name)
);

CREATE INDEX IF NOT EXISTS idx_copybook_usage_program ON copybook_usage(program_id);

-- ============================================
-- Table: business_rules
-- Extracted business logic (LLM populated)
-- ============================================
CREATE TABLE IF NOT EXISTS business_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id TEXT UNIQUE NOT NULL,
    rule_name TEXT NOT NULL,
    rule_statement TEXT NOT NULL,
    category TEXT,  -- VALIDATION, CALCULATION, WORKFLOW, COMPLIANCE
    program_id TEXT,
    paragraph_name TEXT,
    line_start INTEGER,
    line_end INTEGER,
    condition_text TEXT,
    action_text TEXT,
    source_code TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_rules_program ON business_rules(program_id);
CREATE INDEX IF NOT EXISTS idx_rules_category ON business_rules(category);

-- ============================================
-- Table: screens
-- BMS map definitions
-- ============================================
CREATE TABLE IF NOT EXISTS screens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT,
    screen_name TEXT NOT NULL,
    map_name TEXT,
    mapset_name TEXT,
    file_path TEXT,
    associated_program TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    FOREIGN KEY (associated_program) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_screens_transaction ON screens(transaction_id);
CREATE INDEX IF NOT EXISTS idx_screens_program ON screens(associated_program);

-- ============================================
-- Table: screen_fields
-- Fields within BMS screens
-- ============================================
CREATE TABLE IF NOT EXISTS screen_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screen_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    field_type TEXT,  -- INPUT, OUTPUT, BOTH
    length INTEGER,
    row_position INTEGER,
    col_position INTEGER,
    attributes TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    FOREIGN KEY (screen_id) REFERENCES screens(id)
);

-- ============================================
-- Table: modules
-- Logical groupings (auto-detected or manual)
-- ============================================
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_name TEXT UNIQUE NOT NULL,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    business_purpose TEXT
);

-- ============================================
-- Table: module_programs
-- Programs belonging to each module
-- ============================================
CREATE TABLE IF NOT EXISTS module_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    program_id TEXT NOT NULL,
    
    FOREIGN KEY (module_id) REFERENCES modules(id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    UNIQUE(module_id, program_id)
);

-- ============================================
-- Table: jcl_jobs
-- One row per JCL file (job definition)
-- ============================================
CREATE TABLE IF NOT EXISTS jcl_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT UNIQUE NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_hash TEXT,
    job_description TEXT,
    job_class TEXT,
    msg_class TEXT,
    header_comments TEXT,           -- Full block of //* header comments
    programs_called TEXT,           -- JSON array of PGM= values (COBOL programs only)
    input_datasets TEXT,            -- JSON array of input DSNs
    output_datasets TEXT,           -- JSON array of output DSNs
    step_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jcl_jobs_name ON jcl_jobs(job_name);

-- ============================================
-- Table: jcl_steps
-- One row per EXEC step inside a JCL job
-- ============================================
CREATE TABLE IF NOT EXISTS jcl_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    step_name TEXT NOT NULL,
    step_order INTEGER NOT NULL,
    program TEXT,                   -- PGM= value (COBOL program or utility)
    proc TEXT,                      -- PROC= value
    step_type TEXT,                 -- PGM | PROC | UTIL | UNKNOWN
    step_comments TEXT,             -- //* lines immediately above this EXEC
    cond TEXT,                      -- COND= value
    line_number INTEGER,
    sysin_data TEXT,                -- Inline SYSIN content (JSON array of lines)
    FOREIGN KEY (job_name) REFERENCES jcl_jobs(job_name) ON DELETE CASCADE,
    UNIQUE(job_name, step_name)
);

CREATE INDEX IF NOT EXISTS idx_jcl_steps_job ON jcl_steps(job_name);
CREATE INDEX IF NOT EXISTS idx_jcl_steps_program ON jcl_steps(program);

-- ============================================
-- Table: jcl_datasets
-- DD cards — files/datasets per step
-- ============================================
CREATE TABLE IF NOT EXISTS jcl_datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    step_name TEXT NOT NULL,
    dd_name TEXT NOT NULL,
    dsn TEXT,
    disp TEXT,
    disposition_normal TEXT,
    disposition_abnormal TEXT,
    direction TEXT,                 -- INPUT | OUTPUT | SYSTEM | INLINE
    recfm TEXT,
    lrecl TEXT,
    unit TEXT,
    space TEXT,
    is_inline INTEGER DEFAULT 0,
    FOREIGN KEY (job_name) REFERENCES jcl_jobs(job_name) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_jcl_datasets_job ON jcl_datasets(job_name);
CREATE INDEX IF NOT EXISTS idx_jcl_datasets_dsn ON jcl_datasets(dsn);

-- ============================================
-- Full-Text Search Tables (FTS5)
-- ============================================
CREATE VIRTUAL TABLE IF NOT EXISTS programs_fts USING fts5(
    program_id,
    business_name,
    business_purpose,
    content='programs',
    content_rowid='id'
);

CREATE VIRTUAL TABLE IF NOT EXISTS data_items_fts USING fts5(
    name,
    business_name,
    description,
    content='data_items',
    content_rowid='id'
);

CREATE VIRTUAL TABLE IF NOT EXISTS business_rules_fts USING fts5(
    rule_name,
    rule_statement,
    condition_text,
    action_text,
    content='business_rules',
    content_rowid='id'
);

-- ============================================
-- FTS Triggers for auto-sync
-- ============================================
CREATE TRIGGER IF NOT EXISTS programs_ai AFTER INSERT ON programs BEGIN
    INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
    VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
END;

CREATE TRIGGER IF NOT EXISTS programs_ad AFTER DELETE ON programs BEGIN
    INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
    VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
END;

CREATE TRIGGER IF NOT EXISTS programs_au AFTER UPDATE ON programs BEGIN
    INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
    VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
    INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
    VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
END;

CREATE TRIGGER IF NOT EXISTS data_items_ai AFTER INSERT ON data_items BEGIN
    INSERT INTO data_items_fts(rowid, name, business_name, description)
    VALUES (NEW.id, NEW.name, NEW.business_name, NEW.description);
END;

CREATE TRIGGER IF NOT EXISTS business_rules_ai AFTER INSERT ON business_rules BEGIN
    INSERT INTO business_rules_fts(rowid, rule_name, rule_statement, condition_text, action_text)
    VALUES (NEW.id, NEW.rule_name, NEW.rule_statement, NEW.condition_text, NEW.action_text);
END;

-- ============================================
-- Useful Views
-- ============================================

-- View: Program call hierarchy
CREATE VIEW IF NOT EXISTS v_call_hierarchy AS
SELECT 
    pc.caller_program,
    p1.business_name as caller_business_name,
    pc.called_program,
    p2.business_name as called_business_name,
    pc.line_number
FROM program_calls pc
LEFT JOIN programs p1 ON pc.caller_program = p1.program_id
LEFT JOIN programs p2 ON pc.called_program = p2.program_id;

-- View: Program with file operations
CREATE VIEW IF NOT EXISTS v_program_files AS
SELECT 
    p.program_id,
    p.business_name as program_business_name,
    f.file_name,
    f.file_type,
    f.access_mode,
    f.business_name as file_business_name
FROM programs p
JOIN files f ON p.program_id = f.program_id;

-- View: Business rules by program
CREATE VIEW IF NOT EXISTS v_program_rules AS
SELECT 
    p.program_id,
    p.business_name as program_business_name,
    br.rule_id,
    br.rule_name,
    br.rule_statement,
    br.category
FROM programs p
JOIN business_rules br ON p.program_id = br.program_id;
