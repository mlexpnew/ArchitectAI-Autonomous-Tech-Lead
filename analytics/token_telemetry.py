"""
ArchitectAI Token Telemetry & LLM Unit Economics Engine

Tracks real-time token usage (prompt, completion, total), calculates exact run
costs ($/run) across supported models (Claude 3.5 Sonnet, GPT-4o, Gemini Flash, Ollama, Groq),
and generates multi-model unit economic comparisons for enterprise decision makers.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import time
from typing import Any

from config.settings import settings


# ==============================================================================
# Model Pricing Catalog (Rates per 1,000,000 tokens in USD)
# ==============================================================================
MODEL_PRICING: dict[str, dict[str, Any]] = {
    # Anthropic
    "claude-3-5-sonnet-20241022": {
        "display_name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "input_per_m": 3.00,
        "output_per_m": 15.00,
        "tier": "Flagship Reasoning",
        "icon": "🟣",
        "context_window": "200k",
    },
    "claude-3-5-sonnet": {
        "display_name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "input_per_m": 3.00,
        "output_per_m": 15.00,
        "tier": "Flagship Reasoning",
        "icon": "🟣",
        "context_window": "200k",
    },
    # OpenAI
    "gpt-4o": {
        "display_name": "GPT-4o",
        "provider": "OpenAI",
        "input_per_m": 2.50,
        "output_per_m": 10.00,
        "tier": "Flagship Multimodal",
        "icon": "🟢",
        "context_window": "128k",
    },
    "gpt-4o-mini": {
        "display_name": "GPT-4o mini",
        "provider": "OpenAI",
        "input_per_m": 0.15,
        "output_per_m": 0.60,
        "tier": "Lightweight Fast",
        "icon": "🟢",
        "context_window": "128k",
    },
    # Google Gemini
    "gemini-2.5-flash": {
        "display_name": "Gemini 2.5 Flash",
        "provider": "Google",
        "input_per_m": 0.075,
        "output_per_m": 0.30,
        "tier": "Cost-Optimized",
        "icon": "⚡",
        "context_window": "1M",
    },
    "gemini-1.5-flash": {
        "display_name": "Gemini 1.5 Flash",
        "provider": "Google",
        "input_per_m": 0.075,
        "output_per_m": 0.30,
        "tier": "Cost-Optimized",
        "icon": "⚡",
        "context_window": "1M",
    },
    # Groq LPU
    "qwen/qwen3.8-27b": {
        "display_name": "Groq Qwen 3.8",
        "provider": "Groq LPU",
        "input_per_m": 0.59,
        "output_per_m": 0.79,
        "tier": "Ultra-Low Latency",
        "icon": "🚀",
        "context_window": "32k",
    },
    "llama-3.3-70b-versatile": {
        "display_name": "Groq Llama 3.3 70B",
        "provider": "Groq LPU",
        "input_per_m": 0.59,
        "output_per_m": 0.79,
        "tier": "High Velocity",
        "icon": "🚀",
        "context_window": "128k",
    },
    # Ollama (Local / Air-Gapped)
    "ollama": {
        "display_name": "Ollama Local (Llama 3.2)",
        "provider": "Ollama (Local)",
        "input_per_m": 0.00,
        "output_per_m": 0.00,
        "tier": "Air-Gapped & Free",
        "icon": "🦙",
        "context_window": "128k",
    },
    "llama3.2": {
        "display_name": "Ollama Llama 3.2",
        "provider": "Ollama (Local)",
        "input_per_m": 0.00,
        "output_per_m": 0.00,
        "tier": "Air-Gapped & Free",
        "icon": "🦙",
        "context_window": "128k",
    },
}

# Standard models compared on enterprise dashboard
BENCHMARK_ROUTER_MODELS = [
    "claude-3-5-sonnet-20241022",
    "gpt-4o",
    "gemini-2.5-flash",
    "ollama",
    "qwen/qwen3.8-27b",
]

DEFAULT_FALLBACK_PRICING = {
    "display_name": "Generic LLM",
    "provider": "Custom",
    "input_per_m": 1.00,
    "output_per_m": 3.00,
    "tier": "Standard",
    "icon": "⚙️",
    "context_window": "32k",
}


def get_model_pricing(model_name: str | None) -> dict[str, Any]:
    """
    Returns pricing specs for a given model string with resilient fallback matching.
    """
    if not model_name:
        return DEFAULT_FALLBACK_PRICING

    clean_name = model_name.strip().lower()

    # Exact match
    if clean_name in MODEL_PRICING:
        return MODEL_PRICING[clean_name]

    # Strip prefixes like "openai/", "anthropic/", "ollama/"
    if "/" in clean_name:
        short_name = clean_name.split("/", 1)[1]
        if short_name in MODEL_PRICING:
            return MODEL_PRICING[short_name]

    # Substring heuristics
    if "claude" in clean_name or "sonnet" in clean_name:
        return MODEL_PRICING["claude-3-5-sonnet-20241022"]
    if "gpt-4o-mini" in clean_name:
        return MODEL_PRICING["gpt-4o-mini"]
    if "gpt-4o" in clean_name or "gpt-4" in clean_name:
        return MODEL_PRICING["gpt-4o"]
    if "gemini" in clean_name or "flash" in clean_name:
        return MODEL_PRICING["gemini-2.5-flash"]
    if "ollama" in clean_name or "llama3" in clean_name or "local" in clean_name:
        return MODEL_PRICING["ollama"]
    if "groq" in clean_name or "qwen" in clean_name:
        return MODEL_PRICING["qwen/qwen3.8-27b"]

    return DEFAULT_FALLBACK_PRICING


def estimate_tokens_from_text(text: str | None) -> int:
    """
    High-fidelity token estimation based on character and word heuristics
    aligned with standard BPE tokenizers (1 token ≈ 4 characters / 0.75 words).
    """
    if not text:
        return 0
    cleaned = text.strip()
    if not cleaned:
        return 0
    # Average of char-based (len / 3.8) and word-based (words * 1.33)
    char_est = len(cleaned) / 3.8
    word_est = len(cleaned.split()) * 1.33
    est = int((char_est + word_est) / 2)
    return max(1, est)


# ==============================================================================
# Telemetry Step & Tracker
# ==============================================================================

@dataclass
class TelemetryStep:
    """Records token usage and unit economics for an individual stage."""
    name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    model_name: str
    cost_usd: float
    duration_seconds: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TokenTelemetry:
    """
    Production telemetry engine capturing prompt/completion counters,
    run costs, and multi-model economic analysis.
    """

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.get_active_model()
        self.steps: list[TelemetryStep] = []
        self._start_time = time.perf_counter()

    def record_step(
        self,
        name: str,
        prompt_tokens: int,
        completion_tokens: int,
        model_name: str | None = None,
        duration_seconds: float = 0.0,
    ) -> TelemetryStep:
        """
        Record exact token counts for a step.
        """
        active_model = model_name or self.model_name
        pricing = get_model_pricing(active_model)

        prompt_cost = (prompt_tokens / 1_000_000) * pricing["input_per_m"]
        completion_cost = (completion_tokens / 1_000_000) * pricing["output_per_m"]
        cost_usd = round(prompt_cost + completion_cost, 6)

        total_tokens = prompt_tokens + completion_tokens

        step = TelemetryStep(
            name=name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            model_name=active_model,
            cost_usd=cost_usd,
            duration_seconds=round(duration_seconds, 2),
        )
        self.steps.append(step)
        return step

    def record_text(
        self,
        name: str,
        prompt_text: str | None,
        completion_text: str | None,
        model_name: str | None = None,
        duration_seconds: float = 0.0,
    ) -> TelemetryStep:
        """
        Estimate tokens from input and output strings, and record the step.
        """
        prompt_tokens = estimate_tokens_from_text(prompt_text)
        completion_tokens = estimate_tokens_from_text(completion_text)
        return self.record_step(
            name=name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model_name=model_name,
            duration_seconds=duration_seconds,
        )

    @property
    def total_prompt_tokens(self) -> int:
        return sum(s.prompt_tokens for s in self.steps)

    @property
    def total_completion_tokens(self) -> int:
        return sum(s.completion_tokens for s in self.steps)

    @property
    def total_tokens(self) -> int:
        return sum(s.total_tokens for s in self.steps)

    @property
    def total_cost_usd(self) -> float:
        return round(sum(s.cost_usd for s in self.steps), 6)

    @property
    def total_duration_seconds(self) -> float:
        return round(time.perf_counter() - self._start_time, 2)

    def calculate_cost_for_model(
        self,
        target_model: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
    ) -> float:
        """
        Calculates what the run (or given tokens) would cost on a specific target model.
        """
        p_tokens = self.total_prompt_tokens if prompt_tokens is None else prompt_tokens
        c_tokens = self.total_completion_tokens if completion_tokens is None else completion_tokens

        pricing = get_model_pricing(target_model)
        cost = (p_tokens / 1_000_000) * pricing["input_per_m"] + (
            c_tokens / 1_000_000
        ) * pricing["output_per_m"]
        return round(cost, 6)

    def get_model_comparison(self) -> dict[str, dict[str, Any]]:
        """
        Generates cross-model cost comparison for the current run across top providers.
        """
        p_tokens = self.total_prompt_tokens
        c_tokens = self.total_completion_tokens

        claude_cost = self.calculate_cost_for_model("claude-3-5-sonnet-20241022", p_tokens, c_tokens)

        comparison = {}
        for m_key in BENCHMARK_ROUTER_MODELS:
            pricing = get_model_pricing(m_key)
            cost = self.calculate_cost_for_model(m_key, p_tokens, c_tokens)

            # Savings vs Claude 3.5 Sonnet flagship baseline
            if claude_cost > 0:
                savings_pct = round(((claude_cost - cost) / claude_cost) * 100, 1)
            else:
                savings_pct = 0.0

            comparison[m_key] = {
                "display_name": pricing["display_name"],
                "provider": pricing["provider"],
                "tier": pricing["tier"],
                "icon": pricing["icon"],
                "cost_usd": cost,
                "input_rate": f"${pricing['input_per_m']:.3f}/1M",
                "output_rate": f"${pricing['output_per_m']:.3f}/1M",
                "savings_vs_claude_percent": savings_pct,
                "is_current": (
                    m_key == self.model_name
                    or pricing["display_name"].lower() in self.model_name.lower()
                ),
            }

        return comparison

    def get_unit_economics_summary(self) -> dict[str, Any]:
        """
        Full unit economics and telemetry summary suitable for UI and JSON reports.
        """
        active_pricing = get_model_pricing(self.model_name)
        total_p = self.total_prompt_tokens
        total_c = self.total_completion_tokens
        total_tok = self.total_tokens
        cost_usd = self.total_cost_usd

        cost_per_1k = round((cost_usd / max(total_tok, 1)) * 1000, 6)

        return {
            "model_name": self.model_name,
            "display_name": active_pricing["display_name"],
            "provider": active_pricing["provider"],
            "tier": active_pricing["tier"],
            "icon": active_pricing["icon"],
            "prompt_tokens": total_p,
            "completion_tokens": total_c,
            "total_tokens": total_tok,
            "cost_usd": cost_usd,
            "cost_per_1k_tokens": cost_per_1k,
            "duration_seconds": self.total_duration_seconds,
            "step_count": len(self.steps),
            "steps": [s.to_dict() for s in self.steps],
            "model_comparison": self.get_model_comparison(),
        }


# ==============================================================================
# Global Active Telemetry Context (Singleton for concurrent stages)
# ==============================================================================

_ACTIVE_TELEMETRY: TokenTelemetry | None = None


def get_active_telemetry() -> TokenTelemetry | None:
    return _ACTIVE_TELEMETRY


def set_active_telemetry(telemetry: TokenTelemetry | None) -> None:
    global _ACTIVE_TELEMETRY
    _ACTIVE_TELEMETRY = telemetry
