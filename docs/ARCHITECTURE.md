# Architecture

- **CLI (auditor.py):** orchestrates fetching -> extraction -> rule scan -> optional LLM -> reports.
- **policy_fetcher.py:** heuristics + small web search to find policy URLs.
- **text_extract.py:** HTML/PDF -> clean text (Trafilatura -> Readability fallback; PDFMiner for PDFs).
- **analyzers/rule_engine.py:** YAML-driven rules; returns excerpts.
- **analyzers/llm_assistant.py:** optional OpenAI pass for 5-point summary.
- **os_discovery.py:** platform-specific app enumeration.
- **rules/risk_rules.yaml:** risk policy patterns and severity.
