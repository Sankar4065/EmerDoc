from agents.base import Agent

class ReasoningAgent(Agent):
    def run(self, context: dict) -> dict:
        print("Reasoning agent running...")

        return {
            "answer": context["retrieved"],
            "intent": context["intent"],
            "source": "qdrant_memory"
        }
