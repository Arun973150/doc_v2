"""
Run the COBOL Documentation Pipeline

Usage:
  python run_pipeline.py                    # Full pipeline (parse + load + docs)
  python run_pipeline.py --skip-parse       # Skip parsing (use existing parsed_output/)
  python run_pipeline.py --skip-enrich      # Skip LLM enrichment
  python run_pipeline.py --enrich           # Enable LLM enrichment (requires GROQ_API_KEY in .env)

Output:
  docs/00-SYSTEM-OVERVIEW.md       # Layer 1: System overview
  docs/modules/*.md                # Layer 2: Module documentation
  docs/programs/*.md               # Layer 3: Program walkthroughs
  docs/business-rules/*.md         # Layer 4: Business rules catalog
  docs/screens/*.md                # Layer 5: Screen catalog
  docs/diagrams/call-graph.md      # Call graph diagram
  docs/data-dictionary.md          # Data dictionary
  docs/copybook-reference.md       # Copybook reference
"""
import sys
sys.path.insert(0, 'src')

from orchestrator import run_pipeline

result = run_pipeline(
    repo_path="carddemo",
    output_dir="docs",
    db_path="data/cobol_knowledge.db",
    schema_path="schemas/cobol_knowledge.sql",
    skip_parse=True,       # Set to False to re-parse with ProLeap
    skip_jcl=False,        # Parse JCL files from carddemo/
    skip_enrich=False,     # Set to False + set GROQ_API_KEY to enable LLM enrichment
    skip_neo4j=False,      # Neo4j Desktop running at localhost:7687
    cobol_format="FIXED",
    groq_model="gemini-2.0-flash",   # Vertex AI model
)
