import json
import time
import traceback
import queue
import re
import os

from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq

from agent.prompts import planner_prompt, architect_prompt
from agent.states import Plan, TaskPlan, CoderState
from agent.tools import (
    write_file,
    read_file
)

load_dotenv()

PLANNER_MODEL = "llama-3.3-70b-versatile"
CODER_MODEL = "llama-3.3-70b-versatile"


# ✅ Safe JSON extractor
def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found:\n{text}")
    return json.loads(match.group())


def run_agent_thread(user_prompt: str, log_q: queue.Queue):
    try:
        planner_llm = ChatGroq(model=PLANNER_MODEL)
        coder_llm = ChatGroq(model=CODER_MODEL)

        os.makedirs("generated_project", exist_ok=True)

        log_q.put(("log", "info", f"Starting generation: {user_prompt}"))

        # ------------------ PLANNER ------------------
        log_q.put(("stage", "planner", None))

        raw_plan = planner_llm.invoke(planner_prompt(user_prompt))
        plan = Plan(**extract_json(raw_plan.content))

        log_q.put(("plan", None, plan))

        # ------------------ ARCHITECT ------------------
        log_q.put(("stage", "architect", None))

        raw_tasks = planner_llm.invoke(
            architect_prompt(plan.model_dump_json())
        )

        task_plan = TaskPlan(**extract_json(raw_tasks.content))
        log_q.put(("task_plan", None, task_plan))

        # ------------------ CODER ------------------
        log_q.put(("stage", "coder", None))

        steps = task_plan.implementation_steps
        coder_state = CoderState(task_plan=task_plan, current_step_idx=0)

        for idx, step in enumerate(steps):

            filepath = step.filepath
            full_path = f"generated_project/{filepath}"

            log_q.put(("log", "info", f"🚀 STEP {idx+1}: {full_path}"))

            existing = read_file.run(full_path)

            # 🔥 CLEAN GENERATION PROMPT
            response = coder_llm.invoke(
                f"""
You are a Python developer.

Write clean, correct Python code.

Task:
{step.task_description}

File: {filepath}

Existing content:
{existing}

STRICT RULES:
- Output ONLY Python code
- DO NOT include markdown (no ```python)
- DO NOT include explanations
- DO NOT include '>>>'
- Code must be directly runnable
"""
            )

            code = response.content.strip()

            # extra safety cleanup
            code = code.replace("```python", "").replace("```", "").strip()

            write_file.run({
                "path": full_path,
                "content": code
            })

            log_q.put(("log", "success", f"✔ Written: {full_path}"))

            coder_state.current_step_idx = idx + 1
            log_q.put(("coder_state", None, coder_state))

            time.sleep(0.5)

        log_q.put(("stage", "done", None))
        log_q.put(("done", None, None))

    except Exception as e:
        log_q.put(("log", "error", f"ERROR: {str(e)}"))
        log_q.put(("log", "error", traceback.format_exc()))
        log_q.put(("error", None, None))