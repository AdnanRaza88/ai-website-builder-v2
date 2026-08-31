import streamlit as st
from core.database import SessionLocal
from core.models import Project, ARun, AStatus
from utils.helpers import fmt_dt

st.title("Workspace")

if "selected_project_id" not in st.session_state or not st.session_state.selected_project_id:
    st.warning("Pehle Projects page se ek project select / create karo.")
    if st.button("Go to Projects"):
        st.switch_page("pages/1_Projects.py")
    st.stop()

pid = st.session_state.selected_project_id
db = SessionLocal()
proj = db.query(Project).filter(Project.id == pid, Project.owner_id == st.session_state.user["id"]).first()

if not proj:
    st.error("Project not found")
    db.close()
    st.stop()

st.subheader(proj.name)
st.caption(proj.description or "")

col1, col2, col3 = st.columns(3)
col1.metric("Status", proj.status.value if hasattr(proj.status, "value") else str(proj.status))
col2.metric("Format", proj.output_format.value if hasattr(proj.output_format, "value") else str(proj.output_format))
col3.metric("Updated", fmt_dt(proj.updated_at))

st.divider()

st.markdown("### Run Agent")
prompt = st.text_area("What do you want to build / change?", height=120, placeholder="Create a modern SaaS landing page with pricing, features and CTA...")

if st.button("Run Pipeline", type="primary", use_container_width=True):
    if not prompt.strip():
        st.error("Prompt likho")
    else:
        run = ARun(project_id=pid, status=AStatus.RUNNING, input_text=prompt)
        db.add(run)
        db.commit()
        st.success("Run started (demo mode — full LangGraph pipeline abhi connect nahi hai)")
        st.info("Full agents/graph + nodes ke saath next step mein connect karenge.")

st.divider()
st.markdown("### Recent Runs")
runs = db.query(ARun).filter(ARun.project_id == pid).order_by(ARun.created_at.desc()).limit(10).all()
if not runs:
    st.caption("No runs yet")
else:
    for r in runs:
        with st.container(border=True):
            st.markdown(f"**{r.status.value if hasattr(r.status,'value') else r.status}** · {fmt_dt(r.created_at)}")
            st.caption(r.input_text[:120] + ("..." if len(r.input_text) > 120 else ""))

db.close()
