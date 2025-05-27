#!/bin/bash

# 🚀 간소화된 배포 스크립트 - 안정적 버전

echo "🚀 엘리트 뷰티 클리닉 AI 챗봇 - 안정적 배포 시작..."

# 프로젝트 정보
PROJECT_ID="elite-cms-2025"
SERVICE_NAME="beauty-clinic-ai"
REGION="us-central1"

# Google Cloud 설정
echo "🔧 Google Cloud 프로젝트 설정..."
gcloud config set project $PROJECT_ID

# 기본 Dockerfile 교체
echo "📋 최소 의존성 Dockerfile로 교체..."
cp Dockerfile.minimal Dockerfile

# 간소화된 버전으로 배포
echo "🚀 최소 의존성 버전으로 배포 중..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --min-instances 0 \
  --set-env-vars="PORT=8080" \
  --timeout 300

# 결과 확인
if [ $? -eq 0 ]; then
    echo "✅ 배포 성공!"
    echo "🌐 서비스 URL:"
    gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
    
    echo ""
    echo "🎉 새로운 친근한 AI 상담사가 준비되었습니다!"
    echo ""
    echo "📝 테스트할 문장들:"
    echo "  - '아우 질만 들었네'"
    echo "  - '지금 이게 연동된거니?'"
    echo "  - '상담이 좀 기계적인 것 같아요'"
    echo "  - '보톡스 시술 받고 싶어요'"
    echo "  - '예약하고 싶어요'"
    echo ""
else
    echo "❌ 배포 실패"
    echo "💡 빌드 로그 확인:"
    echo "https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"
    exit 1
fi

echo "🎯 배포 완료!"
