# backend/assessment.py

QUESTION_BANK = {
    "Recursion": [
        {
            "id": 1,
            "question": "What is the base case in a recursive function?",
            "options": ["A) The condition that stops recursion", "B) The function name", "C) The maximum loop counter", "D) The memory limit"],
            "answer": "A",
            "explanation": "The base case provides a stopping condition to prevent infinite recursive calls and stack overflow."
        },
        {
            "id": 2,
            "question": "What happens if a recursive function lacks a base case?",
            "options": ["A) Infinite loop / Stack Overflow", "B) Returns 0", "C) Runs faster", "D) Syntax error"],
            "answer": "A",
            "explanation": "Without a base case, calls accumulate indefinitely on the call stack until memory is exhausted."
        }
    ],
    "Arrays": [
        {
            "id": 3,
            "question": "What is the time complexity of accessing an element by index in an array?",
            "options": ["A) O(1)", "B) O(n)", "C) O(log n)", "D) O(n^2)"],
            "answer": "A",
            "explanation": "Arrays use contiguous memory locations, allowing direct memory address calculation in constant time."
        }
    ],
    "OOP": [
        {
            "id": 4,
            "question": "Which OOP concept wraps data and methods into a single unit while restricting direct access?",
            "options": ["A) Encapsulation", "B) Inheritance", "C) Polymorphism", "D) Abstraction"],
            "answer": "A",
            "explanation": "Encapsulation hides internal state details and only exposes public methods for access and modification."
        }
    ]
}

def generate_quiz(topic: str):
    """Retrieves quiz questions for a specific weak topic."""
    return QUESTION_BANK.get(topic, [])

def evaluate_quiz(user_answers: list):
    """
    Evaluates submitted user answers.
    Expects items like: [{"question_id": 1, "topic": "Recursion", "selected": "A"}]
    """
    score = 0
    total = len(user_answers)
    detailed_feedback = []

    for item in user_answers:
        topic_questions = QUESTION_BANK.get(item.get("topic"), [])
        matched_q = next((q for q in topic_questions if q["id"] == item.get("question_id")), None)
        
        if matched_q:
            is_correct = (item.get("selected").upper() == matched_q["answer"])
            if is_correct:
                score += 1
            
            detailed_feedback.append({
                "question_id": matched_q["id"],
                "topic": item.get("topic"),
                "correct": is_correct,
                "correct_answer": matched_q["answer"],
                "explanation": matched_q["explanation"]
            })

    percentage = (score / total * 100) if total > 0 else 0
    return {
        "score": score,
        "total": total,
        "percentage": round(percentage, 2),
        "feedback": detailed_feedback
    }