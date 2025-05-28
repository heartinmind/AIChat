#!/bin/bash

# 포트 3000 정리 후 Frontend 시작 스크립트

echo "🔧 포트 3000 정리 및 Frontend 시작"
echo "==================================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 포트 3000 사용 중인 프로세스 확인 및 종료
echo "포트 3000을 사용 중인 프로세스 확인..."
PORT_PID=$(lsof -ti :3000)

if [ ! -z "$PORT_PID" ]; then
    echo "포트 3000을 사용 중인 프로세스 발견 (PID: $PORT_PID)"
    echo "종료하시겠습니까? (y/n)"
    read -r response
    
    if [ "$response" = "y" ]; then
        kill -9 $PORT_PID
        echo "✅ 프로세스 종료됨"
        sleep 2
    else
        echo "다른 포트를 사용하려면 방법 2를 사용하세요"
        exit 1
    fi
else
    echo "✅ 포트 3000이 사용 가능합니다"
fi

# 2. Frontend 시작
echo ""
echo "Frontend를 시작합니다..."
cd admin

# PORT 환경변수 설정 (기본값 3000)
export PORT=3000

nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..
echo $FRONTEND_PID > .frontend.pid

# 3. 시작 확인
sleep 5

if ps -p $FRONTEND_PID > /dev/null; then
    echo ""
    echo "✅ Frontend 시작됨 (PID: $FRONTEND_PID)"
    echo ""
    echo "==================================="
    echo "✨ 시스템이 준비되었습니다!"
    echo "==================================="
    echo ""
    echo "📌 접속 정보:"
    echo "   Admin Dashboard: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API 문서: http://localhost:8000/docs"
    echo ""
    echo "⏳ React 앱이 로딩 중입니다..."
    echo "   약 10-30초 후 브라우저가 자동으로 열립니다"
else
    echo "❌ Frontend 시작 실패"
    tail -20 frontend.log
fi
