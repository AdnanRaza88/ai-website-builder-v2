import streamlit as st
from core.database import init_db, SessionLocal
from core.auth import auth_user, create_user, make_token, decode_token
from core.seed import seed_db
from core.models import User

st.set_page_config(page_title="Agentic Builder", page_icon="", layout="wide", initial_sidebar_state="expanded")

init_db()
db = SessionLocal()
seed_db(db)
db.close()

if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Persistent auth via localStorage + query_params sync
st.components.v1.html("""
<script>
const params = new URLSearchParams(window.location.search);
const tokenFromUrl = params.get("_t");
if (tokenFromUrl) {
    localStorage.setItem("ab_token", tokenFromUrl);
    params.delete("_t");
    window.history.replaceState({}, "", window.location.pathname + "?" + params.toString());
} else {
    const saved = localStorage.getItem("ab_token");
    if (saved) {
        params.set("_t", saved);
        window.history.replaceState({}, "", window.location.pathname + "?" + params.toString());
    }
}
</script>
""", height=0)

# Restore from query params if present
qp = st.query_params
if "_t" in qp and not st.session_state.auth_token:
    t = qp["_t"]
    payload = decode_token(t)
    if payload:
        st.session_state.auth_token = t
        db = SessionLocal()
        u = db.query(User).filter(User.id == payload.get("sub")).first()
        db.close()
        if u:
            st.session_state.user = {"id": u.id, "email": u.email, "display_name": u.display_name}

# Theme CSS
THEMES = {
    "dark": {
        "bg": "#0b0f19", "bg2": "#111827", "card": "rgba(30, 41, 59, 0.6)",
        "text": "#f8fafc", "text2": "#94a3b8", "border": "rgba(148, 163, 184, 0.15)",
        "accent": "#6366f1", "accent2": "#4f46e5", "glass": "rgba(17, 24, 39, 0.7)",
        "shadow": "0 8px 32px rgba(0,0,0,0.4)", "input_bg": "rgba(30, 41, 59, 0.5)",
    },
    "light": {
        "bg": "#f8fafc", "bg2": "#f1f5f9", "card": "rgba(255, 255, 255, 0.7)",
        "text": "#0f172a", "text2": "#475569", "border": "rgba(148, 163, 184, 0.25)",
        "accent": "#4f46e5", "accent2": "#4338ca", "glass": "rgba(255, 255, 255, 0.7)",
        "shadow": "0 8px 32px rgba(0,0,0,0.1)", "input_bg": "rgba(255, 255, 255, 0.6)",
    },
}

t = THEMES[st.session_state.theme]

css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {{ font-family: 'Inter', sans-serif !important; }}

.stApp {{
    background: {t['bg']};
    background-image: radial-gradient(circle at 20% 50%, rgba(99,102,241,0.08) 0%, transparent 50%),
                      radial-gradient(circle at 80% 20%, rgba(139,92,246,0.06) 0%, transparent 50%);
    color: {t['text']};
}}

.glass {{
    background: {t['glass']};
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid {t['border']};
    border-radius: 16px;
    box-shadow: {t['shadow']};
}}

.glass-card {{
    background: {t['card']};
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid {t['border']};
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}}

.glass-card:hover {{
    border-color: {t['accent']}40;
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}}

.glass-input {{
    background: {t['input_bg']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    color: {t['text']} !important;
    backdrop-filter: blur(10px);
}}

.stButton > button {{
    background: linear-gradient(135deg, {t['accent']}, {t['accent2']}) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px {t['accent']}40 !important;
}}

.stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 20px {t['accent']}60 !important;
}}

.stButton > button:active {{
    transform: translateY(0);
}}

h1, h2, h3, h4, h5, h6 {{
    color: {t['text']} !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: transparent !important;
}}

.stTabs [data-baseweb="tab"] {{
    background: {t['input_bg']} !important;
    border-radius: 10px !important;
    color: {t['text2']} !important;
    border: 1px solid {t['border']} !important;
    backdrop-filter: blur(10px);
}}

.stTabs [aria-selected="true"] {{
    background: {t['accent']} !important;
    color: white !important;
    border-color: {t['accent']} !important;
}}

.status-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}

.status-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}}

pre, code {{
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    background: {t['bg2']} !important;
    border-radius: 8px !important;
}}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {{
    background: {t['input_bg']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    color: {t['text']} !important;
    backdrop-filter: blur(10px);
}}

.stMarkdown hr {{
    border-color: {t['border']} !important;
}}

[data-testid="stSidebar"] {{
    background: {t['glass']} !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid {t['border']} !important;
}}

[data-testid="stSidebarNav"] {{
    background: transparent !important;
}}

[data-testid="stSidebarUserContent"] {{
    padding-top: 1rem !important;
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


def login(email, password):
    db = SessionLocal()
    try:
        u = auth_user(db, email, password)
        if u:
            tok = make_token({"sub": u.id, "email": u.email})
            st.session_state.auth_token = tok
            st.session_state.user = {"id": u.id, "email": u.email, "display_name": u.display_name}
            st.query_params["_t"] = tok
            return True
        return False
    finally:
        db.close()


def signup(email, password, name):
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email.lower().strip()).first():
            return False, "Email already registered"
        u = create_user(db, email, password, name)
        tok = make_token({"sub": u.id, "email": u.email})
        st.session_state.auth_token = tok
        st.session_state.user = {"id": u.id, "email": u.email, "display_name": u.display_name}
        st.query_params["_t"] = tok
        return True, ""
    except Exception as e:
        return False, str(e)
    finally:
        db.close()


def logout():
    st.session_state.auth_token = None
    st.session_state.user = None
    st.query_params.clear()
    st.components.v1.html("<script>localStorage.removeItem('ab_token');</script>", height=0)
    st.rerun()


def require_auth():
    if not st.session_state.auth_token:
        return False
    payload = decode_token(st.session_state.auth_token)
    if not payload:
        st.session_state.auth_token = None
        st.session_state.user = None
        return False
    return True


if not require_auth():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
        with st.container():
            st.markdown(f"""
            <div class="glass" style="padding: 3rem; text-align: center;">
                <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, {t['accent']}, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Agentic Builder</h1>
                <p style="color: {t['text2']}; font-size: 1.1rem; margin-bottom: 2rem;">AI-powered website generation platform</p>
            </div>
            """, unsafe_allow_html=True)

            tab1, tab2 = st.tabs(["Sign In", "Create Account"])
            with tab1:
                with st.form("login"):
                    em = st.text_input("Email", placeholder="you@example.com")
                    pw = st.text_input("Password", type="password")
                    if st.form_submit_button("Sign In", use_container_width=True):
                        if login(em, pw):
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
            with tab2:
                with st.form("signup"):
                    se = st.text_input("Email", placeholder="you@example.com", key="se")
                    sn = st.text_input("Display Name", placeholder="John Doe")
                    sp = st.text_input("Password", type="password", key="sp")
                    sp2 = st.text_input("Confirm Password", type="password", key="sp2")
                    if st.form_submit_button("Create Account", use_container_width=True):
                        if sp != sp2:
                            st.error("Passwords do not match")
                        elif len(sp) < 6:
                            st.error("Minimum 6 characters")
                        else:
                            ok, msg = signup(se, sp, sn)
                            if ok:
                                st.rerun()
                            else:
                                st.error(msg)
    st.stop()

with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1rem 0;">
        <p style="font-weight: 700; font-size: 1.1rem; margin: 0;">{st.session_state.user.get('display_name', 'User')}</p>
        <p style="color: {t['text2']}; font-size: 0.8rem; margin: 0;">{st.session_state.user['email']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    if st.button("Toggle Theme", use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

    st.divider()

    pages = {
        "Workspace": st.Page("pages/0_Workspace.py", title="Workspace", default=True),
        "Projects": st.Page("pages/1_Projects.py", title="Projects"),
        "Providers": st.Page("pages/2_Providers.py", title="Providers"),
        "Prompts": st.Page("pages/3_Prompts.py", title="Prompts"),
        "Templates": st.Page("pages/4_Templates.py", title="Templates"),
        "Settings": st.Page("pages/5_Settings.py", title="Settings"),
        "Runtime": st.Page("pages/6_Runtime.py", title="Runtime"),
        "Versions": st.Page("pages/7_Versions.py", title="Versions"),
        "MCP": st.Page("pages/8_MCP.py", title="MCP Connectors"),
    }
    pg = st.navigation(pages, position="sidebar")

    st.divider()
    if st.button("Logout", use_container_width=True):
        logout()

pg.run()
