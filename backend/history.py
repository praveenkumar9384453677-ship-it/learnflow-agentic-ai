# backend/history.py
from datetime import datetime

# In-memory storage for assessment history
# (Can be connected to SQLite database in upcoming phases)
ASSESSMENT_HISTORY = []

def record_assessment(topic: str, score: int, total: int, percentage: float):
    """Stores the result of a completed assessment attempt."""
    record = {
        "id": len(ASSESSMENT_HISTORY) + 1,
        "topic": topic,
        "score": score,
        "total": total,
        "percentage": percentage,
        "timestamp": datetime.now().isoformat()
    }
    ASSESSMENT_HISTORY.append(record)
    return record

def get_topic_history(topic: str = None):
    """
    Returns assessment attempts.
    If a topic is provided, returns history for that specific topic.
    Otherwise returns all recorded attempts.
    """
    if topic:
        return [item for item in ASSESSMENT_HISTORY if item["topic"].lower() == topic.lower()]
    return ASSESSMENT_HISTORY