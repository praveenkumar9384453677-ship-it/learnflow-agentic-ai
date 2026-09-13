"""
agent/decisions.py

Evaluates the current student state and determines the next action 
the agent should execute.
"""

from typing import Dict, Any


def evaluate_next_action(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes the student state and returns the next decision.
    """
    weak_topics = state.get("weak_topics", [])
    missed_sessions = state.get("missed_sessions", [])
    current_plan = state.get("current_plan", [])
    current_topic = state.get("current_topic")

    # Rule 1: Immediate adaptation if a session was missed
    if missed_sessions:
        return {
            "action": "REPLAN",
            "reason": f"Detected {len(missed_sessions)} missed session(s). Adjusting schedule.",
            "target_topic": current_topic
        }

    # Rule 2: If weak topics exist but no active plan is built
    if weak_topics and not current_plan:
        return {
            "action": "GENERATE_PLAN",
            "reason": f"Weak topic identified ({current_topic}). Need to retrieve resources and build schedule.",
            "target_topic": current_topic
        }

    # Rule 3: Active plan exists, proceed with current learning steps
    if current_plan:
        return {
            "action": "EXECUTE_SESSION",
            "reason": f"Executing active plan for {current_topic}.",
            "target_topic": current_topic
        }

    # Rule 4: No weak topics left
    if not weak_topics:
        return {
            "action": "COMPLETE",
            "reason": "All topics satisfy the mastery threshold (>= 60%). Goal achieved!",
            "target_topic": None
        }

    # Default fallback
    return {
        "action": "WAIT",
        "reason": "Awaiting further student interaction or data.",
        "target_topic": current_topic
    }