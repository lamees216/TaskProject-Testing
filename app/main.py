from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import database
from app.database import engine, Base  # تأكدي من استيراد engine و Base

app = FastAPI()
# هذا الجزء يقوم بإنشاء الجداول عند بدء تشغيل السيرفر تلقائياً
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
# دالة 1: التحقق من الطول
def validate_task_title(title: str):
    if len(title) < 3:
        raise ValueError("Title too short")
    return title.strip()

# دالة 2: التحقق من التكرار (تأكدي من وجود هذه الدالة تحديداً)
def validate_unique_title(title: str, db: Session):
    existing_task = db.query(database.Task).filter(database.Task.title == title).first()
    if existing_task:
        raise ValueError("Title already exists")
    return title.strip()

@app.get("/")
def read_root():
    return {"message": "Task Manager API is running"}

@app.post("/tasks/")
def create_task(title: str, db: Session = Depends(database.get_db)):
    try:
        clean_title = validate_task_title(title)
        validate_unique_title(clean_title, db) # استخدام الدالة الجديدة
        
        new_task = database.Task(title=clean_title)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks/")
def get_tasks(db: Session = Depends(database.get_db)):
    return db.query(database.Task).all()
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # غيري هذه الجملة لتطابق ما هو موجود في main.py
    assert response.json() == {"message": "Task Manager API is running"}