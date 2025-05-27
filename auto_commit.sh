#!/bin/bash
# 자동 git 커밋 스크립트

cd /Users/unipurple/Projects/AIChat

echo "🔍 Git 상태 확인..."
git status --short

echo ""
echo "📦 모든 변경사항 스테이징..."
git add -A

echo ""
echo "💾 커밋 실행..."
git commit -m "[정리] 프로젝트 구조 개선 및 보안 강화

- 테스트 파일들을 tests/ 디렉토리로 이동
- 데모/예제 파일들을 examples/ 디렉토리로 구조화  
- 문서들을 docs/ 디렉토리로 정리
- service-account-key.json 보안을 위해 제거
- 불필요한 설정 파일 정리 (tsconfig.json, setup_development.*)
- Cursor IDE 제어 규칙 추가 (.cursorrules)
- 안전 작업 도구 추가 (safe_work.sh)"

echo ""
echo "✅ 커밋 완료!"
echo ""
echo "🚀 GitHub에 푸시하려면:"
echo "git push origin main"
