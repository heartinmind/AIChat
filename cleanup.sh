#!/bin/bash

# 로그 및 임시 파일 정리 스크립트

echo "🧹 로그 및 임시 파일을 정리합니다..."

cd /Users/unipurple/Projects/AIChat

# 로그 파일 삭제
rm -f backend.log frontend.log npm_install.log

# PID 파일 삭제
rm -f .backend.pid .frontend.pid

# Python 캐시 삭제
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# SQLite 데이터베이스 백업 (선택사항)
if [ -f "elite_beauty.db" ]; then
    echo -n "데이터베이스를 백업하시겠습니까? (y/N): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp elite_beauty.db elite_beauty.db.backup
        echo "✓ 데이터베이스가 백업되었습니다."
    fi
fi

echo "✅ 정리가 완료되었습니다!"
