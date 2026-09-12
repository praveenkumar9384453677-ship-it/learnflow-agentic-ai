import { useState } from 'react'
import './App.css'

function App() {
  const [goal, setGoal] = useState("Learn Java in 30 days")
  const [agentTrace, setAgentTrace] = useState([
    "Goal received: Learn Java in 30 days",
    "Analyzed scores: Arrays (75%), OOP (45%), Recursion (30%)",
    "Identified weak topic: Recursion",
    "Created initial schedule focused on Recursion"
  ])

  const [schedule, setSchedule] = useState([
    { day: "Day 1 (Mon)", topic: "Recursion Basics & Call Stack", status: "pending" },
    { day: "Day 2 (Tue)", topic: "Recursion Practice Problems", status: "pending" },
    { day: "Day 3 (Wed)", topic: "Recursion Quiz & Assessment", status: "pending" }
  ])

  // When student clicks "Completed"
  const handleComplete = (index) => {
    const updated = [...schedule]
    updated[index].status = "completed"
    setSchedule(updated)
    setAgentTrace((prev) => [
      ...prev,
      `Session completed: ${updated[index].day} - ${updated[index].topic}`
    ])
  }

  // When student clicks "Missed" -> Triggers Agent Replanning!
  const handleMissed = (index) => {
    const updated = [...schedule]
    updated[index].status = "missed"
    
    // Agent replans: moves the missed topic to the next slot
    const replanned = [
      ...updated.slice(0, index + 1),
      { day: `Day ${index + 2} (Replanned)`, topic: updated[index].topic, status: "pending" },
      { day: `Day ${index + 3} (Replanned)`, topic: "Practice & Quiz", status: "pending" }
    ]

    setSchedule(replanned)
    setAgentTrace((prev) => [
      ...prev,
      `⚠️ ALERT: Student missed ${updated[index].day}!`,
      `🧠 AGENT REPLANNING: Rescheduling ${updated[index].topic} to next day.`,
      `✅ New learning schedule generated.`
    ])
  }

  return (
    <div className="container">
      <header>
        <h1>LearnFlow</h1>
        <p>Autonomous AI Learning Planner</p>
      </header>

      {/* Section 1: Student Goal */}
      <div className="card">
        <h2>Target Learning Goal</h2>
        <input 
          type="text" 
          value={goal} 
          onChange={(e) => setGoal(e.target.value)}
          style={{ width: '100%', padding: '8px', fontSize: '1rem' }}
        />
      </div>

      {/* Section 2: Agent Live Trace */}
      <div className="card">
        <h2>Agent Decision Log (Proof of Autonomy)</h2>
        <div className="trace-box">
          {agentTrace.map((log, i) => (
            <div key={i}>&gt; {log}</div>
          ))}
        </div>
      </div>

      {/* Section 3: Learning Schedule */}
      <div className="card">
        <h2>Interactive Study Plan</h2>
        {schedule.map((session, index) => (
          <div key={index} className="session-item">
            <div>
              <strong>{session.day}:</strong> {session.topic}
              <span style={{ marginLeft: '10px', color: session.status === 'completed' ? '#10b981' : session.status === 'missed' ? '#ef4444' : '#6b7280' }}>
                ({session.status})
              </span>
            </div>
            {session.status === 'pending' && (
              <div className="btn-group">
                <button className="btn-complete" onClick={() => handleComplete(index)}>
                  Completed
                </button>
                <button className="btn-miss" onClick={() => handleMissed(index)}>
                  Missed
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default App