import streamlit as st
from core.database import SessionLocal
from core.models import PKey
from core.crypto import encrypt, decrypt
from providers.registry import list_providers
from utils.helpers import mask_key, fmt_dt

st.title("Providers")
st.caption("Manage LLM API keys and providers")

if "test_result" not in st.session_state:
    st.session_state.test_result = None

def get_keys():
    db = SessionLocal()
    try:
        return db.query(PKey).filter(PKey.owner_id == st.session_state.user["id"]).all()
    finally:
        db.close()

def add_key(label, pid, base_url, api_key, model):
    db = SessionLocal()
    try:
        enc = encrypt(api_key)
        pk = PKey(
            owner_id=st.session_state.user["id"],
            label=label,
            provider_id=pid,
            base_url=base_url or None,
            key_enc=enc,
            default_model=model or None,
        )
        db.add(pk)
        db.commit()
        return True
    except Exception as e:
        st.error(str(e))
        return False
    finally:
        db.close()

def delete_key(kid):
    db = SessionLocal()
    try:
        pk = db.query(PKey).filter(PKey.id == kid, PKey.owner_id == st.session_state.user["id"]).first()
        if pk:
            db.delete(pk)
            db.commit()
    finally:
        db.close()

providers = list_providers()

tab1, tab2 = st.tabs(["My Keys", "Add New Key"])

with tab1:
    keys = get_keys()
    if not keys:
        st.info("No API keys yet. Add one in the next tab.")
    else:
        for k in keys:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{k.label}**")
                    st.caption(f"{k.provider_id} · {k.default_model or 'default model'}")
                with col2:
                    st.code(mask_key(decrypt(k.key_enc) if k.key_enc else ""), language=None)
                with col3:
                    if st.button("Delete", key=f"del_{k.id}"):
                        delete_key(k.id)
                        st.rerun()

with tab2:
    with st.form("add_key"):
        label = st.text_input("Label", placeholder="My OpenAI Key")
        pid = st.selectbox("Provider", options=list(providers.keys()) if isinstance(providers, dict) else ["openai", "anthropic", "google", "groq", "xai"])
        model = st.text_input("Default Model", placeholder="gpt-4o")
        base_url = st.text_input("Base URL (optional)", placeholder="https://api.openai.com/v1")
        api_key = st.text_input("API Key", type="password")
        if st.form_submit_button("Save Key", use_container_width=True):
            if not label or not api_key:
                st.error("Label and API Key required")
            else:
                if add_key(label, pid, base_url, api_key, model):
                    st.success("Key saved!")
                    st.rerun()
