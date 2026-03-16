# COBOL Documentation Pipeline

Automated documentation generator for legacy COBOL codebases using ProLeap parsing, LangGraph+Groq LLM enrichment, and Swimm-style interactive documentation.

## Features

- **ProLeap Parser Integration** - ANTLR4-based COBOL parsing with mock fallback
- **LangGraph + Groq LLM** - AI-powered name translation and business rule extraction
- **SQLite Knowledge Base** - Structured storage with FTS5 full-text search
- **Interactive Dashboard** - Streamlit-based UI with Mermaid diagrams and Program Explorer
- **AI Chat Assistant** - CLI and Web-based RAG chat for system queries
- **Swimm-Style Documentation** - Interactive Markdown with live code links
- **Neo4j Graph Export** - Visual dependency and impact analysis

## 🚀 Quick Start

For a complete from-scratch setup, follow the [Installation Guide](file:///c:/Users/ADMIN/OneDrive/Desktop/doc_demo/INSTALLATION_GUIDE.md).

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Clone CardDemo (Example Repository)

```bash
git clone https://github.com/aws-samples/aws-mainframe-modernization-carddemo.git carddemo
```

### 4. Run the Pipeline

```bash
# Full pipeline with LLM enrichment
python src/orchestrator.py ./carddemo --api-key YOUR_GROQ_API_KEY

# Basic documentation (no LLM)
python src/orchestrator.py ./carddemo --skip-enrich

# With Neo4j graph export
python src/orchestrator.py ./carddemo --api-key KEY --neo4j
```

## Pipeline Stages

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  ProLeap Parser │───▶│ LangGraph+Groq  │───▶│     SQLite      │
│  (.cbl → JSON)  │    │  (Enrichment)   │    │  (Knowledge DB) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
                       ┌─────────────────┐            │
                       │    Neo4j        │◀───────────┤
                       │  (Graph DB)     │            │
                       └─────────────────┘            │
                                                      ▼
                       ┌─────────────────────────────────────┐
                       │        Swimm-Style Docs              │
                       │  • System Overview                   │
                       │  • Program Walkthroughs             │
                       │  • Business Rules Catalog           │
                       │  • Interactive Diagrams             │
                       └─────────────────────────────────────┘
```

## Output Structure

```
docs/
├── 00-SYSTEM-OVERVIEW.md    # Entry point with architecture diagram
├── programs/
│   ├── CBACT01C.md          # Program documentation with live links
│   └── ...
├── business-rules/
│   ├── INDEX.md             # Rules catalog
│   └── BR-001.md            # Individual rule docs
├── diagrams/
│   └── call-graph.md        # Mermaid call hierarchy
└── data-dictionary.md       # All data items
```

## Requirements

- Python 3.10+
- Java 11+ (for ProLeap parser, optional)
- Neo4j 5.x (optional, for graph visualization)
- Groq API key (for LLM enrichment)

## CLI Reference

```bash
python src/orchestrator.py REPO_PATH [OPTIONS]

Options:
  -o, --output DIR      Output directory (default: docs)
  --api-key KEY         Groq API key
  --model MODEL         Groq model (default: llama-3.1-70b-versatile)
  --db PATH             SQLite database path
  --skip-parse          Skip parsing (use existing JSON)
  --skip-enrich         Skip LLM enrichment
  --neo4j               Enable Neo4j export
  --neo4j-uri URI       Neo4j connection URI
```

## Individual Components

```bash
# Parse only
python src/proleap_wrapper.py ./carddemo --output parsed_output

# Enrich only
python src/langgraph_enricher.py parsed_output/programs.json --api-key KEY

# Load to SQLite only
python src/sqlite_loader.py --enriched enriched_output

# Generate docs only
python src/doc_generator.py --db data/cobol_knowledge.db --output docs

# Export to Neo4j only
python src/neo4j_exporter.py --db data/cobol_knowledge.db
```

## License

MIT
