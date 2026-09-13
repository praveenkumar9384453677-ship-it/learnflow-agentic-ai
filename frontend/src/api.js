// Toggle between mock data and real FastAPI backend
const USE_MOCK_API = true; 
const BACKEND_URL = "http://localhost:8000/api";

export async function fetchInitialState() {
  if (USE_MOCK_API) {
    return {
      goal: "Learn Java in 30 days",
      scores: [
        { topic: "Arrays", score: 75, color: "#10b981", tag: "Solid" },
        { topic: "OOP Concepts", score: 45, color: "#f59e0b", tag: "Needs Practice" },
        { topic: "Recursion", score: 30, color: "#ef4444", tag: "Critical Gap" }
      ],
      activeTopic: "Recursion",
      schedule: [
        { id: 1, dayNumber: 1, topic: "Recursion Basics & Call Stack", status: "pending" },
        { id: 2, dayNumber: 2, topic: "Recursion Practice Problems", status: "pending" },
        { id: 3, dayNumber: 3, topic: "Recursion Quiz & Assessment", status: "pending" }
      ]
    };
  }

  const res = await fetch(`${BACKEND_URL}/state`);
  return res.json();
}

export async function notifyMissedSession(sessionId, topic, dayNumber) {
  if (USE_MOCK_API) {
    return {
      success: true,
      message: `Triggered replan for Day ${dayNumber} (${topic})`
    };
  }

  const res = await fetch(`${BACKEND_URL}/replan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sessionId, topic, dayNumber })
  });
  return res.json();
}

export async function submitQuizAnswers(answers) {
  if (USE_MOCK_API) {
    let score = 0;
    if (answers.q1 === "A") score += 50;
    if (answers.q2 === "B") score += 50;
    return { score, passed: score >= 80 };
  }

  const res = await fetch(`${BACKEND_URL}/quiz/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(answers)
  });
  return res.json();
}