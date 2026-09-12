import sys
from pathlib import Path

# Add project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from backend.performance import analyze_performance
from backend.assessment import generate_quiz, evaluate_quiz
from backend.history import record_assessment, get_topic_history

print("=" * 50)
print(" LEARNFLOW BACKEND END-TO-END DEMO")
print("=" * 50)

print("\n[1] Analyzing Student Performance...")
mock_scores = {"Recursion": 45, "OOP": 85, "Arrays": 50}
analysis = analyze_performance(mock_scores, threshold=60)
print(f"-> Weak Topics Identified: {analysis['weak_topics']}")

target_topic = analysis['weak_topics'][0]
print(f"\n[2] Fetching Quiz Questions for: {target_topic}...")
quiz = generate_quiz(target_topic)
print(f"-> Retrieved {len(quiz)} questions successfully.")

print("\n[3] Grading Student Answers...")
user_submission = [
    {"question_id": 1, "topic": "Recursion", "selected": "A"},
    {"question_id": 2, "topic": "Recursion", "selected": "B"}
]
result = evaluate_quiz(user_submission)
print(f"-> Final Score: {result['score']}/{result['total']} ({result['percentage']}%)")
print(f"-> Explanations Given: {len(result['feedback'])}")

print("\n[4] Logging Progress into History Engine...")
record_assessment(target_topic, result['score'], result['total'], result['percentage'])
history = get_topic_history(target_topic)
print(f"-> Total Attempts Recorded for {target_topic}: {len(history)}")

print("\n" + "=" * 50)
print(" ALL BACKEND MODULES OPERATIONAL!")
print("=" * 50)
