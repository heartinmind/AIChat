#!/bin/bash

echo "🔄 프로젝트 최종 버전 커밋"
echo "========================="
echo ""

# 현재 날짜와 시간
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
VERSION="v1.0.0"

# Git 초기화 확인
if [ ! -d ".git" ]; then
    echo "Git 저장소 초기화..."
    git init
fi

# .gitignore 생성/업데이트
echo "📝 .gitignore 업데이트..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
venv_*/
ENV/
env/
*.egg
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Next.js
.next/
out/
build/

# Production
/build
*.production

# Misc
.DS_Store
*.pem
*.log

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite
*.sqlite3
backend/elite_beauty.db

# Logs
logs/
*.log
backend.log
frontend.log
admin.log

# OS
.DS_Store
Thumbs.db

# Backups
*.backup
*.bak
project_backup_*/

# PID files
.*.pid

# Temporary files
*.tmp
temp/
tmp/
EOF

# 모든 파일 추가
echo "📦 변경사항 스테이징..."
git add -A

# 커밋
echo "💾 커밋 생성..."
git commit -m "feat: Elite Beauty AI Chat System v1.0.0

- 백엔드: FastAPI + SQLAlchemy + Claude AI
- 프론트엔드: Next.js + TypeScript + Tailwind CSS
- 관리자: React + Material-UI
- 데이터베이스: SQLite (개발) / PostgreSQL (프로덕션)

주요 기능:
- AI/상담원 하이브리드 채팅
- 실시간 메시징
- 관리자 대시보드
- 환경별 설정 관리
- JWT 인증

해결된 이슈:
- Python 3.13 호환성 → Python 3.12 사용
- Anthropic 라이브러리 버전 충돌 해결
- 자연스러운 AI 대화 구현"

# 태그 생성
echo "🏷️  버전 태그 생성..."
git tag -a $VERSION -m "Release version $VERSION"

echo ""
echo "✅ Git 커밋 완료!"
echo "버전: $VERSION"
echo "커밋 해시: $(git rev-parse HEAD)"
echo ""
echo "다음 명령으로 원격 저장소에 푸시할 수 있습니다:"
echo "git remote add origin <your-repository-url>"
echo "git push -u origin main"
echo "git push origin $VERSION"
