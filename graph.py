"""
LangGraph pipeline — the core of this version.

COMPARISON WITH RAW PYTHON VERSION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Raw Python                    │  LangGraph
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PipelineState dataclass       │  TypedDict (auto-managed)
  run_agent() with retries      │  Same, but nodes return state
  ThreadPoolExecutor / sequential│  graph.add_edge() defines flow
  Manual DAG with if/then       │  StateGraph with edges
  Callbacks for UI updates      │  Stream events natively
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The graph:

    ┌────────────┐   ┌────────────┐
    │ Compliance │   │    Risk    │   ← fan-out (parallel*)
    └─────┬──────┘   └─────┬──────┘
          └────────┬───────┘
                   ▼
          ┌────────────────┐
          │ Communication  │          ← fan-in, then sequential
          └───────┬────────┘
                  ▼
          ┌────────────────┐
          │   Synthesis    │
          └───────┬────────┘
                  ▼
          ┌────────────────┐
          │ Quality Check  │          ← LLM-as-Judge
          └────────────────┘

  * LangGraph supports parallel via fan-out from a single node.
    For Streamlit compatibility we run sequentially (same as raw version).
"""

import json
import time
from typing import Optional, Callable

from anthropic import Anthropic
from langgraph.graph import StateGraph, START, END

from state import PipelineState
from agents import (
    AgentDef, COMPLIANCE, RISK, COMMUNICATION, SYNTHESIS, QUALITY_CHECKER,
)

# ── Client ─────────────────────────────────────────────────────────
client = Anthropic()
MODEL = "claude-sonnet-4-20250514"

StatusCallback = Callable[[str, str, int], None]

# ── Shared helpers ─────────────────────────────────────────────────

def _scenario_to_prompt(scenario: dict) -> str:
    return f"""\
BORROWER PROFILE
  Name:              {scenario.get("borrower_name", "N/A")}
  Property State:    {scenario.get("state", "N/A")}
  Property Type:     {scenario.get("property_type", "Single Family")}
  Loan Type:         {scenario.get("loan_type", "N/A")}
  Original Amount:   {scenario.get("original_amount", "N/A")}
  Current Balance:   {scenario.get("current_balance", "N/A")}
  Interest Rate:     {scenario.get("interest_rate", "N/A")}
  Monthly Payment:   {scenario.get("monthly_payment", "N/A")}
  Origination Date:  {scenario.get("origination_date", "N/A")}
  Credit Score:      {scenario.get("credit_score", "N/A")}
  DTI Ratio:         {scenario.get("dti_ratio", "N/A")}

PAYMENT HISTORY
  {scenario.get("payment_history", "No history available.")}

CURRENT REQUEST / SITUATION
  {scenario.get("situation", "General servicing review.")}

ADDITIONAL CONTEXT
  {scenario.get("additional_context", "None.")}
"""


def _clean_json(text: str) -> str:
    t = text.strip()
    if t.startswith("```json"):
        t = t[7:]
    elif t.startswith("```"):
        t = t[3:]
    if t.endswith("```"):
        t = t[:-3]
    return t.strip()


def _call_agent(
    agent: AgentDef,
    user_message: str,
    max_retries: int = 2,
    cb: Optional[StatusCallback] = None,
) -> tuple[dict, dict]:
    """
    Call Claude, validate JSON, retry on failure.
    Returns (output_dict, log_entry_dict).
    """
    start = time.time()
    retries = 0
    raw_text = ""

    while retries <= max_retries:
        try:
            status = "retrying" if retries > 0 else "running"
            if cb:
                cb(agent.name, status, retries)

            response = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=agent.system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            raw_text = response.content[0].text
            output = json.loads(_clean_json(raw_text))

            duration = round(time.time() - start, 2)
            if cb:
                cb(agent.name, "complete", retries)

            log = {"agent": agent.name, "status": "complete",
                   "duration_s": duration, "retries": retries, "error": None}
            return output, log

        except json.JSONDecodeError as exc:
            retries += 1
            if retries > max_retries:
                duration = round(time.time() - start, 2)
                if cb:
                    cb(agent.name, "failed", retries)
                log = {"agent": agent.name, "status": "failed",
                       "duration_s": duration, "retries": retries, "error": str(exc)}
                return {"error": "JSON parse failure", "raw_snippet": raw_text[:300]}, log

        except Exception as exc:
            retries += 1
            if retries > max_retries:
                duration = round(time.time() - start, 2)
                if cb:
                    cb(agent.name, "failed", retries)
                log = {"agent": agent.name, "status": "failed",
                       "duration_s": duration, "retries": retries, "error": str(exc)}
                return {"error": str(exc)}, log


# ── Graph nodes ────────────────────────────────────────────────────
# Each node is a function that takes PipelineState, does work,
# and returns the fields it wants to update.
# LangGraph merges the returned dict into the shared state.

# We store the callback in a module-level variable so nodes can use it.
# (LangGraph nodes only receive state as input.)
_status_cb: Optional[StatusCallback] = None


def compliance_node(state: PipelineState) -> dict:
    """Node: run Compliance Agent on the raw scenario."""
    prompt = _scenario_to_prompt(state["scenario"])
    output, log = _call_agent(COMPLIANCE, prompt, cb=_status_cb)
    return {
        "compliance": output,
        "agent_log": state.get("agent_log", []) + [log],
    }


def risk_node(state: PipelineState) -> dict:
    """Node: run Risk Agent on the raw scenario."""
    prompt = _scenario_to_prompt(state["scenario"])
    output, log = _call_agent(RISK, prompt, cb=_status_cb)
    return {
        "risk": output,
        "agent_log": state.get("agent_log", []) + [log],
    }


def communication_node(state: PipelineState) -> dict:
    """Node: run Communication Agent — depends on compliance + risk."""
    base = _scenario_to_prompt(state["scenario"])
    prompt = (
        f"{base}\n\n"
        f"── COMPLIANCE FINDINGS ──\n{json.dumps(state['compliance'], indent=2)}\n\n"
        f"── RISK ASSESSMENT ──\n{json.dumps(state['risk'], indent=2)}"
    )
    output, log = _call_agent(COMMUNICATION, prompt, cb=_status_cb)
    return {
        "communication": output,
        "agent_log": state.get("agent_log", []) + [log],
    }


def synthesis_node(state: PipelineState) -> dict:
    """Node: run Synthesis Agent — depends on all three."""
    base = _scenario_to_prompt(state["scenario"])
    prompt = (
        f"{base}\n\n"
        f"── COMPLIANCE AGENT OUTPUT ──\n{json.dumps(state['compliance'], indent=2)}\n\n"
        f"── RISK AGENT OUTPUT ──\n{json.dumps(state['risk'], indent=2)}\n\n"
        f"── COMMUNICATION AGENT OUTPUT ──\n{json.dumps(state['communication'], indent=2)}"
    )
    output, log = _call_agent(SYNTHESIS, prompt, cb=_status_cb)
    return {
        "synthesis": output,
        "agent_log": state.get("agent_log", []) + [log],
    }


def quality_check_node(state: PipelineState) -> dict:
    """Node: run Quality Checker — depends on everything."""
    base = _scenario_to_prompt(state["scenario"])
    prompt = (
        f"{base}\n\n"
        f"── COMPLIANCE AGENT OUTPUT ──\n{json.dumps(state['compliance'], indent=2)}\n\n"
        f"── RISK AGENT OUTPUT ──\n{json.dumps(state['risk'], indent=2)}\n\n"
        f"── COMMUNICATION AGENT OUTPUT ──\n{json.dumps(state['communication'], indent=2)}\n\n"
        f"── SYNTHESIS AGENT OUTPUT ──\n{json.dumps(state['synthesis'], indent=2)}"
    )
    output, log = _call_agent(QUALITY_CHECKER, prompt, cb=_status_cb)
    return {
        "quality_check": output,
        "agent_log": state.get("agent_log", []) + [log],
    }


# ── Build the graph ───────────────────────────────────────────────

def build_graph() -> StateGraph:
    """
    Construct the LangGraph StateGraph.

    Graph edges define the DAG:
        START ──→ compliance ──→ communication ──→ synthesis ──→ quality_check ──→ END
        START ──→ risk ───────↗
    """
    graph = StateGraph(PipelineState)

    # Add nodes
    graph.add_node("compliance", compliance_node)
    graph.add_node("risk", risk_node)
    graph.add_node("communication", communication_node)
    graph.add_node("synthesis", synthesis_node)
    graph.add_node("quality_check", quality_check_node)

    # Define edges (the DAG)
    # Step 1: START fans out to compliance and risk
    graph.add_edge(START, "compliance")
    graph.add_edge(START, "risk")

    # Step 2: Both feed into communication
    graph.add_edge("compliance", "communication")
    graph.add_edge("risk", "communication")

    # Step 3: Communication feeds into synthesis
    graph.add_edge("communication", "synthesis")

    # Step 4: Synthesis feeds into quality check
    graph.add_edge("synthesis", "quality_check")

    # Step 5: Quality check is the final node
    graph.add_edge("quality_check", END)

    return graph


# Compile once at module level
pipeline = build_graph().compile()


# ── Entry point ───────────────────────────────────────────────────

def run_pipeline(
    scenario: dict,
    cb: Optional[StatusCallback] = None,
) -> dict:
    """
    Execute the full LangGraph pipeline.
    Returns the final PipelineState as a dict.
    """
    global _status_cb
    _status_cb = cb

    start = time.time()

    initial_state: PipelineState = {
        "scenario": scenario,
        "compliance": {},
        "risk": {},
        "communication": {},
        "synthesis": {},
        "quality_check": {},
        "agent_log": [],
    }

    # LangGraph's invoke() runs the full graph and returns final state
    final_state = pipeline.invoke(initial_state)

    final_state["total_duration_s"] = round(time.time() - start, 2)

    _status_cb = None

    if cb:
        cb("Pipeline", "complete", 0)

    return final_state
