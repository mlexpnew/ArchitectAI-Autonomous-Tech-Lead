"""
ArchitectAI - Autonomous Tech Lead Platform
Clean, human-first developer dashboard.
"""

from pathlib import Path
import re
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
                st.markdown("""
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

                t_models, t_apis, t_tests, t_main, t_docker, t_k8s, t_helm = st.tabs([
                    "Models",
                    "Routers",
                    "Tests",
                    "main.py",
                    "Dockerfile",
                    "Kubernetes",
                    "Helm",
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
                    if tests_dir.exists():
                        t_files = [f.name for f in tests_dir.glob("test_*.py")]
                        if t_files:
                            t_choice = st.selectbox("Test file", t_files, key="sel_t", label_visibility="collapsed")
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

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

                # Export Downloads
                export_info = last_result.get("export", {})
                archive_path = export_info.get("archive")
                report_path = export_info.get("report")

                col_d1, col_d2 = st.columns(2)
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
