from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag.embedder import embed_document
from backend.rag.retriever import ask_question
from backend.agents.planner_agent import run_planner_agent
from backend.agents.quiz_agent import run_quiz_agent
from backend.agents.progress_agent import run_progress_agent
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Study Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

class PlannerRequest(BaseModel):
    subjects: str
    days: int
    hours_per_day: int

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5

class ProgressRequest(BaseModel):
    scores: dict

@app.get("/")
def root():
    return {"message": "AI Study Planner API is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    result = embed_document(file_path)
    return {"message": result, "filename": file.filename}

@app.post("/ask")
async def ask(request: QuestionRequest):
    answer = ask_question(request.question)
    return {"answer": answer}

@app.post("/plan")
async def create_plan(request: PlannerRequest):
    plan = run_planner_agent(request.subjects, request.days, request.hours_per_day)
    return {"plan": plan}

@app.post("/quiz")
async def generate_quiz(request: QuizRequest):
    questions = run_quiz_agent(request.topic, request.num_questions)
    return {"questions": questions}

@app.post("/progress")
async def track_progress(request: ProgressRequest):
    feedback = run_progress_agent(request.scores)
    return {"feedback": feedback}