# Agent Instructions

## graphify

This project has a graphify knowledge graph at `graphify-out/`.

Rules:
- Before answering architecture or codebase questions, read `graphify-out/GRAPH_REPORT.md` for god nodes and community structure.
- If `graphify-out/wiki/index.md` exists, navigate it instead of reading raw files.
- For cross-module "how does X relate to Y" questions, prefer to use the graphify python module to query the graph (`graph.json`) or use graphify tools to explore instead of scanning files.
- After modifying code files, you should ideally rebuild or update the graph to keep it current.
