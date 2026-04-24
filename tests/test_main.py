from fastapi.testclient import TestClient
from app.main import app  # استيراد التطبيق الخاص بكِ

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # تأكدي أن النص هنا يطابق تماماً ما في ملف main.py
    assert response.json() == {"message": "Task Manager API is running"}