"""
Database models for Elite Beauty Clinic AI Consultation System
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey, ARRAY, Time, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class AgentStatus(enum.Enum):
    ACTIVE = "active"
    OFFLINE = "offline"
    ON_CALL = "on_call"

class SessionStatus(enum.Enum):
    ACTIVE = "active"
    ENDED = "ended"
    FAILED = "failed"

class SourceType(enum.Enum):
    WEB = "web"
    MOBILE = "mobile"
    KAKAO = "kakao"

class RouteTarget(enum.Enum):
    AGENT = "agent"
    AI = "ai"

class SenderType(enum.Enum):
    USER = "user"
    AGENT = "agent"
    AI = "ai"

class SummaryType(enum.Enum):
    RAG = "rag"
    EMOTION = "emotion"
    KEYWORD = "keyword"

class CreatedBy(enum.Enum):
    AI = "ai"
    HUMAN = "human"

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    gender = Column(String(10))
    birth_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    sessions = relationship("Session", back_populates="user")

class Agent(Base):
    __tablename__ = 'agents'
    
    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.OFFLINE)
    department = Column(String(50))
    last_active = Column(DateTime)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("Session", back_populates="agent")

class Session(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.agent_id'), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE)
    source = Column(Enum(SourceType), default=SourceType.WEB)
    route_target = Column(Enum(RouteTarget))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    agent = relationship("Agent", back_populates="sessions")
    messages = relationship("Message", back_populates="session")
    summaries = relationship("Summary", back_populates="session")

class Message(Base):
    __tablename__ = 'messages'
    
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.session_id'))
    sender = Column(Enum(SenderType), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    emotion_tag = Column(String(50))
    is_answer = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="messages")

class Summary(Base):
    __tablename__ = 'summaries'
    
    summary_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.session_id'))
    type = Column(Enum(SummaryType), nullable=False)
    summary_text = Column(Text, nullable=False)
    created_by = Column(Enum(CreatedBy), default=CreatedBy.AI)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="summaries")

class WorkingHours(Base):
    __tablename__ = 'working_hours'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_of_week = Column(Integer, nullable=False)  # 0=Sunday, 6=Saturday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_holiday = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RAGDocument(Base):
    __tablename__ = 'rag_documents'
    
    document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50))
    keywords = Column(ARRAY(Text))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ClinicInfo(Base):
    __tablename__ = 'clinic_info'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50))
    name = Column(String(100), nullable=False)
    price = Column(String(50))
    description = Column(Text)
    duration = Column(String(50))
    effect_period = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)