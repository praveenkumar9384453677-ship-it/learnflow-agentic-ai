# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from backend.performance import analyze_performance
from backend.assessment import generate_quiz, evaluate_quiz

app = FastAPI(title="LearnFlow Assessment API")

# Request model for performance analysis
class PerformanceRequest(BaseModel):
    scores: dict
    threshold: int = 60

# Model for an individual answer item
class AnswerItem(BaseModel):
    question_id: int
    topic: str
    selected: str

# Request model for quiz evaluation
class EvaluateRequest(BaseModel):
    answers: List[AnswerItem]

# Endpoint 1: Analyze Student Performance
@app.post("/api/performance/analyze")
def api_analyze_performance(data: PerformanceRequest):
    return analyze_performance(data.scores, data.threshold)

# Endpoint 2: Generate Quiz for a Topic
@app.get("/api/assessment/quiz/{topic}")
def api_generate_quiz(topic: str):
    questions = generate_quiz(topic)
    return {"topic": topic, "questions": questions}

# Endpoint 3: Evaluate Quiz Answers
@app.post("/api/assessment/evaluate")
def api_evaluate_quiz(payload: EvaluateRequest):
    # Convert Pydantic models back to dictionaries for backend.assessment
    raw_answers = [item.dict() for item in payload.answers]
    return evaluate_quiz(raw_answers)