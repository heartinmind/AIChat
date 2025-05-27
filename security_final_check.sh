#!/bin/bash
# 보안 완료 체크리스트

echo "🔐 보안 조치 최종 확인 중..."
echo ""

# 1. 파일 삭제 확인
echo "1️⃣ service-account-key.json 파일 확인:"
if [ -f "service-account-key.json" ]; then
    echo "   ❌ 파일이 아직 존재합니다!"
else
    echo "   ✅ 파일이 삭제되었습니다."
fi

# 2. Git 상태 확인
echo ""
echo "2️⃣ Git 히스토리 확인:"
git log --oneline --all -- service-account-key.json 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ⚠️  Git 히스토리에 기록이 있습니다!"
    echo "   다음 명령으로 완전 제거 필요:"
    echo "   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch service-account-key.json' --prune-empty --tag-name-filter cat -- --all"
else
    echo "   ✅ Git 히스토리에 없습니다."
fi

# 3. .gitignore 확인
echo ""
echo "3️⃣ .gitignore 확인:"
if grep -q "service-account-key.json" .gitignore; then
    echo "   ✅ .gitignore에 추가되어 있습니다."
else
    echo "   ❌ .gitignore에 추가 필요!"
    echo "service-account-key.json" >> .gitignore
    echo "   ✅ 자동으로 추가했습니다."
fi

# 4. 원격 저장소 확인
echo ""
echo "4️⃣ 원격 저장소 상태:"
git remote -v

echo ""
echo "📋 추가 권장사항:"
echo "1. GCP 콘솔에서 서비스 계정 키 교체"
echo "2. 환경변수 방식으로 전환 (GOOGLE_APPLICATION_CREDENTIALS)"
echo "3. GitHub Secrets 사용 검토"
echo ""
echo "✅ 보안 점검 완료!"
