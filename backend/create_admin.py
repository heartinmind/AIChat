"""
초기 Admin 계정 생성 스크립트
"""

from sqlalchemy.orm import Session
from database.connection import SessionLocal, engine
from database.models import Base, Agent
from passlib.context import CryptContext
import uuid

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_account():
    """초기 Admin 계정 생성"""
    db = SessionLocal()
    
    try:
        # 기존 Admin 계정 확인
        existing_admin = db.query(Agent).filter(Agent.email == "admin@elitebeauty.com").first()
        
        if existing_admin:
            print("Admin 계정이 이미 존재합니다.")
            return
        
        # Admin 계정 생성
        admin = Agent(
            agent_id=uuid.uuid4(),
            name="시스템 관리자",
            email="admin@elitebeauty.com",
            password_hash=pwd_context.hash("admin123"),
            department="IT",
            role="시스템 관리자",
            status="active",
            is_admin=True
        )
        
        db.add(admin)
        db.commit()
        
        print("Admin 계정이 생성되었습니다.")
        print("이메일: admin@elitebeauty.com")
        print("비밀번호: admin123")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # Admin 계정 생성
    create_admin_account()
