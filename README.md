# App Policy Auditor

Audit privacy policies/EULAs of the apps/software you use. Fetches docs, extracts text, flags risky clauses with rules, and (optionally) produces AI summaries.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python auditor.py --seed examples/seed_targets.txt --out report
```
