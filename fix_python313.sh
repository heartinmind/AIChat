#!/bin/bash

# 문제 해결 스크립트 - Python 3.13 호환성 문제 해결

echo "🔧 Python 3.13 호환성 문제를 해결합니다..."
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 기존 프로세스 정리
echo "1. 기존 프로세스 정리..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "node.*react-scripts" 2>/dev/null
sleep 2

# 2. 가상환경 활성화
echo "2. 가상환경 활성화..."
source venv/bin/activate

# 3. pip 업그레이드
echo "3. pip 업그레이드..."
pip install --upgrade pip

# 4. 패키지 재설치
echo "4. 호환되는 패키지 설치..."
pip uninstall -y fastapi sqlalchemy
pip install --force-reinstall -r backend/requirements_minimal.txt

# 5. Backend 테스트
echo "5. Backend 테스트 실행..."
cd backend
python -c "
import sys
print(f'Python 버전: {sys.version}')
try:
    import fastapi
    print(f'FastAPI 버전: {fastapi.__version__}')
    import sqlalchemy
    print(f'SQLAlchemy 버전: {sqlalchemy.__version__}')
    import anthropic
    print('Anthropic 패키지 OK')
    print('✅ 모든 패키지가 정상적으로 로드되었습니다!')
except Exception as e:
    print(f'❌ 오류: {e}')
"

echo ""
echo "6. Backend 서버 시작..."
python main.py
