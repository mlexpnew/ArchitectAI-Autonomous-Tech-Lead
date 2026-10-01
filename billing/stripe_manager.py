"""
ArchitectAI Stripe Billing & Pro Subscriptions Manager

Handles Stripe Checkout sessions, payment links, subscription tiers,
credits tracking, and webhook reconciliation for Pro generation runs.
"""

import os
import json
import uuid
import time
import logging
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, List
from pathlib import Path

try:
    import stripe
except ImportError:
    stripe = None

from auth.models import User
from auth.auth_manager import get_auth_manager
from security_guardrails.guardrail_manager import get_guardrails

logger = logging.getLogger("architectai.billing")


@dataclass
class Plan:
    plan_id: str
    name: str
    amount_cents: int
    display_price: str
    interval: Optional[str]  # "month" or None for one-time
    description: str
    features: List[str]
    is_recurring: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


PLANS = {
    "plan_pro_run": Plan(
        plan_id="plan_pro_run",
        name="⚡ Single Pro Microservice Run",
        amount_cents=1900,
        display_price="$19",
        interval=None,
        description="Single production-grade microservice build with full test suite & Kubernetes manifests.",
        features=[
            "1 Production Microservice Architecture Build",
            "SQLAlchemy 2.0 Models & FastAPI Routers",
            "100% Green Pytest Test Suite",
            "Docker, Kubernetes & Helm Packaging",
            "Interactive Swagger OpenAPI Runner",
        ],
        is_recurring=False,
    ),
    "plan_pro_monthly": Plan(
        plan_id="plan_pro_monthly",
        name="🚀 Architect Pro (Monthly Unlimited)",
        amount_cents=4900,
        display_price="$49/mo",
        interval="month",
        description="Unlimited autonomous tech lead builds, Claude 3.5 Sonnet & GPT-4o, and 1-Click GitHub PRs.",
        features=[
            "Unlimited Microservice Generation Runs",
            "1-Click Automated GitHub / GitLab Pull Requests",
            "Flagship LLM Access (Claude 3.5 Sonnet & GPT-4o)",
            "Self-Healing Code Repair Loop (up to 3 auto-retries)",
            "Unlimited Multi-Tenant Isolated Workspaces",
            "Priority Support & Export Downloads",
        ],
        is_recurring=True,
    ),
    "plan_enterprise": Plan(
        plan_id="plan_enterprise",
        name="🏢 Enterprise SOC2 Compliance Tier",
        amount_cents=49900,
        display_price="$499/mo",
        interval="month",
        description="Institutional-grade security posture, M&A data room export, and air-gapped model hosting.",
        features=[
            "Everything in Pro Unlimited",
            "SOC2 Type II Cryptographic Chained Audit Ledger",
            "M&A Due Diligence Data Room & License IP Audit",
            "Adversarial Prompt Injection Shield & PII Redactor",
            "Air-Gapped Offline Local LLM Support (Ollama)",
            "Dedicated Support Architect & SLA",
        ],
        is_recurring=True,
    ),
}


class StripeManager:
    """Manages Stripe Checkout Sessions, payment links, and plan subscriptions."""

    def __init__(self, api_key: Optional[str] = None, auth_manager: Optional[Any] = None):
        self.api_key = api_key or os.getenv("STRIPE_API_KEY", "")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
        self.auth_manager = auth_manager
        self.is_live = bool(self.api_key and stripe and not self.api_key.startswith("mock_"))
        
        if self.is_live and stripe:
            stripe.api_key = self.api_key

    def get_plans(self) -> Dict[str, Plan]:
        return PLANS

    def get_plan(self, plan_id: str) -> Optional[Plan]:
        return PLANS.get(plan_id)

    def create_checkout_session(
        self,
        user_id: str,
        user_email: str,
        plan_id: str = "plan_pro_monthly",
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> Dict:
        """
        Creates a Stripe Checkout Session or returns a deterministic sandbox payment link.
        """
        plan = self.get_plan(plan_id) or PLANS["plan_pro_monthly"]

        default_success = "http://localhost:8501/?payment_status=success&plan_id=" + plan.plan_id
        default_cancel = "http://localhost:8501/?payment_status=cancelled"
        
        target_success = success_url or default_success
        target_cancel = cancel_url or default_cancel

        # 1. Live Stripe Checkout Session
        if self.is_live and stripe:
            try:
                line_item = {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"ArchitectAI · {plan.name}",
                            "description": plan.description,
                        },
                        "unit_amount": plan.amount_cents,
                    },
                    "quantity": 1,
                }
                if plan.is_recurring:
                    line_item["price_data"]["recurring"] = {"interval": plan.interval or "month"}

                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[line_item],
                    mode="subscription" if plan.is_recurring else "payment",
                    success_url=target_success + "&session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=target_cancel,
                    customer_email=user_email,
                    client_reference_id=user_id,
                    metadata={"user_id": user_id, "plan_id": plan_id},
                )

                logger.info(f"Created Stripe checkout session: {session.id} for user {user_id}")
                return {
                    "success": True,
                    "mode": "live",
                    "checkout_url": session.url,
                    "session_id": session.id,
                    "plan": plan.to_dict(),
                }
            except Exception as e:
                logger.warning(f"Stripe API call failed ({e}). Falling back to Sandbox Payment Link.")

        # 2. High-Fidelity Sandbox / Demo Simulation Payment Link
        mock_session_id = f"cs_test_mock_{uuid.uuid4().hex[:16]}"
        simulated_payment_link = (
            f"http://localhost:8501/?payment_status=success&session_id={mock_session_id}&plan_id={plan.plan_id}"
        )

        return {
            "success": True,
            "mode": "sandbox",
            "checkout_url": simulated_payment_link,
            "session_id": mock_session_id,
            "plan": plan.to_dict(),
            "message": "Stripe Sandbox Checkout Link Ready",
        }

    def process_successful_payment(
        self,
        user_id: str,
        plan_id: str,
        transaction_id: str,
    ) -> Optional[User]:
        """
        Activates user subscription or credits after a verified Stripe payment.
        """
        auth_mgr = self.auth_manager or get_auth_manager()
        user = auth_mgr.get_user_by_id(user_id)
        if not user:
            logger.error(f"User {user_id} not found for payment {transaction_id}")
            return None

        plan = self.get_plan(plan_id) or PLANS["plan_pro_monthly"]

        if plan_id == "plan_pro_run":
            user.credits_remaining += 1
            if user.tier == "Starter":
                user.tier = "Pro Run"
        elif plan_id == "plan_pro_monthly":
            user.tier = "Pro"
            user.credits_remaining = 999999
        elif plan_id == "plan_enterprise":
            user.tier = "Enterprise"
            user.credits_remaining = 999999

        user.stripe_subscription_id = transaction_id
        auth_mgr.save_users()

        # Cryptographically log payment event in SOC2 audit ledger
        try:
            guardrails = get_guardrails()
            guardrails.audit_logger.log_event(
                event_type="STRIPE_PAYMENT_PROCESSED",
                actor_role=user.role,
                action=f"Upgraded to {plan.name} (${plan.amount_cents / 100:.2f})",
                status="SUCCESS",
                metadata={
                    "user_id": user_id,
                    "plan_id": plan_id,
                    "transaction_id": transaction_id,
                    "new_tier": user.tier,
                },
            )
        except Exception as e:
            logger.debug(f"Audit log failed for payment: {e}")

        logger.info(f"Successfully upgraded user {user.email} to {user.tier}")
        return user

    def check_user_generation_credits(self, user: User) -> Dict:
        """
        Validates if a user has sufficient credits or active Pro tier to generate a microservice.
        """
        if user.tier in ("Pro", "Enterprise"):
            return {
                "can_generate": True,
                "tier": user.tier,
                "is_unlimited": True,
                "credits_remaining": 999999,
                "badge": "⭐ PRO UNLIMITED",
            }
        
        runs_left = max(0, user.credits_remaining)
        can_run = runs_left > 0

        return {
            "can_generate": can_run,
            "tier": user.tier,
            "is_unlimited": False,
            "credits_remaining": runs_left,
            "badge": f"⚡ {runs_left} Runs Left" if can_run else "⚠️ 0 Runs Left",
        }

    def consume_generation_credit(self, user_id: str) -> bool:
        """Deducts one generation credit if not on an unlimited plan."""
        auth_mgr = self.auth_manager or get_auth_manager()
        user = auth_mgr.get_user_by_id(user_id)
        if not user:
            return False

        if user.tier in ("Pro", "Enterprise"):
            return True

        if user.credits_remaining > 0:
            user.credits_remaining -= 1
            auth_mgr.save_users()
            return True

        return False


_stripe_manager: Optional[StripeManager] = None


def get_stripe_manager() -> StripeManager:
    global _stripe_manager
    if _stripe_manager is None:
        _stripe_manager = StripeManager()
    return _stripe_manager
