#!/bin/bash

# 정적 사이트 배포 옵션 스크립트

echo "🌐 Elite Beauty Admin - 정적 사이트 배포"
echo "========================================"
echo ""

cd /Users/unipurple/Projects/AIChat/admin

# 환경 변수 설정
export REACT_APP_API_URL="https://elite-beauty-api-asia-northeast3-lm.a.run.app"

# 빌드
echo "📦 Admin Dashboard 빌드 중..."
npm run build

echo ""
echo "🚀 배포 옵션을 선택하세요:"
echo ""
echo "1) Firebase Hosting (무료, 추천)"
echo "2) Cloud Storage (가장 저렴)"
echo "3) App Engine (자동 관리)"
echo "4) Cloud Run (현재 방식 유지)"
echo ""
read -p "선택 (1-4): " choice

case $choice in
  1)
    echo ""
    echo "🔥 Firebase Hosting 배포"
    echo "------------------------"
    
    # Firebase CLI 확인
    if ! command -v firebase &> /dev/null; then
        echo "Firebase CLI 설치 중..."
        npm install -g firebase-tools
    fi
    
    echo "다음 명령어를 실행하세요:"
    echo ""
    echo "firebase login"
    echo "firebase use elite-cms-2025"
    echo "firebase deploy --only hosting"
    echo ""
    echo "URL: https://elite-cms-2025.web.app"
    ;;
    
  2)
    echo ""
    echo "☁️ Cloud Storage 배포"
    echo "--------------------"
    
    BUCKET_NAME="elite-beauty-admin-static"
    
    # 버킷 생성
    gsutil mb -p elite-cms-2025 gs://$BUCKET_NAME 2>/dev/null
    
    # 정적 웹사이트 설정
    gsutil web set -m index.html -e index.html gs://$BUCKET_NAME
    
    # 파일 업로드
    gsutil -m rsync -r -d build/ gs://$BUCKET_NAME
    
    # 공개 액세스 설정
    gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME
    
    echo ""
    echo "✅ 배포 완료!"
    echo "URL: https://storage.googleapis.com/$BUCKET_NAME/index.html"
    ;;
    
  3)
    echo ""
    echo "⚙️ App Engine 배포"
    echo "-----------------"
    
    gcloud app deploy app.yaml \
      --project elite-cms-2025 \
      --quiet
    
    echo ""
    echo "✅ 배포 완료!"
    echo "URL: https://elite-cms-2025.appspot.com"
    ;;
    
  4)
    echo ""
    echo "🐳 Cloud Run 배포 (현재 방식)"
    echo "----------------------------"
    
    gcloud run deploy elite-beauty-admin \
      --source . \
      --region asia-northeast3 \
      --allow-unauthenticated \
      --project elite-cms-2025
    
    echo ""
    echo "✅ 배포 완료!"
    echo "URL: https://elite-beauty-admin-asia-northeast3-lm.a.run.app"
    ;;
    
  *)
    echo "잘못된 선택입니다."
    exit 1
    ;;
esac

echo ""
echo "👤 관리자 로그인 정보:"
echo "- 이메일: admin@elitebeauty.com"
echo "- 비밀번호: admin123"
