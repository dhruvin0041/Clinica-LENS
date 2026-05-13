# Project Instructions: Clinica-LENS

## Foundational Mandates

### Graphify & Architecture
- This project uses a **graphify** knowledge graph located at `graphify-out/`.
- **Pre-Analysis:** Before answering architecture or codebase questions, analyze `graphify-out/GRAPH_REPORT.md` to understand "God Nodes" (core abstractions) and community structure.
- **Navigation:** If `graphify-out/wiki/index.md` exists, navigate it for context instead of scanning raw files.
- **Relationship Discovery:** For cross-module "how does X relate to Y" questions, prefer to use the graphify Python module to query `graph.json` or use graphify tools to explore instead of scanning files.

### Development Workflow
- **Mandatory Commits:** Every modification to the codebase MUST be followed by a git commit with a clear, concise message.
- **Validation & Sync:** Always verify changes and rebuild/update the graph after modifications (using `graphify --update`) to keep it synchronized with the code.
- **Testing:** Ensure all tests in `tests/` pass before concluding a task.
