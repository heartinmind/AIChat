#!/bin/bash

# 🚀 엘리트 뷰티 클리닉 AI 챗봇 - 빠른 배포 스크립트

echo "🚀 엘리트 뷰티 클리닉 AI 챗봇 배포 시작..."

# 1. 프로젝트 정보 설정
PROJECT_ID="elite-cms-2025"
SERVICE_NAME="beauty-clinic-ai"
REGION="us-central1"

# 2. 현재 Google Cloud 프로젝트 확인
echo "📋 현재 Google Cloud 설정 확인..."
gcloud config list

# 3. 프로젝트 설정
echo "🔧 Google Cloud 프로젝트 설정..."
gcloud config set project $PROJECT_ID

# 4. 필요한 API 활성화
echo "🔌 필요한 Google Cloud API 활성화..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# 5. Cloud Run 배포
echo "🚀 Cloud Run에 배포 중..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --min-instances 1 \
  --set-env-vars="PORT=8080,PYTHON_PATH=/app" \
  --timeout 300

# 6. 배포 결과 확인
if [ $? -eq 0 ]; then
    echo "✅ 배포 성공!"
    echo "🌐 서비스 URL:"
    gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
    
    echo ""
    echo "🎉 배포 완료! 웹사이트에서 새로운 친근한 AI 상담사를 확인해보세요!"
    echo ""
    echo "📝 테스트할 문장들:"
    echo "  - '아우 질만 들었네'"
    echo "  - '지금 이게 연동된거니?'"
    echo "  - '상담이 좀 기계적인 것 같아요'"
    echo ""
else
    echo "❌ 배포 실패. 로그를 확인해주세요."
    exit 1
fi

echo "🎯 배포 스크립트 완료!"
