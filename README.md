# Trauma Wholebody CT Agent

> **Domain:** Diagnostic Radiology & Medical Imaging AI  
> **Reference Guidelines & Standards:** `American College of Radiology (ACR) RADS & Fleischner Society`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Trauma Wholebody CT Agent** is an advanced analytical and computational platform implementing Whole-Body Pan-Scan AAST Organ Injury Scaling Agent. It provides multi-agent trauma assessment with cryptographic audit trails and PHI protection.

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/trauma-wholebody-ct-agent.git
cd trauma-wholebody-ct-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest
```

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`Severity`** — Alert severity classification (INFO, ADVISORY, WARNING, CRITICAL)
- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks
- **`AgentAlert`** — Structured alert model with clinical findings and recommendations
- **`OrganInjuryScalingAgent`**: Specialized Sub-Agent 1 - Primary metric threshold evaluation
- **`BlushExtravasationDetectorAgent`**: Specialized Sub-Agent 2 - STAT kinetics & escalation
- **`InjurySeverityScoreSynthesizerAgent`**: Specialized Sub-Agent 3 - Biomarker concordance

### 🏗️ Architecture Components

| Module | Purpose |
|:-------|:--------|
| `agents/` | Core enterprise agent system with PHI guard, HMAC audit, and FastAPI server |
| `trauma_wholebody_ct_agent/` | Clinical agent system with AAST OIS 2018 guideline engine |
| `enrichment.py` | Enrichment feature suite with 8 domain-specific evaluation engines |
| `simulator.py` | High-throughput stress testing and simulation |
| `cli.py` | Command-line interface for audit, chat, batch processing, and serving |

---

## 💻 CLI Quickstart & Usage

### 1. Run Single Audit
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Query Supervisory Chat
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task/case identifier | TASK-2026-001 |
| `--target` | Target identifier | KEY-TARGET-01 |
| `--primary` | Primary metric value (float) | 28.5 |
| `--secondary` | Secondary metric value (float) | 14.2 |
| `--critical` | Flag critical/emergency status | False |
| `--status` | Status descriptor | DISCORDANT |

### Input Data Schema (CSV Batch)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `case_id` | Case identifier | Required |
| `patient_synthetic_id` | Synthetic patient identifier | Required |
| `metric_primary` | Primary measurement value | Required |
| `metric_secondary` | Secondary measurement value | Required |
| `is_stat` | STAT emergency flag | Required |
| `status_flag` | Status descriptor | Required |

---

## 🛡️ Security & Enterprise Architecture

### Zero-PHI Outbound Interceptor
Active regex inspection blocking SSNs, MRNs, phone numbers, emails, DOBs, and patient identifiers. Raises `SecurityException` on detection.

### Tamper-Evident HMAC-SHA256 Audit Trail
Chained, cryptographically signed logs for every evaluation and state transition. Each entry includes:
- Unique audit ID and timestamp
- Actor and event type
- SHA-256 payload hash
- Previous hash (chain linkage)
- HMAC-SHA256 signature

### Input Validation
All metric values are validated to ensure they are finite numbers within safe bounds (rejects NaN, Infinity, and extreme values > 1e9).

### Security Configuration
**IMPORTANT:** Set the `AUDIT_SECRET_KEY` environment variable in production:
```bash
# Linux/macOS
export AUDIT_SECRET_KEY="your-secure-random-key-here"

# Windows
set AUDIT_SECRET_KEY=your-secure-random-key-here
```

### Additional Features
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

### Test Coverage
- PHI guard enforcement and redaction
- Specialized worker evaluation logic
- Supervisor consensus and audit trail integrity
- Metric input validation (NaN, Infinity, bounds)
- Enrichment engine threshold evaluation
- CLI command execution

---

## 🐳 Container Deployment

### Docker
```bash
# Build
docker build -t trauma-wholebody-ct-agent .

# Run (with secure key)
docker run -p 8000:8000 -e AUDIT_SECRET_KEY="your-secure-key" trauma-wholebody-ct-agent
```

### Docker Compose
```bash
# Set your secure key
export AUDIT_SECRET_KEY="your-secure-key"

# Launch
docker-compose up -d
```

---

## 📁 Project Structure

```
trauma-wholebody-ct-agent/
├── agents/                    # Core enterprise agent system
│   ├── api.py                 # FastAPI REST server
│   ├── base.py                # PHI guard, HMAC audit, security
│   ├── models.py              # Pydantic data models
│   ├── supervisor.py          # Multi-agent orchestrator
│   ├── workers.py             # Specialized evaluation workers
│   ├── llm_factory.py         # LLM provider factory
│   ├── metrics.py             # Prometheus metrics
│   ├── learning.py            # Bayesian calibration engine
│   └── streamer.py            # WebSocket telemetry
├── trauma_wholebody_ct_agent/ # Clinical agent system
│   ├── agents.py              # Clinical sub-agents
│   ├── engine.py              # AAST OIS 2018 guideline engine
│   ├── models.py              # Clinical data models
│   ├── cli.py                 # Clinical CLI
│   └── server.py              # Clinical FastAPI server
├── tests/                     # Test suite
├── web/                       # Operations console (HTML)
├── cli.py                     # Main CLI entry point
├── simulator.py               # Load testing simulator
├── enrichment.py              # Enrichment feature suite
├── trauma_scan_sentinel.py    # Standalone sentinel CLI/API
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Compose configuration
└── pyproject.toml             # Project metadata
```
