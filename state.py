"""
LangGraph state schema.

In the raw Python version we manually managed a PipelineState dataclass.
LangGraph replaces that with a TypedDict that automatically flows through
the graph. Each node reads from and writes to this shared state.
"""

from typing import TypedDict, Any


class PipelineState(TypedDict):
    """Shared state that flows through the LangGraph pipeline."""

    # Input
    scenario: dict

    # Agent outputs (populated as nodes execute)
    compliance: dict
    risk: dict
    communication: dict
    synthesis: dict
    quality_check: dict

    # Tracking
    agent_log: list[dict]  # [{agent, status, duration_s, retries}]
