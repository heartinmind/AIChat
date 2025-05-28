#!/bin/bash

# 빠른 진단 스크립트

echo "🔍 시스템 상태 진단"
echo "=================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. Python 환경 확인
echo "1. Python 환경:"
if [ -d "venv" ]; then
    echo "   ✓ 가상환경 존재"
    source venv/bin/activate
    echo "   Python: $(python --version)"
    
    # 주요 패키지 확인
    echo ""
    echo "2. 설치된 주요 패키지:"
    python -c "
import pkg_resources
packages = ['fastapi', 'anthropic', 'sqlalchemy', 'httpx']
for pkg in packages:
    try:
        version = pkg_resources.get_distribution(pkg).version
        print(f'   ✓ {pkg}: {version}')
    except:
        print(f'   ✗ {pkg}: 설치되지 않음')
"
else
    echo "   ✗ 가상환경이 없습니다"
fi

# 2. Backend 상태
echo ""
echo "3. Backend 상태:"
if [ -f ".backend.pid" ] && kill -0 $(cat .backend.pid) 2>/dev/null; then
    echo "   ✓ 실행 중 (PID: $(cat .backend.pid))"
else
    echo "   ✗ 실행되지 않음"
fi

# API 응답 확인
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✓ API 응답 정상"
else
    echo "   ✗ API 응답 없음"
fi

# 3. Frontend 상태
echo ""
echo "4. Frontend 상태:"
if [ -f ".frontend.pid" ] && kill -0 $(cat .frontend.pid) 2>/dev/null; then
    echo "   ✓ 실행 중 (PID: $(cat .frontend.pid))"
else
    echo "   ✗ 실행되지 않음"
fi

if [ -d "admin/node_modules" ]; then
    echo "   ✓ node_modules 존재"
else
    echo "   ✗ node_modules 없음"
fi

# 4. 최근 에러 로그
echo ""
echo "5. 최근 에러 (있는 경우):"
if [ -f "backend.log" ]; then
    errors=$(grep -i "error\|exception\|traceback" backend.log | tail -5)
    if [ -n "$errors" ]; then
        echo "$errors"
    else
        echo "   Backend 에러 없음"
    fi
else
    echo "   Backend 로그 파일 없음"
fi

echo ""
echo "진단 완료!"
echo ""
echo "문제가 있다면 다음 명령을 실행하세요:"
echo "./complete_fix.sh"
