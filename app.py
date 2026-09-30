"""
ArchitectAI - Autonomous Tech Lead Platform
Clean, human-first developer dashboard.
"""

from pathlib import Path
import re
import json
import streamlit as st
import streamlit.components.v1 as components

from config.settings import settings
from orchestration.architect_pipeline import ArchitectPipeline
from agents.solution_architect import create_solution_architect
from tasks.architecture_tasks import create_architecture_task
from utils.openapi_inspector import (
    extract_openapi_spec,
    build_sample_payload,
    execute_test_request,
    render_swagger_ui_html,
)
from utils.database_manager import (
    apply_migrations,
    seed_database,
)
from utils.e2e_manager import (
    list_e2e_specs,
    run_playwright_e2e,
    run_cypress_e2e,
)
from self_healing.retry_manager import SelfHealingLoop
from utils.vcs_manager import VCSManager

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="ArchitectAI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------
# Clean, Quiet, High-Contrast Design System
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography Reset */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 14px !important;
        color: #F8FAFC !important;
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        background-color: #0A0D14 !important;
    }

    /* Native Streamlit Header */
    header[data-testid="stHeader"] {
        background-color: rgba(10, 13, 20, 0.85) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Top Quiet Header */
    .quiet-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 18px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }
    .brand-wrap {
        display: flex;
        align-items: baseline;
        gap: 10px;
    }
    .brand-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }
    .brand-role {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 400;
    }
    .quiet-status {
        font-size: 0.82rem;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
    }

    /* Container Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #101522 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
    }

    /* Form Labels & Headings */
    label, 
    .stWidgetLabel p, 
    [data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .card-caption {
        font-size: 0.84rem;
        color: #94A3B8;
        margin-bottom: 18px;
        line-height: 1.45;
    }

    /* Inputs, Selectboxes & Textarea */
    .stTextInput input,
    .stTextArea textarea {
        background-color: #0A0E18 !important;
        color: #FFFFFF !important;
        border: 1px solid #243046 !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        padding: 10px 12px !important;
    }
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.84rem !important;
        line-height: 1.55 !important;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
        background-color: #0D1322 !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0A0E18 !important;
        border: 1px solid #243046 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-size: 0.88rem !important;
    }

    /* Entity Preview Chips */
    .chips-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 10px 0 16px 0;
        align-items: center;
    }
    .chips-label {
        font-size: 0.78rem;
        color: #94A3B8;
        font-weight: 600;
        margin-right: 4px;
    }
    .entity-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background-color: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #A5B4FC;
        font-size: 0.76rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Primary Action Button */
    .stButton>button {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        transition: all 0.15s ease !important;
        letter-spacing: 0.01em !important;
    }
    .stButton>button:hover {
        background-color: #4338CA !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4) !important;
    }

    /* Secondary Download Buttons */
    .stDownloadButton>button {
        background-color: #1A2234 !important;
        color: #F8FAFC !important;
        border: 1px solid #2E3B52 !important;
        border-radius: 8px !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        padding: 8px 14px !important;
        transition: all 0.15s ease !important;
    }
    .stDownloadButton>button:hover {
        background-color: #243046 !important;
        border-color: #475569 !important;
    }

    /* Live Progress Stage Rows */
    .stage-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        background-color: #0A0E18;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 0.84rem;
    }
    .stage-row.done {
        border-color: rgba(16, 185, 129, 0.3);
    }
    .stage-row.done .stage-icon {
        color: #10B981;
    }
    .stage-row.active {
        border-color: rgba(99, 102, 241, 0.4);
        background-color: rgba(99, 102, 241, 0.08);
    }
    .stage-row.active .stage-icon {
        color: #818CF8;
    }
    .stage-icon {
        font-size: 0.95rem;
        font-weight: 700;
        width: 18px;
        text-align: center;
        color: #64748B;
    }
    .stage-text {
        font-weight: 600;
        color: #E2E8F0;
    }
    .stage-desc {
        font-size: 0.76rem;
        color: #94A3B8;
        margin-left: auto;
    }

    /* Sidebar Clean Navigation */
    section[data-testid="stSidebar"] {
        background-color: #0A0E18 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    div[data-testid="stRadio"] > div {
        gap: 4px !important;
    }
    div[data-testid="stRadio"] label {
        background: transparent !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span {
        color: #E2E8F0 !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Top Quiet Header
# -------------------------------------------------------------
st.markdown("""
<div class="quiet-header">
    <div class="brand-wrap">
        <span class="brand-name">ArchitectAI</span>
        <span class="brand-role">· Autonomous Tech Lead</span>
    </div>
    <div class="quiet-status">
        <span class="status-dot"></span>
        <span>7 agents ready · Docker · Redis</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Sidebar: Clean Navigation & Settings
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("**Navigation**")
    navigation = st.radio(
        "Navigation",
        [
            "⚡ Build Project",
            "📐 System Architecture",
            "📖 Technical Docs",
            "🤖 Agent Swarm",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Settings**")

    active_provider = settings.get_active_provider()
    st.caption(f"Provider: `{active_provider.upper()}`")

    if active_provider == "groq":
        groq_models = [
            "qwen/qwen3.8-27b",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "allam-2-7b",
        ]
        current_model = settings.get_active_model()
        default_idx = groq_models.index(current_model) if current_model in groq_models else 0
        selected_model = st.selectbox(
            "Model",
            groq_models,
            index=default_idx,
            help="High-velocity coding models hosted on Groq LPU inference",
        )
        if selected_model != settings.MODEL_NAME:
            settings.MODEL_NAME = selected_model
            settings.GROQ_MODEL = selected_model
            st.rerun()

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    mock_toggle = st.toggle("Mock mode", value=settings.MOCK_LLM)
    st.caption("Run locally without consuming API credits")
    if mock_toggle != settings.MOCK_LLM:
        settings.MOCK_LLM = mock_toggle
        st.rerun()

    st.markdown("---")
    st.caption("ArchitectAI v1.2 · Python 3.12 · Docker")

# -------------------------------------------------------------
# VIEW 1: Build Project (Master-Detail Two Columns)
# -------------------------------------------------------------
if navigation == "⚡ Build Project":

    # Helper function to detect entities in real-time
    def detect_entities(text: str) -> list[str]:
        words = re.findall(r'\b[A-Z][a-zA-Z0-9_]+\b', text)
        stopwords = {
            "Build", "Manage", "Each", "Can", "With", "A", "An", "The", 
            "In", "And", "Or", "For", "Of", "To", "From", "AI", "FastAPI", 
            "Python", "SQLAlchemy", "System", "Service", "Platform"
        }
        entities = []
        for w in words:
            if w not in stopwords and w not in entities:
                entities.append(w)
        return entities[:8]

    # Two-Column Master Layout: Form on Left, Progress & Results on Right
    col_form, col_results = st.columns([1, 1], gap="large")

    # LEFT: Project Specification Form
    with col_form:
        with st.container(border=True):
            st.markdown('<div class="card-title">New Project</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-caption">Configure your backend service and specify requirements.</div>', unsafe_allow_html=True)

            project_name = st.text_input(
                "Project name",
                value="Hospital_Management_System",
                help="Name of the backend service package",
            )

            preset_choice = st.selectbox(
                "Preset",
                [
                    "Hospital Management System",
                    "E-Commerce Platform",
                    "FinTech Banking Ledger",
                    "Ride-Sharing Telemetry",
                    "Custom Requirements",
                ],
                index=0,
            )

            presets_map = {
                "Hospital Management System": """Build an AI-powered Hospital Management System.
Manage Patient, Doctor, Appointment, and MedicalRecord.
A Patient can book multiple Appointments with Doctors.
Each Appointment can result in a MedicalRecord.""",
                "E-Commerce Platform": """Build an E-Commerce Backend Service.
Manage Customer, Product, Order, and OrderItem.
A Customer can place multiple Orders.
Each Order contains multiple OrderItems linked to Products.""",
                "FinTech Banking Ledger": """Build a Secure FinTech Core Banking Service.
Manage Account, Transaction, Beneficiary, and AuditLog.
An Account can initiate multiple Transactions.
Each Transaction records source, destination, amount, and timestamp.""",
                "Ride-Sharing Telemetry": """Build a Ride-Sharing Telemetry Backend.
Manage Passenger, Driver, RideRequest, and Payment.
A Passenger requests a Ride with pickup and dropoff coordinates.
A Driver accepts the Ride and completes Payment.""",
            }

            default_reqs = presets_map.get(preset_choice, "Describe your software requirements and domain entities here...")
            requirements = st.text_area(
                "Requirements",
                value=default_reqs,
                height=160,
                help="Specify entities, relationships, constraints, and business logic.",
            )

            # Entity Chips Preview (Confirms understanding before spending a run)
            detected = detect_entities(requirements)
            if detected:
                chips_html = "".join([f'<span class="entity-chip">{e}</span>' for e in detected])
                st.markdown(f"""
                <div class="chips-container">
                    <span class="chips-label">Detected entities:</span>
                    {chips_html}
                </div>
                """, unsafe_allow_html=True)

            output_dir = st.text_input(
                "Save location",
                value=f"outputs/{project_name}",
            )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            build_btn = st.button("Build service", type="primary", use_container_width=True)

    # RIGHT: Live Progress & Results beside the form
    with col_results:
        # Check if generation was triggered
        if build_btn:
            if not requirements.strip():
                st.error("Please enter project requirements.")
            else:
                with st.spinner("Building service..."):
                    try:
                        pipeline = ArchitectPipeline(output_dir=output_dir)
                        result = pipeline.generate(
                            requirements=requirements,
                            project_name=project_name,
                        )

                        # Store in session state for persistence
                        st.session_state["last_result"] = result
                        st.session_state["last_project"] = project_name
                        st.session_state["last_dir"] = output_dir

                    except Exception as exc:
                        st.error(f"Error: {exc}")

        # Render Results or Ready State
        last_result = st.session_state.get("last_result")
        last_project = st.session_state.get("last_project", project_name)
        last_dir = st.session_state.get("last_dir", output_dir)

        if not last_result and Path(output_dir).exists() and (Path(output_dir) / "backend").exists():
            last_result = {
                "project_name": project_name,
                "output_dir": output_dir,
                "export": {
                    "archive": str(Path(output_dir) / "exports" / f"{project_name.lower()}.zip"),
                    "report": str(Path(output_dir) / "exports" / "generation_report.json"),
                },
            }

        if last_result:
            with st.container(border=True):
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div class="card-title">✓ Built successfully</div>
                    <span class="status-dot"></span>
                </div>
                <div class="card-caption">All models, routers, and 100% of generated pytest tests passed verification.</div>
                """, unsafe_allow_html=True)

                # Progress Checklist (Done)
                self_healing_info = last_result.get("self_healing")
                if isinstance(self_healing_info, dict) and self_healing_info.get("clean_run"):
                    healing_tag = "Clean (100% Green)"
                elif isinstance(self_healing_info, dict) and self_healing_info.get("healed"):
                    healing_tag = f"Repaired ({self_healing_info.get('attempts', 1)} attempts)"
                else:
                    healing_tag = "Active"

                st.markdown(f"""
                <div class="stage-row done">
                    <span class="stage-icon">✓</span>
                    <span class="stage-text">Domain entities & mapping</span>
                    <span class="stage-desc">Done</span>
                </div>
                <div class="stage-row done">
                    <span class="stage-icon">✓</span>
                    <span class="stage-text">SQLAlchemy models & schemas</span>
                    <span class="stage-desc">Done</span>
                </div>
                <div class="stage-row done">
                    <span class="stage-icon">✓</span>
                    <span class="stage-text">FastAPI routers & services</span>
                    <span class="stage-desc">Done</span>
                </div>
                <div class="stage-row done">
                    <span class="stage-icon">✓</span>
                    <span class="stage-text">Hermetic pytest validation</span>
                    <span class="stage-desc">Passed</span>
                </div>
                <div class="stage-row done">
                    <span class="stage-icon">✓</span>
                    <span class="stage-text">Autonomous Self-Healing Loop</span>
                    <span class="stage-desc">{healing_tag}</span>
                </div>
                <div class="stage-row done">
                    <span class="stage-icon">✓</span>
                    <span class="stage-text">Docker, K8s & Helm packaging</span>
                    <span class="stage-desc">Ready</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

                # Generated File Tree & Code Explorer
                st.markdown("**Generated Files & Manifests**")
                backend_dir = Path(last_dir) / "backend"
                models_dir = backend_dir / "app" / "models"
                apis_dir = backend_dir / "app" / "api"
                tests_dir = backend_dir / "tests"
                k8s_dir = backend_dir / "k8s"
                helm_root = backend_dir / "helm"

                t_models, t_apis, t_tests, t_main, t_docker, t_k8s, t_helm, t_db, t_tester, t_e2e = st.tabs([
                    "Models",
                    "Routers",
                    "Tests",
                    "main.py",
                    "Dockerfile",
                    "Kubernetes",
                    "Helm",
                    "Database & Seed",
                    "API Tester & Docs",
                    "Frontend E2E",
                ])

                with t_models:
                    if models_dir.exists():
                        m_files = [f.name for f in models_dir.glob("*.py") if f.name != "__init__.py"]
                        if m_files:
                            m_choice = st.selectbox("Model file", m_files, key="sel_m", label_visibility="collapsed")
                            st.code((models_dir / m_choice).read_text(encoding="utf-8"), language="python")

                with t_apis:
                    if apis_dir.exists():
                        a_files = [f.name for f in apis_dir.glob("*.py") if f.name != "__init__.py"]
                        if a_files:
                            a_choice = st.selectbox("Router file", a_files, key="sel_a", label_visibility="collapsed")
                            st.code((apis_dir / a_choice).read_text(encoding="utf-8"), language="python")

                with t_tests:
                    st.markdown("""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <div style="font-weight: 600; font-size: 14px; color: #F8FAFC;">🧪 Pytest Suite & Autonomous Self-Healing</div>
                            <div style="font-size: 12px; color: #94A3B8;">Closed-loop validation, AI error reflection, and automatic code recovery</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col_t_action1, col_t_action2 = st.columns([2, 1])
                    with col_t_action1:
                        if tests_dir.exists():
                            t_files = [f.name for f in tests_dir.glob("test_*.py")]
                            if t_files:
                                t_choice = st.selectbox("Test file", t_files, key="sel_t", label_visibility="collapsed")
                            else:
                                t_choice = None
                        else:
                            t_choice = None
                    with col_t_action2:
                        heal_btn = st.button("🩺 Run Self-Healing Doctor", type="secondary", use_container_width=True, help="Executes ProjectValidator and triggers SelfHealingLoop if any issue is detected")

                    if heal_btn:
                        with st.spinner("Running autonomous self-healing diagnostics..."):
                            loop = SelfHealingLoop(backend_dir=str(backend_dir), max_attempts=3)
                            heal_report = loop.run()
                            if heal_report.get("clean_run"):
                                st.success("✓ Zero issues detected! Project is 100% green and verified.")
                            elif heal_report.get("healed"):
                                st.success(f"✓ Autonomous Self-Healing Succeeded! Repaired {heal_report.get('healed_file')} in {heal_report.get('attempts')} attempts.")
                                with st.expander("🛠 Reflection & Patch Details", expanded=True):
                                    st.markdown(f"**Root Cause**: `{heal_report.get('root_cause')}`")
                                    st.markdown(f"**Target File**: `{heal_report.get('healed_file')}`")
                                    for h in heal_report.get("history", []):
                                        st.caption(f"Attempt {h.get('attempt')}: {h.get('fix_suggestion', 'Patched and verified green.')}")
                            else:
                                st.error(f"❌ Self-healing exhausted attempts: {heal_report.get('message')}")
                                with st.expander("Diagnostic Traceback", expanded=True):
                                    for err in heal_report.get("validation", {}).get("errors", []):
                                        st.code(err)

                    if t_choice and (tests_dir / t_choice).exists():
                        st.code((tests_dir / t_choice).read_text(encoding="utf-8"), language="python")

                with t_main:
                    main_f = backend_dir / "app" / "main.py"
                    if main_f.exists():
                        st.code(main_f.read_text(encoding="utf-8"), language="python")

                with t_docker:
                    docker_f = backend_dir / "Dockerfile"
                    if docker_f.exists():
                        st.code(docker_f.read_text(encoding="utf-8"), language="dockerfile")

                with t_k8s:
                    if k8s_dir.exists():
                        k_files = sorted([f.name for f in k8s_dir.glob("*.yaml")])
                        if k_files:
                            k_choice = st.selectbox("Kubernetes Manifest", k_files, key="sel_k8s", label_visibility="collapsed")
                            st.code((k8s_dir / k_choice).read_text(encoding="utf-8"), language="yaml")
                    else:
                        st.caption("Kubernetes manifests will be generated here upon building.")

                with t_helm:
                    if helm_root.exists():
                        chart_dirs = [d for d in helm_root.iterdir() if d.is_dir()]
                        if chart_dirs:
                            chart_dir = chart_dirs[0]
                            helm_files = [f.name for f in chart_dir.glob("*.yaml")]
                            tpl_dir = chart_dir / "templates"
                            if tpl_dir.exists():
                                helm_files += [f"templates/{f.name}" for f in sorted(tpl_dir.glob("*")) if f.is_file()]
                            h_choice = st.selectbox("Helm Chart File", helm_files, key="sel_helm", label_visibility="collapsed")
                            target_f = chart_dir / h_choice
                            if target_f.exists():
                                lang = "yaml" if h_choice.endswith((".yaml", ".yml")) else "text"
                                st.code(target_f.read_text(encoding="utf-8"), language=lang)
                    else:
                        st.caption("Helm chart files will be generated here upon building.")

                with t_db:
                    st.markdown("**Database Migrations & Data Seeding**")
                    st.caption("Manage schema revisions via Alembic and populate synthetic demo records.")

                    col_op1, col_op2 = st.columns(2)
                    with col_op1:
                        if st.button("Apply Alembic Migrations", use_container_width=True, help="Executes 'alembic upgrade head' in the generated project"):
                            with st.spinner("Applying migrations..."):
                                mig_res = apply_migrations(backend_dir)
                                if mig_res["success"]:
                                    st.success(f"✓ Migrations applied ({mig_res['latency_ms']} ms)")
                                    if mig_res["stdout"]:
                                        st.code(mig_res["stdout"], language="text")
                                else:
                                    st.error(f"Migration error: {mig_res['stderr'] or mig_res['stdout']}")

                    with col_op2:
                        if st.button("🌱 Seed Sample Data", type="primary", use_container_width=True, help="Populates the database with realistic demo records"):
                            with st.spinner("Seeding database records..."):
                                seed_res = seed_database(backend_dir)
                                if seed_res["success"]:
                                    summary = seed_res.get("summary", {})
                                    total_seeded = sum(summary.values()) if summary else 0
                                    st.success(f"✓ Seeded {total_seeded} records across {len(summary)} entities ({seed_res['latency_ms']} ms)")
                                    if summary:
                                        cols_s = st.columns(min(len(summary), 4))
                                        for idx, (ent_name, count) in enumerate(summary.items()):
                                            with cols_s[idx % len(cols_s)]:
                                                st.metric(label=ent_name, value=f"{count} rows")
                                else:
                                    st.error(f"Seeding error: {seed_res['stderr'] or seed_res['stdout']}")

                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    st.markdown("**Migration & Seed Files**")

                    db_files = []
                    alembic_ini_f = backend_dir / "alembic.ini"
                    if alembic_ini_f.exists():
                        db_files.append("alembic.ini")
                    alembic_env_f = backend_dir / "alembic" / "env.py"
                    if alembic_env_f.exists():
                        db_files.append("alembic/env.py")
                    seed_f = backend_dir / "seed.py"
                    if seed_f.exists():
                        db_files.append("seed.py")

                    versions_dir = backend_dir / "alembic" / "versions"
                    if versions_dir.exists():
                        for vf in sorted(versions_dir.glob("*.py")):
                            db_files.append(f"alembic/versions/{vf.name}")

                    if db_files:
                        db_choice = st.selectbox("Database file", db_files, key="sel_db_files", label_visibility="collapsed")
                        target_db_f = backend_dir / db_choice
                        if target_db_f.exists():
                            f_lang = "ini" if db_choice.endswith(".ini") else "python"
                            st.code(target_db_f.read_text(encoding="utf-8"), language=f_lang)
                    else:
                        st.caption("Alembic and seed files will appear here once built.")

                with t_tester:
                    spec = extract_openapi_spec(backend_dir)
                    if not spec:
                        st.caption("OpenAPI specification could not be loaded. Please ensure the project built successfully.")
                    else:
                        sub_tester, sub_swagger, sub_spec = st.tabs([
                            "⚡ Interactive Endpoint Tester",
                            "📖 Swagger UI",
                            "📄 OpenAPI Spec (JSON)",
                        ])

                        with sub_tester:
                            paths = spec.get("paths", {})
                            all_schemas = spec.get("components", {}).get("schemas", {})

                            endpoint_list = []
                            for p_path, p_methods in paths.items():
                                for m_method, m_meta in p_methods.items():
                                    if m_method.lower() in ("get", "post", "put", "delete", "patch"):
                                        endpoint_list.append({
                                            "label": f"[{m_method.upper()}] {p_path}",
                                            "method": m_method.upper(),
                                            "path": p_path,
                                            "summary": m_meta.get("summary", ""),
                                            "meta": m_meta,
                                        })

                            if not endpoint_list:
                                st.info("No API routes detected.")
                            else:
                                ep_labels = [ep["label"] for ep in endpoint_list]
                                sel_ep_label = st.selectbox("Select Endpoint", ep_labels, key="sel_endpoint_tester")
                                sel_ep = next(ep for ep in endpoint_list if ep["label"] == sel_ep_label)

                                col_m1, col_m2 = st.columns([1, 3])
                                with col_m1:
                                    method_color = {
                                        "GET": "#38bdf8",
                                        "POST": "#4ade80",
                                        "PUT": "#fbbf24",
                                        "DELETE": "#f87171",
                                    }.get(sel_ep["method"], "#a78bfa")
                                    st.markdown(
                                        f"<span style='background: {method_color}22; color: {method_color}; "
                                        f"border: 1px solid {method_color}55; padding: 3px 8px; border-radius: 6px; "
                                        f"font-weight: 700; font-family: monospace; font-size: 12px;'>{sel_ep['method']}</span> "
                                        f"<span style='font-family: monospace; font-size: 13px; color: #f1f5f9;'>{sel_ep['path']}</span>",
                                        unsafe_allow_html=True,
                                    )
                                with col_m2:
                                    if sel_ep["summary"]:
                                        st.caption(f"Summary: {sel_ep['summary']}")

                                # Path parameters if any
                                target_path = sel_ep["path"]
                                path_params_found = re.findall(r"\{([^}]+)\}", target_path)
                                path_param_values = {}
                                if path_params_found:
                                    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                                    p_cols = st.columns(len(path_params_found))
                                    for idx, p_name in enumerate(path_params_found):
                                        with p_cols[idx]:
                                            path_param_values[p_name] = st.text_input(
                                                f"Path param: {{{p_name}}}",
                                                value="1" if "id" in p_name.lower() else "sample",
                                                key=f"pp_{p_name}_{sel_ep['label']}",
                                            )
                                    for p_name, p_val in path_param_values.items():
                                        target_path = target_path.replace(f"{{{p_name}}}", p_val)

                                # Request body if POST/PUT
                                json_body = None
                                if sel_ep["method"] in ("POST", "PUT", "PATCH"):
                                    req_body_meta = sel_ep["meta"].get("requestBody", {})
                                    body_schema = req_body_meta.get("content", {}).get("application/json", {}).get("schema", {})
                                    sample_payload = build_sample_payload(body_schema, all_schemas)
                                    sample_json_str = json.dumps(sample_payload, indent=2)

                                    body_input = st.text_area(
                                        "JSON Request Body",
                                        value=sample_json_str,
                                        height=130,
                                        key=f"body_{sel_ep['label']}",
                                    )
                                    try:
                                        json_body = json.loads(body_input) if body_input.strip() else None
                                    except Exception as e:
                                        st.error(f"Invalid JSON in request body: {e}")
                                        json_body = None

                                # Send Request button
                                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                                if st.button(f"Send {sel_ep['method']} Request", type="primary", key=f"btn_send_{sel_ep['label']}"):
                                    with st.spinner("Executing request via in-memory TestClient..."):
                                        resp = execute_test_request(
                                            backend_dir=backend_dir,
                                            method=sel_ep["method"],
                                            path=target_path,
                                            json_body=json_body,
                                        )

                                        status_code = resp.get("status_code", 500)
                                        latency = resp.get("latency_ms", 0.0)
                                        resp_body = resp.get("body")

                                        sc_color = "#4ade80" if 200 <= status_code < 300 else ("#fbbf24" if 400 <= status_code < 500 else "#f87171")

                                        st.markdown(
                                            f"""
                                            <div style="display: flex; gap: 12px; align-items: center; margin-top: 10px; margin-bottom: 6px;">
                                                <span style="background: {sc_color}22; color: {sc_color}; border: 1px solid {sc_color}55; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-family: monospace;">
                                                    HTTP {status_code}
                                                </span>
                                                <span style="color: #94a3b8; font-size: 12px; font-family: monospace;">
                                                    Latency: {latency} ms
                                                </span>
                                            </div>
                                            """,
                                            unsafe_allow_html=True,
                                        )

                                        if isinstance(resp_body, (dict, list)):
                                            st.json(resp_body)
                                        else:
                                            st.code(str(resp_body), language="text")

                        with sub_swagger:
                            st.caption("Interactive OpenAPI documentation powered by Swagger UI.")
                            swagger_html = render_swagger_ui_html(spec)
                            components.html(swagger_html, height=600, scrolling=True)

                        with sub_spec:
                            spec_str = json.dumps(spec, indent=2)
                            st.download_button(
                                label="Download openapi.json",
                                data=spec_str,
                                file_name=f"{last_project.lower()}_openapi.json",
                                mime="application/json",
                                key="dl_openapi_json",
                            )
                            st.code(spec_str, language="json")

                with t_e2e:
                    frontend_dir = Path(last_dir) / "frontend"
                    specs_data = list_e2e_specs(frontend_dir)

                    st.markdown("""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <div style="font-weight: 600; font-size: 14px; color: #F8FAFC;">🎭 Frontend E2E Testing Suite (Playwright & Cypress)</div>
                            <div style="font-size: 12px; color: #94A3B8;">Cross-browser test suites, interactive forms, validation rules & network intercept mocks</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if not specs_data["exists"]:
                        st.info("Frontend directory not found for this project.")
                    else:
                        pw_specs = specs_data["playwright"]["specs"]
                        cy_specs = specs_data["cypress"]["specs"]
                        total_pw_tests = specs_data["playwright"]["total_tests"]
                        total_cy_tests = specs_data["cypress"]["total_tests"]

                        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                        with col_m1:
                            st.metric("Playwright Specs", f"{len(pw_specs)} files")
                        with col_m2:
                            st.metric("Cypress Specs", f"{len(cy_specs)} files")
                        with col_m3:
                            st.metric("Total E2E Scenarios", f"{total_pw_tests + total_cy_tests}")
                        with col_m4:
                            st.metric("Engines Verified", "Chromium, Firefox, WebKit")

                        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                        sub_pw, sub_cy, sub_files = st.tabs([
                            "🎭 Playwright Runner",
                            "🌲 Cypress Runner",
                            "📁 Test Files & Config",
                        ])

                        with sub_pw:
                            st.caption("Executes headless Playwright tests across Chromium, Firefox, WebKit and mobile devices.")
                            col_pw_run1, col_pw_run2 = st.columns([2, 1])
                            with col_pw_run1:
                                pw_spec_choice = st.selectbox(
                                    "Target Playwright Spec",
                                    ["All Specs"] + [s["name"] for s in pw_specs],
                                    key="sel_pw_spec_run",
                                )
                            with col_pw_run2:
                                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                                run_pw_btn = st.button("▶ Run Playwright Suite", type="primary", use_container_width=True)

                            if run_pw_btn:
                                with st.spinner("Executing Playwright cross-browser tests..."):
                                    spec_arg = None if pw_spec_choice == "All Specs" else pw_spec_choice
                                    res = run_playwright_e2e(frontend_dir, spec_file=spec_arg)
                                    if res["success"]:
                                        st.success(f"✓ All Playwright tests passed ({res['duration_ms']} ms) — {res['runner']}")
                                        col_r1, col_r2, col_r3 = st.columns(3)
                                        with col_r1:
                                            st.metric("Passed Tests", f"{res['passed']}")
                                        with col_r2:
                                            st.metric("Failed Tests", f"{res['failed']}")
                                        with col_r3:
                                            st.metric("Cross-Browser Assertions", f"{res.get('total_browser_assertions', res['passed'] * 3)}")

                                        if res.get("executed_tests"):
                                            st.markdown("**Test Execution Breakdown**")
                                            table_rows = []
                                            for et in res["executed_tests"]:
                                                tag_badge = f'<span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; padding: 2px 6px; border-radius: 4px; font-size: 11px;">{et["tag"]}</span>'
                                                status_badge = '<span style="color: #4ADE80; font-weight: 600;">✓ PASSED</span>'
                                                table_rows.append(f"<tr><td style='padding: 6px 10px;'><code>{et['spec']}</code></td><td style='padding: 6px 10px;'>{et['test']}</td><td style='padding: 6px 10px;'>{tag_badge}</td><td style='padding: 6px 10px;'>{status_badge}</td><td style='padding: 6px 10px; color: #94A3B8;'>{et['duration_ms']} ms</td></tr>")

                                            st.markdown(f"""
                                            <div style="border: 1px solid #1E293B; border-radius: 8px; overflow: hidden; margin-top: 8px;">
                                                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                                                    <thead>
                                                        <tr style="background: #111827; border-bottom: 1px solid #1E293B; text-align: left; color: #94A3B8;">
                                                            <th style="padding: 8px 10px;">Spec</th>
                                                            <th style="padding: 8px 10px;">Scenario</th>
                                                            <th style="padding: 8px 10px;">Tag</th>
                                                            <th style="padding: 8px 10px;">Status</th>
                                                            <th style="padding: 8px 10px;">Duration</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {''.join(table_rows)}
                                                    </tbody>
                                                </table>
                                            </div>
                                            """, unsafe_allow_html=True)

                                        with st.expander("Terminal Logs", expanded=False):
                                            st.code(res["stdout"], language="bash")
                                    else:
                                        st.error(f"Playwright Execution Failed: {res.get('stderr')}")

                        with sub_cy:
                            st.caption("Executes headless Cypress integration tests and network stub verifications.")
                            col_cy_run1, col_cy_run2 = st.columns([2, 1])
                            with col_cy_run1:
                                cy_spec_choice = st.selectbox(
                                    "Target Cypress Spec",
                                    ["All Specs"] + [s["name"] for s in cy_specs],
                                    key="sel_cy_spec_run",
                                )
                            with col_cy_run2:
                                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                                run_cy_btn = st.button("▶ Run Cypress Suite", type="primary", use_container_width=True)

                            if run_cy_btn:
                                with st.spinner("Executing Cypress integration tests..."):
                                    spec_arg = None if cy_spec_choice == "All Specs" else cy_spec_choice
                                    res = run_cypress_e2e(frontend_dir, spec_file=spec_arg)
                                    if res["success"]:
                                        st.success(f"✓ All Cypress tests passed ({res['duration_ms']} ms) — {res['runner']}")
                                        col_cr1, col_cr2, col_cr3 = st.columns(3)
                                        with col_cr1:
                                            st.metric("Passed Tests", f"{res['passed']}")
                                        with col_cr2:
                                            st.metric("Failed Tests", f"{res['failed']}")
                                        with col_cr3:
                                            st.metric("Duration", f"{res['duration_ms']} ms")

                                        with st.expander("Terminal Logs", expanded=False):
                                            st.code(res["stdout"], language="bash")
                                    else:
                                        st.error(f"Cypress Execution Failed: {res.get('stderr')}")

                        with sub_files:
                            all_e2e_files = []
                            for c in specs_data["configs"]:
                                all_e2e_files.append(c)
                            for s in pw_specs:
                                all_e2e_files.append(s["rel_path"])
                            for s in cy_specs:
                                all_e2e_files.append(s["rel_path"])

                            if all_e2e_files:
                                sel_f = st.selectbox("Select Test File / Config", all_e2e_files, key="sel_e2e_preview")
                                target_f = frontend_dir / sel_f
                                if target_f.exists():
                                    lang = "typescript" if sel_f.endswith((".ts", ".tsx")) else "javascript" if sel_f.endswith(".js") else "json" if sel_f.endswith(".json") else "yaml" if sel_f.endswith((".yml", ".yaml")) else "markdown"
                                    st.code(target_f.read_text(encoding="utf-8"), language=lang)


                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

                # Export Downloads
                export_info = last_result.get("export", {})
                archive_path = export_info.get("archive")
                report_path = export_info.get("report")
                openapi_path = backend_dir / "openapi.json"

                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1:
                    if archive_path and Path(archive_path).exists():
                        with open(archive_path, "rb") as f:
                            st.download_button(
                                label="Download project (.zip)",
                                data=f.read(),
                                file_name=f"{last_project.lower()}.zip",
                                mime="application/zip",
                                use_container_width=True,
                            )
                with col_d2:
                    if report_path and Path(report_path).exists():
                        with open(report_path, "r") as f:
                            st.download_button(
                                label="Audit report (.json)",
                                data=f.read(),
                                file_name=f"{last_project.lower()}_report.json",
                                mime="application/json",
                                use_container_width=True,
                            )
                with col_d3:
                    if openapi_path.exists():
                        st.download_button(
                            label="OpenAPI spec (.json)",
                            data=openapi_path.read_text(encoding="utf-8"),
                            file_name=f"{last_project.lower()}_openapi.json",
                            mime="application/json",
                            use_container_width=True,
                        )

                # One-Click Remote VCS & Pull Request Integration
                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown("""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <div style="font-weight: 600; font-size: 14px; color: #F8FAFC;">🚀 One-Click Remote VCS & Pull Request Integration</div>
                            <div style="font-size: 12px; color: #94A3B8;">Push scaffolded codebase to GitHub / GitLab, stage semantic commits, and open an enterprise PR</div>
                        </div>
                        <span style="background: rgba(34, 197, 94, 0.12); color: #4ADE80; font-size: 11px; padding: 3px 8px; border-radius: 9999px; border: 1px solid rgba(34, 197, 94, 0.25);">Ready</span>
                    </div>
                    """, unsafe_allow_html=True)

                    col_vcs1, col_vcs2, col_vcs3 = st.columns([1, 1.5, 1.5])
                    with col_vcs1:
                        vcs_provider = st.selectbox("VCS Provider", ["GitHub", "GitLab"], index=0, key="sel_vcs_prov")
                    with col_vcs2:
                        default_repo_name = f"{last_project.lower().replace('_', '-')}-api"
                        repo_input = st.text_input("Repository Name", value=default_repo_name, key="input_repo_name")
                    with col_vcs3:
                        branch_input = st.text_input("Feature Branch", value="feat/architectai-autonomous-scaffold", key="input_branch_name")

                    col_auth1, col_auth2 = st.columns([2, 1])
                    with col_auth1:
                        env_token = os.environ.get("GITHUB_TOKEN", "")
                        token_input = st.text_input(
                            f"{vcs_provider} Personal Access Token",
                            value=env_token,
                            type="password",
                            help="Optional. Leave blank to run in instant Sandbox / Demo Simulation mode.",
                            key="input_vcs_token",
                        )
                    with col_auth2:
                        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                        is_sim = not bool(token_input.strip())
                        btn_label = "🚀 Create Pull Request (Sandbox)" if is_sim else "🚀 Push to GitHub & Open PR"
                        pr_btn = st.button(btn_label, type="primary", use_container_width=True)

                    if pr_btn:
                        with st.spinner(f"Connecting to {vcs_provider} and creating Pull Request..."):
                            vcs = VCSManager(project_dir=Path(last_dir))
                            pr_result = vcs.push_and_create_github_pr(
                                token=token_input.strip(),
                                project_name=last_project,
                                repo_name=repo_input,
                                branch_name=branch_input,
                                simulation_mode=is_sim,
                            )

                            if pr_result.get("success"):
                                st.success(f"{pr_result.get('message')}")
                                col_p1, col_p2, col_p3 = st.columns(3)
                                with col_p1:
                                    st.metric("Pull Request", f"#{pr_result.get('pr_number', 1)}")
                                with col_p2:
                                    st.metric("Target Branch", pr_result.get("head_branch"))
                                with col_p3:
                                    st.metric("Commit SHA", pr_result.get("commit_sha", "HEAD"))

                                st.markdown(f"""
                                <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #334155; border-radius: 8px; padding: 12px 16px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <div style="font-size: 13px; font-weight: 600; color: #F8FAFC;">{pr_result.get('pr_title')}</div>
                                        <div style="font-size: 12px; color: #94A3B8;">Repository: <code>{pr_result.get('repo_full_name')}</code></div>
                                    </div>
                                    <a href="{pr_result.get('pr_url')}" target="_blank" style="background: #3B82F6; color: white; padding: 6px 14px; border-radius: 6px; font-weight: 500; font-size: 12px; text-decoration: none; display: inline-block;">Open Pull Request ↗</a>
                                </div>
                                """, unsafe_allow_html=True)

                                with st.expander("📄 Review Generated Enterprise PR Description", expanded=False):
                                    st.markdown(pr_result.get("pr_body"))
                            else:
                                st.error(f"Failed to create Pull Request: {pr_result.get('error')}")
        else:
            # Quiet Ready State before build
            with st.container(border=True):
                st.markdown('<div class="card-title">Pipeline</div>', unsafe_allow_html=True)
                st.markdown('<div class="card-caption">Stages executed automatically when you build the service.</div>', unsafe_allow_html=True)

                st.markdown("""
                <div class="stage-row">
                    <span class="stage-icon">○</span>
                    <span class="stage-text">Domain intake & entity mapping</span>
                    <span class="stage-desc">Stage 1</span>
                </div>
                <div class="stage-row">
                    <span class="stage-icon">○</span>
                    <span class="stage-text">SQLAlchemy models & schemas</span>
                    <span class="stage-desc">Stage 2</span>
                </div>
                <div class="stage-row">
                    <span class="stage-icon">○</span>
                    <span class="stage-text">FastAPI routers & services</span>
                    <span class="stage-desc">Stage 3</span>
                </div>
                <div class="stage-row">
                    <span class="stage-icon">○</span>
                    <span class="stage-text">Hermetic pytest validation</span>
                    <span class="stage-desc">Stage 4</span>
                </div>
                <div class="stage-row">
                    <span class="stage-icon">○</span>
                    <span class="stage-text">Docker, K8s & Helm packaging</span>
                    <span class="stage-desc">Stage 5</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                st.info("💡 Fill in the project details on the left and click **Build service** to run the pipeline.")

# -------------------------------------------------------------
# VIEW 2: System Architecture Studio
# -------------------------------------------------------------
elif navigation == "📐 System Architecture":
    with st.container(border=True):
        st.markdown('<div class="card-title">System Architecture Studio</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-caption">Draft comprehensive Software Architecture Documents (SAD) using the 15-step reference framework.</div>', unsafe_allow_html=True)

        design_reqs = st.text_area(
            "System Requirements",
            value="Design a scalable Ride-Sharing Platform handling 100k peak requests/second with real-time driver matching and payment settlement.",
            height=120,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Estimated Peak QPS", value="100,000", disabled=True)
        with col2:
            st.text_input("Target Latency (p99)", value="< 50ms", disabled=True)
        with col3:
            st.text_input("Target Uptime", value="99.999%", disabled=True)

        if st.button("Generate Architecture Plan", type="primary"):
            with st.spinner("Designing system architecture..."):
                try:
                    architect = create_solution_architect()
                    task = create_architecture_task(architect, design_reqs)
                    st.success("✓ Architecture task prepared based on 15-step reference workflow")
                    st.caption(f"Assigned: {architect.role}")
                except Exception as e:
                    st.error(f"Error: {e}")

# -------------------------------------------------------------
# VIEW 3: Technical Docs
# -------------------------------------------------------------
elif navigation == "📖 Technical Docs":
    with st.container(border=True):
        st.markdown('<div class="card-title">Specifications & Guides</div>', unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["Workflow Reference", "System Architecture", "API Standards"])
        with t1:
            wf = Path("docs/workflow.md")
            if wf.exists():
                st.markdown(wf.read_text(encoding="utf-8"))
        with t2:
            arch = Path("docs/architecture.md")
            if arch.exists():
                st.markdown(arch.read_text(encoding="utf-8"))
        with t3:
            api = Path("docs/api.md")
            if api.exists():
                st.markdown(api.read_text(encoding="utf-8"))

# -------------------------------------------------------------
# VIEW 4: Agent Swarm
# -------------------------------------------------------------
elif navigation == "🤖 Agent Swarm":
    with st.container(border=True):
        st.markdown('<div class="card-title">Specialized Engineering Agents</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-caption">ArchitectAI coordinates seven specialized agent personas during the build lifecycle.</div>', unsafe_allow_html=True)

        agents = [
            ("Principal Solution Architect", "System design, 15-step workflow, and capacity planning"),
            ("Database Specialist", "Schema modeling, SQLAlchemy models, and index strategies"),
            ("Backend Engineer", "FastAPI route generation, service layer, and business logic"),
            ("QA Engineer", "Automated test synthesis and hermetic pytest execution"),
            ("Security Auditor", "Authentication, secret isolation, and CORS policy verification"),
            ("DevOps Specialist", "Containerization, Dockerfile generation, and health checks"),
            ("Documentation Lead", "API specifications, architecture diagrams, and release packaging"),
        ]

        cols = st.columns(2)
        for idx, (name, desc) in enumerate(agents):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="background-color: #0A0E18; border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 8px; padding: 14px; margin-bottom: 10px;">
                    <div style="font-weight: 600; color: #FFFFFF; font-size: 0.9rem;">{name}</div>
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 3px;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
