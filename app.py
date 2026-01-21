from fastapi import FastAPI
from agent.agent import run_agent

app = FastAPI()

@app.get("/")
def health():
    return {"status": "Privacy Agent running"}

@app.post("/ask")
def ask(query: str, user_id: str = "demo_user"):
    return run_agent(query, user_id)
