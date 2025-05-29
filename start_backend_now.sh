#!/bin/bash

# 🚀 빠른 서버 시작 스크립트

cd /Users/unipurple/Projects/AIChat

# Python 3.12 확인
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
else
    echo "❌ Python 3.12가 없습니다."
    echo "먼저 다음을 실행하세요: brew install python@3.12"
    exit 1
fi

# 가상환경이 없으면 생성
if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    $PYTHON_CMD -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate

# 백엔드 디렉토리로 이동
cd backend

# 포트 확인
PORT=8000
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️ 포트 8000이 사용 중입니다. 종료합니다..."
    kill -9 $(lsof -ti :8000) 2>/dev/null
    sleep 2
fi

# 환경변수 설정
export SECRET_KEY="elite-beauty-secret-key-2024"
export DATABASE_URL="sqlite:///./elite_beauty.db"

echo "✅ 서버 시작 중... (Python $(python --version 2>&1 | awk '{print $2}'))"
echo "URL: http://localhost:8000"
echo ""

# 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port $PORT
