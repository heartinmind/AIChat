#!/bin/bash

# 호환성 문제 해결 스크립트

echo "🔧 패키지 호환성 문제를 해결합니다..."
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 프로세스 정리
echo "1. 기존 프로세스 정리..."
pkill -f "python.*main.py" 2>/dev/null
sleep 2

# 2. 가상환경 활성화
echo "2. 가상환경 활성화..."
source venv/bin/activate

# 3. 캐시 정리
echo "3. 캐시 정리..."
pip cache purge

# 4. 문제 패키지 제거
echo "4. 기존 패키지 제거..."
pip uninstall -y anthropic httpx fastapi sqlalchemy

# 5. 업데이트된 패키지 설치
echo "5. 호환되는 패키지 설치..."
pip install fastapi==0.115.9
pip install sqlalchemy==2.0.35
pip install httpx==0.25.2
pip install anthropic==0.39.0
pip install uvicorn[standard]==0.24.0
pip install python-multipart==0.0.6
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-dotenv==1.0.0
pip install pydantic==2.5.0
pip install loguru==0.7.2
pip install bcrypt==4.1.2

# 6. 설치 확인
echo ""
echo "6. 설치된 패키지 버전 확인..."
python -c "
import sys
print(f'Python: {sys.version.split()[0]}')
try:
    import fastapi
    print(f'FastAPI: {fastapi.__version__}')
    import sqlalchemy
    print(f'SQLAlchemy: {sqlalchemy.__version__}')
    import httpx
    print(f'httpx: {httpx.__version__}')
    import anthropic
    print(f'anthropic: {anthropic.__version__}')
    print('✅ 모든 패키지가 설치되었습니다!')
except Exception as e:
    print(f'❌ 오류: {e}')
"

# 7. Backend 테스트
echo ""
echo "7. Backend 서버 시작 테스트..."
cd backend
python -c "
# 간단한 import 테스트
try:
    from main import app
    print('✅ main.py import 성공!')
except Exception as e:
    print(f'❌ Import 오류: {e}')
"

echo ""
echo "8. Backend 서버를 시작합니다..."
python main.py
