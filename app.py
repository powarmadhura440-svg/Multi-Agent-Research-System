import re
import streamlit as st
from pipeline import run_research_popeline

st.set_page_config(page_title="Research Assistant", page_icon="🔎", layout="centered")

st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}
.block-container {max-width: 820px; padding-top: 2rem; padding-bottom: 6rem;}
.welcome {text-align: center; margin: 10vh 0 2rem 0;}
.welcome h1 {font-size: 2.3rem; font-weight: 700;}
.welcome p {opacity: .65; font-size: 1.05rem;}
[data-testid="stChatMessage"] {background: transparent; padding: .6rem 0;}
[data-testid="stMetric"] {background: #2A2A2A; border: 1px solid #3A3A3A;
                          border-radius: 12px; padding: .8rem 1rem;}
</style>
""", unsafe_allow_html=True)

st.session_state.setdefault("messages", [])


def show_result(state, key):
    st.markdown(state["report"])
    m = re.search(r"Score:?\**\s*(\d+(?:\.\d+)?)\s*/\s*10", state["feedback"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Report length", f"{len(state['report'].split())} words")
    c2.metric("Content scraped", f"{len(state['scraped_content'].split())} words")
    c3.metric("Critic score", f"{m.group(1)}/10" if m else "N/A")
    with st.expander("🧐 Critic review"):
        st.markdown(state["feedback"])
    with st.expander("🌐 Scraped content"):
        st.markdown(state["scraped_content"])
    with st.expander("🔍 Search results"):
        st.markdown(state["search_result"])
    st.download_button("⬇️ Download report (.md)", state["report"],
                       file_name="report.md", key=f"dl_{key}")


with st.sidebar:
    st.title("🔎 Research Assistant")
    if st.button("➕ New chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    st.divider()
    st.caption("RECENT TOPICS")
    topics = [m["content"] for m in st.session_state["messages"] if m["role"] == "user"]
    if topics:
        for t in reversed(topics[-8:]):
            st.write(f"💬 {t}")
    else:
        st.caption("No topics yet.")
    st.divider()
    st.caption("Built with LangChain, Gemini, Tavily & Streamlit")

if not st.session_state["messages"]:
    st.markdown("""
    <div class="welcome">
      <h1>What would you like to research?</h1>
      <p>Four AI agents will search, read, write and review a report for you.</p>
    </div>
    """, unsafe_allow_html=True)
    examples = ["Impact of AI on jobs", "Future of electric vehicles", "Benefits of remote work"]
    cols = st.columns(3)
    for col, ex in zip(cols, examples):
        if col.button(ex, use_container_width=True):
            st.session_state["pending"] = ex
            st.rerun()

for i, msg in enumerate(st.session_state["messages"]):
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        elif msg.get("state"):
            show_result(msg["state"], i)
        else:
            st.error(msg["content"])

prompt = st.chat_input("Enter a research topic...")
if not prompt and st.session_state.get("pending"):
    prompt = st.session_state.pop("pending")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.status("Agents are working... this takes 1-2 minutes", expanded=True) as status:
            st.write("🔍 Searching → 📖 Reading → ✍️ Writing → 🧐 Reviewing")
            try:
                state = run_research_popeline(prompt)
                status.update(label="Research complete ✅", state="complete", expanded=False)
                st.session_state["messages"].append(
                    {"role": "assistant", "content": "", "state": state})
            except Exception as e:
                status.update(label="Something went wrong ❌", state="error")
                st.session_state["messages"].append(
                    {"role": "assistant", "content": str(e), "state": None})
    st.rerun()