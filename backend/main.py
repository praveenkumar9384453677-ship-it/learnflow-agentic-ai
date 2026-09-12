# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from backend.performance import analyze_performance
from backend.assessment import generate_quiz, evaluate_quiz

app = FastAPI(title="LearnFlow Assessment API")

# Request model for performance analysis
class PerformanceRequest(BaseModel):
    scores: dict
    threshold: int = 60

# Endpoint 1: Analyze Student Performance
@app.post("/api/performance/analyze")
def api_analyze_performance(data: PerformanceRequest):
    result = analyze_performance(data.scores, data.threshold)
    return result

# Endpoint 2: Generate Quiz for a Topic
@app.get("/api/assessment/quiz/{topic}")
def api_generate_quiz(topic: str):
    questions = generate_quiz(topic)
    return {"topic": topic, "questions": questions}

# Endpoint 3: Evaluate Quiz Answers
@app.post("/api/assessment/evaluate")
def api_evaluate_quiz(user_answers: list):
    result = evaluate_quiz(user_answers)
    return result