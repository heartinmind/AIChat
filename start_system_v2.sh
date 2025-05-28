#!/bin/bash

# Elite Beauty Clinic AI 상담 시스템 시작 스크립트 (개선된 버전)

echo "🚀 Elite Beauty Clinic AI 상담 시스템을 시작합니다..."

# 프로젝트 디렉토리로 이동
PROJECT_DIR="/Users/unipurple/Projects/AIChat"
cd "$PROJECT_DIR"

# Python 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 Python 가상환경을 생성합니다..."
    python3 -m venv venv
fi

# 가상환경 활성화
echo "📦 가상환경을 활성화합니다..."
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# Backend 패키지 설치
echo "📚 Backend 패키지를 설치합니다..."
pip install -r backend/requirements.txt

# .env 파일 생성 (없는 경우)
if [ ! -f ".env" ]; then
    echo "📝 .env 파일을 생성합니다..."
    cat > .env << EOL
# Elite Beauty Clinic AI System Environment Variables
SECRET_KEY=your-secret-key-here-change-this-in-production
CLAUDE_API_KEY=your-claude-api-key-here
DATABASE_URL=sqlite:///./elite_beauty.db
EOL
fi

# Admin 계정 생성
echo "👤 Admin 계정을 확인합니다..."
cd backend
python create_admin.py

# 백엔드 서버 실행
echo "🔧 백엔드 서버를 시작합니다 (포트: 8000)..."
python main.py &
BACKEND_PID=$!

# 백엔드가 시작될 때까지 대기
echo "⏳ 백엔드 서버가 시작되기를 기다립니다..."
sleep 5

# Admin 대시보드 디렉토리로 이동
cd ../admin

# node_modules가 있는지 확인
if [ ! -d "node_modules" ]; then
    echo "🧹 기존 파일을 정리합니다..."
    rm -rf package-lock.json
    
    echo "📦 Admin 대시보드 패키지를 설치합니다..."
    npm install --legacy-peer-deps
fi

# Admin 대시보드 실행
echo "🎨 Admin 대시보드를 시작합니다 (포트: 3000)..."
npm start &
FRONTEND_PID=$!

# 시작 완료 메시지
echo ""
echo "✅ 시스템이 성공적으로 시작되었습니다!"
echo "================================================"
echo "🌐 Backend API: http://localhost:8000"
echo "🌐 API 문서: http://localhost:8000/docs"
echo "🎨 Admin Dashboard: http://localhost:3000"
echo ""
echo "📧 Admin 로그인 정보:"
echo "   이메일: admin@elitebeauty.com"
echo "   비밀번호: admin123"
echo "================================================"
echo ""
echo "🛑 종료하려면 Ctrl+C를 누르세요"

# Ctrl+C 시그널 처리
trap "echo '종료 중...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 프로세스 종료 대기
wait $BACKEND_PID
wait $FRONTEND_PID
