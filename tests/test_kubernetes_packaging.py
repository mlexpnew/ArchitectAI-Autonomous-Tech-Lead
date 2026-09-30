"""
Tests for Kubernetes and Helm manifest generation in ProjectPackagingGenerator.
"""

import tempfile
import yaml
from pathlib import Path
from unittest.mock import MagicMock

from generators.project_packaging_generator import ProjectPackagingGenerator


def test_sanitize_k8s_name():
    assert ProjectPackagingGenerator.sanitize_k8s_name("Library Management System") == "library-management-system"
    assert ProjectPackagingGenerator.sanitize_k8s_name("E-Commerce_Store_v2!") == "e-commerce-store-v2"
    assert ProjectPackagingGenerator.sanitize_k8s_name("---patient---service---") == "patient-service"
    assert ProjectPackagingGenerator.sanitize_k8s_name("") == "architectai-service"


def test_generate_kubernetes_manifests():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = ProjectPackagingGenerator(output_dir=tmpdir)
        gen.generate_kubernetes_manifests(project_name="Order Tracking Service")

        k8s_dir = Path(tmpdir) / "backend" / "k8s"
        assert k8s_dir.exists()

        expected_files = [
            "deployment.yaml",
            "service.yaml",
            "configmap.yaml",
            "ingress.yaml",
            "hpa.yaml",
            "kustomization.yaml",
        ]

        for fname in expected_files:
            fpath = k8s_dir / fname
            assert fpath.exists(), f"Missing expected K8s file: {fname}"
            # Verify YAML syntax validity
            parsed = yaml.safe_load(fpath.read_text(encoding="utf-8"))
            assert parsed is not None

        # Verify deployment specifics
        dep = yaml.safe_load((k8s_dir / "deployment.yaml").read_text(encoding="utf-8"))
        assert dep["kind"] == "Deployment"
        assert dep["metadata"]["name"] == "order-tracking-service"
        assert dep["spec"]["replicas"] == 2
        container = dep["spec"]["template"]["spec"]["containers"][0]
        assert container["ports"][0]["containerPort"] == 8000
        assert "livenessProbe" in container
        assert "readinessProbe" in container
        assert "resources" in container

        # Verify service specifics
        svc = yaml.safe_load((k8s_dir / "service.yaml").read_text(encoding="utf-8"))
        assert svc["kind"] == "Service"
        assert svc["metadata"]["name"] == "order-tracking-service-service"
        assert svc["spec"]["ports"][0]["port"] == 80
        assert svc["spec"]["ports"][0]["targetPort"] == 8000


def test_generate_helm_chart():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = ProjectPackagingGenerator(output_dir=tmpdir)
        gen.generate_helm_chart(project_name="Inventory API")

        helm_dir = Path(tmpdir) / "backend" / "helm" / "inventory-api"
        assert helm_dir.exists()

        chart_yaml = yaml.safe_load((helm_dir / "Chart.yaml").read_text(encoding="utf-8"))
        assert chart_yaml["name"] == "inventory-api"
        assert chart_yaml["apiVersion"] == "v2"
        assert chart_yaml["type"] == "application"

        values_yaml = yaml.safe_load((helm_dir / "values.yaml").read_text(encoding="utf-8"))
        assert values_yaml["replicaCount"] == 2
        assert values_yaml["service"]["port"] == 80
        assert values_yaml["service"]["targetPort"] == 8000
        assert values_yaml["autoscaling"]["enabled"] is True

        templates_dir = helm_dir / "templates"
        assert (templates_dir / "_helpers.tpl").exists()
        assert (templates_dir / "deployment.yaml").exists()
        assert (templates_dir / "service.yaml").exists()
        assert (templates_dir / "configmap.yaml").exists()
        assert (templates_dir / "ingress.yaml").exists()
        assert (templates_dir / "hpa.yaml").exists()


def test_packaging_generator_end_to_end():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = ProjectPackagingGenerator(output_dir=tmpdir)
        mock_blueprint = MagicMock()
        mock_blueprint.entities = []
        mock_blueprint.relationships = []

        gen.generate(project_name="Hospital Service", blueprint=mock_blueprint)

        backend_dir = Path(tmpdir) / "backend"
        assert (backend_dir / "requirements.txt").exists()
        assert (backend_dir / ".env.example").exists()
        assert (backend_dir / "Dockerfile").exists()
        assert (backend_dir / ".dockerignore").exists()
        assert (backend_dir / ".gitignore").exists()
        assert (backend_dir / "README.md").exists()
        assert (backend_dir / "pytest.ini").exists()
        assert (backend_dir / "architectai_manifest.json").exists()
        assert (backend_dir / "k8s" / "deployment.yaml").exists()
        assert (backend_dir / "helm" / "hospital-service" / "Chart.yaml").exists()
