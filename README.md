# 🏠 Mortgage Servicing Intelligence — LangGraph Version

**Same multi-agent pipeline, rebuilt with LangGraph to compare orchestration approaches.**

> Companion to the [raw Python version](https://github.com/<your-username>/mortgage-servicing-orchestrator). Same agents, same prompts, same output — only the orchestration layer changed.

---

## Why Two Versions?

| | Raw Python | LangGraph |
|---|---|---|
| **State management** | Manual `PipelineState` dataclass | `TypedDict` auto-managed by LangGraph |
| **DAG definition** | `if/then` + sequential calls | `graph.add_edge()` declarations |
| **Execution** | Custom `run_pipeline()` (~120 lines) | `graph.invoke()` (~30 lines) |
| **Parallel support** | ThreadPoolExecutor (manual) | Built-in fan-out from START |
| **Shows** | You understand the fundamentals | You know the ecosystem |

Having both says: *"I can build it from scratch AND I know when to use a framework."*

## Architecture

```python
graph = StateGraph(PipelineState)

graph.add_node("compliance", compliance_node)
graph.add_node("risk", risk_node)
graph.add_node("communication", communication_node)
graph.add_node("synthesis", synthesis_node)
graph.add_node("quality_check", quality_check_node)

graph.add_edge(START, "compliance")    # fan-out
graph.add_edge(START, "risk")          # fan-out
graph.add_edge("compliance", "communication")   # fan-in
graph.add_edge("risk", "communication")          # fan-in
graph.add_edge("communication", "synthesis")
graph.add_edge("synthesis", "quality_check")
graph.add_edge("quality_check", END)
```

## Project Structure

```
├── state.py           # LangGraph TypedDict state schema
├── agents.py          # Agent definitions (same prompts as raw version)
├── graph.py           # LangGraph pipeline (nodes + edges + execution)
├── scenarios.py       # Synthetic mortgage scenarios (shared)
├── app.py             # Streamlit UI
├── requirements.txt
└── .streamlit/
    └── config.toml
```

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
streamlit run app.py
```

## Key Differences in Code

**Raw Python** — you write the execution engine:
```python
compliance_result = run_agent(COMPLIANCE, prompt)
risk_result = run_agent(RISK, prompt)
state.compliance = compliance_result.output
# manually chain to next agent...
```

**LangGraph** — you declare the graph, it handles execution:
```python
graph.add_edge(START, "compliance")
graph.add_edge(START, "risk")
graph.add_edge("compliance", "communication")
# LangGraph manages state flow automatically
final_state = pipeline.invoke(initial_state)
```

---

*Built by [Your Name] — UC Berkeley Haas MBA '25*
