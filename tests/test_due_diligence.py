"""
Unit tests for Due Diligence Package: Benchmark Suite, License Compliance Audit, and Data Room.
"""

from pathlib import Path
import zipfile
import pytest

from due_diligence.license_audit import LicenseComplianceAuditor, run_license_audit_and_export
from due_diligence.benchmark_suite import BenchmarkSuite, BENCHMARK_DOMAINS
from due_diligence.data_room_generator import DueDiligencePackager
from config.settings import settings


def test_license_compliance_audit():
    auditor = LicenseComplianceAuditor()
    summary = auditor.run_audit()

    assert summary["target_system"] == "ArchitectAI - Autonomous Tech Lead"
    assert summary["total_dependencies_audited"] > 10
    assert summary["permissive_count"] > 10
    # ZERO viral copyleft licenses (GPL/AGPL)
    assert summary["viral_copyleft_count"] == 0
    assert summary["ip_compliance_status"] == "APPROVED_FOR_COMMERCIAL_ACQUISITION"
    assert "AAA" in summary["ip_clearance_rating"]

    # Verify SBOM format
    sbom = summary["sbom"]
    assert sbom["bomFormat"] == "CycloneDX-compatible"
    assert len(sbom["components"]) > 10
    for comp in sbom["components"]:
        assert comp["commercial_safe"] is True
        assert comp["license"] in ["MIT", "Apache-2.0", "BSD-3-Clause", "BSD", "Permissive (Commercial)"]


def test_license_audit_markdown_generation(tmp_path):
    report_res = run_license_audit_and_export(output_dir=str(tmp_path))
    assert Path(report_res["json_path"]).exists()
    assert Path(report_res["sbom_path"]).exists()
    assert Path(report_res["markdown_path"]).exists()

    md_text = Path(report_res["markdown_path"]).read_text(encoding="utf-8")
    assert "ArchitectAI Intellectual Property & License Compliance Audit Report" in md_text
    assert "ZERO contamination" in md_text
    assert "Software Bill of Materials (SBOM)" in md_text


def test_benchmark_suite_single_domain(tmp_path):
    settings.MOCK_LLM = True
    suite = BenchmarkSuite(output_root=str(tmp_path / "benchmarks"))
    dom = BENCHMARK_DOMAINS[0]  # Healthcare

    res = suite.run_benchmark_for_domain(dom)
    assert res.domain == dom["domain"]
    assert res.generation_time_seconds > 0.0
    assert res.entities_generated >= 2
    assert res.python_files_count >= 8
    assert res.lines_of_code > 200
    assert res.syntax_pass_rate == 100.0
    assert res.test_pass_rate == 100.0
    assert res.cost_gemini_flash > 0.0
    assert res.cost_claude_35 > res.cost_gemini_flash
    assert res.cost_ollama_local == 0.0


def test_benchmark_suite_aggregation(tmp_path):
    settings.MOCK_LLM = True
    suite = BenchmarkSuite(output_root=str(tmp_path / "benchmarks"))
    summary = suite.run_full_suite(limit=2)

    assert summary["total_domains_tested"] == 2
    assert "latency" in summary
    assert summary["latency"]["average_seconds"] > 0
    assert summary["quality"]["syntax_validity_percent"] == 100.0
    assert summary["quality"]["test_pass_rate_percent"] == 100.0
    assert summary["unit_economics"]["gemini_cost_reduction_vs_claude_percent"] > 90.0

    # Markdown generation
    md_content = suite.generate_markdown_report(summary)
    assert "# ArchitectAI Automated System Performance & Quality Benchmark Report" in md_content
    assert "Executive Performance & SLA Scorecard" in md_content


def test_due_diligence_data_room_packager(tmp_path):
    settings.MOCK_LLM = True
    packager = DueDiligencePackager(output_dir=str(tmp_path / "due_diligence"))

    # Build package with quick benchmark
    res = packager.build_package(run_benchmarks=False)

    zip_file = Path(res["zip_path"])
    assert zip_file.exists()
    assert zip_file.stat().st_size > 500

    # Inspect zip contents
    with zipfile.ZipFile(zip_file, "r") as z:
        names = z.namelist()
        assert any("EXECUTIVE_SYSTEM_ARCHITECTURE_WHITEPAPER.md" in n for n in names)
        assert any("LICENSE_COMPLIANCE_AUDIT.md" in n for n in names)
        assert any("sbom.json" in n for n in names)
        assert any("DATA_ROOM_INDEX.json" in n for n in names)
