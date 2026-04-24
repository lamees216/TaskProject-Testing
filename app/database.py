from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# إعداد قاعدة البيانات
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- هذا هو الجزء الذي كان ينقصك (تعريف الجدول) ---
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
# -----------------------------------------------

# دالة الحصول على الجلسة
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()