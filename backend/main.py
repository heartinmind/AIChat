"""
Elite Beauty Clinic AI Consultation System - Main API Server
Claude API 버전
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from typing import Optional, List
import os
import uvicorn
from datetime import datetime, time
import anthropic
from jose import jwt
from passlib.context import CryptContext

from database.connection import get_db, engine, DATABASE_URL
from database.models import Base, User, Agent, Session as DBSession, Message, Summary, WorkingHours, ClinicInfo
from pydantic import BaseModel, UUID4
from enum import Enum

# Claude API 클라이언트 초기화
claude_client = anthropic.Anthropic(
    api_key=os.getenv("CLAUDE_API_KEY", "your-claude-api-key-here")
)

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

# 보안 설정
security = HTTPBearer()

# Pydantic 모델들
class UserCreate(BaseModel):
    name: str
    phone: str
    gender: Optional[str] = None
    birth_year: Optional[int] = None

class SessionRoute(BaseModel):
    current_time: Optional[datetime] = None
    agent_status: Optional[str] = None

class MessageCreate(BaseModel):
    session_id: UUID4
    content: str
    sender: str = "user"

class AgentLogin(BaseModel):
    email: str
    password: str

class RouteResponse(BaseModel):
    target: str  # "agent" or "ai"
    reason: str

class SessionCreate(BaseModel):
    user_id: UUID4
    route_target: str
    agent_id: Optional[UUID4] = None

# 관리자 계정 자동 생성 함수
def create_default_admin(db: Session):
    """기본 관리자 계정 생성"""
    admin_email = "admin@elitebeauty.com"
    
    try:
        # 이미 존재하는지 확인
        existing_admin = db.query(Agent).filter(Agent.email == admin_email).first()
        if not existing_admin:
            # 관리자 계정 생성
            import uuid
            admin = Agent(
                agent_id=uuid.uuid4(),
                email=admin_email,
                name="관리자",
                password_hash=pwd_context.hash("admin123"),
                department="관리부",
                role="admin",
                is_admin=True,
                status="active"
            )
            db.add(admin)
            db.commit()
            print(f"✅ 기본 관리자 계정 생성됨: {admin_email} / 비밀번호: admin123")
            print(f"   계정 ID: {admin.agent_id}")
            print(f"   비밀번호 해시: {admin.password_hash[:20]}...")
        else:
            print(f"ℹ️ 관리자 계정이 이미 존재합니다: {admin_email}")
            print(f"   계정 ID: {existing_admin.agent_id}")
            print(f"   관리자 권한: {existing_admin.is_admin}")
            print(f"   상태: {existing_admin.status}")
    except Exception as e:
        print(f"❌ 관리자 계정 생성 중 오류: {e}")
        db.rollback()
        raise

# 데이터베이스 테이블 생성 및 초기 데이터 설정
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 애플리케이션 시작 중...")
    print(f"📁 작업 디렉토리: {os.getcwd()}")
    print(f"🗄️ 데이터베이스 URL: {DATABASE_URL}")
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 생성 완료")
    
    # 기본 관리자 계정 생성
    db = next(get_db())
    try:
        create_default_admin(db)
        
        # 생성된 계정 확인
        admin_count = db.query(Agent).filter(Agent.is_admin == True).count()
        print(f"📊 전체 관리자 계정 수: {admin_count}")
        
    except Exception as e:
        print(f"❌ 초기화 중 오류 발생: {e}")
    finally:
        db.close()
    
    print("✅ 애플리케이션 초기화 완료")
    
    yield
    
    # Shutdown
    print("👋 애플리케이션 종료 중...")

# 앱 생성
app = FastAPI(
    title="Elite Beauty Clinic AI Consultation API",
    version="1.0.0",
    description="병원 상담 시스템 API (Claude AI 기반)",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 헬퍼 함수들
def get_current_agent(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Agent:
    """현재 인증된 상담원 가져오기"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        agent_id = payload.get("agent_id")
        # 실제로는 DB에서 조회
        return agent_id
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication")

def is_working_hours(db: Session) -> bool:
    """현재 근무 시간인지 확인"""
    now = datetime.now()
    day_of_week = now.weekday()  # 0=Monday, 6=Sunday
    current_time = now.time()
    
    # PostgreSQL weekday와 Python weekday 변환 (PostgreSQL: 0=Sunday)
    pg_day_of_week = (day_of_week + 1) % 7
    
    working_hour = db.query(WorkingHours).filter(
        WorkingHours.day_of_week == pg_day_of_week,
        WorkingHours.is_holiday == False
    ).first()
    
    if not working_hour:
        return False
    
    return working_hour.start_time <= current_time <= working_hour.end_time

def get_available_agent(db: Session) -> Optional[Agent]:
    """사용 가능한 상담원 찾기"""
    return db.query(Agent).filter(
        Agent.status == "active",
        Agent.is_admin == False
    ).first()

async def get_claude_response(message: str, context: str = "") -> str:
    """Claude API를 사용한 응답 생성"""
    system_prompt = """당신은 엘리트 뷰티 클리닉의 AI 상담사입니다.
    
핵심 역할:
- 친근하고 자연스러운 대화를 나눕니다
- 일상적인 대화도 가능하며, 필요할 때 병원 정보를 제공합니다
- 고객이 편안함을 느낄 수 있도록 대화합니다
- 병원 관련 질문이 아니어도 친절하게 응답합니다

대화 스타일:
- 딱딱한 상담사가 아닌 친구처럼 대화합니다
- 이모티콘이나 친근한 표현을 적절히 사용합니다
- 상황에 맞게 유머도 사용할 수 있습니다
- 고객의 감정에 공감하고 반응합니다

병원 정보 (필요시 제공):
- 위치: 서울시 강남구 청담동 엘리트타워 5층
- 영업시간: 평일 10:00-20:00, 토요일 10:00-17:00, 일요일 휴무
- 전화: 02-1234-5678

주요 시술 (관련 질문시 안내):
- 보톡스: 이마(15만원), 미간(10만원), 눈가(15만원)
- 필러: 팔자주름(40만원), 볼(60만원), 턱(50만원)
- 레이저: 기미(회당 20만원), 모공(회당 30만원)

중요: 고객이 일상 대화를 원하면 자연스럽게 응대하고, 병원 관련 질문을 할 때만 상담사 역할을 합니다."""
    
    try:
        # 대화 컨텍스트가 있으면 메시지와 함께 전달
        if context:
            full_message = f"이전 대화:\n{context}\n\n현재 메시지: {message}"
        else:
            full_message = message
            
        response = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": full_message}
            ]
        )
        return response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
    except Exception as e:
        print(f"Claude API 오류: {e}")
        return "죄송합니다. 잠시 기술적인 문제가 발생했습니다. 잠시 후 다시 시도해주세요."

# API 엔드포인트들

@app.get("/")
async def root():
    return {"message": "Elite Beauty Clinic AI Consultation API"}

@app.post("/api/session/route", response_model=RouteResponse)
async def determine_route(db: Session = Depends(get_db)):
    """상담 주체 결정 (근무시간 체크)"""
    if is_working_hours(db):
        available_agent = get_available_agent(db)
        if available_agent:
            return RouteResponse(
                target="agent",
                reason="상담원이 대기 중입니다"
            )
    
    return RouteResponse(
        target="ai",
        reason="AI 상담사가 도와드리겠습니다"
    )

@app.post("/api/users", response_model=dict)
async def create_or_get_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """사용자 생성 또는 조회"""
    # 기존 사용자 확인
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    
    if existing_user:
        return {
            "user_id": str(existing_user.user_id),
            "is_existing": True,
            "name": existing_user.name
        }
    
    # 새 사용자 생성
    new_user = User(
        name=user_data.name,
        phone=user_data.phone,
        gender=user_data.gender,
        birth_year=user_data.birth_year
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "user_id": str(new_user.user_id),
        "is_existing": False,
        "name": new_user.name
    }

@app.post("/api/sessions", response_model=dict)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    """새 상담 세션 생성"""
    # 기존 활성 세션 확인
    active_session = db.query(DBSession).filter(
        DBSession.user_id == session_data.user_id,
        DBSession.status == "active"
    ).first()
    
    if active_session:
        return {
            "session_id": str(active_session.session_id),
            "is_new": False
        }
    
    # 새 세션 생성
    new_session = DBSession(
        user_id=session_data.user_id,
        agent_id=session_data.agent_id,
        route_target=session_data.route_target,
        source="web"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "session_id": str(new_session.session_id),
        "is_new": True
    }

@app.post("/api/messages", response_model=dict)
async def send_message(message_data: MessageCreate, db: Session = Depends(get_db)):
    """메시지 전송 및 응답 생성"""
    # 세션 확인
    session = db.query(DBSession).filter(
        DBSession.session_id == message_data.session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 사용자 메시지 저장
    user_message = Message(
        session_id=message_data.session_id,
        sender="user",
        content=message_data.content
    )
    db.add(user_message)
    
    # AI 응답 생성 (Claude API 사용)
    if session.route_target == "ai":
        # 이전 대화 컨텍스트 가져오기
        previous_messages = db.query(Message).filter(
            Message.session_id == message_data.session_id
        ).order_by(Message.timestamp.desc()).limit(10).all()
        
        context = "\n".join([f"{msg.sender}: {msg.content}" for msg in reversed(previous_messages)])
        
        ai_response = await get_claude_response(message_data.content, context)
        
        # AI 응답 저장
        ai_message = Message(
            session_id=message_data.session_id,
            sender="ai",
            content=ai_response,
            is_answer=True
        )
        db.add(ai_message)
        db.commit()
        
        return {
            "response": ai_response,
            "sender": "ai"
        }
    else:
        # 상담원 응답 대기 (실제로는 WebSocket 등으로 구현)
        return {
            "response": "상담원이 곧 응답할 예정입니다.",
            "sender": "system"
        }

@app.get("/api/sessions/{session_id}/messages", response_model=List[dict])
async def get_session_messages(session_id: UUID4, db: Session = Depends(get_db)):
    """세션의 모든 메시지 조회"""
    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(Message.timestamp).all()
    
    return [
        {
            "message_id": str(msg.message_id),
            "sender": msg.sender,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
            "emotion_tag": msg.emotion_tag,
            "is_answer": msg.is_answer
        }
        for msg in messages
    ]

@app.put("/api/sessions/{session_id}/end")
async def end_session(session_id: UUID4, db: Session = Depends(get_db)):
    """세션 종료"""
    session = db.query(DBSession).filter(
        DBSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.status = "ended"
    session.ended_at = datetime.utcnow()
    
    # 세션 요약 생성 (Claude API 사용)
    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(Message.timestamp).all()
    
    if messages:
        conversation = "\n".join([f"{msg.sender}: {msg.content}" for msg in messages])
        
        summary_prompt = f"""다음 상담 대화를 간단히 요약해주세요:

{conversation}

요약 형식:
- 주요 상담 내용:
- 제공된 정보:
- 후속 조치:"""
        
        try:
            summary_response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": summary_prompt}]
            )
            
            summary_text = summary_response.content[0].text if hasattr(summary_response.content[0], 'text') else str(summary_response.content[0])
            
            summary = Summary(
                session_id=session_id,
                type="keyword",
                summary_text=summary_text
            )
            db.add(summary)
        except Exception as e:
            print(f"요약 생성 오류: {e}")
    
    db.commit()
    
    return {"message": "Session ended successfully"}

@app.get("/api/clinic/info")
async def get_clinic_info(category: Optional[str] = None, db: Session = Depends(get_db)):
    """병원 정보 조회"""
    query = db.query(ClinicInfo).filter(ClinicInfo.is_active == True)
    
    if category:
        query = query.filter(ClinicInfo.category == category)
    
    clinic_info = query.all()
    
    return [
        {
            "id": str(info.id),
            "category": info.category,
            "subcategory": info.subcategory,
            "name": info.name,
            "price": info.price,
            "description": info.description,
            "duration": info.duration,
            "effect_period": info.effect_period
        }
        for info in clinic_info
    ]

# 상담원 관련 API
@app.post("/api/agents/login")
async def agent_login(login_data: AgentLogin, db: Session = Depends(get_db)):
    """상담원 로그인"""
    print(f"🔐 로그인 시도: {login_data.email}")
    
    agent = db.query(Agent).filter(Agent.email == login_data.email).first()
    
    if not agent:
        print(f"❌ 계정 없음: {login_data.email}")
        # 모든 에이전트 목록 출력 (디버깅용)
        all_agents = db.query(Agent).all()
        print(f"📋 전체 에이전트 수: {len(all_agents)}")
        for a in all_agents:
            print(f"   - {a.email} (관리자: {a.is_admin})")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not pwd_context.verify(login_data.password, agent.password_hash):
        print(f"❌ 비밀번호 불일치: {login_data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    print(f"✅ 로그인 성공: {login_data.email}")
    
    # JWT 토큰 생성
    token_data = {
        "agent_id": str(agent.agent_id),
        "email": agent.email,
        "name": agent.name,
        "is_admin": agent.is_admin
    }
    token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    # 상태 업데이트
    agent.status = "active"
    agent.last_active = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": token,
        "agent_id": str(agent.agent_id),
        "name": agent.name,
        "is_admin": agent.is_admin
    }

@app.get("/api/agents/sessions")
async def get_agent_sessions(
    current_agent: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """상담원의 활성 세션 목록"""
    sessions = db.query(DBSession).filter(
        DBSession.agent_id == current_agent,
        DBSession.status == "active"
    ).all()
    
    return [
        {
            "session_id": str(session.session_id),
            "user_name": session.user.name,
            "started_at": session.started_at.isoformat(),
            "message_count": len(session.messages)
        }
        for session in sessions
    ]

# Admin API 엔드포인트들
@app.get("/api/admin/dashboard")
async def get_dashboard_stats(
    current_agent: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """대시보드 통계 조회"""
    today = datetime.now().date()
    
    # 오늘 상담 건수
    today_sessions = db.query(DBSession).filter(
        DBSession.started_at >= datetime.combine(today, time.min)
    ).count()
    
    # 진행 중인 상담
    active_sessions = db.query(DBSession).filter(
        DBSession.status == "active"
    ).count()
    
    # 전체 사용자 수
    total_users = db.query(User).count()
    
    # 활성 상담원 수
    active_agents = db.query(Agent).filter(
        Agent.status == "active"
    ).count()
    
    return {
        "today_sessions": today_sessions,
        "active_sessions": active_sessions,
        "total_users": total_users,
        "active_agents": active_agents
    }

@app.get("/api/admin/sessions")
async def get_all_sessions(
    skip: int = 0,
    limit: int = 10,
    current_agent: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """모든 상담 세션 조회 (Admin)"""
    sessions = db.query(DBSession).order_by(
        DBSession.started_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "session_id": str(session.session_id),
            "user_name": session.user.name if session.user else "Unknown",
            "agent_name": session.agent.name if session.agent else "AI",
            "started_at": session.started_at.isoformat(),
            "ended_at": session.ended_at.isoformat() if session.ended_at else None,
            "status": session.status,
            "route_target": session.route_target,
            "message_count": len(session.messages)
        }
        for session in sessions
    ]

@app.get("/api/admin/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 10,
    current_agent: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """모든 사용자 조회 (Admin)"""
    users = db.query(User).order_by(
        User.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "user_id": str(user.user_id),
            "name": user.name,
            "phone": user.phone,
            "created_at": user.created_at.isoformat(),
            "session_count": len(user.sessions),
            "last_session": max([s.started_at for s in user.sessions]).isoformat() if user.sessions else None
        }
        for user in users
    ]

@app.get("/api/admin/agents")
async def get_all_agents(
    current_agent: str = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """모든 상담원 조회 (Admin)"""
    agents = db.query(Agent).all()
    
    return [
        {
            "agent_id": str(agent.agent_id),
            "name": agent.name,
            "email": agent.email,
            "department": agent.department,
            "role": agent.role,
            "status": agent.status,
            "is_admin": agent.is_admin,
            "created_at": agent.created_at.isoformat(),
            "last_active": agent.last_active.isoformat() if agent.last_active else None
        }
        for agent in agents
    ]

# 건강 체크
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "ai_engine": "Claude 3 Sonnet"
    }

# 관리자 계정 확인 엔드포인트 (디버깅용)
@app.get("/api/debug/admin-check")
async def check_admin_exists(db: Session = Depends(get_db)):
    """관리자 계정 존재 여부 확인 (개발용)"""
    admin = db.query(Agent).filter(Agent.email == "admin@elitebeauty.com").first()
    all_agents = db.query(Agent).all()
    
    return {
        "admin_exists": admin is not None,
        "admin_email": admin.email if admin else None,
        "admin_name": admin.name if admin else None,
        "is_admin": admin.is_admin if admin else None,
        "total_agents": len(all_agents),
        "all_agents": [
            {
                "email": agent.email,
                "name": agent.name,
                "is_admin": agent.is_admin,
                "status": agent.status
            }
            for agent in all_agents
        ],
        "database_path": DATABASE_URL,
        "working_directory": os.getcwd()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )