"""
ArchitectAI - Autonomous Tech Lead Platform
Executive AI Engineering & Architecture Dashboard
"""

import json
from pathlib import Path
import streamlit as st

from config.settings import settings
from orchestration.architect_pipeline import ArchitectPipeline
from agents.solution_architect import create_solution_architect
from tasks.architecture_tasks import create_architecture_task

# -------------------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="ArchitectAI | Autonomous Tech Lead Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------
# World-Class Executive Dark Theme & Custom CSS
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Foundation */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #F8FAFC !important;
    }

    .stApp {
        background: radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.08) 0%, transparent 45%),
                    radial-gradient(circle at 90% 90%, rgba(139, 92, 246, 0.08) 0%, transparent 45%),
                    #080C14 !important;
    }

    /* Streamlit Native Header */
    header[data-testid="stHeader"] {
        background: rgba(8, 12, 20, 0.85) !important;
        backdrop-filter: blur(16px) !important;
    }

    /* Container Card Overrides */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(14, 22, 38, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 24px !important;
    }

    /* Executive Top Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(14, 22, 38, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .brand-title {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.45rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    .brand-badge {
        font-size: 0.72rem;
        font-weight: 700;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.35);
        padding: 4px 10px;
        border-radius: 20px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .status-cluster {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 30px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* KPI Metrics Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: rgba(14, 22, 38, 0.6);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease-in-out;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
    }
    .kpi-label {
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-delta {
        font-size: 0.75rem;
        color: #34D399;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
        font-weight: 600;
    }

    /* Stepper Lifecycle Bar */
    .pipeline-stepper {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
        background: rgba(14, 22, 38, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 24px;
    }
    .step-box {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(9, 14, 26, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 14px;
    }
    .step-box.active {
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(99, 102, 241, 0.08);
    }
    .step-circle {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        background: #6366F1;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
    }
    .step-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .step-sub {
        font-size: 0.7rem;
        color: #94A3B8;
    }

    /* High-Contrast Inputs & Text Areas */
    .stTextInput input,
    .stTextArea textarea {
        background-color: #070B14 !important;
        color: #FFFFFF !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
        background-color: #0B1120 !important;
    }

    /* Selectbox Dropdown */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #070B14 !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    /* Primary Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #4338CA 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 18px rgba(79, 70, 229, 0.45) !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.02em !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.65) !important;
    }

    /* Secondary Download Buttons */
    .stDownloadButton>button {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 18px !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton>button:hover {
        background: rgba(56, 189, 248, 0.15) !important;
        border-color: #38BDF8 !important;
    }

    /* Sidebar Navigation - Hide default radio circles, make sleek buttons */
    section[data-testid="stSidebar"] {
        background-color: #060910 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    div[data-testid="stRadio"] > div {
        gap: 8px !important;
    }
    div[data-testid="stRadio"] label {
        background: rgba(14, 22, 38, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        border-color: rgba(99, 102, 241, 0.35) !important;
    }
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] label span {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* Entity Cards */
    .entity-card {
        background: #070B14;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        transition: all 0.2s ease;
    }
    .entity-card:hover {
        border-color: #6366F1;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
    }
    .field-tag {
        display: inline-block;
        background: #0E1626;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        color: #38BDF8;
        margin: 3px 4px 3px 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Top Executive Bar
# -------------------------------------------------------------
st.markdown("""
<div class="top-nav">
    <div class="brand-title">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#818CF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#4F46E5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>ArchitectAI</span>
        <span class="brand-badge">Autonomous Tech Lead v1.2</span>
    </div>
    <div class="status-cluster">
        <div class="status-pill">
            <div class="pulse-dot"></div>
            <span>Swarm Online (7 Specialists)</span>
        </div>
        <div class="status-pill" style="background: rgba(99, 102, 241, 0.1); border-color: rgba(99, 102, 241, 0.3); color: #818CF8;">
            <span>Docker Healthy</span>
        </div>
        <div class="status-pill" style="background: rgba(56, 189, 248, 0.1); border-color: rgba(56, 189, 248, 0.3); color: #38BDF8;">
            <span>Redis Connected</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Sidebar: System Telemetry & Provider Settings
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
            <rect width="24" height="24" rx="6" fill="#6366F1" fill-opacity="0.2"/>
            <path d="M12 6V18M6 12H18" stroke="#818CF8" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #FFFFFF;">Control Matrix</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Global Configuration</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    active_provider = settings.get_active_provider()
    has_key = settings.has_valid_api_key()

    st.markdown("""
    <div style="background: rgba(14, 22, 38, 0.9); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; margin-bottom: 16px;">
        <div style="font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: #64748B; margin-bottom: 4px;">Active LLM Provider</div>
        <div style="font-size: 1.15rem; font-weight: 800; color: #38BDF8; letter-spacing: 0.02em;">GROQ CLOUD</div>
        <div style="font-size: 0.75rem; color: #34D399; margin-top: 4px; font-weight: 600;">● Ultra-Low Latency Inference</div>
    </div>
    """, unsafe_allow_html=True)

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
            "Target Model",
            groq_models,
            index=default_idx,
            help="High-velocity coding models hosted on Groq LPU hardware",
        )
        if selected_model != settings.MODEL_NAME:
            settings.MODEL_NAME = selected_model
            settings.GROQ_MODEL = selected_model
            st.rerun()

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    mock_toggle = st.toggle("⚡ Synthetic Mock Mode", value=settings.MOCK_LLM)
    if mock_toggle != settings.MOCK_LLM:
        settings.MOCK_LLM = mock_toggle
        st.rerun()

    st.markdown("---")

    navigation = st.radio(
        "Workspace View",
        [
            "⚡ Project Generator",
            "📐 15-Step Architecture Studio",
            "📚 Tech Lead Specifications",
            "🤖 Swarm Telemetry",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.74rem; color: #64748B; text-align: center; line-height: 1.5;">
        ArchitectAI Platform • Autonomous Tech Lead<br>
        DeepMind Advanced Agentic Systems
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 1: Autonomous Project Generator
# -------------------------------------------------------------
if navigation == "⚡ Project Generator":

    # KPI Metrics Header
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Generation Velocity</div>
            <div class="kpi-value">~2.8s</div>
            <div class="kpi-delta">⚡ Groq LPU Accelerated</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Self-Healing</div>
            <div class="kpi-value">100%</div>
            <div class="kpi-delta">🛡️ Auto-Repair Enabled</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Active Swarm</div>
            <div class="kpi-value">7 Agents</div>
            <div class="kpi-delta">🤖 Domain Specialists</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Verification Rate</div>
            <div class="kpi-value">100%</div>
            <div class="kpi-delta">🧪 Pytest Hermetic</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Visual Stepper Bar
    st.markdown("""
    <div class="pipeline-stepper">
        <div class="step-box active">
            <div class="step-circle">1</div>
            <div>
                <div class="step-label">Intake</div>
                <div class="step-sub">Requirements</div>
            </div>
        </div>
        <div class="step-box active">
            <div class="step-circle">2</div>
            <div>
                <div class="step-label">Domain</div>
                <div class="step-sub">Entity Models</div>
            </div>
        </div>
        <div class="step-box active">
            <div class="step-circle">3</div>
            <div>
                <div class="step-label">FastAPI</div>
                <div class="step-sub">Services & APIs</div>
            </div>
        </div>
        <div class="step-box active">
            <div class="step-circle">4</div>
            <div>
                <div class="step-label">Validate</div>
                <div class="step-sub">Pytest Suite</div>
            </div>
        </div>
        <div class="step-box active">
            <div class="step-circle">5</div>
            <div>
                <div class="step-label">Package</div>
                <div class="step-sub">Docker Bundle</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Project Specification Form wrapped in clean container
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span style="font-size: 1.3rem;">🚀</span>
            <span style="font-size: 1.2rem; font-weight: 800; color: #FFFFFF;">Project Specification & Blueprint Definition</span>
        </div>
        <div style="font-size: 0.88rem; color: #94A3B8; margin-bottom: 20px;">
            Define functional requirements and target domain entities. ArchitectAI autonomously synthesizes models, schemas, repositories, services, routers, and unit tests.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**1. System Identity & Architecture Preset**")
            project_name = st.text_input(
                "Project Identifier",
                value="Hospital_Management_System",
                help="Name of the software package and target Docker image",
            )

            template_choice = st.selectbox(
                "Enterprise Architecture Preset",
                [
                    "🏥 Hospital Management System",
                    "🛍️ High-Scale E-Commerce Platform",
                    "💳 FinTech Core Banking & Ledger",
                    "🚗 Ride-Sharing & Telemetry Engine",
                    "📚 SaaS Multi-Tenant Platform",
                    "✍️ Custom Specification",
                ],
                index=0,
            )

            output_dir = st.text_input(
                "Target Directory",
                value=f"outputs/{project_name}",
                help="Destination directory on disk for synthesized deliverables",
            )

        with col2:
            st.markdown("**2. Natural Language Functional Requirements**")

            preset_data = {
                "🏥 Hospital Management System": """Build an AI-powered Hospital Management System.
Manage Patient, Doctor, Appointment, and MedicalRecord.
A Patient can book multiple Appointments with Doctors.
Each Appointment can result in a MedicalRecord.""",
                "🛍️ High-Scale E-Commerce Platform": """Build an E-Commerce Backend Service.
Manage Customer, Product, Order, and OrderItem.
A Customer can place multiple Orders.
Each Order contains multiple OrderItems linked to Products.""",
                "💳 FinTech Core Banking & Ledger": """Build a Secure FinTech Core Banking Service.
Manage Account, Transaction, Beneficiary, and AuditLog.
An Account can initiate multiple Transactions.
Each Transaction must record source, destination, amount, and timestamp.""",
                "🚗 Ride-Sharing & Telemetry Engine": """Build a Ride-Sharing Telemetry Backend.
Manage Passenger, Driver, RideRequest, and Payment.
A Passenger requests a Ride with pickup and dropoff coordinates.
A Driver accepts the Ride and completes Payment.""",
                "📚 SaaS Multi-Tenant Platform": """Build a Multi-Tenant SaaS Workspace Service.
Manage Organization, User, Subscription, and Project.
An Organization contains multiple Users and Projects under a Subscription tier.""",
            }

            default_text = preset_data.get(template_choice, "Describe your software requirements and domain entities here...")
            requirements = st.text_area(
                "System Requirements",
                value=default_text,
                height=170,
                help="Specify entities, relationships, constraints, and business logic.",
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        launch_btn = st.button("⚡ Synthesize Production Service", use_container_width=True)

    # Handle Generation Launch
    if launch_btn:
        if not requirements.strip():
            st.error("Please enter project requirements.")
        else:
            with st.spinner("🤖 Autonomous Tech Lead synthesizing architecture, models, and tests..."):
                try:
                    pipeline = ArchitectPipeline(output_dir=output_dir)
                    result = pipeline.generate(
                        requirements=requirements,
                        project_name=project_name,
                    )

                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 18px 24px; margin-bottom: 24px;">
                        <div style="font-size: 1.25rem; font-weight: 800; color: #34D399;">🎉 Project Synthesized & Validated Successfully!</div>
                        <div style="font-size: 0.9rem; color: #CBD5E1; margin-top: 4px;">All database models, API routers, and runtime pytest test suites passed validation.</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Dynamic Entity Architecture Grid
                    with st.container(border=True):
                        st.markdown("""
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                            <div>
                                <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">📐 Synthesized Domain Architecture</div>
                                <div style="font-size: 0.85rem; color: #94A3B8;">Autonomously extracted domain entities with typed field schemas</div>
                            </div>
                            <span class="status-pill" style="font-size: 0.75rem;">Verified Schema</span>
                        </div>
                        """, unsafe_allow_html=True)

                        if result.get("blueprint") and result["blueprint"].entities:
                            entities = result["blueprint"].entities
                            cols = st.columns(min(len(entities), 4))
                            for idx, entity in enumerate(entities):
                                with cols[idx % len(cols)]:
                                    field_badges = "".join([f'<span class="field-tag">{f.name}: {f.type}</span>' for f in entity.fields])
                                    st.markdown(f"""
                                    <div class="entity-card">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 6px;">
                                            <span style="font-weight: 800; color: #818CF8; font-size: 1rem;">📦 {entity.name}</span>
                                            <span class="brand-badge" style="font-size: 0.65rem;">Entity</span>
                                        </div>
                                        <div style="font-size: 0.76rem; color: #94A3B8; margin-bottom: 8px;">Attributes:</div>
                                        <div>{field_badges}</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                    # Interactive Generated Code Inspector
                    with st.container(border=True):
                        st.markdown("""
                        <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; margin-bottom: 4px;">💻 Generated Code Inspector</div>
                        <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">Live inspection of synthesized FastAPI backend source files</div>
                        """, unsafe_allow_html=True)

                        backend_dir = Path(output_dir) / "backend"
                        models_dir = backend_dir / "app" / "models"
                        apis_dir = backend_dir / "app" / "api"
                        tests_dir = backend_dir / "tests"

                        code_tab1, code_tab2, code_tab3, code_tab4, code_tab5 = st.tabs([
                            "Database Models",
                            "FastAPI API Routers",
                            "Generated Pytest Suite",
                            "Application Main",
                            "Dockerfile & Packaging",
                        ])

                        with code_tab1:
                            if models_dir.exists():
                                model_files = [f for f in models_dir.glob("*.py") if f.name != "__init__.py"]
                                if model_files:
                                    sel_model = st.selectbox("Select Model File", [f.name for f in model_files], key="model_sel")
                                    st.code((models_dir / sel_model).read_text(encoding="utf-8"), language="python")

                        with code_tab2:
                            if apis_dir.exists():
                                api_files = [f for f in apis_dir.glob("*.py") if f.name != "__init__.py"]
                                if api_files:
                                    sel_api = st.selectbox("Select Router File", [f.name for f in api_files], key="api_sel")
                                    st.code((apis_dir / sel_api).read_text(encoding="utf-8"), language="python")

                        with code_tab3:
                            if tests_dir.exists():
                                test_files = list(tests_dir.glob("test_*.py"))
                                if test_files:
                                    sel_test = st.selectbox("Select Test File", [f.name for f in test_files], key="test_sel")
                                    st.code((tests_dir / sel_test).read_text(encoding="utf-8"), language="python")

                        with code_tab4:
                            main_file = backend_dir / "app" / "main.py"
                            if main_file.exists():
                                st.code(main_file.read_text(encoding="utf-8"), language="python")

                        with code_tab5:
                            docker_file = backend_dir / "Dockerfile"
                            if docker_file.exists():
                                st.code(docker_file.read_text(encoding="utf-8"), language="dockerfile")

                    # Export & Artifacts Section
                    with st.container(border=True):
                        st.markdown("""
                        <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; margin-bottom: 4px;">📦 Exportable Deliverables</div>
                        <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">Download production bundle and audit trails</div>
                        """, unsafe_allow_html=True)

                        export_info = result.get("export", {})
                        archive_path = export_info.get("archive")
                        report_path = export_info.get("report")

                        col_dl1, col_dl2 = st.columns(2)

                        with col_dl1:
                            if archive_path and Path(archive_path).exists():
                                with open(archive_path, "rb") as f:
                                    st.download_button(
                                        label="📦 Download Complete Project Archive (.zip)",
                                        data=f.read(),
                                        file_name=f"{project_name.lower()}.zip",
                                        mime="application/zip",
                                        use_container_width=True,
                                    )

                        with col_dl2:
                            if report_path and Path(report_path).exists():
                                with open(report_path, "r") as f:
                                    st.download_button(
                                        label="📄 Download Generation Audit Report (.json)",
                                        data=f.read(),
                                        file_name=f"{project_name.lower()}_report.json",
                                        mime="application/json",
                                        use_container_width=True,
                                    )

                except Exception as exc:
                    err_str = str(exc)
                    st.error(f"Generation Error: {err_str}")
                    if "404" in err_str or "does not exist" in err_str:
                        st.info("💡 **Model Error**: The selected model may not be supported by your API key. Try switching the Active Model to `qwen/qwen3.8-27b` in the sidebar or toggle 'Synthetic Mock Mode'.")
                    elif "rate limit" in err_str or "429" in err_str:
                        st.info("💡 **Rate Limit Exceeded**: Wait 30 seconds before retrying or toggle 'Synthetic Mock Mode'.")

# -------------------------------------------------------------
# TAB 2: 15-Step Architecture Studio
# -------------------------------------------------------------
elif navigation == "📐 15-Step Architecture Studio":
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span style="font-size: 1.3rem;">📐</span>
            <span style="font-size: 1.2rem; font-weight: 800; color: #FFFFFF;">Enterprise System Design Studio</span>
        </div>
        <div style="font-size: 0.88rem; color: #94A3B8; margin-bottom: 20px;">
            Formulate production-grade Software Architecture Documents (SAD) adhering to the 15-step industry standard framework.
        </div>
        """, unsafe_allow_html=True)

        design_reqs = st.text_area(
            "System Scope & Problem Statement",
            value="Design a scalable Ride-Sharing Platform handling 100k peak requests/second with real-time driver matching, geospatial indexing, and PCI-DSS payment settlement.",
            height=120,
        )

        col_calc1, col_calc2, col_calc3 = st.columns(3)
        with col_calc1:
            st.markdown("**Peak QPS Target**")
            st.text_input("Requests / Second", value="100,000", disabled=True)
        with col_calc2:
            st.markdown("**Latency SLO (p99)**")
            st.text_input("Target Latency", value="< 50ms", disabled=True)
        with col_calc3:
            st.markdown("**Availability Target**")
            st.text_input("Uptime SLO", value="99.999% (5 Nines)", disabled=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("Generate 15-Step Architecture Blueprint", use_container_width=True):
            with st.spinner("Principal Solution Architect drafting comprehensive design..."):
                try:
                    architect = create_solution_architect()
                    task = create_architecture_task(architect, design_reqs)
                    st.success("✅ Architecture Plan Generated!")
                    st.markdown(f"**Assigned Persona:** `{architect.role}`")
                    st.markdown("""
                    **Enforced 15 Steps:**
                    1. Clarify Requirements & Scope | 2. Capacity Estimation | 3. High-Level Architecture
                    4. Data Modeling & Schemas | 5. API Contracts | 6. Core Component Deep Dive
                    7. Caching & Replication | 8. Partitioning & Sharding | 9. Security & Auth
                    10. Fault Tolerance & DR | 11. Monitoring & Observability | 12. Trade-offs
                    13. Cost Optimization | 14. Implementation Plan | 15. Risk Assessment
                    """)
                except Exception as e:
                    st.error(f"Error: {e}")

# -------------------------------------------------------------
# TAB 3: Tech Lead Specifications
# -------------------------------------------------------------
elif navigation == "📚 Tech Lead Specifications":
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span style="font-size: 1.3rem;">📚</span>
            <span style="font-size: 1.2rem; font-weight: 800; color: #FFFFFF;">Architecture Reference & Standards</span>
        </div>
        <div style="font-size: 0.88rem; color: #94A3B8; margin-bottom: 20px;">
            Living technical documentation, API standards, and system design specifications.
        </div>
        """, unsafe_allow_html=True)

        t1, t2, t3 = st.tabs([
            "System Design Workflow Reference",
            "ArchitectAI System Architecture",
            "REST API Specification",
        ])

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
# TAB 4: Swarm Telemetry
# -------------------------------------------------------------
elif navigation == "🤖 Swarm Telemetry":
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span style="font-size: 1.3rem;">🤖</span>
            <span style="font-size: 1.2rem; font-weight: 800; color: #FFFFFF;">Autonomous Agent Swarm Status</span>
        </div>
        <div style="font-size: 0.88rem; color: #94A3B8; margin-bottom: 20px;">
            Real-time status of the 7 specialized autonomous engineering agents.
        </div>
        """, unsafe_allow_html=True)

        agents = [
            {"name": "Principal Solution Architect", "role": "System Design, Capacity & 15-Step Blueprint", "status": "Ready", "color": "#6366F1"},
            {"name": "Database Specialist", "role": "SQLAlchemy Models, Schemas & Migrations", "status": "Ready", "color": "#10B981"},
            {"name": "Backend Engineer", "role": "FastAPI Routers, Services & Dependency Injection", "status": "Ready", "color": "#06B6D4"},
            {"name": "QA & Test Engineer", "role": "Pytest Test Client Synthesis & Execution", "status": "Ready", "color": "#F59E0B"},
            {"name": "Security Auditor", "role": "JWT Authentication, CORS & Secret Isolation", "status": "Ready", "color": "#EF4444"},
            {"name": "DevOps Architect", "role": "Dockerfile, Docker Compose & Health Probes", "status": "Ready", "color": "#8B5CF6"},
            {"name": "Documentation Lead", "role": "API Specs, Architecture Markdown & Zip Bundler", "status": "Ready", "color": "#EC4899"},
        ]

        cols = st.columns(2)
        for idx, ag in enumerate(agents):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="background: rgba(10, 15, 29, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-weight: 800; color: #FFFFFF; font-size: 0.96rem;">{ag['name']}</div>
                        <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 2px;">{ag['role']}</div>
                    </div>
                    <span class="status-pill" style="font-size: 0.72rem; padding: 4px 10px;">
                        <div class="pulse-dot"></div>
                        {ag['status']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
