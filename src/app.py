"""
COBOL Documentation Dashboard — Streamlit app
Provides interactive exploration of the parsed and enriched COBOL system:
  - System Overview & Stats
  - Interactive Call Graph (pyvis)
  - Module Structure (all programs)
  - Program Explorer with control flow
  - Migration Readiness Assessment
  - Business Rules Catalog
  - Live Search
"""

import streamlit as st
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
import sqlite3
import pandas as pd
import tempfile
import io

# Ensure src/ is on path when launched as `streamlit run src/app.py`
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Force IPv4 for Vertex AI gRPC
os.environ.setdefault("GRPC_DNS_RESOLVER", "native")

from orchestrator import run_pipeline
from sqlite_loader import SQLiteLoader

st.set_page_config(
    page_title="COBOL Migration Hub",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.main { background-color: #0e1117; }
.stButton>button {
    width: 100%; border-radius: 5px; height: 3em;
    background-color: #262730; color: #00ff00; border: 1px solid #00ff00;
}
.stButton>button:hover { background-color: #00ff00; color: #000000; }
.metric-card {
    padding: 15px; border-radius: 8px; background-color: #1e1e1e;
    border: 1px solid #333; text-align: center;
}
.risk-high { color: #f85149; font-weight: bold; }
.risk-medium { color: #d29922; font-weight: bold; }
.risk-low { color: #3fb950; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


# 
# Helpers
# 

@st.cache_resource
def get_loader():
    db_path = os.getenv("DB_PATH", "data/cobol_knowledge.db")
    return SQLiteLoader(db_path)


def db_connect():
    loader = get_loader()
    loader.connect()
    return loader


def search_cobol_files(repo_path, query):
    results = []
    if not repo_path or not os.path.exists(repo_path):
        return results
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.upper().endswith((".CBL", ".COB", ".CPY")):
                file_path = Path(root) / file
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        for i, line in enumerate(f):
                            if query.lower() in line.lower():
                                results.append({
                                    "file": file, "line": i + 1,
                                    "content": line.strip(),
                                })
                except Exception:
                    pass
    return results


def migration_score(prog: dict) -> int:
    """Score 1-5: how hard to migrate. 5 = hardest."""
    score = 1
    lines = prog.get("line_count", 0) or 0
    if lines > 2000:
        score += 2
    elif lines > 500:
        score += 1
    ptype = prog.get("program_type", "")
    if ptype == "ONLINE":
        score += 1          # CICS screen programs are harder
    bp = prog.get("business_purpose") or ""
    if any(kw in bp.lower() for kw in ["cics", "vsam", "db2", "complex", "batch"]):
        score += 1
    return min(score, 5)


def score_label(s: int) -> str:
    if s >= 4:
        return "High"
    if s == 3:
        return "🟡Medium"
    return "🟢Low"


def render_mermaid(diagram_code: str, height: int = 400):
    """Render a Mermaid diagram using mermaid.js via HTML component."""
    # Strip ```mermaid ... ``` fences if present
    code = diagram_code.strip()
    if code.startswith("```mermaid"):
        code = code[len("```mermaid"):].strip()
    if code.endswith("```"):
        code = code[:-3].strip()

    html = f"""
    <div id="mermaid-container" style="background:#1e1e2e;padding:16px;border-radius:8px;overflow:auto;">
      <div class="mermaid" style="text-align:center;">
{code}
      </div>
    </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{
        startOnLoad: true,
        theme: 'dark',
        themeVariables: {{
          primaryColor: '#58a6ff',
          primaryTextColor: '#c9d1d9',
          primaryBorderColor: '#30363d',
          lineColor: '#8b949e',
          secondaryColor: '#161b22',
          tertiaryColor: '#0d1117',
          background: '#1e1e2e',
          mainBkg: '#1e1e2e',
          nodeBorder: '#30363d',
          clusterBkg: '#161b22',
          titleColor: '#c9d1d9',
          edgeLabelBackground: '#161b22',
          fontSize: '14px'
        }}
      }});
    </script>
    """
    st.components.v1.html(html, height=height, scrolling=True)


# 
# Sidebar
# 

def render_sidebar():
    st.sidebar.title("Control Panel")
    repo_path = st.sidebar.text_input("Repository Path", value="./carddemo/app")
    output_dir = st.sidebar.text_input("Output Directory", value="docs_streamlit")

    st.sidebar.subheader("Pipeline Steps")
    do_parse   = st.sidebar.checkbox("Parse COBOL (ProLeap)", value=True)
    do_jcl     = st.sidebar.checkbox("Parse JCL Jobs", value=True)
    do_enrich  = st.sidebar.checkbox("AI Enrichment (Groq)", value=False)
    do_neo4j   = st.sidebar.checkbox("Export to Neo4j", value=False)

    if st.sidebar.button("Run Full Pipeline"):
        with st.status("Executing Pipeline...", expanded=True) as status:
            run_pipeline(
                repo_path=repo_path,
                output_dir=output_dir,
                skip_parse=not do_parse,
                skip_jcl=not do_jcl,
                skip_enrich=not do_enrich,
                skip_neo4j=not do_neo4j,
                groq_api_key=os.getenv("GROQ_API_KEY"),
                groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            )
            status.update(label="Pipeline Complete!", state="complete", expanded=False)
        st.success("Documentation generated successfully!")

    return repo_path, output_dir


# 
# Tab 1: Overview
# 

def page_overview():
    st.header("System Overview")
    try:
        loader = db_connect()
        programs = loader.get_all_programs()
        rules    = loader.get_all_business_rules()
        screens  = loader.get_all_screens()
        modules  = loader.get_all_modules()
        cg       = loader.get_call_graph()
        loader.close()
    except Exception as e:
        st.error(f"Database not ready — run the pipeline first. ({e})")
        return

    online = [p for p in programs if p.get("program_type") == "ONLINE"]
    batch  = [p for p in programs if p.get("program_type") != "ONLINE"]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Programs", len(programs))
    c2.metric("Online (CICS)", len(online))
    c3.metric("Batch", len(batch))
    c4.metric("Modules", len(modules))
    c5.metric("Business Rules", len(rules))

    c6, c7, c8 = st.columns(3)
    c6.metric("BMS Screens", len(screens))
    c7.metric("Inter-Program Calls", len(cg))
    c8.metric("Enriched Programs", sum(1 for p in programs if p.get("business_purpose")))

    st.divider()
    st.subheader("System Architecture")

    try:
        from pyvis.network import Network as _Network
        _pyvis_ok = True
    except ImportError:
        _pyvis_ok = False

    if not _pyvis_ok:
        st.warning("pyvis not installed — install it with `pip install pyvis` to see the 3-layer graph.")
    else:
        # Query JCL→Program links
        try:
            _db_path = os.getenv("DB_PATH", "data/cobol_knowledge.db")
            _conn = sqlite3.connect(_db_path)
            _jcl_df = pd.read_sql_query(
                "SELECT DISTINCT job_name, program FROM jcl_steps "
                "WHERE program IS NOT NULL AND program != ''",
                _conn,
            )
            _cb_df = pd.read_sql_query(
                "SELECT copybook_name, COUNT(*) as cnt FROM copybook_usage "
                "GROUP BY copybook_name HAVING cnt >= 3",
                _conn,
            )
            _conn.close()
            _jcl_rows = [(_r["job_name"], _r["program"]) for _, _r in _jcl_df.iterrows()]
            _top_cbs  = [_r["copybook_name"] for _, _r in _cb_df.iterrows()]
        except Exception:
            _jcl_rows = []
            _top_cbs  = []

        # Build module color maps for this page
        _module_colors = [
            "#58a6ff","#3fb950","#d29922","#f85149","#bc8cff",
            "#39d353","#ff7b72","#79c0ff","#ffa657","#56d364",
            "#e3b341","#db6d28","#388bfd","#f0883e","#7ee787",
        ]
        _prog_to_color  = {}
        _prog_to_module = {}
        for _i, _m in enumerate(modules):
            _c = _module_colors[_i % len(_module_colors)]
            _n = _m.get("business_name") or _m.get("module_name", "")
            for _p in _m.get("programs", []):
                _prog_to_color[_p["program_id"]]  = _c
                _prog_to_module[_p["program_id"]] = _n

        _arch_net = _Network(height="580px", width="100%", bgcolor="#0e1117",
                             font_color="white", directed=True)
        _arch_net.barnes_hut(gravity=-5000, central_gravity=0.4, spring_length=150)

        _added_arch = set()

        # Layer 1: JCL Jobs — triangle, orange
        _jcl_jobs = sorted({r[0] for r in _jcl_rows})
        for _job in _jcl_jobs[:20]:
            _arch_net.add_node(
                f"JOB_{_job}", label=_job,
                color="#f0883e", shape="triangle", size=22,
                title=f"<b>JCL Job: {_job}</b>",
            )
            _added_arch.add(f"JOB_{_job}")

        # Layer 2: Programs — dot, colored by module
        for _prog in programs[:60]:
            _pid = _prog["program_id"]
            _col = _prog_to_color.get(_pid, "#484f58")
            _mod = _prog_to_module.get(_pid, "Unknown")
            _arch_net.add_node(
                _pid, label=_pid,
                color=_col, shape="dot", size=14,
                title=f"<b>{_pid}</b><br>Module: {_mod}<br>Type: {_prog.get('program_type','?')}",
            )
            _added_arch.add(_pid)

        # Layer 3: Key copybooks — square, gold
        for _cb in _top_cbs[:30]:
            _arch_net.add_node(
                f"CB_{_cb}", label=_cb,
                color="#d29922", shape="square", size=10,
                title=f"<b>{_cb}</b><br>Shared Copybook",
            )
            _added_arch.add(f"CB_{_cb}")

        # Edges: JCL → Program (orange)
        for _job, _prog_name in _jcl_rows:
            if f"JOB_{_job}" in _added_arch and _prog_name in _added_arch:
                _arch_net.add_edge(f"JOB_{_job}", _prog_name, color="#f0883e", arrows="to", width=2)

        # Edges: Program → Program (blue)
        for _c in cg[:50]:
            if _c.get("called_program") and _c["called_program"] != "UNKNOWN":
                if _c["caller_program"] in _added_arch and _c["called_program"] in _added_arch:
                    _arch_net.add_edge(_c["caller_program"], _c["called_program"],
                                       color="#58a6ff", arrows="to", width=1)

        # Edges: Program → Copybook (dashed yellow)
        try:
            _db_path2 = os.getenv("DB_PATH", "data/cobol_knowledge.db")
            _conn2 = sqlite3.connect(_db_path2)
            _cu_df = pd.read_sql_query("SELECT program_id, copybook_name FROM copybook_usage", _conn2)
            _conn2.close()
            for _, _row in _cu_df.iterrows():
                _pid2 = _row["program_id"]
                _cb2  = f"CB_{_row['copybook_name']}"
                if _pid2 in _added_arch and _cb2 in _added_arch:
                    _arch_net.add_edge(_pid2, _cb2, color="#d29922", arrows="to",
                                       dashes=True, width=1)
        except Exception:
            pass

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as _f:
            _arch_net.save_graph(_f.name)
            _arch_html_path = _f.name
        with open(_arch_html_path, "r", encoding="utf-8") as _f:
            _arch_html = _f.read()
        st.components.v1.html(_arch_html, height=600, scrolling=False)
        st.caption("JCL Jobs (Layer 1) →  Programs (Layer 2, colors=modules) → 🟡 Shared Copybooks (Layer 3)")

    st.divider()
    st.subheader("Modules at a Glance")
    rows = []
    for m in modules:
        rows.append({
            "Module": m.get("business_name") or m.get("module_name"),
            "Programs": len(m.get("programs", [])),
            "Purpose": (m.get("business_purpose") or m.get("description") or "-")[:80],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# 
# Tab 2: Interactive Call Graph
# 

def page_call_graph():
    st.header("Interactive Call Graph")
    st.caption("Click and drag nodes. Scroll to zoom. Hover for details.")

    try:
        from pyvis.network import Network
    except ImportError:
        st.error("pyvis not installed. Run: `pip install pyvis`")
        return

    try:
        loader = db_connect()
        programs = loader.get_all_programs()
        cg       = loader.get_call_graph()
        modules  = loader.get_all_modules()
        loader.close()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    # Build module → color map
    module_colors = [
        "#58a6ff", "#3fb950", "#d29922", "#f85149", "#bc8cff",
        "#39d353", "#ff7b72", "#79c0ff", "#ffa657", "#56d364",
        "#e3b341", "#db6d28", "#388bfd", "#f0883e", "#7ee787",
    ]
    prog_to_module = {}
    prog_to_color  = {}
    module_name_list = []
    for i, m in enumerate(modules):
        color = module_colors[i % len(module_colors)]
        name  = m.get("business_name") or m.get("module_name", "")
        if name:
            module_name_list.append(name)
        for p in m.get("programs", []):
            prog_to_module[p["program_id"]] = name
            prog_to_color[p["program_id"]]  = color

    prog_map = {p["program_id"]: p for p in programs}

    #  Filters row 
    col_mod, col_cb = st.columns([3, 1])
    with col_mod:
        selected_module = st.selectbox(
            "Filter by Module",
            ["All Modules"] + sorted(module_name_list),
            key="call_graph_module_filter",
        )
    with col_cb:
        show_copybooks = st.checkbox("Show Copybooks", value=False, key="call_graph_show_copybooks")

    # Apply module filter — keep programs in selected module + their direct neighbours
    if selected_module != "All Modules":
        module_programs = {
            p["program_id"]
            for p in programs
            if prog_to_module.get(p["program_id"]) == selected_module
        }
        # Include direct call neighbours
        neighbour_programs = set()
        for c in cg:
            if c["caller_program"] in module_programs and c.get("called_program") not in (None, "UNKNOWN"):
                neighbour_programs.add(c["called_program"])
            if c.get("called_program") in module_programs:
                neighbour_programs.add(c["caller_program"])
        visible_programs = module_programs | neighbour_programs
        programs_to_show = [p for p in programs if p["program_id"] in visible_programs]
        cg_to_show = [
            c for c in cg
            if c["caller_program"] in visible_programs
            and c.get("called_program") in visible_programs
        ]
    else:
        programs_to_show = programs
        cg_to_show = cg
        visible_programs = {p["program_id"] for p in programs}

    # Query call frequency for edge thickness
    try:
        db_path = os.getenv("DB_PATH", "data/cobol_knowledge.db")
        conn_raw = sqlite3.connect(db_path)
        freq_df = pd.read_sql_query(
            "SELECT caller_program, called_program, COUNT(*) as freq "
            "FROM program_calls WHERE called_program != 'UNKNOWN' "
            "GROUP BY caller_program, called_program",
            conn_raw,
        )
        conn_raw.close()
        freq_map = {(row["caller_program"], row["called_program"]): row["freq"] for _, row in freq_df.iterrows()}
    except Exception:
        freq_map = {}

    # Query copybook usage if needed
    copybook_usage = []
    if show_copybooks:
        try:
            db_path = os.getenv("DB_PATH", "data/cobol_knowledge.db")
            conn_raw = sqlite3.connect(db_path)
            cb_df = pd.read_sql_query(
                "SELECT program_id, copybook_name FROM copybook_usage", conn_raw
            )
            conn_raw.close()
            copybook_usage = [
                (row["program_id"], row["copybook_name"])
                for _, row in cb_df.iterrows()
                if row["program_id"] in visible_programs
            ]
        except Exception:
            copybook_usage = []

    # Determine entry points and leaf programs
    callers = {c["caller_program"] for c in cg_to_show}
    callees = {c["called_program"]  for c in cg_to_show if c["called_program"] != "UNKNOWN"}
    entry_points = {p["program_id"] for p in programs_to_show if p["program_id"] not in callees}
    leaf_progs   = {p["program_id"] for p in programs_to_show if p["program_id"] not in callers}

    net = Network(height="650px", width="100%", bgcolor="#0e1117",
                  font_color="white", directed=True)
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=120)

    # Add program nodes
    added = set()
    for prog in programs_to_show:
        pid   = prog["program_id"]
        color = prog_to_color.get(pid, "#484f58")
        shape = "star" if pid in entry_points else ("diamond" if pid in leaf_progs else "dot")
        bname = prog.get("business_name") or pid
        bpurp = (prog.get("business_purpose") or "")[:120]
        mod   = prog_to_module.get(pid, "Unknown")
        tip   = f"<b>{pid}</b><br>{bname}<br>Module: {mod}<br>Type: {prog.get('program_type','?')}<br>Lines: {prog.get('line_count',0)}<br>{bpurp}"
        net.add_node(pid, label=pid, title=tip, color=color, shape=shape, size=18 if pid in entry_points else 12)
        added.add(pid)

    # Add external/unknown call targets if any
    for c in cg_to_show:
        if c["called_program"] and c["called_program"] != "UNKNOWN" and c["called_program"] not in added:
            net.add_node(c["called_program"], label=c["called_program"],
                         color="#f0883e", shape="triangle", size=10,
                         title=f"<b>{c['called_program']}</b><br>External program")
            added.add(c["called_program"])

    # Add copybook nodes
    if show_copybooks:
        cb_nodes_added = set()
        for prog_id, cb_name in copybook_usage:
            if cb_name not in cb_nodes_added:
                net.add_node(
                    f"CB_{cb_name}", label=cb_name,
                    color="#d29922", shape="square", size=10,
                    title=f"<b>{cb_name}</b><br>Copybook",
                )
                cb_nodes_added.add(cb_name)

    # Add program→program edges with frequency-based thickness
    for c in cg_to_show:
        if c.get("called_program") and c["called_program"] != "UNKNOWN":
            freq = freq_map.get((c["caller_program"], c["called_program"]), 1)
            width = max(1, freq * 2)
            net.add_edge(
                c["caller_program"], c["called_program"],
                title=f"Line {c.get('line_number', '?')} | calls: {freq}",
                arrows="to", color="#555", width=width,
            )

    # Add program→copybook edges (dashed gray)
    if show_copybooks:
        for prog_id, cb_name in copybook_usage:
            if prog_id in added:
                net.add_edge(
                    prog_id, f"CB_{cb_name}",
                    title="USES",
                    arrows="to",
                    color="#888888",
                    dashes=True,
                    width=1,
                )

    # Render
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
        net.save_graph(f.name)
        html_path = f.name

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=670, scrolling=False)

    legend = "**Legend:**  Entry point &nbsp;|&nbsp;  Leaf (no outgoing calls) &nbsp;|&nbsp;  Hub &nbsp;|&nbsp;  External target &nbsp;|&nbsp; *Colors = modules*"
    if show_copybooks:
        legend += " &nbsp;|&nbsp;  Copybook (dashed edge = USES)"
    st.markdown(legend)

    # Call matrix table
    st.subheader("Call Matrix")
    rows = [{"Caller": c["caller_program"],
             "Caller Business Name": c.get("caller_name") or "-",
             "Calls": c["called_program"],
             "Called Business Name": c.get("called_name") or "-",
             "At Line": c.get("line_number") or "-"}
            for c in cg_to_show if c.get("called_program") != "UNKNOWN"]
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# 
# Tab: Dependency Matrix
# 

def page_dependency_matrix():
    st.header("Dependency Heatmap")
    st.caption("Shows which programs use which copybooks. Blue = program uses this copybook. Clusters reveal tightly coupled program groups.")

    try:
        import plotly.graph_objects as go
    except ImportError:
        st.error("plotly not installed. Run: `pip install plotly`")
        return

    try:
        db_path = os.getenv("DB_PATH", "data/cobol_knowledge.db")
        conn_raw = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT program_id, copybook_name FROM copybook_usage", conn_raw)
        conn_raw.close()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    if df.empty:
        st.warning("No copybook usage data found. Run the pipeline first.")
        return

    # Top 20 most-used copybooks
    top_copybooks = (
        df.groupby("copybook_name")["program_id"]
        .count()
        .sort_values(ascending=False)
        .head(20)
        .index.tolist()
    )
    df_filtered = df[df["copybook_name"].isin(top_copybooks)]

    programs_list = sorted(df_filtered["program_id"].unique().tolist())

    # Build presence matrix
    matrix = []
    for prog in programs_list:
        prog_cbs = set(df_filtered[df_filtered["program_id"] == prog]["copybook_name"].tolist())
        row = [1 if cb in prog_cbs else 0 for cb in top_copybooks]
        matrix.append(row)

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=top_copybooks,
        y=programs_list,
        colorscale=["#0e1117", "#58a6ff"],
        showscale=True,
        hovertemplate="Program: %{y}<br>Copybook: %{x}<br>Uses: %{z}<extra></extra>",
    ))
    fig.update_layout(
        title="Program-Copybook Dependency Matrix",
        xaxis_title="Copybook",
        yaxis_title="Program",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#c9d1d9"),
        height=max(400, len(programs_list) * 18 + 150),
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Blue = program uses this copybook. Clusters reveal tightly coupled program groups.")

    # Summary table
    st.subheader("Top Copybooks by Usage")
    summary = (
        df.groupby("copybook_name")["program_id"]
        .count()
        .reset_index()
        .rename(columns={"program_id": "Programs Using It"})
        .sort_values("Programs Using It", ascending=False)
        .head(30)
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)


# 
# Tab: Data Flow Graph
# 

def page_data_flow():
    st.header("Data Flow Graph")
    st.caption("Shows the flow from JCL Jobs → COBOL Programs → Files/Copybooks.")

    try:
        from pyvis.network import Network
    except ImportError:
        st.error("pyvis not installed. Run: `pip install pyvis`")
        return

    try:
        loader = db_connect()
        all_programs = loader.get_all_programs()
        all_jcl_jobs = loader.get_all_jcl_jobs()
        loader.close()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    # Query top files from DB
    try:
        db_path = os.getenv("DB_PATH", "data/cobol_knowledge.db")
        conn_raw = sqlite3.connect(db_path)
        try:
            files_df = pd.read_sql_query("SELECT program_id, file_name FROM files LIMIT 200", conn_raw)
            prog_file_pairs = [(r["program_id"], r["file_name"]) for _, r in files_df.iterrows()]
        except Exception:
            prog_file_pairs = []
        conn_raw.close()
    except Exception:
        prog_file_pairs = []

    net = Network(height="650px", width="100%", bgcolor="#0e1117",
                  font_color="white", directed=True)
    net.barnes_hut(gravity=-6000, central_gravity=0.35, spring_length=140)

    added = set()

    # JCL Job nodes — triangle, orange
    for job in (all_jcl_jobs or [])[:30]:
        jname = job.get("job_name", "")
        if not jname:
            continue
        node_id = f"JOB_{jname}"
        if node_id not in added:
            net.add_node(node_id, label=jname, color="#f0883e", shape="triangle", size=22,
                         title=f"<b>JCL Job: {jname}</b><br>Steps: {job.get('step_count',0)}")
            added.add(node_id)

    # Program nodes — dot, colored by type
    for prog in all_programs[:80]:
        pid = prog["program_id"]
        ptype = prog.get("program_type", "BATCH")
        color = "#58a6ff" if ptype == "ONLINE" else "#3fb950"
        if pid not in added:
            net.add_node(pid, label=pid, color=color, shape="dot", size=14,
                         title=f"<b>{pid}</b><br>Type: {ptype}<br>Lines: {prog.get('line_count',0)}")
            added.add(pid)

    # File nodes — square, gray
    file_nodes = set()
    for prog_id, file_name in prog_file_pairs:
        if not file_name:
            continue
        fn_id = f"FILE_{file_name}"
        if fn_id not in file_nodes:
            net.add_node(fn_id, label=file_name, color="#6e7681", shape="square", size=10,
                         title=f"<b>File: {file_name}</b>")
            file_nodes.add(fn_id)

    # Edges: JCL Job → Program
    for job in (all_jcl_jobs or [])[:30]:
        jname = job.get("job_name", "")
        programs_called = job.get("programs_called") or []
        jnode = f"JOB_{jname}"
        if jnode not in added:
            continue
        for prog_name in programs_called:
            if prog_name and prog_name in added:
                net.add_edge(jnode, prog_name, color="#f0883e", arrows="to", width=2,
                             title=f"{jname} executes {prog_name}")

    # Edges: Program → File
    for prog_id, file_name in prog_file_pairs:
        if not file_name:
            continue
        fn_id = f"FILE_{file_name}"
        if prog_id in added and fn_id in file_nodes:
            net.add_edge(prog_id, fn_id, color="#6e7681", arrows="to", dashes=True, width=1,
                         title=f"{prog_id} accesses {file_name}")

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
        net.save_graph(f.name)
        html_path = f.name
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=670, scrolling=False)

    st.markdown("""
**Legend:**
-  **Triangle (orange)** — JCL Job
-  **Circle (blue)** — Online/CICS Program
- 🟢 **Circle (green)** — Batch Program
-  **Square (gray)** — File/Dataset
- Solid arrow = executes / calls &nbsp;|&nbsp; Dashed arrow = file access
""")


# 
# Tab 3: Module Structure (all programs)
# 

def page_modules():
    st.header("Module Structure")
    try:
        loader = db_connect()
        modules = loader.get_all_modules()
        loader.close()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    for m in modules:
        prog_list = m.get("programs", [])
        name      = m.get("business_name") or m.get("module_name", "")
        purpose   = m.get("business_purpose") or m.get("description") or "-"
        with st.expander(f"**{name}** — {len(prog_list)} programs", expanded=False):
            st.write(f"*{purpose}*")
            rows = []
            for p in prog_list:  # ALL programs — no [:3] limit
                rows.append({
                    "Program ID": p.get("program_id"),
                    "Type": p.get("program_type") or "-",
                    "Lines": p.get("line_count") or 0,
                    "Business Name": p.get("business_name") or "-",
                    "Purpose": (p.get("business_purpose") or "-")[:80],
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# 
# Tab 4: Program Explorer
# 

def page_explorer():
    st.header("Program Explorer")
    try:
        loader = db_connect()
        programs = loader.get_all_programs()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    program_ids = [p["program_id"] for p in programs]
    col_sel, col_filt = st.columns([2, 1])
    with col_filt:
        type_filter = st.selectbox("Filter by type", ["All", "ONLINE", "BATCH"], key="explorer_type_filter")
    with col_sel:
        if type_filter != "All":
            filtered = [p["program_id"] for p in programs if p.get("program_type") == type_filter]
        else:
            filtered = program_ids
        selected = st.selectbox("Select Program", filtered, key="explorer_program_select")

    if not selected:
        loader.close()
        return

    details = loader.get_program_details(selected)
    loader.close()

    if not details:
        st.warning(f"No details found for {selected}")
        return

    tab_overview, tab_flow, tab_data, tab_rules = st.tabs(
        ["Overview", "Control Flow", "Data Items", "Business Rules"]
    )

    with tab_overview:
        bname = details.get("business_name") or selected
        st.markdown(f"### {bname}")
        bpurp = details.get("business_purpose")
        if bpurp:
            st.info(bpurp)
        else:
            st.warning("No business purpose extracted yet. Run LLM enrichment.")

        c1, c2, c3 = st.columns(3)
        c1.metric("Type", details.get("program_type") or "-")
        c2.metric("Lines", details.get("line_count") or 0)
        c3.metric("Paragraphs", len(details.get("paragraphs") or []))

        user_role = details.get("user_role")
        bprocess  = details.get("business_process")
        if user_role:
            st.markdown(f"**Used by:** {user_role}")
        if bprocess:
            st.markdown(f"**Business process:** {bprocess}")

        # Migration score
        score = migration_score(details)
        st.markdown(f"**Migration complexity:** {score_label(score)} ({score}/5)")

        # Callers / callees
        callers  = details.get("called_by") or []
        callees  = details.get("calls") or []
        st.divider()
        c_in, c_out = st.columns(2)
        with c_in:
            st.markdown(f"**Called by ({len(callers)})**")
            for c in callers:
                st.markdown(f"- `{c['caller_program']}`")
        with c_out:
            st.markdown(f"**Calls ({len(callees)})**")
            for c in callees:
                st.markdown(f"- `{c['called_program']}`")

    with tab_flow:
        paragraphs = details.get("paragraphs") or []
        performs   = details.get("performs") or []

        if not paragraphs:
            st.info("No paragraphs found for this program.")
        else:
            # Build mermaid control flow from actual performs data
            safe_id = lambda s: s.replace("-", "_").replace(" ", "_").replace(".", "_")

            # Build a lookup of paragraphs by name for style classification
            para_by_name = {p.get("paragraph_name", ""): p for p in paragraphs}

            # Classify paragraph style
            def _para_style(para):
                has_calls = bool(para.get("calls", []))
                has_performs = bool(para.get("performs", []))
                if has_calls:
                    return "caller"
                if has_performs:
                    return "hub"
                return "simple"

            mermaid = "flowchart TD\n    START([Program Entry])\n"
            for para in paragraphs[:20]:
                pname = para.get("paragraph_name", "?")
                bname = (para.get("business_name") or pname).replace('"', "'")
                rule_count = len(para.get("business_rules") or [])
                badge = f"\\n({rule_count} rules)" if rule_count > 0 else ""
                style_cls = _para_style(para)
                mermaid += f'    {safe_id(pname)}["{bname}{badge}"]:::{style_cls}\n'

            if paragraphs:
                mermaid += f'START --> {safe_id(paragraphs[0]["paragraph_name"])}\n'
            seen = set()
            for pf in performs[:30]:
                src = pf.get("source_paragraph") or pf.get("paragraph_name", "")
                tgt = pf.get("target_paragraph") or pf.get("target", "")
                if src and tgt and f"{src}->{tgt}" not in seen:
                    mermaid += f"    {safe_id(src)} --> {safe_id(tgt)}\n"
                    seen.add(f"{src}->{tgt}")

            # classDef definitions
            mermaid += "    classDef caller fill:#f85149,stroke:#ff7b72,color:#fff\n"
            mermaid += "    classDef hub fill:#388bfd,stroke:#58a6ff,color:#fff\n"
            mermaid += "    classDef simple fill:#2ea043,stroke:#3fb950,color:#fff\n"

            render_mermaid(mermaid, height=450)
            st.caption("Caller (calls other programs) &nbsp;|&nbsp;  Hub (performs other paragraphs) &nbsp;|&nbsp; 🟢 Simple paragraph")

            # Paragraph narratives table
            st.subheader("Paragraph Narratives")
            para_rows = []
            for p in paragraphs:
                para_rows.append({
                    "Paragraph": p.get("paragraph_name"),
                    "Business Name": p.get("business_name") or "-",
                    "Lines": f"{p.get('line_start','?')}–{p.get('line_end','?')}",
                    "Narrative": (p.get("narrative") or p.get("purpose") or "-")[:120],
                })
            st.dataframe(pd.DataFrame(para_rows), use_container_width=True, hide_index=True)

    with tab_data:
        items = details.get("data_items") or []
        if not items:
            st.info("No data items found.")
        else:
            rows = [{
                "Name": d.get("name"),
                "Level": d.get("level_number") or "-",
                "Picture": d.get("picture") or "-",
                "Section": d.get("section") or "-",
                "Business Name": d.get("business_name") or "-",
                "Description": (d.get("description") or "-")[:80],
            } for d in items if d.get("name") != "FILLER"]
            st.caption(f"{len(rows)} data items (FILLER excluded)")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with tab_rules:
        rules = details.get("business_rules") or []
        if not rules:
            st.info("No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.")
        else:
            for r in rules:
                with st.expander(f"**{r.get('rule_id','?')}** — {r.get('rule_name','?')}", expanded=False):
                    st.markdown(f"**Category:** {r.get('category','-')}")
                    st.markdown(f"**Rule:** {r.get('rule_statement','-')}")
                    st.markdown(f"**When:** {r.get('condition_text') or r.get('condition','-')}")
                    st.markdown(f"**Then:** {r.get('action_text') or r.get('action','-')}")
                    if r.get("paragraph_name"):
                        st.caption(f"Paragraph: {r['paragraph_name']} | Lines: {r.get('line_start','?')}–{r.get('line_end','?')}")


# 
# Tab 5: JCL Jobs
# 

def page_jcl():
    st.header("JCL Jobs")
    st.caption("Batch JCL jobs parsed from the repository — which programs they run, what files they read/write.")

    try:
        loader = db_connect()
        jobs = loader.get_all_jcl_jobs()
        loader.close()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    if not jobs:
        st.warning("No JCL jobs found. Run the pipeline with 'Parse JCL Jobs' checked.")
        return

    st.metric("Total JCL Jobs", len(jobs))
    st.divider()

    # Summary table
    rows = []
    for job in jobs:
        rows.append({
            "Job Name":        job.get("job_name"),
            "File":            job.get("file_name"),
            "Description":     (job.get("job_description") or "-")[:60],
            "Steps":           job.get("step_count", 0),
            "Programs Called": ", ".join(job.get("programs_called") or []) or "-",
            "Input Datasets":  len(job.get("input_datasets") or []),
            "Output Datasets": len(job.get("output_datasets") or []),
        })
    st.subheader("All JCL Jobs")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()

    # Detail view
    st.subheader("Job Detail")
    job_names = [j["job_name"] for j in jobs]
    selected_job = st.selectbox("Select Job", job_names, key="jcl_job_select")

    if selected_job:
        try:
            loader = db_connect()
            detail = loader.get_jcl_job_details(selected_job)
            loader.close()
        except Exception as e:
            st.error(str(e))
            return

        if not detail:
            st.warning("No details found.")
            return

        if detail.get("header_comments"):
            st.markdown("**Job Description (Header Comments)**")
            st.code(detail["header_comments"], language=None)

        c1, c2, c3 = st.columns(3)
        c1.metric("Steps", len(detail.get("steps") or []))
        c2.metric("Input Datasets", len(detail.get("input_datasets") or []))
        c3.metric("Output Datasets", len(detail.get("output_datasets") or []))

        if detail.get("programs_called"):
            st.markdown("**COBOL Programs Executed**")
            for p in detail["programs_called"]:
                st.markdown(f"- `{p}`")

        if detail.get("input_datasets"):
            st.markdown("**Input Datasets**")
            for d in detail["input_datasets"]:
                st.code(d, language=None)

        if detail.get("output_datasets"):
            st.markdown("**Output Datasets**")
            for d in detail["output_datasets"]:
                st.code(d, language=None)

        st.subheader("Steps")
        for step in (detail.get("steps") or []):
            with st.expander(
                f"Step {step.get('step_order','?')}: **{step.get('step_name')}** "
                f"— {step.get('step_type','?')} "
                f"{'`' + step['program'] + '`' if step.get('program') else ''}"
            ):
                if step.get("step_comments"):
                    st.info(step["step_comments"])

                datasets = step.get("datasets") or []
                if datasets:
                    dd_rows = []
                    for ds in datasets:
                        if not ds.get("is_inline"):
                            dd_rows.append({
                                "DD Name":   ds.get("dd_name"),
                                "Dataset":   ds.get("dsn") or "-",
                                "DISP":      ds.get("disp") or "-",
                                "Direction": ds.get("direction") or "-",
                                "RECFM":     ds.get("recfm") or "-",
                                "LRECL":     ds.get("lrecl") or "-",
                            })
                    if dd_rows:
                        st.dataframe(pd.DataFrame(dd_rows), use_container_width=True, hide_index=True)

                if step.get("sysin_data"):
                    st.markdown("**Inline SYSIN**")
                    st.code("\n".join(step["sysin_data"]), language=None)


# 
# Tab 6 (was 5): Migration Readiness
# 

def page_migration():
    st.header("Migration Readiness")
    st.markdown("""
This page scores each program by migration complexity and suggests a migration order.
**Migrate leaf programs first** (no outgoing calls), then work up the dependency chain.
""")
    try:
        loader = db_connect()
        programs = loader.get_all_programs()
        cg       = loader.get_call_graph()
        loader.close()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    callers = {c["caller_program"] for c in cg}
    callees = {c["called_program"]  for c in cg if c["called_program"] != "UNKNOWN"}

    rows = []
    for p in programs:
        pid   = p["program_id"]
        score = migration_score(p)
        is_leaf  = pid not in callers
        is_entry = pid not in callees
        outgoing = len([c for c in cg if c["caller_program"] == pid and c.get("called_program") != "UNKNOWN"])
        incoming = len([c for c in cg if c["called_program"] == pid])
        rows.append({
            "Program": pid,
            "Type": p.get("program_type") or "-",
            "Lines": p.get("line_count") or 0,
            "Complexity": score,
            "Complexity Label": score_label(score),
            "Is Leaf": "Yes" if is_leaf else "No",
            "Is Entry Point": "Yes" if is_entry else "No",
            "Incoming Calls": incoming,
            "Outgoing Calls": outgoing,
            "Business Name": p.get("business_name") or "-",
            "Suggested Service": _suggest_service(p),
        })

    # Sort by complexity asc (migrate easy ones first), then leaf first
    rows.sort(key=lambda r: (r["Complexity"], -1 if r["Is Leaf"] == "Yes" else 0))

    st.subheader("Migration Order (easiest first)")
    df = pd.DataFrame(rows)
    st.dataframe(df[[
        "Program", "Type", "Lines", "Complexity Label",
        "Is Leaf", "Incoming Calls", "Outgoing Calls",
        "Business Name", "Suggested Service",
    ]], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Complexity Distribution")
    dist = df["Complexity"].value_counts().sort_index()
    st.bar_chart(dist)

    # Summary
    high   = df[df["Complexity"] >= 4]
    medium = df[df["Complexity"] == 3]
    low    = df[df["Complexity"] <= 2]
    leaves = df[df["Is Leaf"] == "Yes"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🟢Low complexity", len(low))
    c2.metric("🟡Medium complexity", len(medium))
    c3.metric("High complexity", len(high))
    c4.metric("Leaf programs (migrate first)", len(leaves))

    st.divider()
    st.subheader("Suggested Microservice Boundaries")
    st.markdown("""
Each module maps to a candidate microservice. Programs within a module share data
structures (copybooks) and call each other — they belong together.
""")
    try:
        loader = db_connect()
        modules = loader.get_all_modules()
        loader.close()
        for m in modules:
            progs  = m.get("programs", [])
            name   = m.get("business_name") or m.get("module_name", "")
            scores = [migration_score(p) for p in progs]
            avg    = sum(scores) / len(scores) if scores else 0
            st.markdown(
                f"**{name}** — {len(progs)} programs, avg complexity {avg:.1f}/5  \n"
                + ", ".join(f"`{p['program_id']}`" for p in progs)
            )
    except Exception:
        st.info("Run pipeline to see module details.")


def _suggest_service(prog: dict) -> str:
    bp = (prog.get("business_purpose") or prog.get("business_name") or "").lower()
    pid = prog.get("program_id", "").upper()
    if any(k in bp for k in ["sign", "auth", "login", "password"]):
        return "auth-service"
    if any(k in bp for k in ["account", "acct"]) or "ACCT" in pid or "ACT" in pid:
        return "account-service"
    if any(k in bp for k in ["transaction", "trxn", "card"]) or "TRN" in pid or "CBT" in pid:
        return "transaction-service"
    if any(k in bp for k in ["user", "usr"]) or "USR" in pid:
        return "user-service"
    if any(k in bp for k in ["report", "statement"]):
        return "reporting-service"
    if any(k in bp for k in ["billing", "payment"]):
        return "billing-service"
    if prog.get("program_type") == "BATCH":
        return "batch-service"
    return "core-service"


# 
# Tab 6: Business Rules
# 

def page_rules():
    st.header("Business Rules Catalog")
    try:
        loader = db_connect()
        rules = loader.get_all_business_rules()
        loader.close()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    if not rules:
        st.warning("No business rules extracted yet. Run LLM enrichment (enable 'AI Enrichment' in the sidebar and re-run the pipeline).")
        return

    categories = sorted({r.get("category", "GENERAL") for r in rules})
    cat_filter = st.selectbox("Filter by category", ["All"] + categories, key="rules_cat_filter")

    filtered = rules if cat_filter == "All" else [r for r in rules if r.get("category") == cat_filter]
    st.caption(f"Showing {len(filtered)} of {len(rules)} rules")

    for r in filtered:
        with st.expander(f"**{r.get('rule_id','?')}** — {r.get('rule_name','?')} [{r.get('program_id','-')}]"):
            st.markdown(f"**Category:** {r.get('category', '-')}")
            st.markdown(f"**Rule:** {r.get('rule_statement', '-')}")
            st.markdown(f"**When:** {r.get('condition_text') or r.get('condition', '-')}")
            st.markdown(f"**Then:** {r.get('action_text') or r.get('action', '-')}")


# 
# Tab 7: Live Search
# 

def page_search(repo_path):
    st.header("Live Search")
    query = st.text_input("Search programs, data items, rules, or source code")
    if not query:
        return

    tab_docs, tab_code = st.tabs(["Documentation Search", "Source Code Search"])

    with tab_docs:
        try:
            loader = db_connect()
            results = loader.full_text_search(query)
            loader.close()
            progs = results.get("programs", [])
            if progs:
                st.markdown(f"**{len(progs)} programs matched:**")
                for p in progs:
                    st.info(f"**{p['program_id']}** — {p.get('business_name', '')}  \n{(p.get('business_purpose') or '')[:120]}")
            else:
                st.info("No programs matched.")
        except Exception as e:
            st.error(f"Documentation search unavailable: {e}")

    with tab_code:
        matches = search_cobol_files(repo_path, query)
        st.caption(f"{len(matches)} source lines matched")
        for r in matches[:50]:
            with st.expander(f"{r['file']} — Line {r['line']}"):
                st.code(r["content"], language="cobol")


# 
# Tab 8: English Doc Generator (Graph-Aware)
# 

def _fetch_program_subgraph(loader, program_id: str, depth: int) -> list:
    """Walk the call graph up to `depth` hops and return all programs in the subgraph."""
    visited = set()
    frontier = {program_id}

    for _ in range(depth):
        next_frontier = set()
        for pid in frontier:
            if pid in visited:
                continue
            visited.add(pid)
            cg = loader.get_call_graph()
            for edge in cg:
                if edge["caller_program"] == pid and edge.get("called_program") not in ("UNKNOWN", None):
                    next_frontier.add(edge["called_program"])
                if edge["called_program"] == pid:
                    next_frontier.add(edge["caller_program"])
        frontier = next_frontier - visited

    visited.add(program_id)
    all_ids = visited

    programs = []
    for pid in all_ids:
        details = loader.get_program_details(pid)
        if details:
            programs.append(details)
    return programs


def _build_llm_context(programs: list, mode: str, subject: str) -> str:
    """Build a rich context string combining enriched English + raw JSON for each program."""
    lines = []
    lines.append(f"# COBOL System Documentation Context")
    lines.append(f"Mode: {mode} | Subject: {subject}")
    lines.append(f"Total programs in scope: {len(programs)}\n")

    for prog in programs:
        pid = prog.get("program_id", "?")
        lines.append(f"## Program: {pid}")
        lines.append(f"- Type: {prog.get('program_type', '?')}")
        lines.append(f"- Lines: {prog.get('line_count', 0)}")

        # English enrichment
        bname = prog.get("business_name") or ""
        bpurp = prog.get("business_purpose") or ""
        urole = prog.get("user_role") or ""
        bproc = prog.get("business_process") or ""
        if bname:  lines.append(f"- Business Name: {bname}")
        if bpurp:  lines.append(f"- Purpose: {bpurp}")
        if urole:  lines.append(f"- Triggered by: {urole}")
        if bproc:  lines.append(f"- Business Process: {bproc}")

        # Migration context
        mc = prog.get("migration_complexity")
        me = prog.get("modern_equivalent") or ""
        ss = prog.get("suggested_service") or ""
        ma = prog.get("migration_approach") or ""
        if mc:  lines.append(f"- Migration Complexity: {mc}/5")
        if me:  lines.append(f"- Modern Equivalent: {me}")
        if ss:  lines.append(f"- Target Microservice: {ss}")
        if ma:  lines.append(f"- Migration Approach: {ma}")

        # Dependencies (raw JSON)
        calls = [c.get("called_program") for c in (prog.get("calls") or []) if c.get("called_program") not in ("UNKNOWN", None)]
        callers = [c.get("caller_program") for c in (prog.get("called_by") or [])]
        copybooks = [c.get("copybook_name") for c in (prog.get("copybooks") or [])]
        files = [f.get("file_name") for f in (prog.get("files") or [])]
        if calls:     lines.append(f"- Calls: {', '.join(calls)}")
        if callers:   lines.append(f"- Called by: {', '.join(callers)}")
        if copybooks: lines.append(f"- Shared Data (Copybooks): {', '.join(copybooks)}")
        if files:     lines.append(f"- Files Accessed: {', '.join(files)}")

        # Paragraph narratives
        paras = prog.get("paragraphs") or []
        if paras:
            lines.append("- Key Functions:")
            for p in paras[:8]:
                bname_p = p.get("business_name") or p.get("paragraph_name", "")
                narr = p.get("narrative") or p.get("purpose") or ""
                if narr:
                    lines.append(f"  * {bname_p}: {narr[:200]}")

        # Business rules
        rules = prog.get("business_rules") or []
        if rules:
            lines.append(f"- Business Rules ({len(rules)} total):")
            for r in rules[:5]:
                rs = r.get("rule_statement") or r.get("description") or ""
                if rs:
                    lines.append(f"  * {rs[:150]}")

        lines.append("")

    return "\n".join(lines)


def _call_vertex_for_doc(context: str, mode: str, subject: str) -> str:
    """Send context to Gemini API and get back a full English narrative document."""
    try:
        import google.generativeai as genai

        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        if mode == "Program":
            prompt = f"""You are a senior software architect documenting a legacy COBOL system for migration to modern services.

Using the structured data below, write a comprehensive technical documentation document for the program "{subject}" and all its connected programs.

The document must:
1. Start with an Executive Summary — what this program does in plain English, who triggers it, and its business importance
2. Explain each program in the dependency chain in order of execution flow — not alphabetically
3. For each program: explain what it does, what data it reads/writes, what business decisions it makes, and what it produces
4. Describe how the programs connect — which calls which, what data flows between them, what shared data structures exist
5.Highlight any critical business rules or validation logic
6. End with a Migration Notes section — complexity, suggested modern equivalent, recommended microservice boundary

Write as proper technical documentation — clear headings, flowing prose, specific details. Avoid generic statements.

SYSTEM DATA:
{context}

Write the documentation now:"""
        else:
            prompt = f"""You are a senior software architect documenting a legacy COBOL system for migration to modern microservices.

Using the structured data below, write a comprehensive module specification document for the "{subject}" module.

The document must:
1. Start with a Module Overview — what business capability this module provides, who uses it, and its role in the overall system
2. List all programs in this module with their individual purposes
3. Explain the internal flow — how programs within this module interact, the sequence of operations
4. Describe the data architecture — what files, datasets, and shared copybooks this module uses
5. Document all key business rules and validations enforced by this module
6. Describe external dependencies — what other modules/programs this module depends on or is depended upon by
7. End with a Migration Strategy — recommended service boundary, suggested modern architecture (e.g. REST API, event-driven), migration order for programs within this module

Write as a proper software specification — clear sections, numbered headings, specific technical details, flowing explanations. This document will be handed to a development team to rewrite this module in a modern language.

SYSTEM DATA:
{context}

Write the module specification now:"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating documentation: {e}"


def _markdown_to_pdf(markdown_text: str, title: str) -> bytes:
    """Convert Markdown text to PDF bytes using reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch, bottomMargin=inch,
        title=title,
    )

    styles = getSampleStyleSheet()
    style_h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=18, spaceAfter=12, textColor=colors.HexColor("#1a1a2e"))
    style_h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, spaceAfter=8, spaceBefore=16, textColor=colors.HexColor("#16213e"))
    style_h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontSize=12, spaceAfter=6, spaceBefore=10, textColor=colors.HexColor("#0f3460"))
    style_body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, spaceAfter=6, leading=14)
    style_bullet = ParagraphStyle("Bullet", parent=styles["Normal"], fontSize=10, leftIndent=20, spaceAfter=4, bulletIndent=10)
    style_code = ParagraphStyle("Code", parent=styles["Code"], fontSize=8, backColor=colors.HexColor("#f4f4f4"), spaceAfter=6, leading=12)

    story = []

    for line in markdown_text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped:
            story.append(Spacer(1, 6))
            continue

        # Escape XML special chars
        safe = line_stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if line_stripped.startswith("# "):
            story.append(Paragraph(safe[2:], style_h1))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a1a2e")))
        elif line_stripped.startswith("## "):
            story.append(Paragraph(safe[3:], style_h2))
        elif line_stripped.startswith("### "):
            story.append(Paragraph(safe[4:], style_h3))
        elif line_stripped.startswith("- ") or line_stripped.startswith("* "):
            story.append(Paragraph(f"• {safe[2:]}", style_bullet))
        elif line_stripped.startswith("  * ") or line_stripped.startswith("  - "):
            story.append(Paragraph(f"   {safe[4:]}", style_bullet))
        elif line_stripped.startswith("`") and line_stripped.endswith("`"):
            story.append(Paragraph(safe[1:-1], style_code))
        elif line_stripped.startswith("**") and line_stripped.endswith("**"):
            story.append(Paragraph(f"<b>{safe[2:-2]}</b>", style_body))
        else:
            # Handle inline bold
            import re
            formatted = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', safe)
            formatted = re.sub(r'\*(.+?)\*', r'<i>\1</i>', formatted)
            story.append(Paragraph(formatted, style_body))

    doc.build(story)
    return buffer.getvalue()


def page_doc_generator():
    st.header("English Documentation Generator")
    st.markdown("Generate a comprehensive English narrative document for any program or module — treating the system as a connected graph.")

    try:
        loader = db_connect()
        programs = loader.get_all_programs()
        modules  = loader.get_all_modules()
    except Exception as e:
        st.error(f"Database not ready. ({e})")
        return

    #  Mode selector
    col_mode, col_depth = st.columns([1, 1])
    with col_mode:
        mode = st.radio("Documentation Mode", ["Program", "Module"], horizontal=True)
    with col_depth:
        if mode == "Program":
            depth = st.slider("Graph Depth (hops)", min_value=1, max_value=2, value=1,
                              help="1 = direct connections only · 2 = connections of connections")
        else:
            depth = 1  # not used in module mode

    #  Subject selector
    if mode == "Program":
        program_ids = sorted([p["program_id"] for p in programs])
        subject = st.selectbox("Select Program", program_ids, key="docgen_program_select")
        cache_key = f"doc_{subject}_depth{depth}"
        st.caption(f"Will include {subject} + all programs it calls/is called by (up to {depth} hop{'s' if depth > 1 else ''} away)")
    else:
        module_names = [m.get("business_name") or m.get("module_name", "") for m in modules]
        subject = st.selectbox("Select Module", module_names, key="docgen_module_select")
        cache_key = f"doc_module_{subject}"
        sel_module = next((m for m in modules if (m.get("business_name") or m.get("module_name")) == subject), None)
        if sel_module:
            progs_in_module = sel_module.get("programs", [])
            st.caption(f"Module contains {len(progs_in_module)} programs: {', '.join(p['program_id'] for p in progs_in_module[:8])}{'...' if len(progs_in_module) > 8 else ''}")

    #  Generate button
    col_btn, col_clear = st.columns([2, 1])
    with col_btn:
        generate = st.button("Generate English Documentation", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear Cache", use_container_width=True):
            if cache_key in st.session_state:
                del st.session_state[cache_key]
            st.rerun()

    #  Generate or show cached
    if generate or cache_key in st.session_state:
        if cache_key not in st.session_state or generate:
            with st.spinner(f"Fetching graph data and calling Vertex AI for {subject}..."):
                if mode == "Program":
                    prog_data = _fetch_program_subgraph(loader, subject, depth)
                else:
                    prog_data = []
                    if sel_module:
                        for p in sel_module.get("programs", []):
                            details = loader.get_program_details(p["program_id"])
                            if details:
                                prog_data.append(details)

                context = _build_llm_context(prog_data, mode, subject)
                doc_text = _call_vertex_for_doc(context, mode, subject)
                st.session_state[cache_key] = doc_text
                st.session_state[f"{cache_key}_prog_count"] = len(prog_data)

        doc_text = st.session_state[cache_key]
        prog_count = st.session_state.get(f"{cache_key}_prog_count", 0)

        st.success(f"Generated from {prog_count} programs in the subgraph")
        st.divider()

        #  Display doc
        st.markdown(doc_text)

        st.divider()

        #  Export buttons
        col_md, col_pdf = st.columns(2)

        with col_md:
            md_bytes = doc_text.encode("utf-8")
            st.download_button(
                label="Download as Markdown",
                data=md_bytes,
                file_name=f"{subject.replace(' ', '_')}_documentation.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with col_pdf:
            with st.spinner("Generating PDF..."):
                try:
                    pdf_bytes = _markdown_to_pdf(doc_text, f"{subject} — System Documentation")
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_bytes,
                        file_name=f"{subject.replace(' ', '_')}_documentation.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.warning(f"PDF generation failed: {e}. Use Markdown download instead.")

    loader.close()


# 
# Main Layout
# 

repo_path, output_dir = render_sidebar()

tabs = st.tabs([
    "Overview",
    "Call Graph",
    "Dependency Matrix",
    "Data Flow",
    "Modules",
    "Explorer",
    "Doc Generator",
    "JCL Jobs",
    "Migration",
    "Rules",
    "Search",
])

with tabs[0]:
    page_overview()

with tabs[1]:
    page_call_graph()

with tabs[2]:
    page_dependency_matrix()

with tabs[3]:
    page_data_flow()

with tabs[4]:
    page_modules()

with tabs[5]:
    page_explorer()

with tabs[6]:
    page_doc_generator()

with tabs[7]:
    page_jcl()

with tabs[8]:
    page_migration()

with tabs[9]:
    page_rules()

with tabs[10]:
    page_search(repo_path)
