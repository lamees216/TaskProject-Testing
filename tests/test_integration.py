from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# قاعدة بيانات للاختبار
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_integration.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

# Override للـ dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_and_retrieve_task():
    """
    اختبار: إنشاء مهمة ثم جلبها
    """
    # 1. إنشاء مهمة
    response = client.post("/tasks/?title=Integration Test Task")
    assert response.status_code == 200
    task_data = response.json()
    assert task_data["title"] == "Integration Test Task"
    task_id = task_data["id"]
    
    # 2. جلب كل المهام
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    
    # 3. التحقق من وجود المهمة
    assert any(task["id"] == task_id for task in tasks)

def test_duplicate_task_rejected():
    """
    اختبار: رفض المهمة المكررة
    """
    # 1. إنشاء مهمة
    response = client.post("/tasks/?title=Unique Task")
    assert response.status_code == 200
    
    # 2. محاولة إنشاء نفس المهمة
    response = client.post("/tasks/?title=Unique Task")
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_short_title_rejected():
    """
    اختبار: رفض العنوان القصير
    """
    response = client.post("/tasks/?title=Hi")
    assert response.status_code == 400
    assert "too short" in response.json()["detail"]

def test_empty_tasks_list():
    """
    اختبار: قائمة فارغة عند البداية
    """
    # حذف كل المهام أولاً
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []

def test_multiple_tasks():
    """
    اختبار: إضافة عدة مهام
    """
    tasks = ["Task 1", "Task 2", "Task 3"]
    
    for task in tasks:
        response = client.post(f"/tasks/?title={task}")
        assert response.status_code == 200
    
    response = client.get("/tasks/")
    assert len(response.json()) >= len(tasks)