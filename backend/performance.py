# backend/performance.py

def analyze_performance(performance_data: dict, threshold: int = 60) -> dict:
    """
    Analyzes student scores and returns weak topics below the given threshold.
    
    Example input:
        {"Arrays": 75, "OOP": 45, "Recursion": 30}
    """
    if not performance_data:
        return {"weak_topics": [], "strong_topics": [], "primary_weakness": None}

    # Sort topics by score ascending (lowest score first)
    sorted_topics = sorted(performance_data.items(), key=lambda x: x[1])

    weak_topics = [topic for topic, score in sorted_topics if score < threshold]
    strong_topics = [topic for topic, score in sorted_topics if score >= threshold]

    # Primary weakness is the topic with the lowest score
    primary_weakness = weak_topics[0] if weak_topics else None

    return {
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "primary_weakness": primary_weakness
    }