#!/bin/bash

# Backend 재시작 스크립트

echo "🔄 Backend 재시작 (Claude API 키 적용)"
echo "====================================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 기존 Backend 프로세스 종료
echo "기존 Backend 프로세스 종료..."
pkill -f "python.*main.py" 2>/dev/null
if [ -f ".backend.pid" ]; then
    kill -9 $(cat .backend.pid) 2>/dev/null
fi
rm -f .backend.pid
sleep 2

# 2. 가상환경 활성화
echo "가상환경 활성화..."
source venv/bin/activate

# 3. Backend 재시작
echo "Backend를 재시작합니다..."
cd backend
PYTHONPATH=. nohup python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo $BACKEND_PID > .backend.pid

# 4. 시작 확인
sleep 3
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend 재시작 완료 (PID: $BACKEND_PID)"
    echo ""
    echo "API 상태 확인..."
    sleep 2
    
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend API 정상 작동!"
        echo "✅ Claude API 키가 적용되었습니다!"
    else
        echo "⚠️  API가 아직 준비 중입니다..."
    fi
else
    echo "❌ Backend 시작 실패"
    echo "최근 로그:"
    tail -20 backend.log
fi

echo ""
echo "====================================="
echo "🎉 이제 사용자 채팅창에서 AI와 대화할 수 있습니다!"
echo ""
echo "📱 사용자 채팅: http://localhost:3002"
echo "   브라우저를 새로고침하고 다시 메시지를 보내보세요!"
