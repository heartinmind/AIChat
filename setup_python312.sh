#!/bin/bash

# Python 3.12 설치 및 프로젝트 설정 스크립트

echo "🔧 Python 3.12 설치 및 프로젝트 설정"
echo "===================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 1. Homebrew 확인
echo -e "${YELLOW}1. Homebrew 확인${NC}"
if ! command -v brew &> /dev/null; then
    echo -e "${RED}❌ Homebrew가 설치되지 않았습니다!${NC}"
    echo "https://brew.sh 에서 Homebrew를 먼저 설치하세요."
    exit 1
fi
echo -e "${GREEN}✓ Homebrew 설치됨${NC}"
echo ""

# 2. Python 3.12 설치
echo -e "${YELLOW}2. Python 3.12 설치${NC}"
if command -v python3.12 &> /dev/null; then
    echo -e "${GREEN}✓ Python 3.12가 이미 설치되어 있습니다${NC}"
else
    echo "Python 3.12를 설치합니다..."
    brew install python@3.12
fi
echo ""

# 3. Python 3.12 버전 확인
echo -e "${YELLOW}3. Python 3.12 확인${NC}"
python3.12 --version
echo ""

# 4. 프로젝트 디렉토리로 이동
cd /Users/unipurple/Projects/AIChat

# 5. 기존 가상환경 삭제
echo -e "${YELLOW}4. 기존 가상환경 정리${NC}"
if [ -d "venv" ]; then
    rm -rf venv
    echo "기존 가상환경 삭제됨"
fi
echo ""

# 6. Python 3.12로 새 가상환경 생성
echo -e "${YELLOW}5. Python 3.12로 가상환경 생성${NC}"
python3.12 -m venv venv
source venv/bin/activate

echo "Python 경로: $(which python)"
echo "Python 버전: $(python --version)"
echo ""

# 7. pip 업그레이드
echo -e "${YELLOW}6. pip 업그레이드${NC}"
python -m pip install --upgrade pip wheel setuptools
echo ""

# 8. Backend 패키지 설치
echo -e "${YELLOW}7. Backend 패키지 설치${NC}"
pip install -r backend/requirements_fixed.txt
echo ""

# 9. 설치 확인
echo -e "${YELLOW}8. 설치 확인${NC}"
python -c "
import fastapi, sqlalchemy, pydantic, anthropic
print('✓ FastAPI:', fastapi.__version__)
print('✓ SQLAlchemy:', sqlalchemy.__version__)
print('✓ Pydantic:', pydantic.__version__)
print('✓ Anthropic:', anthropic.__version__)
"
echo ""

echo -e "${GREEN}✅ Python 3.12 환경 설정 완료!${NC}"
echo ""
echo "이제 다음 명령을 실행하세요:"
echo "  ./complete_fix_v2.sh"
echo ""
echo "또는 Backend만 시작하려면:"
echo "  source venv/bin/activate"
echo "  cd backend"
echo "  PYTHONPATH=. python main.py"
