# 🏗️ ArchitectAI: Autonomous Tech Lead

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Architecture: Clean Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange.svg)](#architecture)
[![Testing: Pytest](https://img.shields.io/badge/Testing-Pytest%20Passing-brightgreen.svg)](#testing)

**ArchitectAI** is an autonomous, multi-agent AI tech lead and engineering pipeline. It transforms natural-language software specifications into production-ready, clean-architecture backend codebases with automated AST validation, self-healing code repair, deployment packaging, and multi-agent artifact generation.

---

## 🌟 Key Features

- **🧠 End-to-End Autonomous Generation**: Extracts domain entities, attributes, and relationships to synthesize complete FastAPI backends (SQLAlchemy 2.0 models, Pydantic v2 schemas, transactional repositories, business services, and dependency-injected routers).
- **📐 15-Step System Design Workflow**: Implements a disciplined system design methodology ([docs/workflow.md](docs/workflow.md)) covering capacity estimation, NFRs/SLOs, API contracts, resilience patterns (circuit breakers, exponential jitter), and formal Architectural Decision Records (ADRs).
- **🛠️ Automated Validation & Self-Healing**: Validates generated code using Python AST parsing, import graph resolution, and automated test execution. Detects syntax or import failures and repairs them iteratively through the [`SelfHealingEngine`](orchestration/self_healing_engine.py).
- **🌐 Resilient Multi-Provider LLM Engine**: Seamlessly dispatches across **Groq** (Llama-3.3-70B), **Google Gemini** (Gemini-2.5-Flash / Pro), **OpenAI** (GPT-4o), and **Ollama** (local models) using OpenAI-compatible transports with exponential backoff and offline mock modes.
- **🤖 Autonomous Agent Collaboration**: Features specialized agent personas (Solution Architect, Database Architect, Backend Engineer, QA Engineer, Security Engineer, DevOps, and Documentation) collaborating over a versioned [`ArtifactRegistry`](artifacts/registry.py).
- **📦 Production Packaging & Export**: Automatically emits `Dockerfile`, `docker-compose.yml`, environment configurations, README documentation, zip archives, and markdown generation reports.

---

## 📁 Repository Structure

```bash
.
├── architectai.py          # Standalone CLI entry point
├── main.py                 # Universal CLI dispatcher (generate, stage, legacy workflows)
├── config/                 # Pydantic settings, LLM providers, and prompts
├── docs/                   # System Design Workflow, Architecture, and API specifications
│   ├── workflow.md         # 15-Step System Design Workflow Reference
│   ├── architecture.md     # ArchitectAI platform architecture & Mermaid diagrams
│   └── api.md              # CLI and generated REST API standards
├── templates/              # Production deliverable templates (SAD, BRD, API, Sprint)
│   ├── architecture_template.md
│   ├── brd_template.md
│   ├── api_template.md
│   └── sprint_template.md
├── orchestration/          # Master pipeline, project validator, and self-healing engine
├── generators/             # Layered code generators (models, schemas, repos, services, APIs)
├── agents/                 # Autonomous agent manager and specialized engineering agents
├── planner/                # Task planning, DAG scheduling, and parallel execution
├── review/                 # Code reviewer and automated syntax fixer
├── tests/                  # Unit and integration test suite
├── outputs/                # Default generated project workspace
└── requirements.txt        # Runtime dependencies
```

---

## ⚡ Quick Start

### 1. Clone & Setup Environment

```bash
git clone https://github.com/mlexpnew/ArchitectAI-Autonomous-Tech-Lead.git
cd ArchitectAI-Autonomous-Tech-Lead

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment configuration:

```bash
cp .env.example .env
```

Configure your preferred LLM provider in `.env`:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile

# Or configure Google Gemini:
# LLM_PROVIDER=gemini
# GOOGLE_API_KEY=your_gemini_api_key_here
# GEMINI_MODEL=gemini-2.5-flash

# Or enable offline mock mode for testing without credentials:
# MOCK_LLM=true
```

---

## 🚀 Usage

### Autonomous Generation (Master Pipeline)

Run the full end-to-end pipeline from natural-language requirements:

```bash
python3 main.py generate \
  --name "Hospital_Management_System" \
  --requirements "examples/hospital_requirements.txt" \
  --output "outputs/Hospital_Management_System"
```

Or invoke via `architectai.py`:

```bash
python3 architectai.py generate \
  --name "Library_System" \
  --requirements "examples/library_requirements.txt" \
  --output "generated_projects/Library_System"
```

### Single-Stage Execution

Execute specific engineering or generation phases independently:

```bash
# Scaffold folder structure
python3 main.py scaffold

# Generate models only
python3 main.py generate-models

# Run autonomous tech lead workflow
python3 main.py autonomous

# Run CrewAI architecture planning
python3 main.py architecture
```

### Programmatic Python API

```python
from orchestration.architect_pipeline import ArchitectPipeline

pipeline = ArchitectPipeline(output_dir="outputs/Inventory_System")

result = pipeline.generate(
    requirements="""
    Build an Inventory Management System.
    Manage Products, Categories, and Warehouses.
    A Category contains many Products.
    Each Product has inventory counts tracked across Warehouses.
    """,
    project_name="Inventory Management System",
)

print(f"Project generated at: {result['output_dir']}")
print(f"Validation status: {result['validation']['valid']}")
print(f"Archive file: {result['export']['archive']}")
```

---

## 🧪 Testing & Verification

Run the test suite using `pytest`:

```bash
pytest
```

To run tests in offline mode without requiring network access or paid API keys:

```bash
MOCK_LLM=true pytest
```

---

## 📄 Documentation

- [System Design Workflow Reference](docs/workflow.md): Comprehensive 15-step reference guide for scalable software design.
- [System Architecture](docs/architecture.md): Deep-dive into ArchitectAI internal architecture and Mermaid diagrams.
- [API & Interface Standards](docs/api.md): CLI reference and generated RESTful API standards.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
