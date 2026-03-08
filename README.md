# 🏠 Mortgage Servicing Intelligence — LangGraph

**Multi-agent LLM orchestration for mortgage servicing analysis, built with LangGraph.**

---

## What It Does

Input a mortgage servicing scenario (forbearance, collections, loan modification, etc.) → the system orchestrates 5 specialized AI agents through a dependency-aware pipeline → produces a unified action plan with compliance analysis, risk assessment, borrower communication, and rubric-based quality evaluation.

## Architecture

```python
graph = StateGraph(PipelineState)

# 5 agent nodes
graph.add_node("compliance", compliance_node)
graph.add_node("risk", risk_node)
graph.add_node("communication", communication_node)
graph.add_node("synthesis", synthesis_node)
graph.add_node("quality_check", quality_check_node)

# DAG edges
graph.add_edge(START, "compliance")              # fan-out
graph.add_edge(START, "risk")                    # fan-out
graph.add_edge("compliance", "communication")    # fan-in
graph.add_edge("risk", "communication")          # fan-in
graph.add_edge("communication", "synthesis")
graph.add_edge("synthesis", "quality_check")
graph.add_edge("quality_check", END)
```

## Orchestration Patterns

| Pattern | Implementation |
|---------|---------------|
| **Graph-based DAG** | `StateGraph` with declared nodes and edges |
| **Fan-out / Fan-in** | START splits to Compliance + Risk, both merge into Communication |
| **Typed shared state** | `TypedDict` schema auto-managed by LangGraph |
| **Structured output validation** | Every agent returns validated JSON |
| **Retry logic** | Up to 2 retries on parse failure per agent |
| **LLM-as-Judge** | Quality Checker scores all outputs on a 5-dimension rubric |
| **Status callbacks** | Real-time UI updates as nodes execute |

## Agents

1. **Compliance Agent** — federal/state regulations, disclosures, deadlines
2. **Risk Agent** — delinquency risk, refinance eligibility, cross-sell opportunities
3. **Communication Agent** — drafts compliant borrower letters (depends on 1 & 2)
4. **Synthesis Agent** — unified action plan with conflict detection (depends on 1, 2, 3)
5. **Quality Checker** — rubric-based evaluation across accuracy, completeness, consistency, communication quality, and actionability (depends on all)

## Scenarios

12 scenarios across 4 segments:

- **Servicer** — forbearance, refinance, escrow shortage, early payoff
- **Collections** — pre-foreclosure, debt validation disputes, deficiency judgment, third-party collector handoff
- **Originator** — servicing transfer, VA loan assumption
- **Investor/GSE** — loan modification, FHA partial claim

## Tech Stack

- **LangGraph** — graph-based orchestration
- **Claude API (Sonnet)** — agent LLM backend
- **Streamlit** — interactive UI with live pipeline tracker
- **Python** — agent definitions and state schema

## Project Structure

```
├── state.py           # LangGraph TypedDict state schema
├── agents.py          # Agent definitions (system prompts + schemas)
├── graph.py           # LangGraph pipeline (nodes + edges + execution)
├── scenarios.py       # Synthetic mortgage scenarios
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

### Deploy to Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → select `app.py`
4. Add `ANTHROPIC_API_KEY` in Settings → Secrets
5. Deploy
