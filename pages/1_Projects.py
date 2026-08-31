import streamlit as st
from core.database import SessionLocal
from core.models import Project, PStatus, OFormat
from utils.helpers import fmt_dt, status_color

st.title("Projects")
st.caption("Create and manage your website projects")

def get_projects():
    db = SessionLocal()
    try:
        return db.query(Project).filter(Project.owner_id == st.session_state.user["id"]).order_by(Project.updated_at.desc()).all()
    finally:
        db.close()

def create_project(name, desc, fmt):
    db = SessionLocal()
    try:
        p = Project(
            name=name,
            description=desc,
            owner_id=st.session_state.user["id"],
            status=PStatus.DRAFT,
            output_format=OFormat(fmt) if fmt else OFormat.HTML,
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    except Exception as e:
        st.error(str(e))
        return None
    finally:
        db.close()

tab1, tab2 = st.tabs(["All Projects", "New Project"])

with tab1:
    projects = get_projects()
    if not projects:
        st.info("No projects yet. Create one!")
    else:
        for p in projects:
            with st.container(border=True):
                c1, c2, c3 = st.columns([4, 2, 1])
                with c1:
                    st.markdown(f"**{p.name}**")
                    st.caption(p.description or "No description")
                with c2:
                    st.markdown(f"`{p.status.value if hasattr(p.status, 'value') else p.status}` · {p.output_format.value if hasattr(p.output_format, 'value') else p.output_format}")
                    st.caption(fmt_dt(p.updated_at))
                with c3:
                    if st.button("Open", key=f"open_{p.id}"):
                        st.session_state.selected_project_id = p.id
                        st.switch_page("pages/0_Workspace.py")

with tab2:
    with st.form("new_proj"):
        name = st.text_input("Project Name", placeholder="My SaaS Landing")
        desc = st.text_area("Description", placeholder="A modern SaaS landing page...")
        fmt = st.selectbox("Output Format", ["html", "react", "json"])
        if st.form_submit_button("Create Project", use_container_width=True):
            if not name:
                st.error("Name required")
            else:
                p = create_project(name, desc, fmt)
                if p:
                    st.success(f"Created: {p.name}")
                    st.session_state.selected_project_id = p.id
                    st.rerun()
