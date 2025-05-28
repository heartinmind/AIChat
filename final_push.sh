#!/bin/bash

# GitHub Push 최종 준비 스크립트

echo "🚀 GitHub Push 최종 준비"
echo "========================"
echo ""
echo "저장소: https://github.com/heartinmind/AIChat.git"
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. 현재 브랜치 확인
echo "📌 현재 브랜치:"
git branch --show-current
echo ""

# 2. 스테이지되지 않은 변경사항 확인
echo "📋 변경된 파일들:"
git status --short
echo ""

# 3. .gitignore 확인
echo "🔒 .gitignore에 포함된 중요 파일들:"
echo "  • .env ✓"
echo "  • *.db ✓"
echo "  • venv/ ✓"
echo "  • node_modules/ ✓"
echo "  • *.log ✓"
echo ""

# 4. 커밋 준비
echo "📦 커밋 준비:"
echo "다음 명령어를 실행하세요:"
echo ""
echo "  # 모든 파일 추가 (민감한 파일은 .gitignore에 의해 제외됨)"
echo "  git add ."
echo ""
echo "  # 커밋"
echo "  git commit -m 'feat: Complete Elite Beauty Clinic AI Chat System implementation'"
echo ""
echo "  # Push"
echo "  git push origin main"
echo ""
echo "⚠️  주의: Push 전에 .env 파일이 제외되었는지 확인하세요!"
