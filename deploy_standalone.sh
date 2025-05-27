#!/bin/bash

# 🚀 독립형 뷰티 클리닉 AI 챗봇 - 배포 스크립트

echo "🚀 독립형 AI 챗봇 배포를 시작합니다..."

# Google Cloud 프로젝트 설정
PROJECT_ID="elite-cms-2025"
SERVICE_NAME="beauty-clinic-ai-standalone"
REGION="us-central1"

echo "📋 프로젝트: $PROJECT_ID"
echo "🌐 서비스: $SERVICE_NAME"
echo "📍 지역: $REGION"
echo "💪 독립형 버전 (의존성 최소화)"

# Cloud Run에 배포
gcloud run deploy $SERVICE_NAME \
  --source . \
  --dockerfile Dockerfile.standalone \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --project $PROJECT_ID

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 배포 성공!"
    echo "🌐 서비스 URL: https://$SERVICE_NAME-$REGION.run.app"
    echo "🔍 헬스체크: https://$SERVICE_NAME-$REGION.run.app/health"
    echo "💬 채팅 테스트: https://$SERVICE_NAME-$REGION.run.app"
    echo ""
    echo "🎉 독립형 AI 챗봇이 성공적으로 배포되었습니다!"
else
    echo "❌ 배포 실패. 로그를 확인해주세요."
fi 