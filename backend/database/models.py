"""
Database Models for Elite Beauty Clinic AI Consultation System
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey, Time, Float, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class SessionStatus(enum.Enum):
    active = "active"
    ended = "ended"
    abandoned = "abandoned"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    gender = Column(String(10))
    birth_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("Session", back_populates="user")

class Agent(Base):
    __tablename__ = "agents"
    
    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(50))
    role = Column(String(50))
    status = Column(String(20), default="inactive")  # active, inactive, busy
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime)
    
    # Relationships
    sessions = relationship("Session", back_populates="agent")

class Session(Base):
    __tablename__ = "sessions"
    
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.agent_id"), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.active)
    route_target = Column(String(20))  # "ai" or "agent"
    source = Column(String(20))  # "web", "mobile", "app"
    satisfaction_rating = Column(Integer, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    agent = relationship("Agent", back_populates="sessions")
    messages = relationship("Message", back_populates="session")
    summaries = relationship("Summary", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"))
    sender = Column(String(20))  # "user", "ai", "agent", "system"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    emotion_tag = Column(String(20), nullable=True)
    is_answer = Column(Boolean, default=False)
    
    # Relationships
    session = relationship("Session", back_populates="messages")

class Summary(Base):
    __tablename__ = "summaries"
    
    summary_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"))
    type = Column(String(20))  # "keyword", "full", "action"
    summary_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="summaries")

class WorkingHours(Base):
    __tablename__ = "working_hours"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_of_week = Column(Integer)  # 0=Sunday, 6=Saturday
    start_time = Column(Time)
    end_time = Column(Time)
    is_holiday = Column(Boolean, default=False)

class ClinicInfo(Base):
    __tablename__ = "clinic_info"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(50))  # "treatment", "price", "hours", "location"
    subcategory = Column(String(50), nullable=True)
    name = Column(String(100))
    price = Column(Integer, nullable=True)
    description = Column(Text)
    duration = Column(String(50), nullable=True)
    effect_period = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
