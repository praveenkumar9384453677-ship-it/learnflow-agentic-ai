import { useState } from 'react'
import './App.css'

function App() {
  const [goal, setGoal] = useState("Learn Java in 30 days")

  const [scores] = useState([
    { topic: "Arrays", score: 75, color: "#10b981", tag: "Solid" },
    { topic: "OOP Concepts", score: 45, color: "#f59e0b", tag: "Needs Practice" },
    { topic: "Recursion", score: 30, color: "#ef4444", tag: "Critical Gap" }
  ])

  const [agentTrace, setAgentTrace] = useState([
    "Goal received: Learn Java in 30 days",
    "Analyzed scores: Arrays (75%), OOP (45%), Recursion (30%)",
    "Identified weak topic: Recursion",
    "Created initial schedule focused on Recursion"
  ])

  const [schedule, setSchedule] = useState([
    { id: 1, dayNumber: 1, topic: "Recursion Basics & Call Stack", status: "pending" },
    { id: 2, dayNumber: 2, topic: "Recursion Practice Problems", status: "pending" },
    { id: 3, dayNumber: 3, topic: "Recursion Quiz & Assessment", status: "pending" }
  ])

  const handleComplete = (clickedIndex) => {
    setSchedule((prevSchedule) => {
      const updated = prevSchedule.map((item, idx) => 
        idx === clickedIndex ? { ...item, status: "completed" } : item
      )
      return updated
    })

    const completedItem = schedule[clickedIndex]
    setAgentTrace((prev) => [
      ...prev,
      `Session completed: Day ${completedItem.dayNumber} - ${completedItem.topic}`
    ])
  }

  const handleMissed = (clickedIndex) => {
    const missedItem = schedule[clickedIndex]

    setSchedule((prevSchedule) => {
      // 1. Everything up to the clicked item
      const pastItems = prevSchedule.slice(0, clickedIndex)

      // 2. Mark the missed item
      const markedMissed = { ...missedItem, status: "missed" }

      // 3. Topics that still need to be completed (the missed one + everything after it)
      const topicsToLearn = [
        missedItem.topic,
        ...prevSchedule.slice(clickedIndex + 1).map((item) => item.topic)
      ]

      // 4. Create new upcoming days starting from the next day number
      const nextStartDay = missedItem.dayNumber + 1
      const rescheduledItems = topicsToLearn.map((topic, offset) => ({
        id: Date.now() + offset,
        dayNumber: nextStartDay + offset,
        topic: topic,
        status: "pending"
      }))

      // Combine: History + Missed record + All shifted items preserved
      return [...pastItems, markedMissed, ...rescheduledItems]
    })

    setAgentTrace((prev) => [
      ...prev,
      `⚠️ ALERT: Student missed Day ${missedItem.dayNumber}!`,
      `🧠 AGENT REPLANNING: Rescheduling "${missedItem.topic}" to Day ${missedItem.dayNumber + 1}.`,
      `⏩ Pushing subsequent lessons forward so zero content is lost.`
    ])
  }

  return (
    <div className="container">
      <header>
        <h1>LearnFlow</h1>
        <p>Autonomous AI Learning Planner</p>
      </header>

      {/* Section 1: Target Goal */}
      <div className="card">
        <h2>Target Learning Goal</h2>
        <input 
          type="text" 
          value={goal} 
          onChange={(e) => setGoal(e.target.value)}
          style={{ width: '100%', padding: '8px', fontSize: '1rem' }}
        />
      </div>

      {/* Section 2: Initial Diagnostics */}
      <div className="card">
        <h2>Initial Diagnostic Performance</h2>
        <div className="scores-grid">
          {scores.map((item, idx) => (
            <div key={idx} className="score-chip">
              <div className="score-header">
                <span>{item.topic}</span>
                <span>{item.score}%</span>
              </div>
              <div className="progress-bar-bg">
                <div 
                  className="progress-bar-fill" 
                  style={{ width: `${item.score}%`, backgroundColor: item.color }} 
                />
              </div>
              <span style={{ color: item.color, fontSize: '0.75rem', fontWeight: 'bold' }}>
                {item.tag}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Section 3: Agent Live Trace */}
      <div className="card">
        <h2>Agent Decision Log (Proof of Autonomy)</h2>
        <div className="trace-box">
          {agentTrace.map((log, i) => (
            <div key={i}>&gt; {log}</div>
          ))}
        </div>
      </div>

      {/* Section 4: Learning Schedule */}
      <div className="card">
        <h2>Interactive Study Plan</h2>
        {schedule.map((session, index) => (
          <div key={session.id || index} className="session-item">
            <div>
              <strong>Day {session.dayNumber}:</strong> {session.topic}
              <span style={{ 
                marginLeft: '10px', 
                textTransform: 'capitalize',
                color: session.status === 'completed' ? '#10b981' : session.status === 'missed' ? '#ef4444' : '#6b7280' 
              }}>
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