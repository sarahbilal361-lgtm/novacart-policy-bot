import html
import os

import streamlit as st

# On Community Cloud, keep the API key in App settings > Secrets.
# Locally, bot.py continues to load the key from the ignored .env file.
try:
    cloud_key = st.secrets.get("GEMINI_API_KEY")
    cloud_model = st.secrets.get("GEMINI_MODEL")
except Exception:
    cloud_key = None
    cloud_model = None

if cloud_key:
    os.environ["GEMINI_API_KEY"] = str(cloud_key)
if cloud_model:
    os.environ["GEMINI_MODEL"] = str(cloud_model)

from bot import ask

st.set_page_config(
    page_title="NovaCart | Policy Assistant",
    page_icon="🛍️",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --cocoa: #49352d;
        --brown: #745444;
        --beige: #f5eee3;
        --paper: #fffdf9;
        --sky: #83cfe2;
        --sky-pale: #e5f5f8;
        --maroon: #793544;
        --ink: #332720;
        --muted: #756b62;
        --line: #e5d9ca;
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 94% 4%, rgba(131,207,226,.23), transparent 28%),
            linear-gradient(180deg, #f8f3ea 0%, var(--beige) 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 850px; padding: 2.5rem 1.5rem 2rem; }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.55rem 2.7rem;
        margin-bottom: 1.35rem;
        border: 1px solid rgba(255,255,255,.16);
        border-radius: 25px;
        background: linear-gradient(118deg, #3e2d27 0%, var(--cocoa) 52%, #713c42 100%);
        box-shadow: 0 20px 48px rgba(73,53,45,.19);
        animation: rise-in .65s ease-out both;
    }
    .hero-layout {
        position: relative;
        z-index: 1;
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(150px, .6fr);
        align-items: center;
        gap: 1.1rem;
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 210px;
        height: 210px;
        right: -64px;
        top: -104px;
        border: 1px solid rgba(131,207,226,.48);
        border-radius: 50%;
        box-shadow: 0 0 0 24px rgba(131,207,226,.08), 0 0 0 50px rgba(131,207,226,.045);
        animation: drift 8s ease-in-out infinite;
    }
    .brand {
        position: relative;
        z-index: 1;
        display: inline-flex;
        align-items: center;
        gap: .55rem;
        padding: .42rem .78rem;
        border: 1px solid rgba(131,207,226,.38);
        border-radius: 999px;
        background: rgba(131,207,226,.12);
        color: #bceaf3;
        font-size: .74rem;
        font-weight: 800;
        letter-spacing: .13em;
        text-transform: uppercase;
    }
    .hero h1 {
        position: relative;
        z-index: 1;
        color: #fffaf2;
        font-size: 2.42rem;
        line-height: 1.13;
        letter-spacing: -.035em;
        margin: 1rem 0 .68rem;
    }
    .hero p {
        position: relative;
        z-index: 1;
        max-width: 570px;
        color: #eee0d4;
        font-size: 1.02rem;
        line-height: 1.65;
        margin: 0;
    }
    .hero-art {
        display: grid;
        justify-items: center;
        align-items: center;
        min-height: 170px;
        animation: drift 6s ease-in-out infinite;
    }
    .hero-art svg { width: min(100%, 190px); height: auto; filter: drop-shadow(0 13px 14px rgba(0,0,0,.18)); }
    .topic-row {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: .55rem;
        margin: .15rem 0 1.25rem;
        animation: rise-in .7s .08s ease-out both;
    }
    .topic-pill {
        padding: .48rem .78rem;
        border: 1px solid #e1d4c5;
        border-radius: 999px;
        background: rgba(255,253,249,.82);
        color: #654b3e;
        font-size: .81rem;
        font-weight: 700;
        box-shadow: 0 3px 9px rgba(73,53,45,.035);
    }
    .topics {
        color: var(--brown);
        font-size: .88rem;
        text-align: center;
        margin: .15rem 0 1.25rem;
        animation: rise-in .7s .08s ease-out both;
    }
    [data-testid="stTextInput"] label {
        color: var(--ink) !important;
        font-size: .96rem;
        font-weight: 750;
    }
    [data-testid="stTextInput"] input {
        min-height: 3.2rem;
        border: 1px solid #d8caba;
        border-radius: 13px;
        background: var(--paper);
        color: var(--ink);
        box-shadow: 0 4px 14px rgba(73,53,45,.045);
        transition: border-color .18s ease, box-shadow .18s ease;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #55b6ce;
        box-shadow: 0 0 0 .17rem rgba(131,207,226,.25);
    }
    .stButton > button {
        min-height: 3.05rem;
        border: 1px solid #682b39;
        border-radius: 13px;
        background: var(--maroon);
        color: #fffaf5;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(121,53,68,.18);
        transition: background .18s ease, transform .18s ease, box-shadow .18s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        background: #612a37;
        color: #fffaf5;
        box-shadow: 0 12px 23px rgba(121,53,68,.24);
    }
    [data-testid="stAlert"] { border-radius: 13px; }
    .chat-heading {
        color: var(--maroon);
        font-size: .76rem;
        font-weight: 850;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin: 1.75rem 0 .8rem;
    }
    .chat-row { display: flex; gap: .65rem; align-items: flex-start; margin: .8rem 0; animation: rise-in .35s ease-out both; }
    .chat-row.user { justify-content: flex-end; }
    .chat-avatar {
        display: grid;
        flex: 0 0 2rem;
        width: 2rem;
        height: 2rem;
        place-items: center;
        border-radius: 50%;
        background: var(--cocoa);
        color: #fffaf2;
        font-size: .8rem;
        font-weight: 800;
    }
    .chat-row.user .chat-avatar { order: 2; background: var(--maroon); }
    .chat-bubble {
        max-width: 86%;
        padding: .95rem 1.1rem;
        border: 1px solid var(--line);
        border-radius: 5px 16px 16px 16px;
        background: var(--paper);
        color: var(--ink);
        line-height: 1.7;
        box-shadow: 0 6px 18px rgba(73,53,45,.055);
        overflow-wrap: anywhere;
    }
    .chat-row.user .chat-bubble {
        order: 1;
        border-color: #ead6c8;
        border-radius: 16px 5px 16px 16px;
        background: #f2e6d8;
    }
    .chat-speaker { display: block; margin-bottom: .25rem; color: var(--brown); font-size: .72rem; font-weight: 850; letter-spacing: .08em; text-transform: uppercase; }
    .chat-row.assistant .chat-speaker { color: #28798a; }
    .footer {
        color: var(--muted);
        font-size: .8rem;
        text-align: center;
        margin-top: 2.1rem;
    }
    @keyframes rise-in {
        from { opacity: 0; transform: translateY(9px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes drift {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(9px) rotate(5deg); }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *:before, *:after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
    }
    @media (max-width: 600px) {
        .block-container { padding: 1.35rem 1rem 1.5rem; }
        .hero { padding: 1.85rem 1.5rem; border-radius: 19px; }
        .hero h1 { font-size: 1.95rem; }
        .hero-layout { grid-template-columns: 1fr; }
        .hero-art { display: none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="hero-layout">
        <div>
          <div class="brand">✦ &nbsp; NovaCart · Customer care</div>
          <h1>Policy answers,<br>without the guesswork.</h1>
          <p>Get clear guidance on NovaCart policies, with the supporting sections included in every answer.</p>
        </div>
        <div class="hero-art" aria-hidden="true">
          <svg viewBox="0 0 220 190" xmlns="http://www.w3.org/2000/svg" role="img">
            <circle cx="112" cy="92" r="78" fill="#83cfe2" opacity=".18"/>
            <circle cx="112" cy="92" r="63" fill="#f5eee3" opacity=".10"/>
            <path d="M48 68h124l-10 91a12 12 0 0 1-12 11H70a12 12 0 0 1-12-11L48 68Z" fill="#ead4b8"/>
            <path d="M79 73V57a31 31 0 0 1 62 0v16" fill="none" stroke="#83cfe2" stroke-width="8" stroke-linecap="round"/>
            <path d="M48 68h124" stroke="#fff5e7" stroke-width="5" stroke-linecap="round"/>
            <rect x="80" y="101" width="60" height="39" rx="9" fill="#793544"/>
            <path d="M95 120h30" stroke="#f5eee3" stroke-width="4" stroke-linecap="round"/>
            <path d="m169 46 5 10 11 2-8 8 2 11-10-5-10 5 2-11-8-8 11-2 5-10Z" fill="#83cfe2"/>
            <circle cx="48" cy="125" r="6" fill="#83cfe2"/>
            <circle cx="177" cy="143" r="4" fill="#f2c88e"/>
          </svg>
        </div>
      </div>
    </section>
    <div class="topic-row">
      <span class="topic-pill">↩ Returns</span>
      <span class="topic-pill">✦ Shipping</span>
      <span class="topic-pill">▣ Payments</span>
      <span class="topic-pill">％ Promotions</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form("question_form", clear_on_submit=True):
    question = st.text_input(
        "What can we help you with?",
        placeholder="Ask a question about a NovaCart policy…",
    )
    submitted = st.form_submit_button("Ask NovaCart", use_container_width=True)

if submitted:
    if not question.strip():
        st.warning("Enter a question to get started.")
    else:
        with st.spinner("Checking the policy files…"):
            answer = ask(question.strip())
        st.session_state.messages.append({"role": "user", "content": question.strip()})
        st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.messages:
    st.markdown('<div class="chat-heading">Conversation</div>', unsafe_allow_html=True)
    for message in st.session_state.messages:
        role = message["role"]
        label = "You" if role == "user" else "NovaCart Assistant"
        avatar = "Y" if role == "user" else "N"
        safe_text = html.escape(message["content"]).replace("\n", "<br>")
        st.markdown(
            f'<div class="chat-row {role}">'
            f'<div class="chat-avatar">{avatar}</div>'
            f'<div class="chat-bubble"><span class="chat-speaker">{label}</span>{safe_text}</div>'
            '</div>',
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="footer">NovaCart Policy Assistant &nbsp; · &nbsp; Answers grounded in policy files</div>',
    unsafe_allow_html=True,
)
