import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, Task
from app.main import validate_unique_title

# تعريف الـ Fixture هنا مباشرة لضمان عمله
@pytest.fixture
def db_session():
    # إنشاء قاعدة بيانات في الذاكرة (سريعة جداً للاختبار)
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # إنشاء الجداول
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# دالة الاختبار
def test_validate_unique_title_logic(db_session):
    # 1. إضافة مهمة للتجربة
    fake_task = Task(title="Study FastAPI")
    db_session.add(fake_task)
    db_session.commit()

    # 2. اختبار حالة التكرار (يجب أن يفشل ويعطي ValueError)
    with pytest.raises(ValueError, match="Title already exists"):
        validate_unique_title("Study FastAPI", db_session)

    # 3. اختبار حالة العنوان الجديد (يجب أن ينجح)
    result = validate_unique_title("Finish My Assignment", db_session)
    assert result == "Finish My Assignment"