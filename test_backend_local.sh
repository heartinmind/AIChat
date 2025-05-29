#!/bin/bash

# 🧪 로컬 테스트 스크립트
# 실행: bash test_backend_local.sh

echo "🧪 Backend 로컬 테스트"
echo "====================="
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Python 버전 확인
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${YELLOW}Python 버전: $python_version${NC}"

if [[ "$python_version" == 3.13* ]]; then
    echo -e "${RED}⚠️  경고: Python 3.13은 일부 패키지와 호환성 문제가 있을 수 있습니다.${NC}"
    echo -e "${YELLOW}Python 3.12 사용을 권장합니다.${NC}"
    read -p "계속하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 포트 확인
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}⚠️  포트 8000이 이미 사용 중입니다.${NC}"
    echo "사용 중인 프로세스:"
    lsof -i :8000
    read -p "다른 포트를 사용하시겠습니까? (8001) (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PORT=8001
    else
        echo -e "${YELLOW}기존 프로세스를 종료하려면 다음 명령을 실행하세요:${NC}"
        echo "kill -9 $(lsof -ti :8000)"
        exit 1
    fi
else
    PORT=8000
fi

# 환경 변수 설정
# export CLAUDE_API_KEY="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"
export SECRET_KEY="elite-beauty-secret-key-2024"
export DATABASE_URL="sqlite:///./elite_beauty.db"

# Backend 디렉토리로 이동
cd backend

# 가상환경 확인
if [ ! -d "../venv" ]; then
    echo -e "${YELLOW}가상환경 생성 중...${NC}"
    python3 -m venv ../venv
fi

# 가상환경 활성화
echo -e "${YELLOW}가상환경 활성화...${NC}"
source ../venv/bin/activate

# pip 업그레이드
echo -e "${YELLOW}pip 업그레이드...${NC}"
pip install --upgrade pip

# 의존성 설치
echo -e "${YELLOW}의존성 설치 중...${NC}"
pip install -r requirements.txt

# 환경변수 파일 확인
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env 파일이 없습니다. 환경변수를 export로 설정합니다...${NC}"
fi

# 서버 시작
echo -e "${GREEN}✅ 로컬 서버 시작! (포트: $PORT)${NC}"
echo -e "${YELLOW}URL: http://localhost:$PORT${NC}"
echo ""
echo -e "${YELLOW}테스트 명령어:${NC}"
echo "# 헬스체크"
echo "curl http://localhost:$PORT/health"
echo ""
echo "# 관리자 확인"
echo "curl http://localhost:$PORT/api/debug/admin-check"
echo ""
echo "# 로그인 테스트"
echo "curl -X POST http://localhost:$PORT/api/agents/login \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"email\":\"admin@elitebeauty.com\",\"password\":\"admin123\"}'"
echo ""
echo -e "${YELLOW}종료: Ctrl+C${NC}"
echo ""

# 서버 실행 (uvicorn 사용)
uvicorn main:app --reload --host 0.0.0.0 --port $PORT
