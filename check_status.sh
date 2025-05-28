#!/bin/bash

# 시스템 상태 확인 스크립트

echo "🔍 Elite Beauty AI 시스템 상태 확인"
echo "==================================="
echo ""

cd /Users/unipurple/Projects/AIChat

# Backend 상태
echo "1. Backend 상태:"
if [ -f ".backend.pid" ]; then
    PID=$(cat .backend.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   ✅ 실행 중 (PID: $PID)"
        # API 테스트
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "   ✅ API 응답 정상"
        else
            echo "   ❌ API 응답 없음"
        fi
    else
        echo "   ❌ 실행되지 않음 (PID 파일은 존재)"
    fi
else
    echo "   ❌ 실행되지 않음"
fi

# Frontend 상태
echo ""
echo "2. Frontend 상태:"
if [ -f ".frontend.pid" ]; then
    PID=$(cat .frontend.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   ✅ 실행 중 (PID: $PID)"
    else
        echo "   ❌ 실행되지 않음 (PID 파일은 존재)"
    fi
else
    echo "   ❌ 실행되지 않음"
fi

# 포트 사용 확인
echo ""
echo "3. 포트 사용 상태:"
echo "   포트 3000 (Frontend):"
lsof -i :3000 2>/dev/null | grep LISTEN || echo "   - 사용되지 않음"
echo ""
echo "   포트 8000 (Backend):"
lsof -i :8000 2>/dev/null | grep LISTEN || echo "   - 사용되지 않음"

# npm/node 프로세스 확인
echo ""
echo "4. Node.js 프로세스:"
ps aux | grep -E "node|npm" | grep -v grep | head -5 || echo "   없음"

echo ""
echo "==================================="
