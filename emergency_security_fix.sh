#!/bin/bash
# 긴급 보안 조치 스크립트

echo "🚨 긴급 보안 조치 실행 중..."

# 1. 파일 백업 (안전한 위치로)
echo "1. 서비스 계정 키 백업 중..."
mkdir -p ~/Documents/secure_backup_$(date +%Y%m%d_%H%M%S)
cp service-account-key.json ~/Documents/secure_backup_$(date +%Y%m%d_%H%M%S)/
echo "✅ 백업 완료: ~/Documents/secure_backup_*/"

# 2. Git에서 제거
echo "2. Git 기록에서 완전 제거 중..."
git rm --cached service-account-key.json 2>/dev/null || true
echo "service-account-key.json" >> .gitignore

# 3. 파일 삭제
echo "3. 프로젝트에서 파일 삭제 중..."
rm -f service-account-key.json

# 4. Git 히스토리에서 완전 제거
echo "4. Git 히스토리 정리 중..."
if command -v git-filter-repo &> /dev/null; then
    git filter-repo --path service-account-key.json --invert-paths
else
    echo "⚠️  git-filter-repo가 설치되지 않음. 수동으로 처리 필요!"
    echo "설치: brew install git-filter-repo"
fi

echo "✅ 긴급 조치 완료!"
echo ""
echo "🔴 다음 단계 (매우 중요!):"
echo "1. GCP Console에서 이 서비스 계정 키 즉시 비활성화/삭제"
echo "2. 새로운 서비스 계정 키 생성"
echo "3. GitHub에 이미 푸시했다면, 즉시 키 교체 필요!"
