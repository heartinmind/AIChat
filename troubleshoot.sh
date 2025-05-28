#!/bin/bash

# 문제 해결 도움말 스크립트

echo "🔧 Elite Beauty Clinic AI 시스템 문제 해결 도우미"
echo "=================================================="
echo ""

# 문제 선택
echo "어떤 문제가 있으신가요?"
echo "1) Backend가 시작되지 않음"
echo "2) Frontend가 시작되지 않음"
echo "3) 로그인이 안됨"
echo "4) 페이지가 표시되지 않음"
echo "5) 전체 재설치"
echo "6) 모든 로그 보기"
echo ""
echo -n "번호를 선택하세요 (1-6): "
read choice

case $choice in
    1)
        echo ""
        echo "🔍 Backend 문제 해결 중..."
        echo ""
        echo "1. Python 버전 확인:"
        python3 --version
        echo ""
        echo "2. 가상환경 활성화:"
        cd /Users/unipurple/Projects/AIChat
        source venv/bin/activate
        echo ""
        echo "3. 패키지 재설치:"
        pip install -r backend/requirements_minimal.txt
        echo ""
        echo "4. Backend 직접 실행:"
        cd backend
        python main.py
        ;;
        
    2)
        echo ""
        echo "🔍 Frontend 문제 해결 중..."
        echo ""
        echo "1. Node.js 버전 확인:"
        node --version
        npm --version
        echo ""
        echo "2. 패키지 재설치:"
        cd /Users/unipurple/Projects/AIChat/admin
        rm -rf node_modules package-lock.json
        npm install --legacy-peer-deps
        echo ""
        echo "3. Frontend 직접 실행:"
        npm start
        ;;
        
    3)
        echo ""
        echo "🔑 로그인 정보:"
        echo "이메일: admin@elitebeauty.com"
        echo "비밀번호: admin123"
        echo ""
        echo "Admin 계정 재생성:"
        cd /Users/unipurple/Projects/AIChat/backend
        python create_admin.py
        ;;
        
    4)
        echo ""
        echo "🌐 접속 주소 확인:"
        echo "Admin Dashboard: http://localhost:3000"
        echo "Backend API: http://localhost:8000"
        echo ""
        echo "포트 사용 상태:"
        lsof -i :8000
        lsof -i :3000
        ;;
        
    5)
        echo ""
        echo "🔄 전체 재설치를 시작합니다..."
        cd /Users/unipurple/Projects/AIChat
        
        # 정리
        ./stop_system.sh
        rm -rf venv admin/node_modules
        rm -f .env admin/.env *.db
        
        # 재설치
        python3 -m venv venv
        source venv/bin/activate
        pip install -r backend/requirements_minimal.txt
        
        cd admin
        npm install --legacy-peer-deps
        
        echo ""
        echo "재설치 완료! ./start_complete.sh로 시작하세요."
        ;;
        
    6)
        echo ""
        echo "📋 모든 로그:"
        echo ""
        echo "=== Backend 로그 ==="
        tail -20 /Users/unipurple/Projects/AIChat/backend.log
        echo ""
        echo "=== Frontend 로그 ==="
        tail -20 /Users/unipurple/Projects/AIChat/frontend.log
        ;;
        
    *)
        echo "잘못된 선택입니다."
        ;;
esac

echo ""
echo "추가 도움이 필요하시면 README_SYSTEM.md를 확인하세요."
