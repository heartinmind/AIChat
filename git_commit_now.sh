#!/bin/bash
# Git 상태 확인 및 커밋 스크립트

echo "📊 Git 상태 확인 중..."
echo ""

# 현재 브랜치 확인
echo "🌿 현재 브랜치:"
git branch --show-current

echo ""
echo "📝 변경된 파일들:"
git status --short

echo ""
echo "📦 스테이징할 파일들:"
git add -A
git status --short

echo ""
echo "💾 커밋 준비 완료!"
echo "커밋 메시지: [정리] 프로젝트 구조 개선 및 보안 강화"
echo ""
echo "다음 명령을 실행하세요:"
echo "git commit -m '[정리] 프로젝트 구조 개선 및 보안 강화'"
echo "git push origin main"
