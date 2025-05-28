#!/bin/bash

# GitHub에서 클론 후 첫 실행 스크립트

echo "🚀 Elite Beauty Clinic AI Chat System 초기 설정"
echo "=============================================="
echo ""

# 1. .env 파일 생성
if [ ! -f .env ]; then
    echo "📝 .env 파일을 생성합니다..."
    cp .env.example .env
    echo "⚠️  .env 파일을 열어서 실제 API 키를 입력하세요!"
    echo ""
fi

# 2. Python 환경 설정
echo "🐍 Python 환경을 설정합니다..."
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements_py313.txt

# 3. Admin 계정 생성
echo ""
echo "👤 Admin 계정을 생성합니다..."
cd backend
PYTHONPATH=. python create_admin.py
cd ..

# 4. Frontend 패키지 설치
echo ""
echo "📦 Frontend 패키지를 설치합니다..."
cd admin
npm install
cd ..

cd frontend
npm install
cd ..

echo ""
echo "=============================================="
echo "✅ 초기 설정 완료!"
echo ""
echo "다음 명령어로 시스템을 시작하세요:"
echo "  ./start_all.sh"
echo ""
echo "⚠️  시작 전에 .env 파일에 Claude API 키를 입력하세요!"
