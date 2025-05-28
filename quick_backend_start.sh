#!/bin/bash

# Backend 빠른 시작 스크립트

echo "🚀 Backend 빠른 시작"
echo "==================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 가상환경 확인
if [ ! -d "venv" ]; then
    echo "❌ 가상환경이 없습니다!"
    echo "먼저 다음을 실행하세요: ./fix_python_env.sh"
    exit 1
fi

# 2. 가상환경 활성화
echo "가상환경 활성화..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ 가상환경 활성화 실패!"
    exit 1
fi

# 3. 프로세스 정리
echo "기존 Backend 프로세스 정리..."
pkill -f "python.*main.py" 2>/dev/null
rm -f .backend.pid
sleep 1

# 4. 환경 변수 설정
export PYTHONPATH="${PWD}/backend:$PYTHONPATH"

# 5. .env 파일 확인
if [ ! -f ".env" ]; then
    echo ".env 파일 생성..."
    cat > .env << 'EOL'
SECRET_KEY=elite-beauty-secret-key-2024
CLAUDE_API_KEY=sk-ant-api03-YOUR-KEY-HERE
DATABASE_URL=sqlite:///./elite_beauty.db
EOL
fi

# 6. Admin 계정 확인
echo "Admin 계정 확인..."
cd backend
PYTHONPATH=. python create_admin.py 2>/dev/null || echo "Admin 계정이 이미 존재합니다"

# 7. Backend 시작
echo ""
echo "Backend 서버를 시작합니다..."
echo "================================"
PYTHONPATH=. python main.py

# 만약 백그라운드로 실행하려면 아래 주석을 해제
# PYTHONPATH=. nohup python main.py > ../backend.log 2>&1 &
# BACKEND_PID=$!
# echo $BACKEND_PID > ../.backend.pid
# echo "✅ Backend 시작됨 (PID: $BACKEND_PID)"
# echo "로그 확인: tail -f ../backend.log"
