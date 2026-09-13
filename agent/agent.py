"""
agent/agent.py

The main Agentic Orchestrator for LearnFlow. Connects state, decisions,
replanner, and simulated tools into a goal-driven execution loop.
"""

from typing import Dict, Any, List
from agent.state import create_initial_state, update_performance, mark_session_status
from agent.decisions import evaluate_next_action
from agent.replanner import adapt_schedule_for_missed_sessions, adapt_schedule_for_low_score


class LearnFlowAgent:
    def __init__(self, goal: str, performance: Dict[str, int]):
        self.state = create_initial_state(goal, performance)
        self.execution_trace: List[Dict[str, Any]] = []

    def step(self) -> Dict[str, Any]:
        """
        Executes a single step of the agent loop:
        Evaluate state -> Decide Action -> Take Action -> Update State
        """
        decision = evaluate_next_action(self.state)
        action = decision["action"]
        reason = decision["reason"]
        target = decision["target_topic"]

        trace_entry = {
            "action": action,
            "reason": reason,
            "target_topic": target,
            "previous_status": self.state["status"]
        }

        # Handle actions
        if action == "GENERATE_PLAN":
            self._generate_plan(target)
        elif action == "REPLAN":
            self.state = adapt_schedule_for_missed_sessions(self.state)
        elif action == "COMPLETE":
            self.state["status"] = "completed"

        trace_entry["updated_status"] = self.state["status"]
        trace_entry["current_plan"] = list(self.state["current_plan"])
        self.execution_trace.append(trace_entry)

        return trace_entry

    def _generate_plan(self, topic: str):
        """Simulates resource retrieval and initial schedule creation."""
        new_plan = [
            f"{topic} Concept Overview",
            f"{topic} Deep Dive & Examples",
            f"{topic} Practice Exercises",
            f"{topic} Assessment Quiz"
        ]
        self.state["current_plan"] = new_plan
        self.state["status"] = "learning"

    def simulate_missed_session(self, session_name: str):
        """Simulates an observation of a missed session."""
        self.state = mark_session_status(self.state, session_name, "missed")

    def simulate_quiz_score(self, topic: str, score: int):
        """Simulates an assessment result observation."""
        self.state = update_performance(self.state, topic, score)
        if score < 60:
            self.state = adapt_schedule_for_low_score(self.state, topic, score)


# Quick runner function for testing
def run_demo_simulation():
    agent = LearnFlowAgent("Learn Java in 30 days", {"Arrays": 75, "OOP": 45, "Recursion": 30})
    
    print("--- STEP 1: Initial Decision ---")
    print(agent.step())

    print("\n--- STEP 2: Simulate Missed Session ---")
    agent.simulate_missed_session("Recursion Concept Overview")
    print(agent.step())

    return agent