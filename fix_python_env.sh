#!/bin/bash

# Python 환경 검증 및 복구 스크립트

echo "🔧 Python 환경 검증 및 복구"
echo "=========================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. Python 설치 확인
echo "1. Python 설치 확인:"
echo "-------------------"

# 여러 Python 경로 확인
for py in python3 python3.13 python3.12 python3.11 python3.10 python3.9 python; do
    if command -v $py &> /dev/null; then
        echo "✓ $py 발견: $(which $py)"
        echo "  버전: $($py --version)"
        PYTHON_CMD=$py
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Python이 설치되지 않았습니다!"
    echo ""
    echo "Python을 설치하려면:"
    echo "1. Homebrew가 있다면: brew install python@3.12"
    echo "2. 또는 https://www.python.org 에서 다운로드"
    exit 1
fi

echo ""
echo "사용할 Python: $PYTHON_CMD"
echo ""

# 2. 기존 가상환경 정리
echo "2. 기존 가상환경 정리:"
echo "--------------------"
if [ -d "venv" ]; then
    echo "기존 venv 디렉토리를 삭제합니다..."
    rm -rf venv
    echo "✓ 삭제 완료"
else
    echo "✓ 기존 가상환경 없음"
fi
echo ""

# 3. 새 가상환경 생성
echo "3. 새 가상환경 생성:"
echo "------------------"
echo "명령: $PYTHON_CMD -m venv venv"
$PYTHON_CMD -m venv venv

if [ $? -eq 0 ]; then
    echo "✓ 가상환경 생성 성공!"
else
    echo "❌ 가상환경 생성 실패!"
    echo ""
    echo "다음을 시도해보세요:"
    echo "1. $PYTHON_CMD -m pip install --user virtualenv"
    echo "2. $PYTHON_CMD -m virtualenv venv"
    exit 1
fi
echo ""

# 4. 가상환경 활성화 및 pip 확인
echo "4. 가상환경 활성화:"
echo "-----------------"
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo "✓ 가상환경 활성화 성공!"
    echo "Python 경로: $(which python)"
    echo "pip 경로: $(which pip)"
else
    echo "❌ 가상환경 활성화 실패!"
    exit 1
fi
echo ""

# 5. pip 업그레이드
echo "5. pip 업그레이드:"
echo "----------------"
python -m pip install --upgrade pip
echo ""

# 6. 필수 패키지 설치
echo "6. 필수 패키지 설치:"
echo "------------------"

# requirements_simple.txt 생성
cat > backend/requirements_simple.txt << 'EOL'
# 최소 필수 패키지
fastapi==0.110.0
uvicorn[standard]==0.24.0
sqlalchemy==2.0.25
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
anthropic==0.25.0
httpx==0.25.2
pydantic==2.5.0
loguru==0.7.2
EOL

echo "패키지를 설치합니다..."
pip install -r backend/requirements_simple.txt

if [ $? -eq 0 ]; then
    echo "✓ 패키지 설치 성공!"
else
    echo "❌ 패키지 설치 실패!"
    echo "개별적으로 설치를 시도합니다..."
    
    # 개별 설치
    pip install fastapi==0.110.0
    pip install uvicorn[standard]==0.24.0
    pip install sqlalchemy==2.0.25
    pip install anthropic==0.25.0
    pip install httpx==0.25.2
    pip install python-jose[cryptography]==3.3.0
    pip install passlib[bcrypt]==1.7.4
    pip install python-dotenv==1.0.0
fi
echo ""

# 7. Backend 테스트
echo "7. Backend 테스트:"
echo "----------------"
cd backend
export PYTHONPATH=.
python -c "
import sys
print(f'Python: {sys.version}')
print(f'경로: {sys.path[0]}')

try:
    import fastapi
    print(f'✓ FastAPI: {fastapi.__version__}')
    import sqlalchemy
    print(f'✓ SQLAlchemy: {sqlalchemy.__version__}')
    import anthropic
    print(f'✓ Anthropic: {anthropic.__version__}')
    
    # models import 테스트
    from database.models import Base
    print('✓ database.models import 성공!')
    
    # main import 테스트
    from main import app
    print('✓ main.py import 성공!')
    
    print('')
    print('✅ 모든 테스트 통과! Backend 준비 완료!')
except Exception as e:
    print(f'❌ 오류 발생: {e}')
    import traceback
    traceback.print_exc()
"
cd ..

echo ""
echo "=========================="
echo "검증 완료!"
echo ""
echo "다음 단계:"
echo "1. Backend 실행: cd backend && PYTHONPATH=. python main.py"
echo "2. 또는 전체 시스템 시작: ./quick_backend_start.sh"
