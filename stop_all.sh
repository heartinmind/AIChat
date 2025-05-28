#!/bin/bash

# 전체 시스템 종료 스크립트

echo "🛑 Elite Beauty Clinic AI Chat System 종료"
echo "=========================================="
echo ""

# PID 파일에서 프로세스 종료
if [ -f .backend.pid ]; then
    kill -9 $(cat .backend.pid) 2>/dev/null
    rm .backend.pid
    echo "✓ Backend 종료됨"
fi

if [ -f .admin.pid ]; then
    kill -9 $(cat .admin.pid) 2>/dev/null
    rm .admin.pid
    echo "✓ Admin Dashboard 종료됨"
fi

if [ -f .frontend.pid ]; then
    kill -9 $(cat .frontend.pid) 2>/dev/null
    rm .frontend.pid
    echo "✓ User Chat 종료됨"
fi

# 포트 기반 프로세스 정리
lsof -ti :8000 | xargs kill -9 2>/dev/null
lsof -ti :3001 | xargs kill -9 2>/dev/null
lsof -ti :3002 | xargs kill -9 2>/dev/null

# Python/Node 프로세스 정리
pkill -f "python.*main.py" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null
pkill -f "next dev" 2>/dev/null

echo ""
echo "✅ 모든 서비스가 종료되었습니다."
