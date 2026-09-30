"""
Unit tests for Token Telemetry, Multi-Model Router, and LLM Unit Economics.
"""

import pytest
from analytics.token_telemetry import (
    MODEL_PRICING,
    TokenTelemetry,
    get_model_pricing,
    estimate_tokens_from_text,
    get_active_telemetry,
    set_active_telemetry,
)
from config.settings import settings
from config.llm import get_available_router_models


def test_model_pricing_lookup_and_heuristics():
    # Exact lookup
    claude = get_model_pricing("claude-3-5-sonnet-20241022")
    assert claude["provider"] == "Anthropic"
    assert claude["input_per_m"] == 3.00
    assert claude["output_per_m"] == 15.00

    # Substring heuristics
    gpt = get_model_pricing("openai/gpt-4o")
    assert gpt["provider"] == "OpenAI"
    assert gpt["input_per_m"] == 2.50
    assert gpt["output_per_m"] == 10.00

    gemini = get_model_pricing("gemini-2.5-flash")
    assert gemini["provider"] == "Google"
    assert gemini["input_per_m"] == 0.075
    assert gemini["output_per_m"] == 0.30

    ollama = get_model_pricing("ollama/llama3.2")
    assert ollama["provider"] == "Ollama (Local)"
    assert ollama["input_per_m"] == 0.00
    assert ollama["output_per_m"] == 0.00

    groq = get_model_pricing("qwen/qwen3.8-27b")
    assert groq["provider"] == "Groq LPU"
    assert groq["input_per_m"] == 0.59


def test_token_estimation_from_text():
    empty_est = estimate_tokens_from_text("")
    assert empty_est == 0

    none_est = estimate_tokens_from_text(None)
    assert none_est == 0

    sample = "def calculate_price(quantity: int, unit_price: float) -> float:\n    return quantity * unit_price"
    est = estimate_tokens_from_text(sample)
    assert est > 0
    # ~95 characters -> ~20-30 tokens
    assert 15 <= est <= 35


def test_telemetry_recording_and_cost_calculation():
    telemetry = TokenTelemetry(model_name="claude-3-5-sonnet-20241022")

    # Record 10,000 prompt tokens and 2,000 completion tokens
    # Claude rate: $3.00/1M prompt + $15.00/1M completion
    # Expected: (10,000 / 1M) * 3 + (2,000 / 1M) * 15 = 0.030 + 0.030 = $0.060
    step = telemetry.record_step(
        name="Backend Generation",
        prompt_tokens=10_000,
        completion_tokens=2_000,
        duration_seconds=1.5,
    )

    assert step.total_tokens == 12_000
    assert abs(step.cost_usd - 0.060) < 1e-4

    assert telemetry.total_prompt_tokens == 10_000
    assert telemetry.total_completion_tokens == 2_000
    assert telemetry.total_tokens == 12_000
    assert abs(telemetry.total_cost_usd - 0.060) < 1e-4


def test_telemetry_ollama_zero_cost():
    telemetry = TokenTelemetry(model_name="ollama")
    step = telemetry.record_step(
        name="Local Execution",
        prompt_tokens=50_000,
        completion_tokens=25_000,
        duration_seconds=5.0,
    )
    assert step.cost_usd == 0.0
    assert telemetry.total_cost_usd == 0.0


def test_multi_model_cost_comparison():
    telemetry = TokenTelemetry(model_name="gemini-2.5-flash")
    telemetry.record_step(
        name="Stage 1",
        prompt_tokens=100_000,
        completion_tokens=50_000,
    )

    comparison = telemetry.get_model_comparison()
    assert "claude-3-5-sonnet-20241022" in comparison
    assert "gpt-4o" in comparison
    assert "gemini-2.5-flash" in comparison
    assert "ollama" in comparison

    # Ollama cost must be 0
    assert comparison["ollama"]["cost_usd"] == 0.0
    assert comparison["ollama"]["savings_vs_claude_percent"] == 100.0

    # Gemini cost vs Claude cost
    claude_cost = comparison["claude-3-5-sonnet-20241022"]["cost_usd"]
    gemini_cost = comparison["gemini-2.5-flash"]["cost_usd"]
    assert claude_cost > gemini_cost
    assert comparison["gemini-2.5-flash"]["savings_vs_claude_percent"] > 90.0


def test_active_telemetry_singleton_context():
    set_active_telemetry(None)
    assert get_active_telemetry() is None

    t = TokenTelemetry()
    set_active_telemetry(t)
    assert get_active_telemetry() is t

    set_active_telemetry(None)
    assert get_active_telemetry() is None


def test_settings_switch_model_router():
    s = settings

    # Switch to Claude
    s.switch_model("claude-3-5-sonnet")
    assert s.LLM_PROVIDER == "anthropic"
    assert s.ANTHROPIC_MODEL == "claude-3-5-sonnet-20241022"
    assert s.get_active_model() == "claude-3-5-sonnet-20241022"

    # Switch to GPT-4o
    s.switch_model("gpt-4o")
    assert s.LLM_PROVIDER == "openai"
    assert s.OPENAI_MODEL == "gpt-4o"

    # Switch to Gemini Flash
    s.switch_model("gemini-2.5-flash")
    assert s.LLM_PROVIDER == "gemini"
    assert s.GEMINI_MODEL == "gemini-2.5-flash"

    # Switch to Ollama
    s.switch_model("ollama")
    assert s.LLM_PROVIDER == "ollama"
    assert s.OLLAMA_MODEL == "llama3.2"

    # Switch to Groq
    s.switch_model("qwen/qwen3.8-27b")
    assert s.LLM_PROVIDER == "groq"
    assert s.GROQ_MODEL == "qwen/qwen3.8-27b"


def test_available_router_models_catalog():
    models = get_available_router_models()
    assert len(models) >= 4
    model_ids = [m["id"] for m in models]
    assert "claude-3-5-sonnet-20241022" in model_ids
    assert "gpt-4o" in model_ids
    assert "gemini-2.5-flash" in model_ids
    assert "ollama" in model_ids


def test_pipeline_generates_telemetry(tmp_path):
    import json
    from orchestration.architect_pipeline import ArchitectPipeline

    out_dir = tmp_path / "telemetry_test_project"
    pipeline = ArchitectPipeline(output_dir=str(out_dir))

    settings.MOCK_LLM = True
    result = pipeline.generate(
        requirements="Build a simple Todo service with User and Task entities.",
        project_name="TodoApp",
    )

    assert "telemetry" in result
    telemetry = result["telemetry"]
    assert telemetry["prompt_tokens"] > 0
    assert telemetry["completion_tokens"] > 0
    assert telemetry["total_tokens"] > 0
    assert telemetry["cost_usd"] >= 0.0
    assert "model_comparison" in telemetry
    assert len(telemetry["steps"]) >= 1

    # Verify generation_report.json has telemetry persisted
    report_file = out_dir / "exports" / "generation_report.json"
    assert report_file.exists()
    report_data = json.loads(report_file.read_text(encoding="utf-8"))
    assert "telemetry" in report_data
    assert report_data["telemetry"]["total_tokens"] == telemetry["total_tokens"]
