#!/bin/bash

# JWT 모듈 빠른 수정 스크립트

echo "🔧 JWT 모듈 설치 및 Backend 재시작"
echo "================================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 가상환경 활성화
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ 가상환경 활성화됨"
else
    echo "❌ 가상환경이 없습니다!"
    exit 1
fi

# 2. PyJWT 설치
echo ""
echo "PyJWT를 설치합니다..."
pip install PyJWT==2.9.0

# 3. 설치 확인
echo ""
echo "설치 확인:"
python -c "
try:
    import jwt
    print('✓ PyJWT 설치됨:', jwt.__version__)
except ImportError:
    print('❌ PyJWT 설치 실패!')
"

# 4. Backend 모듈 테스트
echo ""
echo "Backend 모듈 테스트:"
cd backend
export PYTHONPATH=.
python -c "
import sys
sys.path.insert(0, '.')
try:
    from main import app
    print('✅ main.py import 성공!')
    print('✅ Backend 준비 완료!')
except Exception as e:
    print(f'❌ Import 오류: {e}')
    import traceback
    traceback.print_exc()
"

# 5. 기존 Backend 프로세스 종료
echo ""
echo "기존 Backend 프로세스를 종료합니다..."
pkill -f "python.*main.py" 2>/dev/null
rm -f ../.backend.pid
sleep 1

# 6. Backend 재시작
echo ""
echo "Backend를 시작합니다..."
PYTHONPATH=. nohup python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 7. 시작 확인
sleep 3
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend 시작됨 (PID: $BACKEND_PID)"
    echo $BACKEND_PID > .backend.pid
    
    # API 상태 확인
    sleep 2
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend API 정상 작동!"
        echo ""
        echo "================================="
        echo "🎉 성공!"
        echo "================================="
        echo ""
        echo "📌 접속 정보:"
        echo "   Admin Dashboard: http://localhost:3000"
        echo "   Backend API: http://localhost:8000"
        echo "   API 문서: http://localhost:8000/docs"
        echo ""
        echo "🔑 로그인 정보:"
        echo "   이메일: admin@elitebeauty.com"
        echo "   비밀번호: admin123"
    else
        echo "⚠️  Backend API가 아직 준비 중입니다"
        echo "로그 확인: tail -f backend.log"
    fi
else
    echo "❌ Backend 시작 실패"
    echo "최근 로그:"
    tail -20 backend.log
fi
