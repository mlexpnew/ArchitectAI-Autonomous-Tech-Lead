"""
Unit & Integration Tests for Stripe Billing, Pro Payment Links, and Clerk/Supabase Auth.
"""

import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from auth.auth_manager import AuthManager
from auth.workspace_manager import WorkspaceManager
from auth.clerk_supabase_integration import FederatedAuthProvider
from billing.stripe_manager import StripeManager, PLANS
from api_server import app


@pytest.fixture
def temp_billing_env():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        users_file = tmp_path / "users.json"
        workspaces_file = tmp_path / "workspaces.json"
        base_dir = tmp_path / "outputs" / "workspaces"

        wm = WorkspaceManager(workspaces_file=workspaces_file, base_dir=base_dir)
        am = AuthManager(users_file=users_file, workspace_manager=wm)
        sm = StripeManager(api_key="mock_test_key", auth_manager=am)

        yield am, wm, sm, tmp_path


def test_plans_catalog(temp_billing_env):
    _, _, sm, _ = temp_billing_env
    plans = sm.get_plans()
    assert "plan_pro_run" in plans
    assert "plan_pro_monthly" in plans
    assert "plan_enterprise" in plans

    pro = plans["plan_pro_monthly"]
    assert pro.amount_cents == 4900
    assert pro.display_price == "$49/mo"
    assert pro.is_recurring is True


def test_create_checkout_session_sandbox(temp_billing_env):
    _, _, sm, _ = temp_billing_env
    session = sm.create_checkout_session(
        user_id="usr_test_123",
        user_email="test@startup.io",
        plan_id="plan_pro_monthly",
    )
    assert session["success"] is True
    assert "checkout_url" in session
    assert session["mode"] == "sandbox"
    assert "plan" in session
    assert session["plan"]["plan_id"] == "plan_pro_monthly"


def test_process_payment_and_upgrade_tier(temp_billing_env):
    am, _, sm, _ = temp_billing_env
    # Create user
    user = am.register_user(
        email="buyer@saas.com",
        password="secretpassword",
        name="Sarah Buyer",
    )
    assert user.tier == "Starter"
    assert user.credits_remaining == 3

    # Process Pro Monthly Payment
    upgraded = sm.process_successful_payment(
        user_id=user.user_id,
        plan_id="plan_pro_monthly",
        transaction_id="txn_stripe_success_999",
    )
    assert upgraded is not None
    assert upgraded.tier == "Pro"
    assert upgraded.credits_remaining == 999999
    assert upgraded.stripe_subscription_id == "txn_stripe_success_999"

    # Verify credits check
    cred_check = sm.check_user_generation_credits(upgraded)
    assert cred_check["can_generate"] is True
    assert cred_check["is_unlimited"] is True


def test_credit_consumption_flow(temp_billing_env):
    am, _, sm, _ = temp_billing_env
    user = am.register_user(
        email="freeuser@company.com",
        password="password123",
        name="Free User",
    )
    assert user.credits_remaining == 3

    # Consume 1 run
    consumed = sm.consume_generation_credit(user.user_id)
    assert consumed is True
    u_after = am.get_user_by_id(user.user_id)
    assert u_after.credits_remaining == 2

    # Consume remaining
    sm.consume_generation_credit(user.user_id)
    sm.consume_generation_credit(user.user_id)
    u_zero = am.get_user_by_id(user.user_id)
    assert u_zero.credits_remaining == 0

    # 4th run must fail
    assert sm.consume_generation_credit(user.user_id) is False
    check_exhausted = sm.check_user_generation_credits(u_zero)
    assert check_exhausted["can_generate"] is False


def test_clerk_supabase_federated_auth():
    provider = FederatedAuthProvider()
    
    # Supabase federated user
    sb_user = provider.authenticate_supabase("elena@supabase-cloud.io", "demo12345")
    assert sb_user is not None
    assert sb_user.provider == "supabase"
    assert sb_user.email == "elena@supabase-cloud.io"

    # Clerk federated user
    clerk_user = provider.verify_clerk_session("mock_session_token_123", "clerk_lead@clerk.dev", "Clerk Tech Lead")
    assert clerk_user is not None
    assert clerk_user.provider == "clerk"
    assert clerk_user.email == "clerk_lead@clerk.dev"


def test_api_server_billing_endpoints():
    client = TestClient(app)

    # 1. GET /api/v1/billing/plans
    resp = client.get("/api/v1/billing/plans")
    assert resp.status_code == 200
    data = resp.json()
    assert "plans" in data
    assert len(data["plans"]) >= 3

    # 2. POST /api/v1/billing/checkout
    c_resp = client.post("/api/v1/billing/checkout", json={
        "plan_id": "plan_pro_monthly",
        "success_url": "http://localhost:8501/?pay=ok",
    })
    assert c_resp.status_code == 200
    c_data = c_resp.json()
    assert c_data["success"] is True
    assert "checkout_url" in c_data

    # 3. POST /api/v1/billing/webhook
    w_resp = client.post("/api/v1/billing/webhook", json={
        "user_id": "usr_alex_chen",
        "plan_id": "plan_pro_monthly",
        "transaction_id": "test_txn_001",
    })
    assert w_resp.status_code == 200
    assert w_resp.json()["new_tier"] == "Pro"
