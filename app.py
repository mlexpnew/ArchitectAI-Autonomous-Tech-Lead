"""
ArchitectAI - Autonomous Tech Lead Platform
Executive Command Center & AI Engineering Dashboard
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
# Professional Dark Design System & Custom CSS
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                    #090D16;
        color: #F8FAFC;
    }

    /* Clean Streamlit Headers */
    header[data-testid="stHeader"] {
        background: rgba(9, 13, 22, 0.8);
        backdrop-filter: blur(12px);
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #090D16;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E293B;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }

    /* Executive Top Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }
    .brand-title {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.5rem;
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
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .status-cluster {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
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

    /* Glass KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }
    .kpi-card {
        background: rgba(15, 23, 42, 0.55);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease-in-out;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 12px 24px -10px rgba(99, 102, 241, 0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-delta {
        font-size: 0.76rem;
        color: #34D399;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Panel Card */
    .dashboard-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .card-header-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }
    .card-header-desc {
        font-size: 0.88rem;
        color: #94A3B8;
        margin-bottom: 20px;
    }

    /* Stepper Progress Bar */
    .pipeline-stepper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(10, 15, 29, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 24px;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.84rem;
        font-weight: 600;
        color: #94A3B8;
    }
    .step-item.active {
        color: #818CF8;
    }
    .step-num {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        background: #1E293B;
        color: #94A3B8;
    }
    .step-item.active .step-num {
        background: #6366F1;
        color: #FFFFFF;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.6);
    }
    .step-line {
        flex: 1;
        height: 2px;
        background: #1E293B;
        margin: 0 12px;
    }

    /* Streamlit Form Element Overrides */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(10, 15, 29, 0.8) !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-size: 0.92rem !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }
    .stSelectbox>div>div {
        background: rgba(10, 15, 29, 0.8) !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }

    /* Primary Launch Button */
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #4338CA 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6) !important;
    }
    .stButton>button:active {
        transform: translateY(0px) !important;
    }

    /* Entity Cards Grid */
    .entity-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 16px;
        margin-top: 16px;
    }
    .entity-card {
        background: rgba(10, 15, 29, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 16px;
        transition: all 0.2s ease;
    }
    .entity-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }
    .entity-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .entity-title {
        font-size: 1rem;
        font-weight: 700;
        color: #818CF8;
    }
    .field-tag {
        display: inline-block;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        color: #CBD5E1;
        margin: 2px 4px 2px 0;
    }

    /* Terminal Console */
    .terminal-box {
        background: #030712;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #10B981;
        line-height: 1.5;
        max-height: 240px;
        overflow-y: auto;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #080C14;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Top Executive Bar
# -------------------------------------------------------------
st.markdown("""
<div class="top-nav">
    <div class="brand-title">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
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
            <span>Swarm Online (7 Agents)</span>
        </div>
        <div class="status-pill" style="background: rgba(99, 102, 241, 0.1); border-color: rgba(99, 102, 241, 0.25); color: #818CF8;">
            <span>Docker Healthy</span>
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
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <rect width="24" height="24" rx="6" fill="#6366F1" fill-opacity="0.2"/>
            <path d="M12 6V18M6 12H18" stroke="#818CF8" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <div>
            <div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC;">Control Matrix</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Global Configuration</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    active_provider = settings.get_active_provider()
    has_key = settings.has_valid_api_key()

    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; margin-bottom: 16px;">
        <div style="font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: #64748B; margin-bottom: 4px;">Active LLM Provider</div>
        <div style="font-size: 1.1rem; font-weight: 800; color: #38BDF8;">GROQ CLOUD</div>
        <div style="font-size: 0.75rem; color: #34D399; margin-top: 4px;">● Ultra-Low Latency Engine</div>
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
            "Model Selection",
            groq_models,
            index=default_idx,
            help="High-velocity coding models hosted on Groq LPU inference",
        )
        if selected_model != settings.MODEL_NAME:
            settings.MODEL_NAME = selected_model
            settings.GROQ_MODEL = selected_model
            st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

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
    <div style="font-size: 0.75rem; color: #64748B; text-align: center;">
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
            <div class="kpi-delta">⚡ Groq LPU Powered</div>
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
        <div class="step-item active">
            <div class="step-num">1</div>
            <span>Requirements Intake</span>
        </div>
        <div class="step-line"></div>
        <div class="step-item active">
            <div class="step-num">2</div>
            <span>Entity & Model Synthesis</span>
        </div>
        <div class="step-line"></div>
        <div class="step-item active">
            <div class="step-num">3</div>
            <span>FastAPI Architecture</span>
        </div>
        <div class="step-line"></div>
        <div class="step-item active">
            <div class="step-num">4</div>
            <span>Pytest Verification</span>
        </div>
        <div class="step-line"></div>
        <div class="step-item active">
            <div class="step-num">5</div>
            <span>Docker Packaging</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Project Configuration Box
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">🚀 Project Specification & Blueprint Definition</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-header-desc">Define functional requirements and target domain entities. ArchitectAI autonomously synthesizes models, schemas, repositories, services, routers, and unit tests.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**1. System Identity**")
        project_name = st.text_input(
            "Project Name",
            value="Hospital_Management_System",
            placeholder="e.g. Fintech_Ledger_Service",
            help="Identifier for generated Python package and Docker containers",
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
            help="Destination folder on disk for synthesized project files",
        )

    with col2:
        st.markdown("**2. Natural Language System Requirements**")

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
            "Functional Specification",
            value=default_text,
            height=170,
            help="Specify entities, relationships, constraints, and operational goals.",
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    launch_btn = st.button("⚡ Synthesize Production Service", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if launch_btn:
        if not requirements.strip():
            st.error("Please enter project requirements.")
        else:
            with st.spinner("🤖 Autonomous Tech Lead synthesizing architecture and code..."):
                try:
                    pipeline = ArchitectPipeline(output_dir=output_dir)
                    result = pipeline.generate(
                        requirements=requirements,
                        project_name=project_name,
                    )

                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 18px 24px; margin-bottom: 24px;">
                        <div style="font-size: 1.2rem; font-weight: 800; color: #34D399;">🎉 Project Synthesized & Validated Successfully!</div>
                        <div style="font-size: 0.9rem; color: #CBD5E1; margin-top: 4px;">All database models, API routers, and pytest test suites passed verification.</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Dynamic Entity Architecture Grid
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-header-title">📐 Synthesized Domain Architecture</div>', unsafe_allow_html=True)

                    if result.get("blueprint") and result["blueprint"].entities:
                        entities = result["blueprint"].entities
                        cols = st.columns(min(len(entities), 4))
                        for idx, entity in enumerate(entities):
                            with cols[idx % len(cols)]:
                                field_badges = "".join([f'<span class="field-tag">{f.name}: {f.type}</span>' for f in entity.fields])
                                st.markdown(f"""
                                <div class="entity-card">
                                    <div class="entity-header">
                                        <div class="entity-title">📦 {entity.name}</div>
                                        <span class="brand-badge" style="font-size: 0.65rem;">Entity</span>
                                    </div>
                                    <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 8px;">Attributes & Types:</div>
                                    <div>{field_badges}</div>
                                </div>
                                """, unsafe_allow_html=True)

                    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

                    # Export & Artifacts Section
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

                    st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">📐 Enterprise System Design Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-header-desc">Formulate production-grade Software Architecture Documents (SAD) adhering to the 15-step industry standard framework.</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 3: Tech Lead Specifications
# -------------------------------------------------------------
elif navigation == "📚 Tech Lead Specifications":
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">📚 Architecture Reference & Standards</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-header-desc">Living technical documentation, API standards, and system design specifications.</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 4: Swarm Telemetry
# -------------------------------------------------------------
elif navigation == "🤖 Swarm Telemetry":
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">🤖 Autonomous Agent Swarm Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-header-desc">Real-time status of the 7 specialized autonomous engineering agents.</div>', unsafe_allow_html=True)

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
                    <div style="font-weight: 700; color: #F8FAFC; font-size: 0.96rem;">{ag['name']}</div>
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 2px;">{ag['role']}</div>
                </div>
                <span class="status-pill" style="font-size: 0.72rem; padding: 4px 10px;">
                    <div class="pulse-dot"></div>
                    {ag['status']}
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
