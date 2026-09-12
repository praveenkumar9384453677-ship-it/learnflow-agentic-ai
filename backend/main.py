# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from backend.performance import analyze_performance
from backend.assessment import generate_quiz, evaluate_quiz
from backend.history import record_assessment, get_topic_history

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

# Request model for manual history recording
class RecordHistoryRequest(BaseModel):
    topic: str
    score: int
    total: int
    percentage: float

# Endpoint 1: Analyze Student Performance
@app.post("/api/performance/analyze")
def api_analyze_performance(data: PerformanceRequest):
    return analyze_performance(data.scores, data.threshold)

# Endpoint 2: Generate Quiz for a Topic
@app.get("/api/assessment/quiz/{topic}")
def api_generate_quiz(topic: str):
    questions = generate_quiz(topic)
    return {"topic": topic, "questions": questions}

# Endpoint 3: Evaluate Quiz Answers & Auto-Record History
@app.post("/api/assessment/evaluate")
def api_evaluate_quiz(payload: EvaluateRequest):
    raw_answers = [item.dict() for item in payload.answers]
    result = evaluate_quiz(raw_answers)
    
    # Automatically log attempt if answers were evaluated
    if raw_answers:
        primary_topic = raw_answers[0]["topic"]
        record_assessment(
            topic=primary_topic,
            score=result["score"],
            total=result["total"],
            percentage=result["percentage"]
        )
        
    return result

# Endpoint 4: Get Assessment History (Overall or by Topic)
@app.get("/api/assessment/history")
def api_get_history(topic: Optional[str] = None):
    return {"history": get_topic_history(topic)}