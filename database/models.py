# 🗄️ SQLAlchemy 데이터베이스 모델
# PostgreSQL용 ORM 모델 정의

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, DECIMAL, Date, Time, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import uuid

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    birth_date = Column(Date)
    gender = Column(String(10))
    address = Column(Text)
    emergency_contact = Column(String(20))
    
    # 피부 정보
    skin_type = Column(String(20))
    skin_concerns = Column(ARRAY(Text))
    allergies = Column(ARRAY(Text))
    medical_history = Column(Text)
    current_medications = Column(Text)
    
    # 마케팅 동의
    marketing_consent = Column(Boolean, default=False)
    sms_consent = Column(Boolean, default=False)
    email_consent = Column(Boolean, default=False)
    
    # 멤버십 정보
    membership_level = Column(String(20), default='basic')
    total_spent = Column(DECIMAL(10,2), default=0)
    point_balance = Column(Integer, default=0)
    
    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_visit = Column(DateTime(timezone=True))
    status = Column(String(20), default='active')
    notes = Column(Text)
    
    # 관계
    appointments = relationship("Appointment", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")
    consultations = relationship("ConsultationSession", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")

class TreatmentCategory(Base):
    __tablename__ = 'treatment_categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon_url = Column(String(255))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계
    treatments = relationship("Treatment", back_populates="category")

class Treatment(Base):
    __tablename__ = 'treatments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey('treatment_categories.id'))
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    short_description = Column(String(500))
    
    # 가격 정보
    price = Column(DECIMAL(10,2), nullable=False)
    discounted_price = Column(DECIMAL(10,2))
    duration_minutes = Column(Integer, nullable=False)
    
    # 시술 정보
    target_area = Column(String(100))
    recommended_age_min = Column(Integer)
    recommended_age_max = Column(Integer)
    suitable_skin_types = Column(ARRAY(Text))
    
    # 사전/사후 관리
    pre_care_instructions = Column(Text)
    post_care_instructions = Column(Text)
    contraindications = Column(Text)
    possible_side_effects = Column(Text)
    
    # 재고 관리
    requires_inventory = Column(Boolean, default=False)
    current_stock = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=0)
    unit = Column(String(20))
    
    # 메타데이터
    is_active = Column(Boolean, default=True)
    popularity_score = Column(Integer, default=0)
    image_urls = Column(ARRAY(Text))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 관계
    category = relationship("TreatmentCategory", back_populates="treatments")
    appointments = relationship("Appointment", back_populates="treatment")
    reviews = relationship("Review", back_populates="treatment")

class Staff(Base):
    __tablename__ = 'staff'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    specialization = Column(ARRAY(Text))
    phone = Column(String(20))
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계
    appointments = relationship("Appointment", back_populates="staff")
    reviews = relationship("Review", back_populates="staff")

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_number = Column(String(20), unique=True, nullable=False)
    
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    treatment_id = Column(UUID(as_uuid=True), ForeignKey('treatments.id'), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staff.id'))
    
    # 예약 일시
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    # 상태 관리
    status = Column(String(20), default='scheduled')
    cancellation_reason = Column(Text)
    
    # 가격 정보
    original_price = Column(DECIMAL(10,2), nullable=False)
    discount_amount = Column(DECIMAL(10,2), default=0)
    final_price = Column(DECIMAL(10,2), nullable=False)
    payment_status = Column(String(20), default='pending')
    
    # 알림 설정
    reminder_sent = Column(Boolean, default=False)
    confirmation_sent = Column(Boolean, default=False)
    
    # 메타데이터
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(String(100))
    
    # 관계
    customer = relationship("Customer", back_populates="appointments")
    treatment = relationship("Treatment", back_populates="appointments")
    staff = relationship("Staff", back_populates="appointments")
    payments = relationship("Payment", back_populates="appointment")
    review = relationship("Review", back_populates="appointment", uselist=False)

class ConsultationSession(Base):
    __tablename__ = 'consultation_sessions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'))
    session_id = Column(String(100), unique=True, nullable=False)
    
    # 상담 정보
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    channel = Column(String(20), default='web')
    
    # AI 상담 결과
    identified_concerns = Column(ARRAY(Text))
    recommended_treatments = Column(ARRAY(UUID))
    customer_satisfaction_score = Column(Integer)
    
    # 메타데이터
    ip_address = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계
    customer = relationship("Customer", back_populates="consultations")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('consultation_sessions.id'), nullable=False)
    
    # 메시지 정보
    sender_type = Column(String(20), nullable=False)
    message_text = Column(Text, nullable=False)
    message_type = Column(String(20), default='text')
    
    # AI 처리 정보
    intent = Column(String(100))
    confidence_score = Column(DECIMAL(3,2))
    ai_model_version = Column(String(50))
    processing_time_ms = Column(Integer)
    
    # 메타데이터
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_sensitive = Column(Boolean, default=False)
    
    # 관계
    session = relationship("ConsultationSession", back_populates="messages")

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_number = Column(String(20), unique=True, nullable=False)
    
    appointment_id = Column(UUID(as_uuid=True), ForeignKey('appointments.id'))
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    
    # 결제 정보
    amount = Column(DECIMAL(10,2), nullable=False)
    payment_method = Column(String(20), nullable=False)
    payment_provider = Column(String(50))
    transaction_id = Column(String(100))
    
    # 상태
    status = Column(String(20), default='pending')
    
    # 메타데이터
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    receipt_url = Column(String(255))
    notes = Column(Text)
    
    # 관계
    appointment = relationship("Appointment", back_populates="payments")
    customer = relationship("Customer", back_populates="payments")

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey('appointments.id'))
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    treatment_id = Column(UUID(as_uuid=True), ForeignKey('treatments.id'), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staff.id'))
    
    # 평가 정보
    overall_rating = Column(Integer, nullable=False)
    service_rating = Column(Integer)
    cleanliness_rating = Column(Integer)
    value_rating = Column(Integer)
    
    # 리뷰 내용
    title = Column(String(200))
    content = Column(Text)
    pros = Column(Text)
    cons = Column(Text)
    
    # 이미지
    image_urls = Column(ARRAY(Text))
    
    # 상태
    is_verified = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    moderation_status = Column(String(20), default='pending')
    
    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    helpful_count = Column(Integer, default=0)
    
    # 관계
    appointment = relationship("Appointment", back_populates="review")
    customer = relationship("Customer", back_populates="reviews")
    treatment = relationship("Treatment", back_populates="reviews")
    staff = relationship("Staff", back_populates="reviews")

class Promotion(Base):
    __tablename__ = 'promotions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # 할인 정보
    discount_type = Column(String(20), nullable=False)
    discount_value = Column(DECIMAL(10,2), nullable=False)
    min_purchase_amount = Column(DECIMAL(10,2), default=0)
    
    # 적용 조건
    applicable_treatments = Column(ARRAY(UUID))
    customer_segments = Column(ARRAY(Text))
    usage_limit_per_customer = Column(Integer, default=1)
    total_usage_limit = Column(Integer)
    current_usage_count = Column(Integer, default=0)
    
    # 유효 기간
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # 메타데이터
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('staff.id'))

class APILog(Base):
    __tablename__ = 'api_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer)
    ip_address = Column(INET)
    user_agent = Column(Text)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'))
    request_body = Column(JSONB)
    response_body = Column(JSONB)
    error_message = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class BusinessMetric(Base):
    __tablename__ = 'business_metrics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(DECIMAL(15,2), nullable=False)
    metric_type = Column(String(50), nullable=False)
    period_type = Column(String(20), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
