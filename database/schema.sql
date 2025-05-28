-- Elite Beauty Clinic AI Consultation System Database Schema
-- PostgreSQL 기준

-- 사용자 테이블
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    gender VARCHAR(10),
    birth_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- 상담원 테이블
CREATE TABLE agents (
    agent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'offline' CHECK (status IN ('active', 'offline', 'on_call')),
    department VARCHAR(50),
    last_active TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 상담 세션 테이블
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    agent_id UUID REFERENCES agents(agent_id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'ended', 'failed')),
    source VARCHAR(20) DEFAULT 'web' CHECK (source IN ('web', 'mobile', 'kakao')),
    route_target VARCHAR(10) CHECK (route_target IN ('agent', 'ai')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 메시지 테이블
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(session_id),
    sender VARCHAR(10) NOT NULL CHECK (sender IN ('user', 'agent', 'ai')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    emotion_tag VARCHAR(50),
    is_answer BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 요약 테이블
CREATE TABLE summaries (
    summary_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(session_id),
    type VARCHAR(20) NOT NULL CHECK (type IN ('rag', 'emotion', 'keyword')),
    summary_text TEXT NOT NULL,
    created_by VARCHAR(10) DEFAULT 'ai' CHECK (created_by IN ('ai', 'human')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 근무 시간 테이블
CREATE TABLE working_hours (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RAG 문서 테이블
CREATE TABLE rag_documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    keywords TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 병원 정보 테이블
CREATE TABLE clinic_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    name VARCHAR(100) NOT NULL,
    price VARCHAR(50),
    description TEXT,
    duration VARCHAR(50),
    effect_period VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_summaries_session_id ON summaries(session_id);

-- 초기 데이터 삽입
-- 근무 시간 설정 (월-금: 10:00-20:00, 토: 10:00-17:00)
INSERT INTO working_hours (day_of_week, start_time, end_time) VALUES
(1, '10:00', '20:00'), -- 월
(2, '10:00', '20:00'), -- 화
(3, '10:00', '20:00'), -- 수
(4, '10:00', '20:00'), -- 목
(5, '10:00', '20:00'), -- 금
(6, '10:00', '17:00'); -- 토

-- 병원 정보 초기 데이터
INSERT INTO clinic_info (category, subcategory, name, price, description, duration, effect_period) VALUES
('시술', '보톡스', '이마 보톡스', '15만원', '이마 주름 개선을 위한 보톡스 시술', '10-15분', '4-6개월'),
('시술', '보톡스', '미간 보톡스', '10만원', '미간 주름 개선을 위한 보톡스 시술', '10분', '4-6개월'),
('시술', '보톡스', '눈가 보톡스', '15만원', '눈가 주름 개선을 위한 보톡스 시술', '10-15분', '4-6개월'),
('시술', '필러', '팔자주름 필러', '40만원', '팔자주름 개선을 위한 필러 시술', '20-30분', '12-18개월'),
('시술', '필러', '볼 필러', '60만원', '볼륨감 있는 얼굴을 위한 필러 시술', '30분', '12-18개월'),
('시술', '레이저', '기미 레이저', '회당 20만원', '기미 개선을 위한 레이저 시술', '30-40분', '즉시-1개월'),
('시술', '레이저', '모공 레이저', '회당 30만원', '모공 축소를 위한 레이저 시술', '40분', '즉시-1개월');