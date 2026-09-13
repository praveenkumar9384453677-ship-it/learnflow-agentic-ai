"""
agent/state.py

Defines the structure and helper functions for managing the student's
learning state in LearnFlow.
"""

from typing import Dict, List, Any


def create_initial_state(goal: str, performance: Dict[str, int]) -> Dict[str, Any]:
    """
    Creates and returns a fresh student state dictionary based on a goal 
    and initial topic scores.
    """
    # Identify initial weak topics (topics with score below 60%)
    weak_topics = [topic for topic, score in performance.items() if score < 60]

    state = {
        "goal": goal,
        "performance": performance,
        "weak_topics": weak_topics,
        "current_topic": weak_topics[0] if weak_topics else None,
        "current_plan": [],
        "completed_sessions": [],
        "missed_sessions": [],
        "assessment_results": [],
        "status": "initialized"  # Status can be: initialized, planning, learning, reassessing, completed
    }
    
    return state


def update_performance(state: Dict[str, Any], topic: str, new_score: int) -> Dict[str, Any]:
    """
    Updates the score for a specific topic and recalculates weak topics.
    """
    state["performance"][topic] = new_score
    
    # Recalculate weak topics (< 60%)
    state["weak_topics"] = [
        t for t, score in state["performance"].items() if score < 60
    ]
    
    # Update current topic to the next weak topic if available
    if state["weak_topics"]:
        if state["current_topic"] not in state["weak_topics"]:
            state["current_topic"] = state["weak_topics"][0]
    else:
        state["current_topic"] = None
        state["status"] = "completed"

    return state


def mark_session_status(state: Dict[str, Any], session_name: str, status: str) -> Dict[str, Any]:
    """
    Marks a study session as 'completed' or 'missed'.
    """
    if status == "completed":
        if session_name not in state["completed_sessions"]:
            state["completed_sessions"].append(session_name)
    elif status == "missed":
        if session_name not in state["missed_sessions"]:
            state["missed_sessions"].append(session_name)
            
    return state

"""
agent/state.py

Defines the structure and helper functions for managing the student's
learning state in LearnFlow.
"""

from typing import Dict, List, Any


def create_initial_state(goal: str, performance: Dict[str, int]) -> Dict[str, Any]:
    """
    Creates and returns a fresh student state dictionary based on a goal 
    and initial topic scores.
    """
    # Identify initial weak topics (topics with score below 60%)
    weak_topics = [topic for topic, score in performance.items() if score < 60]

    state = {
        "goal": goal,
        "performance": performance,
        "weak_topics": weak_topics,
        "current_topic": weak_topics[0] if weak_topics else None,
        "current_plan": [],
        "completed_sessions": [],
        "missed_sessions": [],
        "assessment_results": [],
        "status": "initialized"  # Status can be: initialized, planning, learning, reassessing, completed
    }
    
    return state


def update_performance(state: Dict[str, Any], topic: str, new_score: int) -> Dict[str, Any]:
    """
    Updates the score for a specific topic and recalculates weak topics.
    """
    state["performance"][topic] = new_score
    
    # Recalculate weak topics (< 60%)
    state["weak_topics"] = [
        t for t, score in state["performance"].items() if score < 60
    ]
    
    # Update current topic to the next weak topic if available
    if state["weak_topics"]:
        if state["current_topic"] not in state["weak_topics"]:
            state["current_topic"] = state["weak_topics"][0]
    else:
        state["current_topic"] = None
        state["status"] = "completed"

    return state


def mark_session_status(state: Dict[str, Any], session_name: str, status: str) -> Dict[str, Any]:
    """
    Marks a study session as 'completed' or 'missed'.
    """
    if status == "completed":
        if session_name not in state["completed_sessions"]:
            state["completed_sessions"].append(session_name)
    elif status == "missed":
        if session_name not in state["missed_sessions"]:
            state["missed_sessions"].append(session_name)
            
    return state