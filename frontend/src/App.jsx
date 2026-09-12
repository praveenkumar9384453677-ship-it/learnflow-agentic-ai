import { useState } from 'react'
import './App.css'

function App() {
  const [goal, setGoal] = useState("Learn Java in 30 days")

  const [scores, setScores] = useState([
    { topic: "Arrays", score: 75, color: "#10b981", tag: "Solid" },
    { topic: "OOP Concepts", score: 45, color: "#f59e0b", tag: "Needs Practice" },
    { topic: "Recursion", score: 30, color: "#ef4444", tag: "Critical Gap" }
  ])
  const [activeTopic, setActiveTopic] = useState("Recursion")

  const resourceBank = {
    Recursion: [
      { title: "Recursion in 100 Seconds", type: "Video", tag: "tag-video", duration: "5 mins", link: "#" },
      { title: "Visualizing the Call Stack", type: "Article", tag: "tag-article", duration: "8 mins read", link: "#" },
      { title: "Factorial & Fibonacci Problem Set", type: "Practice", tag: "tag-practice", duration: "4 problems", link: "#" }
    ],
    "OOP Concepts": [
      { title: "Java OOP Basics & Pillars", type: "Video", tag: "tag-video", duration: "12 mins", link: "#" },
      { title: "Encapsulation & Getters/Setters", type: "Article", tag: "tag-article", duration: "6 mins read", link: "#" },
      { title: "Design a Student Class", type: "Practice", tag: "tag-practice", duration: "2 exercises", link: "#" }
    ]
  }

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

  // Quiz state
  const [answers, setAnswers] = useState({ q1: null, q2: null })
  const [quizSubmitted, setQuizSubmitted] = useState(false)

  const handleComplete = (clickedIndex) => {
    const completedItem = schedule[clickedIndex]
    setSchedule((prev) =>
      prev.map((item, idx) => (idx === clickedIndex ? { ...item, status: "completed" } : item))
    )
    setAgentTrace((prev) => [
      ...prev,
      `Session completed: Day ${completedItem.dayNumber} - ${completedItem.topic}`
    ])
  }

  const handleMissed = (clickedIndex) => {
    const missedItem = schedule[clickedIndex]

    setSchedule((prevSchedule) => {
      const pastItems = prevSchedule.slice(0, clickedIndex)
      const markedMissed = { ...missedItem, status: "missed" }
      const topicsToLearn = [
        missedItem.topic,
        ...prevSchedule.slice(clickedIndex + 1).map((item) => item.topic)
      ]
      const nextStartDay = missedItem.dayNumber + 1
      const rescheduledItems = topicsToLearn.map((topic, offset) => ({
        id: Date.now() + offset,
        dayNumber: nextStartDay + offset,
        topic: topic,
        status: "pending"
      }))
      return [...pastItems, markedMissed, ...rescheduledItems]
    })

    setAgentTrace((prev) => [
      ...prev,
      `⚠️ ALERT: Student missed Day ${missedItem.dayNumber}!`,
      `🧠 AGENT REPLANNING: Rescheduling "${missedItem.topic}" to Day ${missedItem.dayNumber + 1}.`,
      `⏩ Pushing subsequent lessons forward so zero content is lost.`
    ])
  }

  // Quiz submission & agent reassessment
  const handleQuizSubmit = () => {
    let correctCount = 0
    if (answers.q1 === "A") correctCount++
    if (answers.q2 === "B") correctCount++
    const percentage = Math.round((correctCount / 2) * 100)
    setQuizSubmitted(true)

    if (percentage >= 80) {
      // Branch 1: High Score -> Topic mastered!
      setScores((prev) =>
        prev.map((s) =>
          s.topic === "Recursion"
            ? { ...s, score: 85, color: "#10b981", tag: "Mastered" }
            : s
        )
      )
      setActiveTopic("OOP Concepts")

      // Add OOP next
      const maxDay = schedule[schedule.length - 1].dayNumber
      setSchedule((prev) => [
        ...prev,
        { id: Date.now(), dayNumber: maxDay + 1, topic: "OOP: Classes & Encapsulation", status: "pending" }
      ])

      setAgentTrace((prev) => [
        ...prev,
        `📝 Quiz Result: ${percentage}% on Recursion!`,
        `🎉 EVALUATION: Student has achieved mastery in Recursion (Score updated to 85%).`,
        `🧠 AGENT DECISION: Transitioning to next weak topic: OOP Concepts.`
      ])
    } else {
      // Branch 2: Low Score -> Add remedial session
      const maxDay = schedule[schedule.length - 1].dayNumber
      setSchedule((prev) => [
        ...prev,
        { id: Date.now(), dayNumber: maxDay + 1, topic: "Remedial Practice: Base Cases & Tree Recursion", status: "pending" },
        { id: Date.now() + 1, dayNumber: maxDay + 2, topic: "Retake Recursion Assessment", status: "pending" }
      ])

      setAgentTrace((prev) => [
        ...prev,
        `📝 Quiz Result: ${percentage}% on Recursion.`,
        `⚠️ EVALUATION: Concept gap persists in Recursion.`,
        `🧠 AGENT DECISION: Adding 2 remedial reinforcement sessions to schedule.`
      ])
    }
  }

  return (
    <div className="container">
      <header>
        <h1>LearnFlow</h1>
        <p>Autonomous AI Learning Planner</p>
      </header>

      {/* 1. Target Goal */}
      <div className="card">
        <h2>Target Learning Goal</h2>
        <input 
          type="text" 
          value={goal} 
          onChange={(e) => setGoal(e.target.value)}
          style={{ width: '100%', padding: '8px', fontSize: '1rem' }}
        />
      </div>

      {/* 2. Diagnostic Scores */}
      <div className="card">
        <h2>Diagnostic Performance & Topic Status</h2>
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

      {/* 3. Agent Decision Log */}
      <div className="card">
        <h2>Agent Decision Log (Proof of Autonomy)</h2>
        <div className="trace-box">
          {agentTrace.map((log, i) => (
            <div key={i}>&gt; {log}</div>
          ))}
        </div>
      </div>
       {/* Dynamic Resource Recommendations */}
      <div className="card">
        <h2>AI-Retrieved Resources ({activeTopic})</h2>
        <div className="resources-grid">
          {resourceBank[activeTopic]?.map((res, i) => (
            <div key={i} className="resource-card">
              <div>
                <span className={`resource-tag ${res.tag}`}>{res.type}</span>
                <p style={{ marginTop: '6px', fontWeight: 'bold' }}>{res.title}</p>
                <small style={{ color: '#64748b' }}>{res.duration}</small>
              </div>
              <a href={res.link} className="resource-link" onClick={(e) => e.preventDefault()}>
                Open Material →
              </a>
            </div>
          ))}
        </div>
      </div>
      {/* 4. Interactive Study Plan */}
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

      {/* 5. Assessment Card */}
      <div className="card">
        <h2>Topic Assessment: Recursion</h2>
        {!quizSubmitted ? (
          <div className="quiz-box">
            <div className="quiz-q">
              <p><strong>1. What happens if a recursive function does not have a base case?</strong></p>
              <div className="quiz-options">
                <button 
                  className={answers.q1 === "A" ? "selected" : ""} 
                  onClick={() => setAnswers({ ...answers, q1: "A" })}>
                  A) StackOverflowError
                </button>
                <button 
                  className={answers.q1 === "B" ? "selected" : ""} 
                  onClick={() => setAnswers({ ...answers, q1: "B" })}>
                  B) Returns 0
                </button>
              </div>
            </div>

            <div className="quiz-q">
              <p><strong>2. In recursion, each function call is placed onto the:</strong></p>
              <div className="quiz-options">
                <button 
                  className={answers.q2 === "A" ? "selected" : ""} 
                  onClick={() => setAnswers({ ...answers, q2: "A" })}>
                  A) Heap Memory
                </button>
                <button 
                  className={answers.q2 === "B" ? "selected" : ""} 
                  onClick={() => setAnswers({ ...answers, q2: "B" })}>
                  B) Call Stack
                </button>
              </div>
            </div>

            <button 
              className="btn-submit-quiz" 
              disabled={!answers.q1 || !answers.q2}
              onClick={handleQuizSubmit}>
              Submit for AI Reassessment
            </button>
          </div>
        ) : (
          <p style={{ color: '#10b981', fontWeight: 'bold' }}>
            Assessment submitted! Check the Agent Decision Log above to see the adaptation.
          </p>
        )}
      </div>
    </div>
  )
}

export default App