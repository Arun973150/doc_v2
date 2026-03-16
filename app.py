"""
CardDemo Knowledge Base — Interactive Dashboard
Streamlit app combining dependency analysis, call graphs, and AI-powered chat.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import os
import sqlite3
import textwrap
from pathlib import Path
from collections import defaultdict

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from src.langgraph_enricher import CobolEnricher
from src.sqlite_loader import SQLiteLoader

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

load_dotenv()
DB_PATH = os.environ.get("DB_PATH", "data/cobol_knowledge.db")


# ═══════════════════════════════════════════════
# JSON Translator (rule-based + optional LLM)
# ═══════════════════════════════════════════════

@st.cache_resource
def get_json_translator():
    try:
        from src.json_translator import JsonTranslator
        return JsonTranslator(parsed_output_dir="parsed_output")
    except Exception:
        try:
            from json_translator import JsonTranslator
            return JsonTranslator(parsed_output_dir="parsed_output")
        except Exception:
            return None


GROQ_MODELS = [
    "llama-3.3-70b-versatile",   # Best free tier
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]


def translate_program_to_english(program_id: str, model: str = None) -> dict:
    """
    Translate parsed JSON for a program into plain English.
    Uses Groq LLM if GROQ_API_KEY is set, otherwise falls back to rule-based.
    """
    import textwrap as _textwrap
    translator = get_json_translator()
    if not translator:
        return {"found": False, "english": "JSON translator not available.", "raw_json": "{}"}

    result = translator.translate_program(program_id)
    if not result.get("found"):
        return result

    groq_api_key = os.environ.get("GROQ_API_KEY", "")
    groq_model = model or os.environ.get("GROQ_MODEL", "llama-3.1-70b-versatile")

    if groq_api_key and groq_api_key != "your_groq_api_key_here":
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)
            prompt = _textwrap.dedent(f"""\
                You are a COBOL legacy system expert. Below is the raw parsed JSON
                output from a COBOL parser for program {program_id.upper()}.

                Explain this program in clear, plain English. Cover:
                1. What the program does (its purpose)
                2. Its control flow (how paragraphs call each other via PERFORMs)
                3. Key data structures and variables
                4. File I/O operations
                5. External program calls
                6. Any copybook dependencies

                Be specific and reference paragraph names and line numbers.
                Use markdown formatting for readability.

                ```json
                {result['raw_json'][:4000]}
                ```
            """)
            response = client.chat.completions.create(
                model=groq_model,
                messages=[
                    {"role": "system", "content": "You are a COBOL documentation expert. Translate parsed COBOL JSON into clear English explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            result["english"] = response.choices[0].message.content
            result["source"] = "llm"
        except Exception as e:
            result["english"] = f"> ⚠️ LLM unavailable ({e}), showing rule-based explanation:\n\n" + result["english"]
            result["source"] = "rules"
    else:
        result["source"] = "rules"

    return result


# ═══════════════════════════════════════════════
# Database helpers
# ═══════════════════════════════════════════════

@st.cache_resource
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def q(query, params=()):
    """Execute a query and return list of dicts."""
    c = get_db().cursor()
    c.execute(query, params)
    return [dict(r) for r in c.fetchall()]


def q1(query, params=()):
    """Execute query, return single row dict or None."""
    rows = q(query, params)
    return rows[0] if rows else None


def m_id(text: str) -> str:
    """Sanitize ID for Mermaid: prefix with 'n_' if starts with digit, replace dashes."""
    s = text.replace("-", "_").replace(" ", "_").replace(".", "_").replace("$", "_").replace("@", "_")
    if s and s[0].isdigit():
        return f"node_{s}"
    return s

def m_label(text: str) -> str:
    """Sanitize label for Mermaid: wrap in quotes and escape internal quotes."""
    clean = str(text or "").replace('"', "'")
    return f'["{clean}"]'

def render_mermaid(code: str, height: int = 500):
    """Render a Mermaid diagram using the Mermaid JS CDN."""
    html = f"""
    <div style="background:#161b22; border-radius:8px; padding:16px; border:1px solid #30363d;">
        <pre class="mermaid" style="text-align:center;">
{code}
        </pre>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {{
                primaryColor: '#1f6feb',
                primaryTextColor: '#e6edf3',
                primaryBorderColor: '#58a6ff',
                lineColor: '#8b949e',
                secondaryColor: '#21262d',
                tertiaryColor: '#161b22',
                background: '#161b22',
                mainBkg: '#21262d',
                nodeBorder: '#58a6ff',
                clusterBkg: 'rgba(88,166,255,0.06)',
                clusterBorder: '#30363d',
                titleColor: '#e6edf3',
                edgeLabelBackground: '#161b22'
            }},
            flowchart: {{ curve: 'basis', padding: 15 }},
            securityLevel: 'loose'
        }});
    </script>
    """
    components.html(html, height=height, scrolling=True)


# ═══════════════════════════════════════════════
# Page config
# ═══════════════════════════════════════════════

st.set_page_config(
    page_title="CardDemo Knowledge Base",
    page_icon="Bank",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #e0e0ff;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1e3f, #2a2a5e);
        border: 1px solid rgba(88,166,255,0.2);
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="stMetric"] label { color: #8b949e !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #58a6ff !important; }

    /* Chat styling */
    .chat-user {
        background: linear-gradient(135deg, #1f6feb, #388bfd);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px; color: white;
        margin: 8px 0; max-width: 80%;
        margin-left: auto; text-align: right;
    }
    .chat-bot {
        background: linear-gradient(135deg, #21262d, #30363d);
        border: 1px solid rgba(88,166,255,0.15);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px; color: #e6edf3;
        margin: 8px 0; max-width: 85%;
    }

    /* Tables */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-size: 16px;
        font-weight: 600;
    }

    /* Hero header */
    .hero { 
        text-align: center; padding: 20px 0 10px;
        border-bottom: 2px solid rgba(88,166,255,0.3);
        margin-bottom: 20px;
    }
    .hero h1 { font-size: 2em; margin: 0; }
    .hero p { color: #8b949e; font-size: 1.1em; }

    /* Risk badges */
    .risk-high { color: #f85149; font-weight: bold; }
    .risk-med { color: #d29922; font-weight: bold; }
    .risk-low { color: #3fb950; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# Sidebar Navigation
# ═══════════════════════════════════════════════

with st.sidebar:
    st.markdown("## CardDemo KB")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Call Graph",
            "Dependency Matrix",
            "Program Explorer",
            "Impact Analysis",
            "Migration Readiness",
            "Copybooks",
            "Data Flow",
            "Chat Assistant",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    # Quick stats in sidebar
    stats = q1("SELECT COUNT(*) as cnt FROM programs")
    st.metric("Programs", stats["cnt"] if stats else 0)
    stats2 = q1("SELECT COUNT(*) as cnt FROM program_calls")
    st.metric("Call Edges", stats2["cnt"] if stats2 else 0)
    stats3 = q1("SELECT COUNT(DISTINCT copybook_name) as cnt FROM copybook_usage")
    st.metric("Copybooks", stats3["cnt"] if stats3 else 0)


# ═══════════════════════════════════════════════
# PAGE: Overview
# ═══════════════════════════════════════════════

def page_overview():
    st.markdown('<div class="hero"><h1>CardDemo Knowledge Base</h1><p>COBOL Legacy System — Interactive Documentation & Analysis</p></div>', unsafe_allow_html=True)

    # Top metrics row
    c1, c2, c3, c4, c5 = st.columns(5)
    programs = q("SELECT * FROM programs")
    calls = q("SELECT * FROM program_calls")
    copybooks = q("SELECT DISTINCT copybook_name FROM copybook_usage")
    files_data = q("SELECT DISTINCT file_name FROM files")
    screens = q("SELECT * FROM screens")

    c1.metric("Programs", len(programs), "Active")
    c2.metric("Call Edges", len(calls), f"{len(calls)//len(programs)} avg")
    c3.metric("Copybooks", len(copybooks), "Shared")
    c4.metric("Files", len(files_data), "VSAM/Seq")
    c5.metric("Screens", len(screens), "BMS Maps")

    st.markdown("---")

    # Program type breakdown
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Programs by Type")
        types = q("SELECT program_type, COUNT(*) as cnt FROM programs GROUP BY program_type ORDER BY cnt DESC")
        import pandas as pd
        if types:
            df = pd.DataFrame(types)
            st.bar_chart(df.set_index("program_type"))

    with col2:
        st.subheader("Modules")
        modules = q("""
            SELECT m.module_name, COUNT(mp.program_id) as program_count
            FROM modules m JOIN module_programs mp ON m.id = mp.module_id
            GROUP BY m.module_name ORDER BY program_count DESC
        """)
        if modules:
            df = pd.DataFrame(modules)
            st.bar_chart(df.set_index("module_name"))

    # Recent programs table
    st.subheader("All Programs")
    all_progs = q("""
        SELECT p.program_id, p.business_name, p.program_type, p.line_count,
               (SELECT COUNT(*) FROM program_calls pc WHERE pc.caller_program = p.program_id) as calls_out,
               (SELECT COUNT(*) FROM program_calls pc WHERE pc.called_program = p.program_id) as called_by,
               (SELECT COUNT(*) FROM copybook_usage cu WHERE cu.program_id = p.program_id) as copybooks
        FROM programs p ORDER BY p.program_id
    """)
    if all_progs:
        import pandas as pd
        df = pd.DataFrame(all_progs)
        st.dataframe(df, use_container_width=True, height=400)
    
    # Modernization Summary
    st.markdown("---")
    st.subheader("Modernization Path")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.info("Priority 1: Easy Wins\nSmall batch utilities with low coupling. Minimal risk for initial cloud migration.")
    with cc2:
        st.warning("Priority 2: Core Logic\nOnline transaction programs (CICS). Requires careful linkage testing.")
    with cc3:
        st.error("Priority 3: The Monoliths\nHigh-complexity programs with >10 incoming calls. Recommended for refactoring first.")


# ═══════════════════════════════════════════════
# PAGE: Call Graph
# ═══════════════════════════════════════════════

def page_call_graph():
    st.header("Program Call Graph")
    st.caption("Inter-program CALL relationships across the CardDemo application")

    calls = q("""
        SELECT pc.caller_program, pc.called_program, pc.call_location, pc.line_number
        FROM program_calls pc ORDER BY pc.caller_program
    """)
    programs = {r["program_id"]: r for r in q("SELECT * FROM programs")}
    internal = set(programs.keys())

    # Unique edges
    edges = {}
    for c in calls:
        key = f"{c['caller_program']}->{c['called_program']}"
        if key not in edges:
            edges[key] = {**c, "count": 1}
        else:
            edges[key]["count"] += 1

    called_set = set(c["called_program"] for c in calls)
    caller_set = set(c["caller_program"] for c in calls)
    entry_points = sorted(set(programs.keys()) - called_set)
    leaf_programs = sorted(set(programs.keys()) - caller_set)
    external = sorted(called_set - internal)

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Unique Edges", len(edges))
    c2.metric("Entry Points", len(entry_points))
    c3.metric("Leaf Programs", len(leaf_programs))
    c4.metric("External Targets", len(external))

    # Mermaid diagram
    st.subheader("Visual Call Graph")

    # Build Mermaid
    mermaid_lines = ["graph LR"]

    # Get modules for subgraphs
    mod_data = q("SELECT m.module_name, mp.program_id FROM modules m JOIN module_programs mp ON m.id = mp.module_id")
    prog_to_mod = {}
    mods = defaultdict(list)
    for m in mod_data:
        prog_to_mod[m["program_id"]] = m["module_name"]
        mods[m["module_name"]].append(m["program_id"])

    for mod_name, mod_progs in sorted(mods.items()):
        safe_mod = m_id(mod_name)
        mermaid_lines.append(f'    subgraph {safe_mod}{m_label(mod_name)}')
        for pid in sorted(mod_progs):
            sid = m_id(pid)
            mermaid_lines.append(f'        {sid}{m_label(pid)}')
        mermaid_lines.append("    end")

    # Unassigned
    unmod = set(programs.keys()) - set(prog_to_mod.keys())
    if unmod:
        mermaid_lines.append('    subgraph OTHER["Other Programs"]')
        for pid in sorted(unmod):
            sid = m_id(pid)
            mermaid_lines.append(f'        {sid}{m_label(pid)}')
        mermaid_lines.append("    end")

    if external:
        mermaid_lines.append('    subgraph EXT["External"]')
        for ext in external:
            se = m_id(ext)
            mermaid_lines.append(f'        {se}{m_label(ext)}:::ext')
        mermaid_lines.append("    end")

    for key, edge in sorted(edges.items()):
        s = m_id(edge["caller_program"])
        t = m_id(edge["called_program"])
        label_text = f'"{edge["count"]}x"' if edge["count"] > 1 else ""
        edge_label = f"|{label_text}|" if label_text else ""
        mermaid_lines.append(f"    {s} -->{edge_label} {t}")

    mermaid_lines.append("    classDef ext fill:#FF9800,stroke:#E65100,color:#fff")
    mermaid_code = "\n".join(mermaid_lines)

    render_mermaid(mermaid_code, height=600)

    # Interactive tables
    tab1, tab2, tab3, tab4 = st.tabs(["Call Matrix", "Entry Points", "Leaf Programs", "External"])

    import pandas as pd
    with tab1:
        rows = []
        for key, edge in sorted(edges.items()):
            rows.append({
                "Caller": edge["caller_program"],
                "Called": edge["called_program"],
                "Location": edge.get("call_location") or "-",
                "Line": edge.get("line_number") or "-",
                "Instances": edge["count"],
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

    with tab2:
        rows = [{"Program": pid, "Type": programs.get(pid, {}).get("program_type", "-"),
                 "Lines": programs.get(pid, {}).get("line_count", "-"),
                 "Business Name": programs.get(pid, {}).get("business_name") or "-"}
                for pid in entry_points]
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

    with tab3:
        rows = [{"Program": pid, "Type": programs.get(pid, {}).get("program_type", "-"),
                 "Lines": programs.get(pid, {}).get("line_count", "-"),
                 "Business Name": programs.get(pid, {}).get("business_name") or "-"}
                for pid in leaf_programs]
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

    with tab4:
        for ext in external:
            callers = sorted(set(e["caller_program"] for e in edges.values() if e["called_program"] == ext))
            st.markdown(f"**`{ext}`** — called by: {', '.join(callers)}")


# ═══════════════════════════════════════════════
# PAGE: Dependency Matrix
# ═══════════════════════════════════════════════

def page_dependency_matrix():
    st.header("Dependency Matrix")
    st.caption("Complete dependency overview — calls, copybooks, files, screens, and control flow per program")

    programs = q("SELECT * FROM programs ORDER BY program_id")
    import pandas as pd

    # Build dependency counts
    rows = []
    for p in programs:
        pid = p["program_id"]
        out = q1("SELECT COUNT(DISTINCT called_program) as c FROM program_calls WHERE caller_program = ?", (pid,))
        inb = q1("SELECT COUNT(DISTINCT caller_program) as c FROM program_calls WHERE called_program = ?", (pid,))
        cbs = q1("SELECT COUNT(DISTINCT copybook_name) as c FROM copybook_usage WHERE program_id = ?", (pid,))
        fils = q1("SELECT COUNT(DISTINCT file_name) as c FROM files WHERE program_id = ?", (pid,))
        scrs = q1("SELECT COUNT(*) as c FROM screens WHERE associated_program = ?", (pid,))
        perfs = q1("SELECT COUNT(*) as c FROM performs WHERE program_id = ?", (pid,))

        rows.append({
            "Program": pid,
            "Type": p.get("program_type") or "-",
            "Calls Out": out["c"] if out else 0,
            "Called By": inb["c"] if inb else 0,
            "Copybooks": cbs["c"] if cbs else 0,
            "Files": fils["c"] if fils else 0,
            "Screens": scrs["c"] if scrs else 0,
            "PERFORMs": perfs["c"] if perfs else 0,
        })

    df = pd.DataFrame(rows)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.multiselect("Filter by Type", sorted(df["Type"].unique()), default=sorted(df["Type"].unique()))
    with col2:
        search = st.text_input("Search Program", "")

    filtered = df[df["Type"].isin(type_filter)]
    if search:
        filtered = filtered[filtered["Program"].str.contains(search.upper())]

    st.dataframe(filtered, use_container_width=True, height=500)

    # Shared copybooks
    st.markdown("---")
    st.subheader("Shared Copybooks (Data Coupling)")
    st.caption("Copybooks shared by multiple programs — changes affect ALL users")

    shared_cbs = q("""
        SELECT copybook_name, COUNT(DISTINCT program_id) as prog_count,
               GROUP_CONCAT(DISTINCT program_id) as programs
        FROM copybook_usage GROUP BY copybook_name
        ORDER BY prog_count DESC
    """)

    for cb in shared_cbs:
        count = cb["prog_count"]
        if count >= 10:
            risk = "[High Risk]"
        elif count >= 5:
            risk = "[Med Risk]"
        else:
            risk = "[Low Risk]"

        with st.expander(f"{risk} {cb['copybook_name']} — used by {count} programs"):
            progs = cb["programs"].split(",")
            cols = st.columns(min(6, len(progs)))
            for i, p in enumerate(sorted(progs)):
                cols[i % len(cols)].code(p)


# ═══════════════════════════════════════════════
# PAGE: Impact Analysis
# ═══════════════════════════════════════════════

def page_impact_analysis():
    st.header("Impact Analysis")
    st.caption("What happens if you change a program? Who is affected?")

    programs = {r["program_id"]: r for r in q("SELECT * FROM programs")}

    # Build adjacency
    calls_out = defaultdict(set)
    called_by = defaultdict(set)
    for r in q("SELECT caller_program, called_program FROM program_calls"):
        calls_out[r["caller_program"]].add(r["called_program"])
        called_by[r["called_program"]].add(r["caller_program"])

    # Copybook coupling
    cb_to_progs = defaultdict(set)
    prog_to_cbs = defaultdict(set)
    for r in q("SELECT copybook_name, program_id FROM copybook_usage"):
        cb_to_progs[r["copybook_name"]].add(r["program_id"])
        prog_to_cbs[r["program_id"]].add(r["copybook_name"])

    def transitive(pid, graph, visited=None):
        if visited is None:
            visited = set()
        for nxt in graph.get(pid, set()):
            if nxt not in visited and nxt in programs:
                visited.add(nxt)
                transitive(nxt, graph, visited)
        return visited

    def cb_impact(pid):
        affected = set()
        for cb in prog_to_cbs.get(pid, set()):
            affected.update(cb_to_progs.get(cb, set()))
        affected.discard(pid)
        return affected

    # Program selector
    selected = st.selectbox("Select a program to analyze", sorted(programs.keys()))

    if selected:
        p = programs[selected]
        direct_callers = called_by.get(selected, set()) & set(programs.keys())
        trans_callers = transitive(selected, called_by)
        direct_callees = calls_out.get(selected, set()) & set(programs.keys())
        trans_callees = transitive(selected, calls_out)
        coupling = cb_impact(selected)
        total_impact = len(trans_callers | coupling)

        # Risk rating
        if total_impact >= 10:
            risk_label = "HIGH RISK"
            risk_color = "red"
        elif total_impact >= 5:
            risk_label = "MEDIUM RISK"
            risk_color = "orange"
        else:
            risk_label = "LOW RISK"
            risk_color = "green"

        # Program info header
        st.markdown(f"""
        ### {selected} — {p.get('business_name') or 'N/A'}
        **Type:** `{p.get('program_type', '-')}` | **Lines:** `{p.get('line_count', '-')}` | **Risk:** :{risk_color}[{risk_label}] | **Total Impact:** `{total_impact} programs`
        """)

        # Metrics
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Direct Callers", len(direct_callers))
        c2.metric("Transitive Callers", len(trans_callers))
        c3.metric("Direct Callees", len(direct_callees))
        c4.metric("Transitive Callees", len(trans_callees))
        c5.metric("Copybook Coupling", len(coupling))

        # Visualize impact as Mermaid
        if direct_callers or direct_callees or coupling:
            st.subheader("Impact Graph")
            impact_mermaid = ["graph LR"]
            sp = selected.replace("-", "_")
            impact_mermaid.append(f'    {sp}{m_label(selected)}:::target')

            for c in sorted(direct_callers):
                sc = m_id(c)
                impact_mermaid.append(f'    {sc}{m_label(c)}:::caller --> {sp}')
            for c in sorted(direct_callees):
                sc = m_id(c)
                impact_mermaid.append(f'    {sp} --> {sc}{m_label(c)}:::callee')

            # Show a sample of coupling (top 10 to keep readable)
            coupling_sample = sorted(coupling)[:10]
            for c in coupling_sample:
                sc = m_id(c)
                impact_mermaid.append(f'    {sp} -.-|copybook| {sc}{m_label(c)}:::coupled')
            if len(coupling) > 10:
                impact_mermaid.append(f'    {sp} -.-|"+{len(coupling)-10} more"| MORE["..."]:::coupled')

            impact_mermaid.extend([
                "    classDef target fill:#f85149,stroke:#da3633,color:#fff",
                "    classDef caller fill:#58a6ff,stroke:#1f6feb,color:#fff",
                "    classDef callee fill:#3fb950,stroke:#238636,color:#fff",
                "    classDef coupled fill:#d29922,stroke:#9e6a03,color:#fff",
            ])

            render_mermaid(chr(10).join(impact_mermaid), height=450)

        # Detail tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Callers", "Callees", "Copybook Coupling", "Copybooks Used"])

        with tab1:
            if direct_callers:
                for c in sorted(direct_callers):
                    st.markdown(f"- `{c}` — {programs.get(c, {}).get('business_name') or ''}")
            else:
                st.info("No programs call this program directly.")

        with tab2:
            if direct_callees:
                for c in sorted(direct_callees):
                    st.markdown(f"- `{c}` — {programs.get(c, {}).get('business_name') or ''}")
            else:
                st.info("This program doesn't call any other programs.")

        with tab3:
            if coupling:
                st.warning(f"Warning: Changing {selected} may affect {len(coupling)} programs through shared copybooks!")
                for c in sorted(coupling):
                    st.markdown(f"- `{c}` — {programs.get(c, {}).get('business_name') or ''}")
            else:
                st.success("No copybook coupling detected.")

        with tab4:
            cbs = sorted(prog_to_cbs.get(selected, set()))
            if cbs:
                for cb in cbs:
                    users = sorted(cb_to_progs.get(cb, set()) - {selected})
                    st.markdown(f"- **`{cb}`** — also used by: {', '.join(f'`{u}`' for u in users) if users else 'only this program'}")
            else:
                st.info("No copybooks used.")

    # Full impact summary table
    st.markdown("---")
    st.subheader("Full Impact Summary")

    import pandas as pd
    rows = []
    for pid in sorted(programs.keys()):
        tc = transitive(pid, called_by)
        ci = cb_impact(pid)
        total = len(tc | ci)
        rows.append({
            "Program": pid,
            "Type": programs[pid].get("program_type", "-"),
            "Direct Callers": len(called_by.get(pid, set()) & set(programs.keys())),
            "Transitive Callers": len(tc),
            "Copybook Coupling": len(ci),
            "Total Impact": total,
        })

    df = pd.DataFrame(rows).sort_values("Total Impact", ascending=False)
    st.dataframe(df, use_container_width=True, height=400)


# ═══════════════════════════════════════════════
# PAGE: Copybook Dependencies
# ═══════════════════════════════════════════════

def page_copybooks():
    st.header("Copybook Dependency Graph")
    st.caption("Shared data structures — the primary mechanism for data coupling in COBOL")

    import pandas as pd

    copybooks = q("""
        SELECT cu.copybook_name, COUNT(DISTINCT cu.program_id) as prog_count,
               GROUP_CONCAT(DISTINCT cu.program_id) as programs
        FROM copybook_usage cu
        GROUP BY cu.copybook_name
        ORDER BY prog_count DESC
    """)

    total_usages = q1("SELECT COUNT(*) as c FROM copybook_usage")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Copybooks", len(copybooks))
    c2.metric("Total COPY Statements", total_usages["c"] if total_usages else 0)
    high_risk = len([cb for cb in copybooks if cb["prog_count"] >= 10])
    c3.metric("High-Risk Copybooks", high_risk)

    # Search
    search = st.text_input("Search copybook name", "")

    filtered = copybooks
    if search:
        filtered = [cb for cb in copybooks if search.upper() in cb["copybook_name"].upper()]

    # Copybook cards
    for cb in filtered:
        count = cb["prog_count"]
        if count >= 10:
            risk = "[HIGH]"
        elif count >= 5:
            risk = "[MED]"
        else:
            risk = "[LOW]"

        with st.expander(f"{risk} **{cb['copybook_name']}** — {count} programs", expanded=(count >= 10)):
            progs = sorted(cb["programs"].split(","))

            # Show as pills/chips
            prog_str = " • ".join(f"`{p}`" for p in progs)
            st.markdown(prog_str)

            # Bar showing relative usage
            st.progress(min(count / 40, 1.0), text=f"{count} programs use this copybook")

    # Summary table
    st.markdown("---")
    st.subheader("Copybook Usage Table")
    rows = [{"Copybook": cb["copybook_name"], "Programs Using": cb["prog_count"],
             "Risk": "HIGH" if cb["prog_count"] >= 10 else "MED" if cb["prog_count"] >= 5 else "LOW"}
            for cb in copybooks]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: Data Flow
# ═══════════════════════════════════════════════

def page_data_flow():
    st.header("Data Flow Analysis")
    st.caption("How data flows through the CardDemo system — files, VSAM, and I/O patterns")

    import pandas as pd

    files = q("SELECT * FROM files ORDER BY file_name")
    by_file = defaultdict(list)
    for f in files:
        by_file[f["file_name"]].append(f)

    io_stmts = q("""
        SELECT program_id, statement_type, COUNT(*) as cnt
        FROM statements
        WHERE statement_type IN ('READ', 'WRITE', 'REWRITE', 'OPEN', 'CLOSE')
        GROUP BY program_id, statement_type
        ORDER BY program_id
    """)

    c1, c2, c3 = st.columns(3)
    c1.metric("Files Tracked", len(by_file))
    c2.metric("Total File Usages", len(files))
    programs_with_io = len(set(s["program_id"] for s in io_stmts))
    c3.metric("Programs with I/O", programs_with_io)

    # File details
    st.subheader("File Details")
    for fname, fusages in sorted(by_file.items()):
        ftype = fusages[0].get("file_type") or "FILE"
        org = fusages[0].get("organization") or "-"
        progs = sorted(set(fu["program_id"] for fu in fusages))
        accesses = sorted(set(fu.get("access_mode") or "?" for fu in fusages))

        with st.expander(f"File: {fname} ({ftype}) — {len(progs)} programs"):
            st.markdown(f"**Organization:** `{org}`")
            st.markdown(f"**Access Modes:** {', '.join(f'`{a}`' for a in accesses)}")
            st.markdown(f"**Programs:** {', '.join(f'`{p}`' for p in progs)}")

    # I/O Statement Profile
    st.markdown("---")
    st.subheader("I/O Statement Profile")

    io_by_prog = defaultdict(dict)
    for s in io_stmts:
        io_by_prog[s["program_id"]][s["statement_type"]] = s["cnt"]

    rows = []
    for pid in sorted(io_by_prog.keys()):
        stmts = io_by_prog[pid]
        rows.append({
            "Program": pid,
            "READs": stmts.get("READ", 0),
            "WRITEs": stmts.get("WRITE", 0),
            "REWRITEs": stmts.get("REWRITE", 0),
            "OPENs": stmts.get("OPEN", 0),
            "CLOSEs": stmts.get("CLOSE", 0),
        })

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: Program Explorer
# ═══════════════════════════════════════════════

def page_program_explorer():
    st.header("Program Explorer")
    st.caption("Deep-dive into individual programs — source code, local logic, and summaries")

    programs = q("SELECT * FROM programs ORDER BY program_id")
    selected_id = st.selectbox("Select Program", [p["program_id"] for p in programs])

    if selected_id:
        p = q1("SELECT * FROM programs WHERE program_id = ?", (selected_id,))
        
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview", "Source Code", "Paragraphs", "Local Graph", "Business Rules"
        ])

        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(p.get("business_name") or "System Program")
                st.write(p.get("business_purpose") or "No business purpose extracted yet.")
                
                st.markdown("---")
                st.markdown(f"**User Role:** {p.get('user_role') or '-'}")
                st.markdown(f"**Business Process:** {p.get('business_process') or '-'}")
                st.markdown(f"**Type:** `{p.get('program_type') or '-'}`")

                # Enrichment Button
                st.markdown("---")
                if not p.get("business_purpose"):
                    st.warning("This program has not been enriched with business context.")
                    if st.button("Enrich with AI", key=f"enrich_{selected_id}", use_container_width=True):
                        with st.spinner("Analyzing program structure with AI..."):
                            try:
                                api_key = os.environ.get("GROQ_API_KEY")
                                if api_key:
                                    # 1. Fetch full details
                                    loader = SQLiteLoader(DB_PATH)
                                    loader.connect()
                                    full_prog = loader.get_program_details(selected_id)
                                    
                                    # 2. Enrich
                                    enricher = CobolEnricher(groq_api_key=api_key, model="llama-3.1-8b-instant", max_programs=1)
                                    results = enricher.enrich([full_prog])
                                    
                                    # 3. Save (Targeted updates)
                                    # Update program business context
                                    enriched_list = results["programs"]
                                    if enriched_list:
                                        p_enriched = enriched_list[0]
                                        loader.update_business_context(selected_id, p_enriched)
                                    
                                    # Update paragraph narratives
                                    if enriched_list and "paragraphs" in p_enriched:
                                        loader.update_paragraph_narratives(selected_id, p_enriched["paragraphs"])

                                    # Load business rules (this already uses INSERT OR REPLACE and is safe)
                                    loader.load_business_rules(results["business_rules"])
                                    loader.close()
                                    
                                    st.success(f"Successfully enriched {selected_id}!")
                                    st.rerun()
                                else:
                                    st.error("GROQ_API_KEY not found in environment.")
                            except Exception as e:
                                st.error(f"Enrichment failed: {e}")
                else:
                    st.success("Business context is available.")
                    if st.button("Refresh AI Analysis", key=f"re_enrich_{selected_id}", use_container_width=True):
                         # Logic for re-enrichment (optional, same as above)
                        pass
            
            with col2:
                # Complexity Metrics
                st.subheader("Complexity")
                perfs = q1("SELECT COUNT(*) as c FROM performs WHERE program_id = ?", (selected_id,))
                stmts = q1("SELECT COUNT(*) as c FROM statements WHERE program_id = ?", (selected_id,))
                calls = q1("SELECT COUNT(*) as c FROM program_calls WHERE caller_program = ?", (selected_id,))
                
                perf_count = perfs["c"] if perfs else 0
                stmt_count = stmts["c"] if stmts else 0
                call_count = calls["c"] if calls else 0
                
                # Heuristic complexity score
                complexity = (perf_count * 2) + (call_count * 5) + (stmt_count // 10)
                if complexity > 100: risk, color = "High", "red"
                elif complexity > 50: risk, color = "Medium", "orange"
                else: risk, color = "Low", "green"
                
                st.metric("Complexity Score", f"{complexity}")
                st.markdown(f"Risk Profile: :{color}[**{risk}**]")
                
                st.progress(min(complexity / 150, 1.0))
                st.caption(f"Based on {perf_count} PERFORMs and {call_count} External Calls")

        with tab2:
            st.subheader("Source Code")
            fpath = p.get("file_path")
            if fpath:
                try:
                    # Try to read the file
                    code_path = Path(fpath)
                    if not code_path.exists():
                        # Try relative to root
                        code_path = Path("c:/Users/ADMIN/OneDrive/Desktop/doc_demo") / fpath
                    
                    if code_path.exists():
                        code = code_path.read_text(errors="replace")
                        st.code(code, language="cobol", line_numbers=True)
                    else:
                        st.error(f"Source file not found at {fpath}")
                except Exception as e:
                    st.error(f"Error reading source: {e}")
            else:
                st.info("No file path associated with this program.")

        with tab3:
            st.subheader("Paragraphs & Sections")
            paras = q("SELECT * FROM paragraphs WHERE program_id = ? ORDER BY line_start", (selected_id,))
            if paras:
                import pandas as pd
                df = pd.DataFrame(paras)
                st.dataframe(df[["paragraph_name", "business_name", "purpose", "line_start", "line_end"]], use_container_width=True)
            else:
                st.info("No paragraph info available.")

        with tab4:
            st.subheader("Local Control Flow")
            local_calls = q("SELECT * FROM program_calls WHERE caller_program = ?", (selected_id,))
            local_perfs = q("SELECT * FROM performs WHERE program_id = ?", (selected_id,))
            
            if local_calls or local_perfs:
                hide_inline = st.checkbox("Hide INLINE nodes", value=False)
                
                mermaid = ["graph TD"]
                m_start = m_id(selected_id)
                mermaid.append(f'    {m_start}{m_label(selected_id)}:::root')
                
                # External calls
                for c in local_calls:
                    target_raw = c["called_program"]
                    target = m_id(target_raw)
                    label = target_raw if target_raw != "UNKNOWN" else "External Call (Unresolved)"
                    mermaid.append(f'    {m_start} -->|CALL| {target}{m_label(label)}:::ext')
                
                # Internal performs (top 30 for readability)
                for p_flow in local_perfs[:30]:
                    src_raw = p_flow["source_paragraph"]
                    tgt_raw = p_flow["target_paragraph"]
                    src = m_id(src_raw)
                    tgt = m_id(tgt_raw)
                    
                    if hide_inline and (src_raw == "INLINE" or tgt_raw == "INLINE"):
                        continue
                        
                    mermaid.append(f'    {src}{m_label(src_raw)} -->|PERFORM| {tgt}{m_label(tgt_raw)}')

                mermaid.extend([
                    "    classDef root fill:#f85149,stroke:#da3633,color:#fff",
                    "    classDef ext fill:#FF9800,stroke:#E65100,color:#fff",
                ])
                render_mermaid("\n".join(mermaid), height=500)
            else:
                st.info("No local control flow data found.")

        with tab5:
            st.subheader("Business Rules Extracted")
            rules = q("SELECT * FROM business_rules WHERE program_id = ?", (selected_id,))
            if rules:
                for r in rules:
                    with st.expander(f"Rule: {r['rule_name']} ({r['category']})"):
                        st.markdown(f"**Rule:** {r['rule_statement']}")
                        if r.get('condition_text'):
                            st.markdown(f"**Condition:** `{r['condition_text']}`")
                        if r.get('action_text'):
                            st.markdown(f"**Action:** {r['action_text']}")
                        if r.get('source_code'):
                            st.code(r['source_code'], language="cobol")
            else:
                st.info("No business rules extracted for this program yet.")
        
        # Add context-specific Chat Assistant
        st.markdown("---")
        st.subheader(f"💬 Chat about {selected_id}")

        # Action buttons row: PDF + JSON
        act_col1, act_col2, act_col3 = st.columns(3)
        with act_col1:
            if st.button("📄 Download PDF Report", key=f"pdf_{selected_id}", use_container_width=True):
                try:
                    from src.pdf_generator import PDFReportGenerator
                    gen = PDFReportGenerator()
                    prog_data = q1("SELECT * FROM programs WHERE program_id = ?", (selected_id,))
                    calls_from_data = q("SELECT pc.called_program, pc.call_location, pc.line_number, p.business_name FROM program_calls pc LEFT JOIN programs p ON pc.called_program = p.program_id WHERE pc.caller_program = ?", (selected_id,))
                    called_by_data = q("SELECT pc.caller_program, pc.call_location, pc.line_number, p.business_name FROM program_calls pc LEFT JOIN programs p ON pc.caller_program = p.program_id WHERE pc.called_program = ?", (selected_id,))
                    rules_data = q("SELECT * FROM business_rules WHERE program_id = ?", (selected_id,))
                    paras_data = q("SELECT * FROM paragraphs WHERE program_id = ? ORDER BY line_start", (selected_id,))
                    pdf_bytes = gen.generate_program_report(prog_data, calls_from_data, called_by_data, rules_data, paras_data)
                    st.download_button(
                        label=f"⬇️ Download {selected_id}.pdf",
                        data=pdf_bytes,
                        file_name=f"{selected_id}_report.pdf",
                        mime="application/pdf",
                        key=f"dl_pdf_{selected_id}"
                    )
                except ImportError:
                    st.error("PDF generation requires fpdf2. Install with: pip install fpdf2")
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")

        with act_col2:
            if st.button("🔄 JSON → English", key=f"json_{selected_id}", use_container_width=True):
                st.session_state[f"show_json_{selected_id}"] = True

        with act_col3:
            # Neo4j graph query button
            if st.button("🌐 Graph Analysis", key=f"graph_{selected_id}", use_container_width=True):
                st.session_state[f"show_graph_{selected_id}"] = True

        # JSON Translation Panel
        if st.session_state.get(f"show_json_{selected_id}"):
            selected_model = st.selectbox("Groq Model", GROQ_MODELS, key=f"model_sel_{selected_id}")
            with st.spinner(f"Generating English explanation with {selected_model}..."):
                result = translate_program_to_english(selected_id, model=selected_model)
            if result.get("found"):
                source_label = "🤖 LLM (Groq)" if result.get("source") == "llm" else "📐 Rule-based"
                st.caption(f"Explanation source: {source_label}")
                json_tab1, json_tab2 = st.tabs(["📝 English Explanation", "💾 Raw Parsed JSON"])
                with json_tab1:
                    st.markdown(result["english"])
                with json_tab2:
                    st.code(result["raw_json"], language="json")
            else:
                st.warning(result["english"])

        # Neo4j Graph Analysis Panel
        if st.session_state.get(f"show_graph_{selected_id}"):
            if "chat_engine" in st.session_state and st.session_state.chat_engine and st.session_state.chat_engine.neo4j_available:
                graph_tab1, graph_tab2 = st.tabs(["📈 Dependencies", "💥 Blast Radius"])
                with graph_tab1:
                    deps = st.session_state.chat_engine.neo4j_dependencies(selected_id)
                    st.markdown(deps)
                with graph_tab2:
                    impact = st.session_state.chat_engine.neo4j_blast_radius(selected_id)
                    st.markdown(impact)
            else:
                st.info("📌 Neo4j is not connected. Set NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD in `.env` and restart.")

        render_chat_ui(current_program=selected_id)


# ═══════════════════════════════════════════════
# PAGE: Migration Readiness
# ═══════════════════════════════════════════════

def page_migration_readiness():
    st.header("Migration Readiness & Planning")
    st.caption("Identify high-risk programs and prioritize migration effort")

    programs = q("SELECT * FROM programs")
    
    # Adjacency for impact
    called_by = defaultdict(set)
    for r in q("SELECT caller_program, called_program FROM program_calls"):
        called_by[r["called_program"]].add(r["caller_program"])
        
    def transitive_count(pid, visited=None):
        if visited is None: visited = set()
        for nxt in called_by.get(pid, set()):
            if nxt not in visited and nxt in [p["program_id"] for p in programs]:
                visited.add(nxt)
                transitive_count(nxt, visited)
        return len(visited)

    # Calculate metrics for all
    rows = []
    for p in programs:
        pid = p["program_id"]
        
        # Complexity (heuristic)
        perfs = q1("SELECT COUNT(*) as c FROM performs WHERE program_id = ?", (pid,))["c"]
        stmts = q1("SELECT COUNT(*) as c FROM statements WHERE program_id = ?", (pid,))["c"]
        calls = q1("SELECT COUNT(*) as c FROM program_calls WHERE caller_program = ?", (pid,))["c"]
        comp = (perfs * 2) + (calls * 5) + (stmts // 10)
        
        # Impact
        impact = transitive_count(pid)
        
        # Readiness Score (0-100)
        # Higher complexity and higher impact = Lower readiness (more difficult/risky)
        readiness = max(0, 100 - (comp // 2) - (impact * 2))
        
        rows.append({
            "Program": pid,
            "Type": p["program_type"],
            "Complexity": comp,
            "Impact": impact,
            "Readiness": readiness,
            "Effort (Dev Days)": max(1, comp // 10)
        })
        
    import pandas as pd
    df = pd.DataFrame(rows)
    
    # Portfolio Summary
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Readiness", f"{int(df['Readiness'].mean())}%")
    c2.metric("High Risk", len(df[df['Readiness'] < 30]))
    c3.metric("Easy Wins", len(df[df['Readiness'] > 70]))
    c4.metric("Total Est. Effort", f"{int(df['Effort (Dev Days)'].sum())} days")
    
    st.markdown("---")
    
    # Quadrant Chart: Complexity vs Impact
    st.subheader("Migration Strategy Quadrants")
    import plotly.express as px
    fig = px.scatter(df, x="Complexity", y="Impact", text="Program", color="Readiness",
                     color_continuous_scale="RdYlGn", 
                     title="Program Landscape (Red = Hardest/Riskiest to Move)")
    fig.update_traces(textposition='top center')
    fig.add_hline(y=df["Impact"].median(), line_dash="dot", annotation_text="High Impact")
    fig.add_vline(x=df["Complexity"].median(), line_dash="dot", annotation_text="High Complexity")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Legend:**
    - **Top Right (High Impact / High Complex):** Monoliths — Critical path, move with extreme caution.
    - **Top Left (High Impact / Low Complex):** Core Enablers — Strategy target for early migration.
    - **Bottom Right (Low Impact / High Complex):** Isolated Complexity — Refactor before moving.
    - **Bottom Left (Low Impact / Low Complex):** Easy Wins — Proof of concept candidates.
    """)
    
    st.markdown("---")
    st.subheader("Migration Backlog")
    st.dataframe(df.sort_values("Readiness"), use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: Chat Assistant
# ═══════════════════════════════════════════════

# ═══════════════════════════════════════════════
# Shared Chat UI Component
# ═══════════════════════════════════════════════

def render_chat_ui(current_program=None):
    # Initialize chat engine
    if "chat_engine" not in st.session_state or st.session_state.chat_engine is None:
        reinit_chat = True
    else:
        # Check if connection is lost
        try:
            st.session_state.chat_engine.conn.execute("SELECT 1")
            reinit_chat = False
        except:
            reinit_chat = True

    if reinit_chat:
        try:
            from src.chat_cli import KnowledgeBaseChat
            api_key = os.environ.get("GROQ_API_KEY")
            # Inject the global cached connection
            st.session_state.chat_engine = KnowledgeBaseChat(
                DB_PATH, 
                groq_api_key=api_key, 
                connection=get_db()
            )
            st.session_state.chat_mode = "AI" if api_key else "Search"
        except Exception as e:
            st.session_state.chat_engine = None
            st.session_state.chat_error = str(e)

    # Scoped messages for this program (or global)
    msg_key = f"messages_{current_program}" if current_program else "messages"
    
    if msg_key not in st.session_state:
        st.session_state[msg_key] = []

    # Mode indicator
    if st.session_state.get("chat_engine"):
        mode = st.session_state.get("chat_mode", "Search")
        engine = st.session_state.chat_engine
        neo4j_badge = "✅ Neo4j" if engine.neo4j_available else "❌ Neo4j"

        if mode == "AI":
            if current_program:
                st.success(f"AI Chat (Groq) — Context: {current_program} | {neo4j_badge}")
            else:
                st.success(f"AI-powered mode (Groq LLM + RAG) | {neo4j_badge}")
        else:
            if current_program:
                st.warning(f"Search-only mode — Context: {current_program} | {neo4j_badge}")
            else:
                st.warning(f"Search-only mode (no API key) | {neo4j_badge}")
    else:
        st.error(f"Chat engine failed to load: {st.session_state.get('chat_error', 'unknown error')}")
        return

    # Quick action buttons
    st.markdown("**Quick questions:**")
    qcols = st.columns(4)
    if current_program:
        quick_questions = [
            "What does this program do?",
            "Who calls it?",
            "What files does it use?",
            "What are the data items?",
        ]
    else:
        quick_questions = [
            "What does CBACT01C do?",
            "Who calls CBTRN02C?",
            "List all batch programs",
            "What files does CBEXPORT use?",
        ]
        
    for i, qq in enumerate(quick_questions):
        btn_key = f"qq_{current_program}_{i}" if current_program else f"qq_{i}"
        if qcols[i].button(qq, key=btn_key, use_container_width=True):
            st.session_state[msg_key].append({"role": "user", "content": qq})
            with st.spinner("Thinking..."):
                answer = st.session_state.chat_engine.ask(qq, current_program=current_program)
            st.session_state[msg_key].append({"role": "assistant", "content": answer})
            st.rerun()

    st.markdown("---")

    # Chat history display
    for msg in st.session_state[msg_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    chat_prompt_msg = f"Ask about {current_program}..." if current_program else "Ask about the COBOL knowledge base..."
    
    # We use a unique key for the chat input so multiple chat components don't clash on the same page
    input_key = f"chat_input_{current_program}" if current_program else "chat_input_global"
    
    if prompt := st.chat_input(chat_prompt_msg, key=input_key):
        st.session_state[msg_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                answer = st.session_state.chat_engine.ask(prompt, current_program=current_program)
            st.markdown(answer)
        st.session_state[msg_key].append({"role": "assistant", "content": answer})

    # Clear chat button
    if st.session_state[msg_key]:
        clear_key = f"clear_chat_{current_program}" if current_program else "clear_chat"
        if st.button("Clear Chat", key=clear_key):
            st.session_state[msg_key] = []
            if st.session_state.get("chat_engine"):
                st.session_state.chat_engine.history = []
            st.rerun()

# ═══════════════════════════════════════════════
# PAGE: Chat Assistant
# ═══════════════════════════════════════════════

def page_chat():
    st.header("Knowledge Base Chat")
    st.caption("Ask questions about the CardDemo COBOL system — powered by RAG + Groq LLM")

    # Tool buttons
    tool_col1, tool_col2, tool_col3 = st.columns(3)
    with tool_col1:
        if st.button("📄 Export Chat as PDF", key="export_chat_pdf", use_container_width=True):
            msg_key = "messages"
            msgs = st.session_state.get(msg_key, [])
            if msgs:
                try:
                    from src.pdf_generator import PDFReportGenerator
                    gen = PDFReportGenerator()
                    pdf_bytes = gen.generate_chat_pdf(msgs)
                    st.download_button(
                        label="⬇️ Download Chat PDF",
                        data=pdf_bytes,
                        file_name="chat_export.pdf",
                        mime="application/pdf",
                        key="dl_chat_pdf"
                    )
                except ImportError:
                    st.error("Install fpdf2: pip install fpdf2")
                except Exception as e:
                    st.error(f"PDF export failed: {e}")
            else:
                st.info("No chat messages to export yet.")

    with tool_col2:
        json_prog = st.text_input("Program ID for JSON→English", key="json_lookup_input", placeholder="e.g. CBACT01C")
        chat_model_sel = st.selectbox("Groq Model", GROQ_MODELS, key="json_model_sel")
        if json_prog and st.button("🔄 Translate", key="json_lookup_btn"):
            with st.spinner(f"Generating English explanation with {chat_model_sel}..."):
                result = translate_program_to_english(json_prog.strip().upper(), model=chat_model_sel)
            if result.get("found"):
                source_label = "🤖 LLM (Groq)" if result.get("source") == "llm" else "📐 Rule-based"
                st.caption(f"Explanation source: {source_label}")
                json_tab1, json_tab2 = st.tabs(["📝 English Explanation", "💾 Raw JSON"])
                with json_tab1:
                    st.markdown(result["english"])
                with json_tab2:
                    st.code(result["raw_json"], language="json")
            else:
                st.warning(result["english"])

    with tool_col3:
        graph_prog = st.text_input("Program ID for Graph Query", key="graph_lookup_input", placeholder="e.g. CBTRN02C")
        if graph_prog and st.button("🌐 Query Graph", key="graph_lookup_btn"):
            engine = st.session_state.get("chat_engine")
            if engine and engine.neo4j_available:
                pid = graph_prog.strip().upper()
                g_tab1, g_tab2 = st.tabs(["📈 Dependencies", "💥 Blast Radius"])
                with g_tab1:
                    st.markdown(engine.neo4j_dependencies(pid))
                with g_tab2:
                    st.markdown(engine.neo4j_blast_radius(pid))
            else:
                st.info("Neo4j is not connected. Set NEO4J credentials in .env")

    st.markdown("---")
    render_chat_ui(current_program=None)


# ═══════════════════════════════════════════════
# Router
# ═══════════════════════════════════════════════

page_map = {
    "Overview": page_overview,
    "Call Graph": page_call_graph,
    "Dependency Matrix": page_dependency_matrix,
    "Program Explorer": page_program_explorer,
    "Impact Analysis": page_impact_analysis,
    "Migration Readiness": page_migration_readiness,
    "Copybooks": page_copybooks,
    "Data Flow": page_data_flow,
    "Chat Assistant": page_chat,
}

page_map[page]()
