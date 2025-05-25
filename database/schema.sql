-- 🏥 엘리트 뷰티 클리닉 데이터베이스 스키마
-- 실제 상용 서비스용 완전한 스키마 설계

-- ================================
-- 1. 고객 관리 테이블
-- ================================

-- 고객 기본 정보
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_code VARCHAR(20) UNIQUE NOT NULL, -- BC2024001 형태
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    birth_date DATE,
    gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
    address TEXT,
    emergency_contact VARCHAR(20),
    
    -- 피부 정보
    skin_type VARCHAR(20) CHECK (skin_type IN ('oily', 'dry', 'combination', 'sensitive', 'normal')),
    skin_concerns TEXT[], -- ['wrinkles', 'pigmentation', 'acne']
    allergies TEXT[],
    medical_history TEXT,
    current_medications TEXT,
    
    -- 마케팅 동의
    marketing_consent BOOLEAN DEFAULT false,
    sms_consent BOOLEAN DEFAULT false,
    email_consent BOOLEAN DEFAULT false,
    
    -- 멤버십 정보
    membership_level VARCHAR(20) DEFAULT 'basic' CHECK (membership_level IN ('basic', 'silver', 'gold', 'vip')),
    total_spent DECIMAL(10,2) DEFAULT 0,
    point_balance INTEGER DEFAULT 0,
    
    -- 메타데이터
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_visit TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'blocked')),
    notes TEXT
);

-- ================================
-- 2. 시술 및 상품 관리
-- ================================

-- 시술 카테고리
CREATE TABLE treatment_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url VARCHAR(255),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 시술/상품 정보
CREATE TABLE treatments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID REFERENCES treatment_categories(id),
    code VARCHAR(20) UNIQUE NOT NULL, -- BTX001, FILL002 등
    name VARCHAR(200) NOT NULL,
    description TEXT,
    short_description VARCHAR(500),
    
    -- 가격 정보
    price DECIMAL(10,2) NOT NULL,
    discounted_price DECIMAL(10,2),
    duration_minutes INTEGER NOT NULL, -- 시술 소요 시간
    
    -- 시술 정보
    target_area VARCHAR(100), -- '이마', '눈가', '볼' 등
    recommended_age_min INTEGER,
    recommended_age_max INTEGER,
    suitable_skin_types TEXT[], -- ['oily', 'dry']
    
    -- 사전/사후 관리
    pre_care_instructions TEXT,
    post_care_instructions TEXT,
    contraindications TEXT, -- 금기사항
    possible_side_effects TEXT,
    
    -- 재고 관리 (주사류 등)
    requires_inventory BOOLEAN DEFAULT false,
    current_stock INTEGER DEFAULT 0,
    min_stock_level INTEGER DEFAULT 0,
    unit VARCHAR(20), -- 'vial', 'ml', 'piece'
    
    -- 메타데이터
    is_active BOOLEAN DEFAULT true,
    popularity_score INTEGER DEFAULT 0,
    image_urls TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ================================
-- 3. 예약 관리 시스템
-- ================================

-- 직원/의사 정보
CREATE TABLE staff (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    staff_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'doctor', 'nurse', 'manager', 'receptionist'
    specialization TEXT[], -- ['botox', 'filler', 'laser']
    phone VARCHAR(20),
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 예약 정보
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_number VARCHAR(20) UNIQUE NOT NULL, -- APT20240525001
    
    customer_id UUID NOT NULL REFERENCES customers(id),
    treatment_id UUID NOT NULL REFERENCES treatments(id),
    staff_id UUID REFERENCES staff(id),
    
    -- 예약 일시
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL,
    
    -- 상태 관리
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show')),
    cancellation_reason TEXT,
    
    -- 가격 정보
    original_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    final_price DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'partial', 'paid', 'refunded')),
    
    -- 알림 설정
    reminder_sent BOOLEAN DEFAULT false,
    confirmation_sent BOOLEAN DEFAULT false,
    
    -- 메타데이터
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(100) -- 'customer', 'staff', 'ai_chatbot'
);

-- ================================
-- 4. 상담 및 AI 채팅 기록
-- ================================

-- 상담 세션
CREATE TABLE consultation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id),
    session_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- 상담 정보
    start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_time TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    channel VARCHAR(20) DEFAULT 'web' CHECK (channel IN ('web', 'mobile', 'phone', 'in_person')),
    
    -- AI 상담 결과
    identified_concerns TEXT[],
    recommended_treatments UUID[],
    customer_satisfaction_score INTEGER CHECK (customer_satisfaction_score BETWEEN 1 AND 5),
    
    -- 메타데이터
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 채팅 메시지 기록
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES consultation_sessions(id),
    
    -- 메시지 정보
    sender_type VARCHAR(20) NOT NULL CHECK (sender_type IN ('customer', 'ai', 'staff')),
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text' CHECK (message_type IN ('text', 'image', 'file', 'quick_reply')),
    
    -- AI 처리 정보
    intent VARCHAR(100), -- 'booking_inquiry', 'treatment_info', 'price_question'
    confidence_score DECIMAL(3,2),
    ai_model_version VARCHAR(50),
    processing_time_ms INTEGER,
    
    -- 메타데이터
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_sensitive BOOLEAN DEFAULT false -- 개인정보 포함 여부
);

-- ================================
-- 5. 결제 및 재무 관리
-- ================================

-- 결제 정보
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_number VARCHAR(20) UNIQUE NOT NULL, -- PAY20240525001
    
    appointment_id UUID REFERENCES appointments(id),
    customer_id UUID NOT NULL REFERENCES customers(id),
    
    -- 결제 정보
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL CHECK (payment_method IN ('card', 'cash', 'transfer', 'point', 'voucher')),
    payment_provider VARCHAR(50), -- 'toss', 'iamport', 'paypal'
    transaction_id VARCHAR(100),
    
    -- 상태
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'cancelled', 'refunded')),
    
    -- 메타데이터
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    receipt_url VARCHAR(255),
    notes TEXT
);

-- ================================
-- 6. 마케팅 및 이벤트
-- ================================

-- 프로모션/할인 정보
CREATE TABLE promotions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- 할인 정보
    discount_type VARCHAR(20) NOT NULL CHECK (discount_type IN ('percentage', 'fixed_amount', 'free_treatment')),
    discount_value DECIMAL(10,2) NOT NULL,
    min_purchase_amount DECIMAL(10,2) DEFAULT 0,
    
    -- 적용 조건
    applicable_treatments UUID[],
    customer_segments TEXT[], -- ['new', 'vip', 'returning']
    usage_limit_per_customer INTEGER DEFAULT 1,
    total_usage_limit INTEGER,
    current_usage_count INTEGER DEFAULT 0,
    
    -- 유효 기간
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    -- 메타데이터
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES staff(id)
);

-- ================================
-- 7. 리뷰 및 피드백
-- ================================

-- 고객 리뷰
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID REFERENCES appointments(id),
    customer_id UUID NOT NULL REFERENCES customers(id),
    treatment_id UUID NOT NULL REFERENCES treatments(id),
    staff_id UUID REFERENCES staff(id),
    
    -- 평가 정보
    overall_rating INTEGER NOT NULL CHECK (overall_rating BETWEEN 1 AND 5),
    service_rating INTEGER CHECK (service_rating BETWEEN 1 AND 5),
    cleanliness_rating INTEGER CHECK (cleanliness_rating BETWEEN 1 AND 5),
    value_rating INTEGER CHECK (value_rating BETWEEN 1 AND 5),
    
    -- 리뷰 내용
    title VARCHAR(200),
    content TEXT,
    pros TEXT,
    cons TEXT,
    
    -- 이미지
    image_urls TEXT[],
    
    -- 상태
    is_verified BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT true,
    moderation_status VARCHAR(20) DEFAULT 'pending' CHECK (moderation_status IN ('pending', 'approved', 'rejected')),
    
    -- 메타데이터
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    helpful_count INTEGER DEFAULT 0
);

-- ================================
-- 8. 시스템 로그 및 분석
-- ================================

-- API 사용 로그
CREATE TABLE api_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    ip_address INET,
    user_agent TEXT,
    customer_id UUID REFERENCES customers(id),
    request_body JSONB,
    response_body JSONB,
    error_message TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 비즈니스 지표 테이블
CREATE TABLE business_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2) NOT NULL,
    metric_type VARCHAR(50) NOT NULL, -- 'revenue', 'customer_count', 'satisfaction'
    period_type VARCHAR(20) NOT NULL, -- 'daily', 'weekly', 'monthly'
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ================================
-- 인덱스 생성 (성능 최적화)
-- ================================

-- 고객 테이블 인덱스
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_customer_code ON customers(customer_code);
CREATE INDEX idx_customers_membership_level ON customers(membership_level);

-- 예약 테이블 인덱스
CREATE INDEX idx_appointments_customer_id ON appointments(customer_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_staff_id ON appointments(staff_id);

-- 채팅 메시지 인덱스
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp);

-- 결제 인덱스
CREATE INDEX idx_payments_customer_id ON payments(customer_id);
CREATE INDEX idx_payments_appointment_id ON payments(appointment_id);
CREATE INDEX idx_payments_status ON payments(status);

-- ================================
-- 기본 데이터 삽입
-- ================================

-- 시술 카테고리 기본 데이터
INSERT INTO treatment_categories (name, description, display_order) VALUES
('주사 시술', '보톡스, 필러 등 주사를 이용한 시술', 1),
('레이저 시술', '피코, IPL, 프락셔널 등 레이저 시술', 2),
('스킨케어', '하이드라페이셜, 아쿠아필 등 기본 관리', 3),
('리프팅', 'HIFU, 실리프팅 등 리프팅 시술', 4),
('바디케어', '지방 분해, 체형 관리 시술', 5);

-- 기본 직원 데이터
INSERT INTO staff (staff_code, name, role, specialization) VALUES
('DOC001', '김미용', 'doctor', ARRAY['botox', 'filler', 'thread_lift']),
('DOC002', '이성형', 'doctor', ARRAY['laser', 'ipl', 'picosure']),
('NUR001', '박간호', 'nurse', ARRAY['skincare', 'basic_treatment']),
('MNG001', '최관리', 'manager', ARRAY['consultation', 'customer_service']);

-- 기본 시술 데이터 (보톡스)
INSERT INTO treatments (category_id, code, name, description, price, duration_minutes, target_area) 
SELECT id, 'BTX001', '보톡스 (이마)', '이마 주름 개선을 위한 보톡스 시술', 200000, 15, '이마'
FROM treatment_categories WHERE name = '주사 시술';

INSERT INTO treatments (category_id, code, name, description, price, duration_minutes, target_area)
SELECT id, 'BTX002', '보톡스 (눈가)', '눈가 주름 개선을 위한 보톡스 시술', 250000, 15, '눈가'
FROM treatment_categories WHERE name = '주사 시술';

-- 기본 프로모션
INSERT INTO promotions (code, name, description, discount_type, discount_value, start_date, end_date) VALUES
('WELCOME10', '신규 고객 10% 할인', '첫 방문 고객 대상 10% 할인', 'percentage', 10, CURRENT_DATE, CURRENT_DATE + INTERVAL '30 days'),
('VIP20', 'VIP 고객 20% 할인', 'VIP 멤버십 고객 대상 20% 할인', 'percentage', 20, CURRENT_DATE, CURRENT_DATE + INTERVAL '365 days');
