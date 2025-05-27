#!/bin/bash
# 파일 삭제 스크립트

echo "🗑️ 파일 삭제 중..."

# service-account-key.json 삭제 (매우 중요!)
if [ -f "service-account-key.json" ]; then
    rm -f service-account-key.json
    echo "✅ service-account-key.json 삭제됨 (보안상 중요!)"
fi

# setup_development 파일들 삭제
rm -f setup_development.bat setup_development.sh
echo "✅ setup_development.* 파일들 삭제됨"

# tsconfig.json 삭제
rm -f tsconfig.json
echo "✅ tsconfig.json 삭제됨"

# __pycache__ 정리
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "✅ __pycache__ 디렉토리 정리됨"

echo ""
echo "🔒 보안 확인:"
if [ ! -f "service-account-key.json" ]; then
    echo "✅ service-account-key.json이 성공적으로 삭제되었습니다!"
else
    echo "❌ 경고: service-account-key.json이 아직 존재합니다!"
fi

echo ""
echo "📁 현재 디렉토리 구조:"
ls -la | grep -E "(^d|\.py$|\.json$|\.md$)" | head -20
