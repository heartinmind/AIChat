#!/bin/bash
# 의존성 설치 스크립트

echo "🔧 AIChat 의존성 설치 시작..."
echo ""

# 가상환경 확인
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  가상환경이 활성화되지 않았습니다!"
    echo "다음 명령을 먼저 실행하세요:"
    echo "source venv/bin/activate"
    exit 1
fi

echo "✅ 가상환경 활성화 확인: $VIRTUAL_ENV"
echo ""

# pip 업그레이드
echo "📦 pip 업그레이드..."
pip install --upgrade pip

# requirements.txt 설치
echo ""
echo "📦 requirements.txt 설치 중..."
pip install -r requirements.txt

# 설치 확인
echo ""
echo "✅ 설치된 패키지 확인:"
pip list | grep -E "(fastapi|uvicorn|pydantic|google-cloud)"

echo ""
echo "🎉 설치 완료!"
echo ""
echo "🚀 서버 실행:"
echo "python web_server.py"
