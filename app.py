"""
ArchitectAI - Autonomous Tech Lead
Clean, aesthetic, human-first developer dashboard.
"""

from pathlib import Path
import streamlit as st

from config.settings import settings
from orchestration.architect_pipeline import ArchitectPipeline
from agents.solution_architect import create_solution_architect
from tasks.architecture_tasks import create_architecture_task

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="ArchitectAI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------
# Clean, Human, Aesthetic Design System (Inter + Slate)
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Base Reset & Typography */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 14px !important;
        color: #F8FAFC !important;
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        background-color: #0B0F19 !important;
    }

    /* Streamlit Native Header */
    header[data-testid="stHeader"] {
        background-color: rgba(11, 15, 25, 0.8) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Container Card */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
    }

    /* App Header Bar */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 24px;
    }
    .app-logo {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .app-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }
    .app-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 400;
        margin-left: 4px;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34D399;
        font-size: 0.78rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 20px;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #10B981;
        border-radius: 50%;
    }

    /* Form Labels & Text */
    label, 
    .stWidgetLabel p, 
    [data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }
    .stMarkdown p {
        font-size: 0.9rem !important;
        color: #94A3B8 !important;
        line-height: 1.5 !important;
    }

    /* Input Fields & Textareas */
    .stTextInput input,
    .stTextArea textarea {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        padding: 10px 12px !important;
        font-family: inherit !important;
    }
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.84rem !important;
        line-height: 1.6 !important;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        background-color: #131D31 !important;
    }

    /* Selectboxes */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-size: 0.88rem !important;
    }

    /* Primary Button */
    .stButton>button {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        transition: all 0.15s ease !important;
    }
    .stButton>button:hover {
        background-color: #4338CA !important;
        transform: translateY(-1px) !important;
    }
    .stButton>button:active {
        transform: translateY(0) !important;
    }

    /* Download Button */
    .stDownloadButton>button {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        padding: 9px 16px !important;
    }
    .stDownloadButton>button:hover {
        background-color: #334155 !important;
        border-color: #475569 !important;
    }

    /* Sidebar Navigation */
    section[data-testid="stSidebar"] {
        background-color: #0E1422 !important;
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
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* Entity Cards */
    .entity-item {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .entity-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #818CF8;
        margin-bottom: 8px;
    }
    .field-pill {
        display: inline-block;
        background-color: #1E293B;
        border-radius: 4px;
        padding: 2px 6px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        color: #93C5FD;
        margin: 2px 4px 2px 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Top Header Bar
# -------------------------------------------------------------
st.markdown("""
<div class="app-header">
    <div class="app-logo">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#818CF8" stroke-width="2" stroke-linecap="round"/>
            <path d="M2 17L12 22L22 17" stroke="#6366F1" stroke-width="2" stroke-linecap="round"/>
            <path d="M2 12L12 17L22 12" stroke="#4F46E5" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span class="app-title">ArchitectAI</span>
        <span class="app-subtitle">· Autonomous Tech Lead</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <span class="status-badge">
            <span class="status-dot"></span>
            System Ready
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("**Navigation**")
    navigation = st.radio(
        "Navigation",
        [
            "⚡ Project Generator",
            "📐 System Architecture",
            "📖 Technical Docs",
            "🤖 Agent Swarm",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Environment**")

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
            label_visibility="collapsed",
        )
        if selected_model != settings.MODEL_NAME:
            settings.MODEL_NAME = selected_model
            settings.GROQ_MODEL = selected_model
            st.rerun()

    mock_toggle = st.toggle("Offline / Test Mode", value=settings.MOCK_LLM)
    if mock_toggle != settings.MOCK_LLM:
        settings.MOCK_LLM = mock_toggle
        st.rerun()

    st.markdown("---")
    st.caption("ArchitectAI v1.2 · Python 3.12 · Docker")

# -------------------------------------------------------------
# VIEW 1: Project Generator
# -------------------------------------------------------------
if navigation == "⚡ Project Generator":
    with st.container(border=True):
        st.markdown("### Generate Backend Project")
        st.markdown("Enter your requirements below. ArchitectAI will automatically design domain models, build FastAPI routers, write repositories, synthesize unit tests, and validate the code.")

        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            st.markdown("**Configuration**")
            project_name = st.text_input(
                "Project Name",
                value="Hospital_Management_System",
                help="Name of the backend service package",
            )

            template_choice = st.selectbox(
                "Template",
                [
                    "Hospital Management System",
                    "E-Commerce Platform",
                    "FinTech Banking Ledger",
                    "Ride-Sharing Telemetry",
                    "Custom Requirements",
                ],
                index=0,
            )

            output_dir = st.text_input(
                "Output Directory",
                value=f"outputs/{project_name}",
            )

        with col2:
            st.markdown("**Requirements**")

            preset_data = {
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

            default_text = preset_data.get(template_choice, "Describe your software requirements and domain entities here...")
            requirements = st.text_area(
                "Requirements Description",
                value=default_text,
                height=160,
                label_visibility="collapsed",
            )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        col_btn, _ = st.columns([1, 3])
        with col_btn:
            launch_btn = st.button("Generate Project →", type="primary", use_container_width=True)

    if launch_btn:
        if not requirements.strip():
            st.error("Please enter project requirements.")
        else:
            with st.spinner("Analyzing requirements and generating backend..."):
                try:
                    pipeline = ArchitectPipeline(output_dir=output_dir)
                    result = pipeline.generate(
                        requirements=requirements,
                        project_name=project_name,
                    )

                    st.success("✓ Project generated and validated successfully")

                    # Entities
                    with st.container(border=True):
                        st.markdown("#### Domain Entities")
                        if result.get("blueprint") and result["blueprint"].entities:
                            entities = result["blueprint"].entities
                            cols = st.columns(min(len(entities), 3))
                            for idx, entity in enumerate(entities):
                                with cols[idx % len(cols)]:
                                    field_pills = "".join([f'<span class="field-pill">{f.name}: {f.type}</span>' for f in entity.fields])
                                    st.markdown(f"""
                                    <div class="entity-item">
                                        <div class="entity-name">{entity.name}</div>
                                        <div>{field_pills}</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                    # Code Explorer
                    with st.container(border=True):
                        st.markdown("#### Code Explorer")
                        backend_dir = Path(output_dir) / "backend"
                        models_dir = backend_dir / "app" / "models"
                        apis_dir = backend_dir / "app" / "api"
                        tests_dir = backend_dir / "tests"

                        t_models, t_api, t_tests, t_main, t_docker = st.tabs([
                            "Models",
                            "API Endpoints",
                            "Tests",
                            "main.py",
                            "Dockerfile",
                        ])

                        with t_models:
                            if models_dir.exists():
                                files = [f.name for f in models_dir.glob("*.py") if f.name != "__init__.py"]
                                if files:
                                    s_file = st.selectbox("Select Model", files, key="mod_sel")
                                    st.code((models_dir / s_file).read_text(encoding="utf-8"), language="python")

                        with t_api:
                            if apis_dir.exists():
                                files = [f.name for f in apis_dir.glob("*.py") if f.name != "__init__.py"]
                                if files:
                                    s_file = st.selectbox("Select Endpoint", files, key="api_sel")
                                    st.code((apis_dir / s_file).read_text(encoding="utf-8"), language="python")

                        with t_tests:
                            if tests_dir.exists():
                                files = [f.name for f in tests_dir.glob("test_*.py")]
                                if files:
                                    s_file = st.selectbox("Select Test", files, key="test_sel")
                                    st.code((tests_dir / s_file).read_text(encoding="utf-8"), language="python")

                        with t_main:
                            main_p = backend_dir / "app" / "main.py"
                            if main_p.exists():
                                st.code(main_p.read_text(encoding="utf-8"), language="python")

                        with t_docker:
                            docker_p = backend_dir / "Dockerfile"
                            if docker_p.exists():
                                st.code(docker_p.read_text(encoding="utf-8"), language="dockerfile")

                    # Downloads
                    with st.container(border=True):
                        st.markdown("#### Export Deliverables")
                        export_info = result.get("export", {})
                        archive_path = export_info.get("archive")
                        report_path = export_info.get("report")

                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            if archive_path and Path(archive_path).exists():
                                with open(archive_path, "rb") as f:
                                    st.download_button(
                                        label="Download project package (.zip)",
                                        data=f.read(),
                                        file_name=f"{project_name.lower()}.zip",
                                        mime="application/zip",
                                        use_container_width=True,
                                    )
                        with col_dl2:
                            if report_path and Path(report_path).exists():
                                with open(report_path, "r") as f:
                                    st.download_button(
                                        label="Download audit report (.json)",
                                        data=f.read(),
                                        file_name=f"{project_name.lower()}_report.json",
                                        mime="application/json",
                                        use_container_width=True,
                                    )

                except Exception as exc:
                    st.error(f"Error: {exc}")

# -------------------------------------------------------------
# VIEW 2: System Architecture Studio
# -------------------------------------------------------------
elif navigation == "📐 System Architecture":
    with st.container(border=True):
        st.markdown("### System Architecture Studio")
        st.markdown("Draft comprehensive Software Architecture Documents (SAD) using the 15-step reference framework.")

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
        st.markdown("### Specifications & Guides")
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
        st.markdown("### Specialized Engineering Agents")
        st.markdown("ArchitectAI coordinates seven specialized agent personas during the build lifecycle.")

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
                <div style="background-color: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                    <div style="font-weight: 600; color: #FFFFFF; font-size: 0.9rem;">{name}</div>
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
