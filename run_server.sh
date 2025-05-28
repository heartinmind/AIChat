#!/bin/bash
# 서버 실행 및 상태 확인 스크립트

echo "🚀 웹 서버 실행 중..."
echo ""

# 기존 프로세스 확인 (포트 8080)
if lsof -i :8080 > /dev/null 2>&1; then
    echo "⚠️  포트 8080이 이미 사용 중입니다!"
    echo "사용 중인 프로세스:"
    lsof -i :8080
    echo ""
    echo "종료하려면 다음 명령 사용:"
    echo "kill -9 \$(lsof -t -i:8080)"
    echo ""
    echo "또는 다른 포트로 실행:"
    echo "PORT=8081 python web_server.py"
    exit 1
fi

# Python 버전 확인
echo "📋 Python 버전:"
python --version
echo ""

# 서버 실행
echo "🌐 서버 시작..."
echo "📍 URL: http://localhost:8080"
echo "💡 다른 포트로 실행하려면: PORT=원하는포트 python web_server.py"
echo ""
python web_server.py
