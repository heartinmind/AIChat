#!/bin/bash

# 시스템 종료 스크립트

echo "🛑 Elite Beauty Clinic AI 시스템을 종료합니다..."
echo ""

# PID 파일에서 프로세스 ID 읽기
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "✓ Backend 서버를 종료합니다 (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm .backend.pid
    else
        echo "! Backend 프로세스가 이미 종료되었습니다"
        rm .backend.pid
    fi
else
    echo "! Backend PID 파일이 없습니다. 프로세스를 검색합니다..."
    pkill -f "python.*main.py"
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "✓ Admin Dashboard를 종료합니다 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm .frontend.pid
    else
        echo "! Frontend 프로세스가 이미 종료되었습니다"
        rm .frontend.pid
    fi
else
    echo "! Frontend PID 파일이 없습니다. 프로세스를 검색합니다..."
    pkill -f "node.*react-scripts"
fi

# 추가 정리
echo ""
echo "✓ 남은 프로세스를 정리합니다..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "node.*react-scripts" 2>/dev/null

# 포트 확인
echo ""
echo "✓ 포트 사용 상태 확인:"
echo "  포트 8000 (Backend):"
lsof -i :8000 2>/dev/null || echo "  - 사용 중이지 않음"
echo "  포트 3000 (Frontend):"
lsof -i :3000 2>/dev/null || echo "  - 사용 중이지 않음"

echo ""
echo "✅ 시스템이 종료되었습니다."
