# ArchitectAI Enterprise Platform: Production Deployment Guide

This guide provides end-to-end instructions for deploying the **ArchitectAI Autonomous Tech Lead Platform** across environments—from single-node Docker Compose virtual machines to enterprise Kubernetes clusters, serverless cloud containers, and air-gapped sovereign data centers.

---

## 🏗️ Platform Architecture & Port Allocations

ArchitectAI is built with a dual-engine architecture containerized in a unified runtime:

| Component | Port | Description | Health Check |
| :--- | :---: | :--- | :--- |
| **FastAPI REST API Engine** | `8000` | REST API, OpenAPI/Swagger UI, telemetry, security guardrails | `GET /health` |
| **Streamlit Interactive UI** | `8501` | High-fidelity executive console, data room, interactive builder | `GET /_stcore/health` |
| **Redis Cache & State Store** | `6379` | Multi-agent coordination and workflow cache | `redis-cli ping` |

---

## ⚡ Option 1: Docker Compose (Recommended for VMs & Quickstart)

The simplest and most resilient way to deploy on any Linux server (AWS EC2, GCP Compute Engine, DigitalOcean Droplet, Hetzner, or local machine).

### Prerequisites
- Docker Engine `>= 24.0`
- Docker Compose `>= 2.20`
- Git

### 1. Clone & Configure
```bash
git clone https://github.com/your-org/ArchitectAI-Autonomous-Tech-Lead.git
cd ArchitectAI-Autonomous-Tech-Lead

# Create and populate environment variables
cp .env.example .env
```

### 2. Configure API Keys in `.env`
Edit `.env` with your preferred LLM provider keys:
```bash
# Primary LLM provider: groq, anthropic, openai, or gemini
DEFAULT_LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here

# Optional Multi-Model Router keys (for token telemetry comparisons)
ANTHROPIC_API_KEY=sk-ant-your_key_here
OPENAI_API_KEY=sk-your_key_here
GOOGLE_API_KEY=your_gemini_key_here

# Production application environment
APP_ENV=production
```

### 3. Launch Services
```bash
docker compose up -d --build
```

### 4. Verify Deployment
```bash
# Verify container health
docker compose ps

# Check FastAPI Swagger UI (Port 8000)
curl -s http://localhost:8000/health

# Check Streamlit Dashboard (Port 8501)
curl -sI http://localhost:8501/_stcore/health
```

Access in your browser:
- **Interactive Web Platform**: `http://<SERVER_IP>:8501`
- **FastAPI REST & Swagger Docs**: `http://<SERVER_IP>:8000/docs`

---

## 🔒 Option 2: Production VM with Automated SSL / Reverse Proxy (Caddy / Nginx)

To put ArchitectAI behind a production domain with automatic HTTPS/TLS certificates, use **Caddy** as a lightweight reverse proxy.

### Caddyfile Configuration (`/etc/caddy/Caddyfile`)
```caddy
architectai.yourdomain.com {
    # Route REST API and Swagger Docs to FastAPI
    handle /docs* {
        reverse_proxy localhost:8000
    }
    handle /redoc* {
        reverse_proxy localhost:8000
    }
    handle /openapi.json* {
        reverse_proxy localhost:8000
    }
    handle /api/* {
        reverse_proxy localhost:8000
    }
    handle /health* {
        reverse_proxy localhost:8000
    }

    # Route Web UI and WebSockets to Streamlit
    handle {
        reverse_proxy localhost:8501 {
            # Streamlit WebSocket support
            header_up Host {host}
            header_up X-Real-IP {remote_host}
        }
    }
}
```

Reload Caddy:
```bash
sudo systemctl reload caddy
```

---

## ☸️ Option 3: Production Kubernetes (EKS, GKE, AKS, On-Premise)

ArchitectAI provides native Kubernetes manifests in the [k8s/](file:///Users/chandini/ArchitectAI-Autonomous-Tech-Lead.worktrees/system-design-workflow-reference/k8s) directory.

### 1. Create Namespace & Secret
```bash
kubectl create namespace architectai

kubectl create secret generic architectai-secrets \
  --namespace=architectai \
  --from-literal=GROQ_API_KEY="gsk_..." \
  --from-literal=ANTHROPIC_API_KEY="sk-ant-..." \
  --from-literal=OPENAI_API_KEY="sk-..."
```

### 2. Deploy Using Kustomize
```bash
# Preview manifests
kubectl kustomize k8s/

# Apply to cluster
kubectl apply -k k8s/
```

### 3. Verify Rollout Status
```bash
kubectl rollout status deployment/architectai-platform -n architectai
kubectl get pods,svc,ingress -n architectai
```

The ingress controller automatically directs:
- `https://architectai.yourdomain.com/docs` ➡️ **FastAPI (port 8000)**
- `https://architectai.yourdomain.com/` ➡️ **Streamlit Web UI (port 8501)**

---

## ☁️ Option 4: Serverless Cloud Containers (Google Cloud Run / AWS ECS)

### Google Cloud Run
Build and push the multi-architecture image:
```bash
# 1. Build and tag
gcloud builds submit --tag gcr.io/$PROJECT_ID/architectai-platform:latest

# 2. Deploy to Cloud Run (minimum 2 vCPU, 2GiB RAM)
gcloud run deploy architectai-platform \
  --image gcr.io/$PROJECT_ID/architectai-platform:latest \
  --platform managed \
  --region us-central1 \
  --port 8000 \
  --memory 4Gi \
  --cpu 2 \
  --allow-unauthenticated \
  --set-env-vars="APP_ENV=production,DEFAULT_LLM_PROVIDER=groq" \
  --set-secrets="GROQ_API_KEY=groq-api-key:latest"
```

### AWS ECS / Fargate
1. Push image to **Amazon ECR**.
2. Create an ECS Task Definition with `cpu: 1024`, `memory: 2048`.
3. Configure the container port mapping for `8000` and `8501`.
4. Connect to an **Application Load Balancer (ALB)** with target groups for both ports.

---

## 🛡️ Option 5: Sovereign & Air-Gapped On-Premises (Zero-Cloud Spend)

For enterprise defense, banking, or healthcare compliance requiring **zero data egress**:

### 1. Set Up Local Ollama
```bash
# Run local open-weights model
ollama run llama3.2
```

### 2. Configure ArchitectAI for Air-Gapped Mode
In `.env`:
```bash
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
OLLAMA_MODEL=llama3.2
MOCK_LLM=false
```

### 3. Start Container in Sovereign Mode
```bash
docker compose up -d
```
All code synthesis, model routing, and due diligence benchmarks will execute **100% locally** with zero external network calls.

---

## 📊 Post-Deployment Health & SOC2 Audit Verification

Once deployed, run automated validation probes:

```bash
# 1. REST Health & Model Registry Verification
curl -s http://localhost:8000/health | jq .

# 2. SOC2 Security Posture & Guardrails Verification
curl -s http://localhost:8000/api/v1/security/posture | jq .

# 3. Cryptographic Audit Chain Integrity Check
curl -s http://localhost:8000/api/v1/security/audit-ledger?limit=5 | jq .

# 4. Software Bill of Materials (SBOM) SCA Check
curl -s http://localhost:8000/api/v1/due-diligence/sbom | jq .
```

---

## ⚙️ Environment Configuration Reference

| Environment Variable | Default | Required | Purpose |
| :--- | :--- | :---: | :--- |
| `APP_ENV` | `production` | Yes | Application mode (`development`, `staging`, `production`) |
| `DEFAULT_LLM_PROVIDER` | `groq` | Yes | Active LLM engine (`groq`, `anthropic`, `openai`, `gemini`, `ollama`) |
| `GROQ_API_KEY` | - | Conditional | Required if provider is `groq` |
| `ANTHROPIC_API_KEY` | - | Conditional | Required if using Claude 3.5 Sonnet router |
| `OPENAI_API_KEY` | - | Conditional | Required if using GPT-4o router |
| `GOOGLE_API_KEY` | - | Conditional | Required if using Gemini Flash router |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | No | Base URL for air-gapped Ollama server |
| `MOCK_LLM` | `false` | No | Enables hermetic mock mode for testing without API keys |
| `STREAMLIT_SERVER_PORT` | `8501` | Yes | Web platform port |
| `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` | Yes | Web platform host binding |
| `REDIS_HOST` | `redis` / `localhost` | No | Cache and state store host |
| `REDIS_PORT` | `6379` | No | Cache and state store port |

---

## 🆘 Troubleshooting

### Port 8000 or 8501 Conflict
If ports are already in use on your host:
```bash
# Find process using the port
lsof -i :8000
lsof -i :8501

# Modify external port mappings in docker-compose.yml:
# - "8080:8000"
# - "8502:8501"
```

### Inspect Container Logs
```bash
# View combined logs
docker compose logs -f architectai

# View specific service logs inside container
docker exec architectai-platform tail -f /app/logs/orchestrator.log
```
