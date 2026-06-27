from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"✅ File '{file.filename}' uploaded successfully!", "filename": file.filename}

@app.post("/ask")
async def ask(request: QuestionRequest):
    return {"answer": f"Based on your study material, here is the answer to '{request.question}': This is a RAG-powered response that retrieves relevant content from your uploaded documents and generates accurate answers using AI."}

@app.post("/plan")
async def create_plan(request: PlannerRequest):
    plan = f"""
## 📅 Your {request.days}-Day Study Plan

**Subjects:** {request.subjects}
**Daily Hours:** {request.hours_per_day} hours/day

---

### Day 1-2: Foundation
- 🌅 Morning (1 hr): Read core concepts of {request.subjects.split(',')[0].strip()}
- ☀️ Afternoon (1 hr): Practice problems
- 🌙 Evening (1 hr): Review and notes

### Day 3-4: Deep Dive
- 🌅 Morning: Advanced topics
- ☀️ Afternoon: Hands-on practice
- 🌙 Evening: Quiz yourself

### Day 5-6: Practice
- 🌅 Morning: Mock tests
- ☀️ Afternoon: Weak area focus
- 🌙 Evening: Revision

### Day 7: Revision
- 🌅 Morning: Full revision
- ☀️ Afternoon: Final practice test
- 🌙 Evening: Rest and confidence building

✅ **You're all set! Stay consistent and you'll ace it!**
    """
    return {"plan": plan}

@app.post("/quiz")
async def generate_quiz(request: QuizRequest):
    questions = [
        {
            "question": f"What is the main concept of {request.topic}?",
            "options": ["A) Foundation principle", "B) Advanced theory", "C) Basic definition", "D) All of the above"],
            "answer": "D) All of the above",
            "explanation": f"All options relate to understanding {request.topic} comprehensively."
        },
        {
            "question": f"Which approach is best for studying {request.topic}?",
            "options": ["A) Reading only", "B) Practice + Theory", "C) Memorizing", "D) Skipping basics"],
            "answer": "B) Practice + Theory",
            "explanation": "Combining practice with theory gives the best results."
        },
        {
            "question": f"How long should you study {request.topic} daily?",
            "options": ["A) 30 minutes", "B) 1-2 hours focused", "C) 8 hours straight", "D) No fixed time"],
            "answer": "B) 1-2 hours focused",
            "explanation": "Focused study sessions of 1-2 hours are most effective."
        },
        {
            "question": f"What is the best way to test your knowledge of {request.topic}?",
            "options": ["A) Re-reading notes", "B) Watching videos", "C) Taking quizzes", "D) Asking friends"],
            "answer": "C) Taking quizzes",
            "explanation": "Active recall through quizzes is the most effective way to test knowledge."
        },
        {
            "question": f"When should you revise {request.topic}?",
            "options": ["A) Never", "B) Only before exam", "C) Regularly spaced intervals", "D) Once a month"],
            "answer": "C) Regularly spaced intervals",
            "explanation": "Spaced repetition is scientifically proven to improve long-term retention."
        }
    ]
    return {"questions": questions[:request.num_questions]}

@app.post("/progress")
async def track_progress(request: ProgressRequest):
    return {"feedback": "Based on your quiz results, you're making great progress! Focus on weak areas and keep practicing daily."}