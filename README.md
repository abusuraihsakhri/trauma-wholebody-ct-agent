# Trauma Wholebody CT Agent

A **synthetic, rule-based software demonstrator** with a browser interface, Python CLIs, and a FastAPI service. It evaluates generic numerical inputs, a priority flag, and status keywords to exercise logging, validation, and alert workflows.

> **Not a medical device or clinical decision-support system.** The project does not read DICOM or CT images, identify trauma, assign AAST organ-injury grades, perform hemorrhage detection, or validate patient care recommendations. Numerical thresholds are demonstration values, not guideline cutoffs. Never enter real patient data.

## Browser demonstrator

Open [web/index.html](web/index.html) locally in a modern browser. No installation, server, account, or API token is required. Enter **invented** input values, evaluate the three demonstration rules, and optionally export the output as JSON.

The static page makes no data submissions, uses no third-party assets, and does not persist data. It is separate from the Python API. Deployment is configured under [GitHub Actions](.github/workflows/pages.yml); a public site URL should be advertised only after Pages deployment is verified.

## Current functionality

- **Synthetic primary threshold:** a value above 25 produces an elevated demonstration alert.
- **Synthetic secondary threshold:** a value above 12 produces an elevated alert; a manually set critical flag produces a critical demonstration alert.
- **Status keyword matcher:** DISCORDANT, ANOMALY, MUTANT, VIOLATION, FAIL, and REJECT produce an elevated alert.
- **Python CLI and CSV batch:** synthetic task input/output and an in-memory supervisor.
- **FastAPI:** `GET /health`, `GET /metrics`, `POST /api/audit`, and `POST /api/chat` via `agents.api`.
- **Audit trail:** chained HMAC-SHA256 records with full signature verification; records are process-local and not persisted.
- **Other legacy modules:** `trauma_wholebody_ct_agent/`, `trauma_scan_sentinel.py`, and `enrichment.py` preserve compatibility, but their names do not imply implemented CT image analysis or validated AAST scoring.

No external language model is invoked: the LLM factory currently returns deterministic mock responses, including when other provider names are selected. The project's pattern-based sensitive-data guard only identifies certain obvious formats; it is **not** a complete PHI de-identification system or a verified HIPAA control.

## Install and test

Requires Python 3.10+.

```bash
git clone https://github.com/abusuraihsakhri/trauma-wholebody-ct-agent.git
cd trauma-wholebody-ct-agent
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[server,dev]"
python -m pytest -q
```

On Windows, activate the virtual environment using `.venv\Scripts\activate`.

## Python examples

```bash
# Primary CLI (synthetic inputs only)
python cli.py audit --task-id DEMO-001 --target SYNTH-01 --primary 26 --secondary 5
python cli.py chat "status"
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit

# API: binds to loopback by default
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python cli.py serve --host 127.0.0.1 --port 8000

# Secondary historical CLI remains available
python -m trauma_wholebody_ct_agent.cli audit --case-id DEMO-002
```

The primary batch CSV accepts `task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor`. Accepted boolean text includes `True/False`, `1/0`, and `yes/no`; unrecognized values are rejected. `sample.csv` is a legacy input example with a different column naming scheme.

**Security:** The API is unauthenticated and must not be publicly exposed without an appropriate authentication and network-security layer. The default CLI server bind is `127.0.0.1`; Docker Compose publishes to loopback. Supply a unique `AUDIT_SECRET_KEY` for a consistent audit signing key. When unset, the software creates a random process-local key, so old records cannot be verified after restart. Audit entries are stored in volatile memory, and the application makes no claim of compliance with clinical data-protection requirements.

## Container use

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
# http://127.0.0.1:8000/docs
```

The provided Docker configuration is suitable only for local demonstrations; it is not a production healthcare deployment.

## Implementation

Python 3.10+, Pydantic 2, FastAPI (optional server extra), standard-library HMAC-SHA256, pytest, and a plain HTML/CSS/JavaScript browser UI. The browser demonstration does **not** require Pyodide or execute Python in the browser. The CI workflow tests Python 3.10–3.12 and checks browser JavaScript syntax.

## License

[MIT](LICENSE).
