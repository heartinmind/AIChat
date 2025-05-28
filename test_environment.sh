#!/bin/bash

# 빠른 Python 환경 테스트 스크립트

echo "🔍 Python 환경 빠른 테스트"
echo "========================"
echo ""

cd /Users/unipurple/Projects/AIChat

# 가상환경 활성화 시도
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ 가상환경 활성화됨"
    echo "Python: $(which python)"
    echo "버전: $(python --version)"
    echo ""
    
    # 패키지 테스트
    echo "패키지 테스트:"
    python -c "
try:
    import sys
    print(f'Python {sys.version}')
    print('-' * 50)
    
    packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 
        'anthropic', 'httpx', 'passlib', 'jose', 'loguru'
    ]
    
    installed = []
    missing = []
    
    for pkg in packages:
        try:
            module = __import__(pkg)
            version = getattr(module, '__version__', 'unknown')
            installed.append(f'{pkg}: {version}')
        except ImportError:
            missing.append(pkg)
    
    if installed:
        print('✅ 설치된 패키지:')
        for item in installed:
            print(f'   {item}')
    
    if missing:
        print('\\n❌ 누락된 패키지:')
        for item in missing:
            print(f'   {item}')
    
    # Backend 모듈 테스트
    print('\\n모듈 임포트 테스트:')
    sys.path.insert(0, 'backend')
    
    try:
        from database.models import Base
        print('   ✓ database.models')
    except Exception as e:
        print(f'   ✗ database.models: {type(e).__name__}')
    
    try:
        from main import app
        print('   ✓ main.py')
    except Exception as e:
        print(f'   ✗ main.py: {type(e).__name__}')
        
except Exception as e:
    print(f'오류 발생: {e}')
    import traceback
    traceback.print_exc()
"
else
    echo "❌ 가상환경이 없습니다!"
    echo ""
    echo "다음 중 하나를 실행하세요:"
    echo "1. ./complete_fix_v3.sh  (Python 3.13 사용)"
    echo "2. ./setup_python312.sh  (Python 3.12 설치 및 설정)"
fi
