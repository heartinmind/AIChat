#!/bin/bash

# GitHub에 안전하게 Push하는 스크립트

echo "🔐 GitHub Push 준비 (API 키 보호)"
echo "================================="
echo ""

cd /Users/unipurple/Projects/AIChat

# 1. Git 초기화 (아직 안 되어 있다면)
if [ ! -d .git ]; then
    echo "📁 Git 저장소 초기화..."
    git init
fi

# 2. 민감한 파일들이 .gitignore에 있는지 확인
echo ""
echo "🔍 .gitignore 확인..."
if grep -q "\.env" .gitignore; then
    echo "✅ .env 파일이 .gitignore에 포함되어 있습니다"
else
    echo "❌ .env를 .gitignore에 추가합니다"
    echo ".env" >> .gitignore
fi

# 3. 민감한 파일들 상태 확인
echo ""
echo "📋 제외될 파일들:"
echo "-------------------"
for file in .env *.db *.log *.pid venv/ node_modules/ __pycache__/; do
    if [ -e "$file" ]; then
        echo "  • $file"
    fi
done

# 4. 추적 중인 파일 확인
echo ""
echo "📋 커밋될 파일들 미리보기:"
echo "------------------------"
git add -A --dry-run | head -20

# 5. 민감한 정보 검사
echo ""
echo "🔍 민감한 정보 검사..."
SENSITIVE_PATTERNS=(
    "sk-ant-api"
    "CLAUDE_API_KEY"
    "SECRET_KEY"
    "password"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    echo -n "검사 중: $pattern ... "
    if git diff --cached --name-only | xargs grep -l "$pattern" 2>/dev/null | grep -v ".env.example" | grep -v ".gitignore"; then
        echo "⚠️  발견됨!"
        echo "위 파일들을 확인하세요!"
    else
        echo "✅ 안전"
    fi
done

echo ""
echo "================================="
echo "✅ 검사 완료!"
echo ""
echo "다음 명령어로 커밋하세요:"
echo "  git add ."
echo "  git commit -m 'Initial commit - Elite Beauty Clinic AI Chat System'"
echo "  git remote add origin YOUR_GITHUB_REPO_URL"
echo "  git push -u origin main"
echo ""
echo "⚠️  주의: 실제 API 키가 포함되지 않았는지 다시 한번 확인하세요!"
