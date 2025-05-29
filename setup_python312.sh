#!/bin/bash

echo "🔧 Python 3.12 환경 설정 스크립트"
echo "=================================="
echo ""

# 1. Python 3.12 설치 확인
echo "1️⃣ Python 3.12 확인 중..."
if command -v python3.12 &> /dev/null; then
    echo "✅ Python 3.12가 이미 설치되어 있습니다."
    python3.12 --version
else
    echo "❌ Python 3.12가 없습니다. 설치를 시작합니다..."
    brew install python@3.12
fi

echo ""
echo "2️⃣ 가상환경 재생성 중..."
cd /Users/unipurple/Projects/AIChat

# 기존 가상환경 삭제
if [ -d "venv" ]; then
    echo "기존 가상환경 삭제 중..."
    rm -rf venv
fi

# Python 3.12로 새 가상환경 생성
echo "Python 3.12로 가상환경 생성 중..."
python3.12 -m venv venv

# 활성화
source venv/bin/activate

# 버전 확인
echo ""
echo "3️⃣ 설치된 Python 버전:"
python --version

# pip 업그레이드
echo ""
echo "4️⃣ pip 업그레이드 중..."
pip install --upgrade pip

# 의존성 설치
echo ""
echo "5️⃣ 의존성 설치 중..."
cd backend
pip install -r requirements.txt

echo ""
echo "✅ 설정 완료!"
echo ""
echo "이제 다음 명령으로 서버를 시작할 수 있습니다:"
echo "cd /Users/unipurple/Projects/AIChat/backend"
echo "source ../venv/bin/activate"
echo "uvicorn main:app --reload"
