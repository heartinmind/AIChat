#!/bin/bash

echo "💾 프로젝트 백업 스크립트"
echo "======================="
echo ""

# 백업 디렉토리 생성
BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="project_backup_${BACKUP_DATE}"
mkdir -p "../${BACKUP_DIR}"

# 제외할 디렉토리/파일 목록
EXCLUDE_PATTERNS=(
    "node_modules"
    "__pycache__"
    "venv"
    "venv_*"
    ".next"
    "*.log"
    "*.db"
    "*.pyc"
    ".DS_Store"
    ".git"
    "build"
    "dist"
)

# rsync 명령어 구성
RSYNC_CMD="rsync -av --progress"
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    RSYNC_CMD="$RSYNC_CMD --exclude='$pattern'"
done

echo "📦 백업 시작..."
echo "백업 위치: ../${BACKUP_DIR}"
echo ""

# 백업 실행
eval "$RSYNC_CMD . ../${BACKUP_DIR}/"

# 백업 정보 파일 생성
cat > "../${BACKUP_DIR}/BACKUP_INFO.txt" << EOF
Elite Beauty AI Chat System Backup
==================================
백업 일시: $(date)
백업 버전: v1.0.0
Python 버전: $(python3 --version)
Node 버전: $(node --version)

주요 변경사항:
- AI 하이브리드 채팅 시스템 완성
- 관리자 대시보드 구현
- 환경별 설정 분리

Git 커밋: $(git rev-parse HEAD 2>/dev/null || echo "Git 미설정")
EOF

# 백업 압축 (선택사항)
echo ""
read -p "백업을 압축하시겠습니까? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗜️ 압축 중..."
    cd ..
    tar -czf "${BACKUP_DIR}.tar.gz" "${BACKUP_DIR}"
    echo "✅ 압축 완료: ${BACKUP_DIR}.tar.gz"
fi

echo ""
echo "✅ 백업 완료!"
echo "백업 위치: ../${BACKUP_DIR}"
