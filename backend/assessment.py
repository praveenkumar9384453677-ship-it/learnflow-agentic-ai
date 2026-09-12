# backend/assessment.py

# A lightweight quiz bank for testing (can be expanded later)
QUESTION_BANK = {
    "Recursion": [
        {
            "id": 1,
            "question": "What is the base case in a recursive function?",
            "options": ["A) The condition that stops recursion", "B) The function name", "C) The maximum loop counter", "D) The memory limit"],
            "answer": "A"
        },
        {
            "id": 2,
            "question": "What happens if a recursive function lacks a base case?",
            "options": ["A) Infinite loop / Stack Overflow", "B) Returns 0", "C) Runs faster", "D) Syntax error"],
            "answer": "A"
        }
    ],
    "OOP": [
        {
            "id": 1,
            "question": "Which OOP concept hides internal implementation details?",
            "options": ["A) Encapsulation", "B) Inheritance", "C) Polymorphism", "D) Abstraction"],
            "answer": "A"
        }
    ]
}


def generate_quiz(topic: str) -> list:
    """Retrieves questions for a given topic."""
    return QUESTION_BANK.get(topic, [])


def evaluate_quiz(user_answers: list) -> dict:
    """
    Evaluates submitted answers and calculates the final percentage score.
    
    Example input:
        [{"question_id": 1, "topic": "Recursion", "selected": "A"}, ...]
    """
    if not user_answers:
        return {"score_percentage": 0, "passed": False}

    correct_count = 0
    total_questions = len(user_answers)

    for item in user_answers:
        topic = item.get("topic")
        q_id = item.get("question_id")
        selected = item.get("selected")

        # Find matching question in database
        questions = QUESTION_BANK.get(topic, [])
        for q in questions:
            if q["id"] == q_id and q["answer"] == selected:
                correct_count += 1
                break

    score_percentage = int((correct_count / total_questions) * 100)
    passed = score_percentage >= 70

    return {
        "score_percentage": score_percentage,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "passed": passed
    }