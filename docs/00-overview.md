# Health Data Vault — Exploration

**Status:** Research phase
**Origin:** Paul Mederos conversation (2026-02-23)
**Adjacent to:** Kasane (habit deck for family health)

---

## The Core Idea

A structured, local-first personal health data vault that:
1. Ingests health data from multiple sources (lab PDFs, wearable exports, doctor notes)
2. Parses and normalizes it into structured, queryable formats
3. Exposes it via MCP so any LLM or app can read it with your permission
4. Tracks trends over time (not just latest snapshot)

## Key Question

**What needs to be true for this to not just be "upload to Google Drive"?**

→ See: [01-why-not-gdrive.md](./01-why-not-gdrive.md)
→ See: [02-market-landscape.md](./02-market-landscape.md)
→ See: [03-technical-architecture.md](./03-technical-architecture.md)
→ See: [04-mcp-design.md](./04-mcp-design.md)
→ See: [05-mvp-scope.md](./05-mvp-scope.md)

## Files

| File | What's in it |
|------|-------------|
| 00-overview.md | This file — index and framing |
| 01-why-not-gdrive.md | The differentiation argument |
| 02-market-landscape.md | What exists, what's working, what's not |
| 03-technical-architecture.md | FHIR, LOINC, parsing, storage |
| 04-mcp-design.md | MCP server design — tools, resources, queries |
| 05-mvp-scope.md | What to build first and how to test it |
