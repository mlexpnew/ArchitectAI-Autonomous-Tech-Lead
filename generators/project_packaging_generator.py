"""
ArchitectAI Project Packaging Generator

Generates deployment and documentation files
for dynamically generated backend projects.
"""

from pathlib import Path
import json

from generators.writer import FileWriter
from generators.e2e_testing_generator import E2ETestingGenerator


class ProjectPackagingGenerator:

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.backend_dir = self.output_dir / "backend"

    def generate_requirements(self):
        content = """fastapi
uvicorn[standard]
sqlalchemy
pydantic
pytest
httpx
alembic
"""

        FileWriter.write(
            self.backend_dir / "requirements.txt",
            content,
        )

        print("✅ Generated requirements.txt")

    def generate_env_example(self):
        content = """# Generated Backend Configuration

APP_ENV=development
DEBUG=True

DATABASE_URL=sqlite:///./app.db

API_HOST=0.0.0.0
API_PORT=8000
"""

        FileWriter.write(
            self.backend_dir / ".env.example",
            content,
        )

        print("✅ Generated .env.example")

    def generate_dockerfile(self):
        content = """FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

        FileWriter.write(
            self.backend_dir / "Dockerfile",
            content,
        )

        print("✅ Generated Dockerfile")

    def generate_dockerignore(self):
        content = """__pycache__
*.pyc
*.pyo
*.pyd
.pytest_cache
.venv
venv
.env
app.db
*.db
.git
.DS_Store
"""

        FileWriter.write(
            self.backend_dir / ".dockerignore",
            content,
        )

        print("✅ Generated .dockerignore")

    def generate_gitignore(self):
        content = """__pycache__/
*.py[cod]
.venv/
venv/
.env
.pytest_cache/
*.db
app.db
.DS_Store
"""

        FileWriter.write(
            self.backend_dir / ".gitignore",
            content,
        )

        print("✅ Generated .gitignore")

    def generate_pytest_ini(self):
        content = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
pythonpath = .
"""
        FileWriter.write(
            self.backend_dir / "pytest.ini",
            content,
        )
        print("✅ Generated pytest.ini")

    def generate_openapi_spec(self):
        try:
            import subprocess
            import sys
            backend_path = str(self.backend_dir.resolve())
            script = f"""
import sys, json
sys.path.insert(0, {repr(backend_path)})
try:
    from app.main import app
    print("ARCHITECTAI_SPEC_START")
    print(json.dumps(app.openapi()))
    print("ARCHITECTAI_SPEC_END")
except Exception:
    import sys
    sys.exit(1)
"""
            res = subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.backend_dir,
            )
            if res.returncode == 0 and "ARCHITECTAI_SPEC_START" in res.stdout:
                spec_json = res.stdout.split("ARCHITECTAI_SPEC_START")[1].split("ARCHITECTAI_SPEC_END")[0].strip()
                FileWriter.write(self.backend_dir / "openapi.json", spec_json)
                print("✅ Generated openapi.json")
        except Exception as e:
            print(f"⚠️ Could not generate openapi.json: {e}")

    def generate_alembic_setup(self, project_name: str, blueprint=None):
        alembic_dir = self.backend_dir / "alembic"
        versions_dir = alembic_dir / "versions"

        # 1. alembic.ini
        ini_content = """# Alembic Configuration for ArchitectAI Backend

[alembic]
script_location = alembic
prepend_sys_path = .
version_locations = %(here)s/alembic/versions

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
        FileWriter.write(self.backend_dir / "alembic.ini", ini_content)

        # 2. alembic/env.py
        env_py_content = """import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Ensure application package is discoverable
sys.path.insert(0, os.path.abspath("."))

from app.database import Base

try:
    from app.config import settings
    db_url = settings.DATABASE_URL
except Exception:
    db_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Import all models to ensure registration with Base.metadata
try:
    import app.models  # noqa: F401
except Exception:
    pass

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""
        FileWriter.write(alembic_dir / "env.py", env_py_content)

        # 3. alembic/script.py.mako
        mako_content = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""
        FileWriter.write(alembic_dir / "script.py.mako", mako_content)

        # 4. alembic/versions/001_initial_schema.py
        table_creates = []
        table_drops = []
        entities = getattr(blueprint, "entities", []) if blueprint else []

        TYPE_MAP = {
            "integer": "sa.Integer()",
            "string": "sa.String()",
            "float": "sa.Float()",
            "boolean": "sa.Boolean()",
            "date": "sa.Date()",
            "time": "sa.Time()",
        }

        for entity in entities:
            t_name = f"{entity.name.lower()}s"
            cols = ["            sa.Column('id', sa.Integer(), nullable=False, primary_key=True)"]
            for field in getattr(entity, "fields", []):
                if field.name.lower() == "id":
                    continue
                c_type = TYPE_MAP.get(str(field.type).lower(), "sa.String()")
                cols.append(f"            sa.Column('{field.name}', {c_type}, nullable=True)")
            cols_str = ",\n".join(cols)
            table_creates.append(f"""    if '{t_name}' not in existing_tables:
        op.create_table(
            '{t_name}',
{cols_str}
        )""")
            table_drops.append(f"""    if '{t_name}' in existing_tables:
        op.drop_table('{t_name}')""")

        table_init = "    conn = op.get_bind()\n    inspector = sa.inspect(conn)\n    existing_tables = set(inspector.get_table_names())"
        upgrade_body = (table_init + "\n" + "\n".join(table_creates)) if table_creates else "    pass"
        downgrade_body = (table_init + "\n" + "\n".join(reversed(table_drops))) if table_drops else "    pass"

        initial_migration_content = f'''"""001_initial_schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-09-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
{upgrade_body}


def downgrade() -> None:
{downgrade_body}
'''
        FileWriter.write(versions_dir / "001_initial_schema.py", initial_migration_content)
        print("✅ Generated Alembic migration setup (alembic.ini, env.py, script.py.mako, 001_initial_schema.py)")

    def generate_database_seeder(self, project_name: str, blueprint=None):
        entities = getattr(blueprint, "entities", []) if blueprint else []

        seed_blocks = []
        for entity in entities:
            e_name = entity.name
            fields = getattr(entity, "fields", [])
            records = []
            for row_idx in (1, 2, 3):
                row_data = {}
                for field in fields:
                    f_name = field.name
                    if f_name.lower() == "id":
                        continue
                    f_type = str(field.type).lower()
                    if f_type == "integer":
                        row_data[f_name] = row_idx * 10
                    elif f_type == "float":
                        row_data[f_name] = round(row_idx * 29.5, 2)
                    elif f_type == "boolean":
                        row_data[f_name] = (row_idx % 2 == 1)
                    elif f_type == "date":
                        row_data[f_name] = f"2026-09-{row_idx:02d}"
                    elif "email" in f_name.lower():
                        row_data[f_name] = f"{e_name.lower()}{row_idx}@example.com"
                    elif "status" in f_name.lower():
                        row_data[f_name] = "ACTIVE" if row_idx == 1 else ("PENDING" if row_idx == 2 else "COMPLETED")
                    elif any(k in f_name.lower() for k in ("name", "title", "label")):
                        row_data[f_name] = f"{e_name} #{row_idx}"
                    elif f_name.endswith("_id"):
                        row_data[f_name] = 1
                    else:
                        row_data[f_name] = f"Sample {f_name.replace('_', ' ').title()} {row_idx}"
                records.append(row_data)

            records_repr = json.dumps(records, indent=12)
            seed_blocks.append(f"""
        # Seed {e_name}
        existing_{e_name.lower()} = db.query(models.{e_name}).first()
        if not existing_{e_name.lower()}:
            items_{e_name.lower()} = {records_repr}
            for item in items_{e_name.lower()}:
                db.add(models.{e_name}(**item))
            db.commit()
            summary["{e_name}"] = len(items_{e_name.lower()})
            print(f"  ✓ Seeded {{len(items_{e_name.lower()})}} {e_name} records")
        else:
            print(f"  ℹ {e_name} already seeded")
""")

        seed_body = "".join(seed_blocks) if seed_blocks else "        pass"

        seed_py_content = f'''"""
ArchitectAI Synthetic Mock Data Seeder
Populates the database with realistic demo records for {project_name}.
"""

import sys
import os
import json
from pathlib import Path

# Ensure application package is discoverable
sys.path.insert(0, os.path.abspath("."))

from app.database import SessionLocal, Base, engine
import app.models as models


def seed():
    print("🌱 Seeding database with demo records...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    summary = {{}}
    try:
{seed_body}
        total = sum(summary.values())
        print(f"✨ Seeding complete! Added {{total}} total records.")
        return summary
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {{e}}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
'''
        FileWriter.write(self.backend_dir / "seed.py", seed_py_content)
        print("✅ Generated database seeder (seed.py)")

    def generate_readme(
        self,
        project_name: str,
        entities,
    ):
        entity_names = [
            entity.name
            for entity in entities
        ]

        entities_text = "\n".join(
            f"- {name}"
            for name in entity_names
        )

        # Use a normal multi-line string without
        # nested Markdown code fences.
        content = f"""# {project_name}

Automatically generated by ArchitectAI Autonomous Tech Lead.

## Generated Entities

{entities_text}

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest
- Docker
- Kubernetes & Kustomize
- Helm 3

## Run Locally

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Start the API:

    uvicorn app.main:app --reload

Swagger documentation:

    http://127.0.0.1:8000/docs

## Run Tests

    python3 -m pytest tests/ -v

## Docker

Build:

    docker build -t architectai-generated-api .

Run:

    docker run --rm -p 8000:8000 architectai-generated-api

## Kubernetes Deployment

Deploy all resources (Deployment, Service, ConfigMap, Ingress, HPA):

    kubectl apply -k k8s/

Port-forward service to test locally:

    kubectl port-forward service/{self.sanitize_k8s_name(project_name)}-service 8000:80

## Helm Deployment

Install chart:

    helm install {self.sanitize_k8s_name(project_name)} ./helm/{self.sanitize_k8s_name(project_name)}

Upgrade chart:

    helm upgrade {self.sanitize_k8s_name(project_name)} ./helm/{self.sanitize_k8s_name(project_name)}

## Database Migrations (Alembic)

Apply schema migrations:

    alembic upgrade head

Create a new migration revision:

    alembic revision --autogenerate -m "Add new column"

## Seed Sample Data

Populate the database with realistic demo records:

    python seed.py

## Frontend & E2E Testing (Playwright & Cypress)

Run cross-browser automated end-to-end test suites:

    cd ../frontend
    npm install
    npx playwright install --with-deps
    npm run test:e2e       # Headless Playwright across Chromium, Firefox & WebKit
    npm run test:e2e:ui    # Playwright interactive UI mode
    npm run cypress:run    # Headless Cypress suite
    npm run cypress:open   # Cypress interactive runner

## Architecture

    backend/
    ├── alembic/
    │   ├── versions/
    │   │   └── 001_initial_schema.py
    │   ├── env.py
    │   └── script.py.mako
    ├── app/
    │   ├── api/
    │   ├── models/
    │   ├── repositories/
    │   ├── schemas/
    │   ├── services/
    │   ├── database.py
    │   └── main.py
    ├── k8s/
    ├── helm/
    ├── tests/
    ├── alembic.ini
    ├── openapi.json
    └── seed.py

## Generated By

ArchitectAI Autonomous Tech Lead.

This backend was generated from natural-language requirements.
"""

        FileWriter.write(
            self.backend_dir / "README.md",
            content,
        )

        print("✅ Generated README.md")

    def generate_manifest(
        self,
        project_name: str,
        blueprint,
    ):
        entities = []

        for entity in blueprint.entities:
            fields = []

            for field in entity.fields:
                fields.append(
                    {
                        "name": field.name,
                        "type": field.type,
                    }
                )

            entities.append(
                {
                    "name": entity.name,
                    "fields": fields,
                }
            )

        relationships = []

        for relation in blueprint.relationships:
            relationships.append(
                {
                    "source": relation.source,
                    "target": relation.target,
                    "relationship_type": (
                        relation.relationship_type
                    ),
                    "foreign_key": relation.foreign_key,
                }
            )

        manifest = {
            "generator": "ArchitectAI",
            "project_name": project_name,
            "backend": "FastAPI",
            "database": "SQLite",
            "entities": entities,
            "relationships": relationships,
        }

        path = (
            self.backend_dir
            / "architectai_manifest.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                manifest,
                indent=4,
            ),
            encoding="utf-8",
        )

        print(
            "✅ Generated architectai_manifest.json"
        )

    @staticmethod
    def sanitize_k8s_name(name: str) -> str:
        """Sanitize a project name for valid Kubernetes DNS-1123 label."""
        import re
        cleaned = "".join(c if c.isalnum() or c in ("-", "_") else "-" for c in name.lower())
        cleaned = cleaned.replace("_", "-")
        cleaned = re.sub(r"-+", "-", cleaned).strip("-")
        return cleaned or "architectai-service"

    def generate_kubernetes_manifests(self, project_name: str, blueprint=None):
        k8s_name = self.sanitize_k8s_name(project_name)
        k8s_dir = self.backend_dir / "k8s"

        deployment_content = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {k8s_name}
  labels:
    app.kubernetes.io/name: {k8s_name}
    app.kubernetes.io/instance: {k8s_name}
    app.kubernetes.io/managed-by: architectai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {k8s_name}
  template:
    metadata:
      labels:
        app: {k8s_name}
    spec:
      containers:
        - name: {k8s_name}
          image: {k8s_name}:latest
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {k8s_name}-config
          livenessProbe:
            httpGet:
              path: /docs
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 20
            timeoutSeconds: 3
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /docs
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 2
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
"""
        FileWriter.write(k8s_dir / "deployment.yaml", deployment_content)

        service_content = f"""apiVersion: v1
kind: Service
metadata:
  name: {k8s_name}-service
  labels:
    app.kubernetes.io/name: {k8s_name}
    app.kubernetes.io/managed-by: architectai
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 8000
      protocol: TCP
  selector:
    app: {k8s_name}
"""
        FileWriter.write(k8s_dir / "service.yaml", service_content)

        configmap_content = f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {k8s_name}-config
  labels:
    app.kubernetes.io/name: {k8s_name}
    app.kubernetes.io/managed-by: architectai
data:
  APP_ENV: "production"
  DEBUG: "False"
  API_HOST: "0.0.0.0"
  API_PORT: "8000"
  DATABASE_URL: "sqlite:////app/data/app.db"
"""
        FileWriter.write(k8s_dir / "configmap.yaml", configmap_content)

        ingress_content = f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {k8s_name}-ingress
  labels:
    app.kubernetes.io/name: {k8s_name}
    app.kubernetes.io/managed-by: architectai
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
    - host: {k8s_name}.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {k8s_name}-service
                port:
                  number: 80
"""
        FileWriter.write(k8s_dir / "ingress.yaml", ingress_content)

        hpa_content = f"""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {k8s_name}-hpa
  labels:
    app.kubernetes.io/name: {k8s_name}
    app.kubernetes.io/managed-by: architectai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {k8s_name}
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
"""
        FileWriter.write(k8s_dir / "hpa.yaml", hpa_content)

        kustomization_content = f"""apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
metadata:
  name: {k8s_name}-kustomization
resources:
  - configmap.yaml
  - deployment.yaml
  - service.yaml
  - ingress.yaml
  - hpa.yaml
"""
        FileWriter.write(k8s_dir / "kustomization.yaml", kustomization_content)
        print("✅ Generated Kubernetes manifests (deployment, service, configmap, ingress, hpa, kustomization)")

    def generate_helm_chart(self, project_name: str, blueprint=None):
        k8s_name = self.sanitize_k8s_name(project_name)
        helm_dir = self.backend_dir / "helm" / k8s_name
        templates_dir = helm_dir / "templates"

        chart_content = f"""apiVersion: v2
name: {k8s_name}
description: Helm chart for {project_name} FastAPI microservice generated by ArchitectAI
type: application
version: 0.1.0
appVersion: "1.0.0"
keywords:
  - fastapi
  - microservice
  - architectai
maintainers:
  - name: ArchitectAI Tech Lead
"""
        FileWriter.write(helm_dir / "Chart.yaml", chart_content)

        values_content = f"""replicaCount: 2

image:
  repository: {k8s_name}
  pullPolicy: IfNotPresent
  tag: "latest"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: false
  name: ""

podAnnotations: {{}}

podSecurityContext: {{}}

securityContext: {{}}

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: false
  className: "nginx"
  annotations: {{}}
  hosts:
    - host: {k8s_name}.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

env:
  APP_ENV: "production"
  DEBUG: "False"
  API_HOST: "0.0.0.0"
  API_PORT: "8000"
  DATABASE_URL: "sqlite:////app/data/app.db"
"""
        FileWriter.write(helm_dir / "values.yaml", values_content)

        helpers_content = f"""{{{{/*
Expand the name of the chart.
*/}}}}
{{{{- define "{k8s_name}.name" -}}}}
{{{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}}}
{{{{- end }}}}

{{{{/*
Create a default fully qualified app name.
*/}}}}
{{{{- define "{k8s_name}.fullname" -}}}}
{{{{- if .Values.fullnameOverride }}}}
{{{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}}}
{{{{- else }}}}
{{{{- $name := default .Chart.Name .Values.nameOverride }}}}
{{{{- if contains $name .Release.Name }}}}
{{{{- .Release.Name | trunc 63 | trimSuffix "-" }}}}
{{{{- else }}}}
{{{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}}}
{{{{- end }}}}
{{{{- end }}}}
{{{{- end }}}}

{{{{/*
Create chart name and version as used by the chart label.
*/}}}}
{{{{- define "{k8s_name}.chart" -}}}}
{{{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}}}
{{{{- end }}}}

{{{{/*
Common labels
*/}}}}
{{{{- define "{k8s_name}.labels" -}}}}
helm.sh/chart: {{{{ include "{k8s_name}.chart" . }}}}
{{{{ include "{k8s_name}.selectorLabels" . }}}}
{{{{- if .Chart.AppVersion }}}}
app.kubernetes.io/version: {{{{ .Chart.AppVersion | quote }}}}
{{{{- end }}}}
app.kubernetes.io/managed-by: {{{{ .Release.Service }}}}
{{{{- end }}}}

{{{{/*
Selector labels
*/}}}}
{{{{- define "{k8s_name}.selectorLabels" -}}}}
app.kubernetes.io/name: {{{{ include "{k8s_name}.name" . }}}}
app.kubernetes.io/instance: {{{{ .Release.Name }}}}
{{{{- end }}}}
"""
        FileWriter.write(templates_dir / "_helpers.tpl", helpers_content)

        tpl_deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{{{ include "{k8s_name}.fullname" . }}}}
  labels:
    {{{{- include "{k8s_name}.labels" . | nindent 4 }}}}
spec:
  {{{{- if not .Values.autoscaling.enabled }}}}
  replicas: {{{{ .Values.replicaCount }}}}
  {{{{- end }}}}
  selector:
    matchLabels:
      {{{{- include "{k8s_name}.selectorLabels" . | nindent 6 }}}}
  template:
    metadata:
      labels:
        {{{{- include "{k8s_name}.selectorLabels" . | nindent 8 }}}}
    spec:
      containers:
        - name: {{{{ .Chart.Name }}}}
          image: "{{{{ .Values.image.repository }}}}:{{{{ .Values.image.tag | default .Chart.AppVersion }}}}"
          imagePullPolicy: {{{{ .Values.image.pullPolicy }}}}
          ports:
            - name: http
              containerPort: {{{{ .Values.service.targetPort }}}}
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {{{{ include "{k8s_name}.fullname" . }}}}-config
          livenessProbe:
            httpGet:
              path: /docs
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /docs
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            {{{{- toYaml .Values.resources | nindent 12 }}}}
"""
        FileWriter.write(templates_dir / "deployment.yaml", tpl_deployment)

        tpl_service = f"""apiVersion: v1
kind: Service
metadata:
  name: {{{{ include "{k8s_name}.fullname" . }}}}
  labels:
    {{{{- include "{k8s_name}.labels" . | nindent 4 }}}}
spec:
  type: {{{{ .Values.service.type }}}}
  ports:
    - port: {{{{ .Values.service.port }}}}
      targetPort: {{{{ .Values.service.targetPort }}}}
      protocol: TCP
      name: http
  selector:
    {{{{- include "{k8s_name}.selectorLabels" . | nindent 4 }}}}
"""
        FileWriter.write(templates_dir / "service.yaml", tpl_service)

        tpl_configmap = f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {{{{ include "{k8s_name}.fullname" . }}}}-config
  labels:
    {{{{- include "{k8s_name}.labels" . | nindent 4 }}}}
data:
  {{{{- range $key, $val := .Values.env }}}}
  {{{{ $key }}}}: {{{{ $val | quote }}}}
  {{{{- end }}}}
"""
        FileWriter.write(templates_dir / "configmap.yaml", tpl_configmap)

        tpl_ingress = f"""{{{{- if .Values.ingress.enabled -}}}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{{{ include "{k8s_name}.fullname" . }}}}
  labels:
    {{{{- include "{k8s_name}.labels" . | nindent 4 }}}}
  {{{{- with .Values.ingress.annotations }}}}
  annotations:
    {{{{- toYaml . | nindent 4 }}}}
  {{{{- end }}}}
spec:
  {{{{- if .Values.ingress.className }}}}
  ingressClassName: {{{{ .Values.ingress.className }}}}
  {{{{- end }}}}
  rules:
    {{{{- range .Values.ingress.hosts }}}}
    - host: {{{{ .host | quote }}}}
      http:
        paths:
          {{{{- range .paths }}}}
          - path: {{{{ .path }}}}
            pathType: {{{{ .pathType }}}}
            backend:
              service:
                name: {{{{ include "{k8s_name}.fullname" $ }}}}
                port:
                  number: {{{{ $.Values.service.port }}}}
          {{{{- end }}}}
    {{{{- end }}}}
{{{{- end }}}}
"""
        FileWriter.write(templates_dir / "ingress.yaml", tpl_ingress)

        tpl_hpa = f"""{{{{- if .Values.autoscaling.enabled -}}}}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{{{ include "{k8s_name}.fullname" . }}}}
  labels:
    {{{{- include "{k8s_name}.labels" . | nindent 4 }}}}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{{{ include "{k8s_name}.fullname" . }}}}
  minReplicas: {{{{ .Values.autoscaling.minReplicas }}}}
  maxReplicas: {{{{ .Values.autoscaling.maxReplicas }}}}
  metrics:
    {{{{- if .Values.autoscaling.targetCPUUtilizationPercentage }}}}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{{{ .Values.autoscaling.targetCPUUtilizationPercentage }}}}
    {{{{- end }}}}
{{{{- end }}}}
"""
        FileWriter.write(templates_dir / "hpa.yaml", tpl_hpa)
        print("✅ Generated Helm chart (Chart.yaml, values.yaml, templates)")

    def generate_e2e_testing_suite(
        self,
        project_name: str,
        blueprint=None,
    ):
        e2e_gen = E2ETestingGenerator(output_dir=str(self.output_dir))
        e2e_gen.generate(
            project_name=project_name,
            blueprint=blueprint,
        )

    def generate(
        self,
        project_name: str,
        blueprint,
    ):
        print("\n" + "=" * 60)
        print("📦 Packaging Generated Project")
        print("=" * 60)

        self.backend_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.generate_requirements()
        self.generate_env_example()
        self.generate_dockerfile()
        self.generate_dockerignore()
        self.generate_gitignore()
        self.generate_pytest_ini()
        self.generate_kubernetes_manifests(
            project_name=project_name,
            blueprint=blueprint,
        )
        self.generate_helm_chart(
            project_name=project_name,
            blueprint=blueprint,
        )
        self.generate_openapi_spec()
        self.generate_alembic_setup(
            project_name=project_name,
            blueprint=blueprint,
        )
        self.generate_database_seeder(
            project_name=project_name,
            blueprint=blueprint,
        )
        self.generate_e2e_testing_suite(
            project_name=project_name,
            blueprint=blueprint,
        )

        self.generate_readme(
            project_name=project_name,
            entities=blueprint.entities,
        )

        self.generate_manifest(
            project_name=project_name,
            blueprint=blueprint,
        )

        print(
            "\n✅ Project packaging completed"
        )
