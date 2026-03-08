"""
LangGraph state schema.

LangGraph manages this TypedDict as shared state flowing through the graph.
Each node reads from and writes to this state.

The agent_log field uses an Annotated reducer (operator.add) so that
parallel nodes (compliance + risk) can both append to it without conflict.
"""

from typing import TypedDict, Annotated
import operator


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

    # Tracking — uses add reducer so parallel nodes can append
    agent_log: Annotated[list[dict], operator.add]
