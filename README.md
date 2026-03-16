# COBOL Documentation Pipeline

Automated documentation and migration analysis tool for legacy COBOL codebases. Parses COBOL source, enriches with LLM-generated business context, stores in a knowledge graph, and serves an interactive Streamlit dashboard.

Built for the **AWS CardDemo** mainframe modernization sample — 44 programs, 447 business rules, fully documented.

---

## What It Does

```
COBOL Source (.cbl)
      │
      ▼
ProLeap Parser  ──▶  programs.json + copybooks.json
      │
      ▼
LangGraph + Gemini API  ──▶  enriched_programs.json
  (business purpose, migration complexity,
   data contracts, migration approach)
      │
      ▼
SQLite Knowledge Base  ──▶  cobol_knowledge.db
      │
      ├──▶  Neo4j Graph DB  (optional)
      │
      ▼
Streamlit Dashboard  ──▶  http://localhost:8501
  11 tabs: Overview, Call Graph, Dependency Matrix,
  Data Flow, Modules, Explorer, Doc Generator,
  JCL Jobs, Migration, Rules, Search
```

---

## Features

- **ProLeap COBOL Parser** — ANTLR4-based parser, handles IBM Enterprise + TANDEM dialects
- **JCL Parser** — Parses job control language files alongside COBOL programs
- **LangGraph + Gemini API** — AI enrichment: business purpose, migration complexity, data contracts, business rules extraction
- **SQLite Knowledge Base** — FTS5 full-text search, deduplication, incremental loading
- **Neo4j Export** — Push full program/call/copybook graph to Neo4j Desktop
- **Interactive Dashboard** — 11-tab Streamlit UI with:
  - pyvis network graphs (call graph, data flow)
  - Plotly dependency heatmap
  - Mermaid control flow diagrams
  - Graph-aware Doc Generator (PDF + Markdown export)
  - Migration readiness scoring
- **Doc Generator** — Select any program or module, walk the call graph N hops deep, send combined context to Gemini, get a full English technical document — downloadable as PDF or Markdown

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=AIzaSy...        # From https://aistudio.google.com/app/apikey
NEO4J_URI=neo4j://127.0.0.1:7687   # Optional
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
```

### 3. Get the CardDemo COBOL source

```bash
git clone https://github.com/aws-samples/aws-mainframe-modernization-carddemo.git carddemo
```

### 4. Run the pipeline

```bash
python run_pipeline.py
```

This runs: JCL parse → COBOL parse → LLM enrichment → SQLite load → Doc generation → Neo4j export.

To skip steps (e.g. re-use existing parsed output):

```python
# Edit run_pipeline.py:
skip_parse=True,    # Use existing parsed_output/
skip_enrich=True,   # Use existing enriched_output/
skip_neo4j=True,    # Skip Neo4j export
```

### 5. Launch the dashboard

```bash
python -m streamlit run src/app.py --server.port 8501
```

Open **http://localhost:8501**

---

## Project Structure

```
doc_demo/
├── src/
│   ├── app.py                  # Streamlit dashboard (11 tabs)
│   ├── orchestrator.py         # Pipeline coordinator
│   ├── proleap_wrapper.py      # COBOL parser (ProLeap JAR)
│   ├── jcl_parser.py           # JCL file parser
│   ├── langgraph_enricher.py   # LangGraph + Gemini enrichment
│   ├── sqlite_loader.py        # DB loader with dedup + FTS
│   ├── doc_generator.py        # Swimm-style Markdown generator
│   └── neo4j_exporter.py       # Neo4j graph export
├── schemas/
│   └── cobol_knowledge.sql     # SQLite schema
├── lib/
│   └── proleap-cobol-parser.jar
├── carddemo/                   # COBOL source (git cloned)
├── parsed_output/              # ProLeap JSON output
├── enriched_output/            # LLM-enriched JSON
├── data/
│   └── cobol_knowledge.db      # SQLite knowledge base
├── docs/                       # Generated Markdown docs
├── run_pipeline.py             # Main entry point
├── export_english.py           # Merge parsed + enriched JSON
└── requirements.txt
```

---

## Dashboard Tabs

| Tab | Description |
|-----|-------------|
| Overview | System stats, module breakdown, architecture graph |
| Call Graph | Interactive pyvis network with module filter + copybook nodes |
| Dependency Matrix | Plotly heatmap of program-to-program dependencies |
| Data Flow | JCL → Program → File flow visualization |
| Modules | Module-level grouping and program listing |
| Explorer | Deep-dive into any program: paragraphs, data items, control flow |
| Doc Generator | LLM-generated English docs with graph depth control, PDF/MD export |
| JCL Jobs | Parsed job definitions and step sequences |
| Migration | Complexity scoring and migration readiness by module |
| Rules | Full business rules catalog with search |
| Search | FTS5 full-text search across all programs and rules |

---

## Requirements

- Python 3.10+
- Java 11+ (for ProLeap parser)
- Gemini API key (Google AI Studio — free tier works)
- Neo4j Desktop (optional, for graph DB)

---

## License

MIT
