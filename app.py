"""
ArchitectAI Web Platform
Interactive Dashboard for Autonomous System Design, Code Generation, and Multi-Agent Workflows.
"""

from pathlib import Path
import streamlit as st

from config.settings import settings
from orchestration.architect_pipeline import ArchitectPipeline
from agents.solution_architect import create_solution_architect
from tasks.architecture_tasks import create_architecture_task

st.set_page_config(
    page_title="ArchitectAI - Autonomous Tech Lead",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------
# Custom Styling
# -------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Sidebar: System Configuration & Status
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/architecture.png", width=70)
    st.title("ArchitectAI")
    st.caption("Autonomous Tech Lead Platform v1.0.0")

    st.markdown("---")
    st.subheader("⚙️ LLM Provider")

    active_provider = settings.get_active_provider()
    has_key = settings.has_valid_api_key()

    st.write(f"**Provider:** `{active_provider.upper()}`")
    st.write(f"**Active Model:** `{settings.get_active_model()}`")

    if has_key:
        st.success("✅ Credentials Configured")
    else:
        st.warning("⚠️ Credentials Missing in `.env`")

    mock_toggle = st.toggle("Offline / Mock Mode", value=settings.MOCK_LLM)
    if mock_toggle != settings.MOCK_LLM:
        settings.MOCK_LLM = mock_toggle
        st.rerun()

    st.markdown("---")
    navigation = st.radio(
        "Navigation",
        [
            "🚀 Autonomous Generator",
            "📐 System Design Studio",
            "📖 Architecture & Docs",
            "✍️ Content Pipeline (Legacy)",
        ],
    )

# -------------------------------------------------------------
# TAB 1: Autonomous Project Generator
# -------------------------------------------------------------
if navigation == "🚀 Autonomous Generator":
    st.markdown('<div class="main-header">🚀 Autonomous Project Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Generate production-ready FastAPI backends from natural language specifications.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Project Configuration")
        project_name = st.text_input(
            "Project Name",
            value="Hospital_Management_System",
            help="Name of the software service to generate",
        )

        template_choice = st.selectbox(
            "Load Sample Requirements",
            [
                "Custom",
                "Hospital Management System",
                "E-Commerce Platform",
                "Library Management System",
            ],
        )

        output_dir = st.text_input(
            "Output Directory",
            value=f"outputs/{project_name}",
        )

    with col2:
        st.subheader("Requirements Specification")

        sample_reqs = {
            "Hospital Management System": """Build an AI-powered Hospital Management System.
Manage Patient, Doctor, Appointment, and MedicalRecord.
A Patient can book multiple Appointments with Doctors.
Each Appointment can result in a MedicalRecord.""",
            "E-Commerce Platform": """Build an E-Commerce Backend Service.
Manage Customer, Product, Order, and OrderItem.
A Customer can place multiple Orders.
Each Order contains multiple OrderItems linked to Products.""",
            "Library Management System": """Build a Library Management System.
Manage Member, Book, and BorrowRecord.
A Member can borrow multiple Books.
Each BorrowRecord tracks the borrowed date and returned status.""",
        }

        default_text = sample_reqs.get(template_choice, "Describe your project requirements here...")
        requirements = st.text_area(
            "Requirements",
            value=default_text,
            height=180,
        )

    st.markdown("---")

    if st.button("🏗️ Generate Production Project", type="primary", use_container_width=True):
        if not requirements.strip():
            st.error("Please provide software requirements.")
        else:
            with st.spinner("🤖 Autonomous Tech Lead executing pipeline..."):
                try:
                    pipeline = ArchitectPipeline(output_dir=output_dir)
                    result = pipeline.generate(
                        requirements=requirements,
                        project_name=project_name,
                    )

                    st.success("🎉 Project Generated and Validated Successfully!")

                    # Metrics Overview
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Validation", "PASSED" if result["validation"].get("valid") else "FAILED")
                    m2.metric("Entities", len(result["blueprint"].entities) if result.get("blueprint") else 0)
                    m3.metric("Self-Healing", "Clean" if not result.get("self_healing") else "Repaired")
                    m4.metric("Artifacts", len(result.get("artifacts", [])))

                    st.markdown("### 📋 Generated Blueprint Entities")
                    if result.get("blueprint") and result["blueprint"].entities:
                        entity_data = [
                            {"Entity": e.name, "Fields": ", ".join(f.name for f in e.fields)}
                            for e in result["blueprint"].entities
                        ]
                        st.table(entity_data)

                    # Export Download
                    export_info = result.get("export", {})
                    archive_path = export_info.get("archive")
                    if archive_path and Path(archive_path).exists():
                        with open(archive_path, "rb") as f:
                            st.download_button(
                                label="📦 Download Project Archive (.zip)",
                                data=f.read(),
                                file_name=f"{project_name}.zip",
                                mime="application/zip",
                            )

                except Exception as exc:
                    st.error(f"Generation Error: {exc}")

# -------------------------------------------------------------
# TAB 2: System Design Studio
# -------------------------------------------------------------
elif navigation == "📐 System Design Studio":
    st.markdown('<div class="main-header">📐 15-Step System Design Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enterprise system design workflow with capacity estimation, SLOs, and Mermaid diagrams.</div>', unsafe_allow_html=True)

    design_reqs = st.text_area(
        "Enter System Requirements for Architecture Design:",
        value="Design a scalable Ride-Sharing Platform handling 100k peak requests/second with real-time driver matching and payment processing.",
        height=120,
    )

    if st.button("Generate System Architecture Document", type="primary"):
        with st.spinner("Principal Solution Architect generating architecture..."):
            try:
                architect = create_solution_architect()
                task = create_architecture_task(architect, design_reqs)
                st.success("Architecture task configured based on 15-step reference workflow!")
                st.markdown(f"**Assigned Agent:** `{architect.role}`")
                st.markdown("**Expected Output Standard:** Comprehensive 15-step SAD with Mermaid diagrams.")
            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------------------------------------------
# TAB 3: Architecture & Documentation Viewer
# -------------------------------------------------------------
elif navigation == "📖 Architecture & Docs":
    st.markdown('<div class="main-header">📖 Documentation & Specifications</div>', unsafe_allow_html=True)

    doc_tab1, doc_tab2, doc_tab3 = st.tabs([
        "System Design Workflow Reference",
        "ArchitectAI System Architecture",
        "API Standards",
    ])

    with doc_tab1:
        wf_path = Path("docs/workflow.md")
        if wf_path.exists():
            st.markdown(wf_path.read_text(encoding="utf-8"))

    with doc_tab2:
        arch_path = Path("docs/architecture.md")
        if arch_path.exists():
            st.markdown(arch_path.read_text(encoding="utf-8"))

    with doc_tab3:
        api_path = Path("docs/api.md")
        if api_path.exists():
            st.markdown(api_path.read_text(encoding="utf-8"))

# -------------------------------------------------------------
# TAB 4: Legacy Content Pipeline
# -------------------------------------------------------------
elif navigation == "✍️ Content Pipeline (Legacy)":
    st.markdown('<div class="main-header">✍️ AI Agent Workflow (Content Pipeline)</div>', unsafe_allow_html=True)
    st.caption("Researcher ➔ Writer ➔ Evaluator CrewAI Pipeline")

    content_prompt = st.text_input("Enter topic:", placeholder="e.g., How AI is changing software development")
    if st.button("Run Content Crew") and content_prompt:
        try:
            from ai_workflow import run_workflow
            with st.spinner("Running agents..."):
                output = run_workflow(content_prompt)
                st.success("Workflow completed!")
                st.write(output)
        except Exception as exc:
            st.error(f"Error: {exc}")
