import html

import streamlit as st
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
        --ink: #182b3a;
        --muted: #607484;
        --teal: #087f8c;
        --teal-dark: #075e68;
        --line: #dce6eb;
        --paper: #ffffff;
    }
    [data-testid="stAppViewContainer"] {
        background: #f3f7f8;
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 850px; padding: 2.6rem 1.5rem 2rem; }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.5rem 2.7rem;
        margin-bottom: 1.4rem;
        border-radius: 24px;
        background: linear-gradient(115deg, #123d52 0%, #087f8c 68%, #13a49a 100%);
        box-shadow: 0 18px 42px rgba(18,61,82,.16);
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -75px;
        top: -110px;
        border: 1px solid rgba(255,255,255,.17);
        border-radius: 50%;
        box-shadow: 0 0 0 26px rgba(255,255,255,.05), 0 0 0 54px rgba(255,255,255,.035);
    }
    .brand {
        color: #c9f4ed;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .14em;
        text-transform: uppercase;
    }
    .hero h1 {
        position: relative;
        z-index: 1;
        color: #fff;
        font-size: 2.4rem;
        line-height: 1.14;
        letter-spacing: -.035em;
        margin: .9rem 0 .7rem;
    }
    .hero p {
        position: relative;
        z-index: 1;
        max-width: 570px;
        color: #e3f3f4;
        font-size: 1.02rem;
        line-height: 1.6;
        margin: 0;
    }
    .topics {
        color: #526b79;
        font-size: .88rem;
        text-align: center;
        margin: .2rem 0 1.2rem;
    }
    [data-testid="stTextInput"] label {
        color: var(--ink) !important;
        font-size: .96rem;
        font-weight: 700;
    }
    [data-testid="stTextInput"] input {
        min-height: 3.2rem;
        border: 1px solid #cbd9df;
        border-radius: 12px;
        background: var(--paper);
        color: var(--ink);
        box-shadow: 0 3px 12px rgba(24,43,58,.035);
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #31a6a5;
        box-shadow: 0 0 0 .16rem rgba(49,166,165,.14);
    }
    .stButton > button {
        min-height: 3.05rem;
        border: 0;
        border-radius: 12px;
        background: var(--teal);
        color: #fff;
        font-weight: 750;
        box-shadow: 0 7px 16px rgba(8,127,140,.17);
        transition: background .15s ease, transform .15s ease;
    }
    .stButton > button:hover {
        background: var(--teal-dark);
        color: #fff;
        transform: translateY(-1px);
    }
    [data-testid="stAlert"] { border-radius: 12px; }
    .answer-label {
        color: var(--teal-dark);
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin: 1.6rem 0 .55rem;
    }
    .answer-card {
        padding: 1.35rem 1.5rem;
        border: 1px solid var(--line);
        border-left: 4px solid #19a394;
        border-radius: 14px;
        background: var(--paper);
        color: var(--ink);
        line-height: 1.7;
        box-shadow: 0 8px 24px rgba(24,43,58,.055);
        overflow-wrap: anywhere;
    }
    .footer {
        color: var(--muted);
        font-size: .8rem;
        text-align: center;
        margin-top: 2.1rem;
    }
    @media (max-width: 600px) {
        .block-container { padding: 1.3rem 1rem 1.5rem; }
        .hero { padding: 1.8rem 1.5rem; border-radius: 18px; }
        .hero h1 { font-size: 1.9rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="brand">NovaCart · Customer care</div>
      <h1>Policy answers,<br>without the guesswork.</h1>
      <p>Get clear guidance on NovaCart policies, with the source sections included in every answer.</p>
    </section>
    <div class="topics">Returns &nbsp; · &nbsp; Shipping &nbsp; · &nbsp; Payments &nbsp; · &nbsp; Promotions</div>
    """,
    unsafe_allow_html=True,
)

question = st.text_input(
    "What can we help you with?",
    placeholder="Ask a question about a NovaCart policy…",
)

if st.button("Ask NovaCart", use_container_width=True):
    if not question.strip():
        st.warning("Enter a question to get started.")
    else:
        with st.spinner("Looking through the policy files…"):
            answer = ask(question.strip())
        st.markdown('<div class="answer-label">Response</div>', unsafe_allow_html=True)
        safe_answer = html.escape(answer).replace("\n", "<br>")
        st.markdown(f'<div class="answer-card">{safe_answer}</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer">NovaCart Policy Assistant &nbsp; · &nbsp; Answers grounded in official policy files</div>',
    unsafe_allow_html=True,
)
