"""
agent/replanner.py

Provides autonomous schedule adaptation and replanning logic 
when learning conditions change (e.g., missed sessions, low scores).
"""

from typing import Dict, List, Any


def adapt_schedule_for_missed_sessions(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles plan adjustments when sessions are marked as 'missed'.
    Moves missed sessions into a rescheduled queue and clears missed flags.
    """
    missed = state.get("missed_sessions", [])
    current_plan = state.get("current_plan", [])

    if not missed:
        return state

    # Create new adjusted plan: push missed sessions to immediate priority
    rescheduled_sessions = [f"[RESCHEDULED] {session}" for session in missed]
    
    # Filter out original copies of missed sessions from current plan
    remaining_plan = [s for s in current_plan if s not in missed]
    
    # Combine rescheduled sessions with remaining plan steps
    updated_plan = rescheduled_sessions + remaining_plan
    
    state["current_plan"] = updated_plan
    # Clear missed sessions log now that they are rescheduled
    state["missed_sessions"] = []
    state["status"] = "replanned"
    
    return state


def adapt_schedule_for_low_score(state: Dict[str, Any], topic: str, score: int) -> Dict[str, Any]:
    """
    Handles plan adjustments when a student scores below 60% on a reassessment.
    Adds targeted revision and practice sessions.
    """
    if score >= 60:
        return state

    remedial_plan = [
        f"Review core concepts for {topic}",
        f"Watch supplementary video on {topic}",
        f"Solve 5 practice problems on {topic}",
        f"Retake assessment for {topic}"
    ]

    state["current_plan"] = remedial_plan
    state["status"] = "remedial_planning"
    
    return state