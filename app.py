import streamlit as st
import threading
import queue
from pathlib import Path

from agent.graph import run_agent_thread

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AutoEngineer AI",
    layout="wide"
)

st.title("🤖 AutoEngineer AI")
st.markdown("Multi-Agent Software Builder (Planner → Architect → Coder)")

# ------------------ SESSION STATE ------------------
if "logs" not in st.session_state:
    st.session_state.logs = []

if "status" not in st.session_state:
    st.session_state.status = "idle"

if "log_q" not in st.session_state:
    st.session_state.log_q = None


# ------------------ HELPERS ------------------
def list_generated_files():
    root = Path("generated_project")
    if not root.exists():
        return []

    return [str(f) for f in root.rglob("*") if f.is_file()]


# ------------------ INPUT ------------------
user_prompt = st.text_area(
    "💡 Enter your project idea:",
    height=120,
    placeholder="Create a Python file calculator.py..."
)

col1, col2 = st.columns(2)

with col1:
    run_btn = st.button("🚀 Generate")

with col2:
    clear_btn = st.button("🧹 Reset")

if clear_btn:
    st.session_state.logs = []
    st.session_state.status = "idle"
    st.session_state.log_q = None
    st.rerun()


# ------------------ RUN AGENT ------------------
if run_btn:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt")
    else:
        st.session_state.logs = []
        st.session_state.status = "running"

        log_q = queue.Queue()
        st.session_state.log_q = log_q

        thread = threading.Thread(
            target=run_agent_thread,
            args=(user_prompt, log_q),
            daemon=True
        )
        thread.start()


# ------------------ LIVE LOGS ------------------
if st.session_state.status == "running":

    st.info("⏳ Generating project...")

    log_q = st.session_state.log_q
    updated = False

    while not log_q.empty():
        event = log_q.get()
        updated = True

        if event[0] == "log":
            st.session_state.logs.append(event[2])

        elif event[0] == "done":
            st.session_state.status = "done"

        elif event[0] == "error":
            st.session_state.status = "error"

    if updated:
        st.rerun()


# ------------------ DISPLAY ------------------
st.subheader("📜 Execution Logs")

for log in st.session_state.logs:
    st.write(log)


# ------------------ FILES ------------------
files = list_generated_files()

if files:
    st.subheader("📂 Generated Files")

    for file in files:
        st.markdown(f"### {file}")

        try:
            with open(file, "r", encoding="utf-8") as f:
                st.code(f.read(), language="python")
        except:
            st.warning("Could not read file")


# ------------------ STATUS ------------------
if st.session_state.status == "done":
    st.success("✅ Project Generated Successfully!")

elif st.session_state.status == "error":
    st.error("❌ Error occurred during generation")