#!/bin/bash

# 🤗 진짜 친근한 버전 즉시 배포

echo "🤗 진짜 친근한 AI 상담사 배포 시작!"

PROJECT_ID="elite-cms-2025"
SERVICE_NAME="beauty-clinic-ai"
REGION="us-central1"

# Google Cloud 설정
gcloud config set project $PROJECT_ID

# 진짜 친근한 버전으로 배포
echo "🚀 완전히 새로운 친근한 버전 배포 중..."

# 임시 Dockerfile 생성
cat > Dockerfile.friendly << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements_minimal.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY super_friendly_server.py .
COPY templates/ templates/
ENV PYTHONPATH=/app
ENV PORT=8080
CMD exec python super_friendly_server.py
EOF

# 배포 실행
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --dockerfile Dockerfile.friendly \
  --set-env-vars="PORT=8080" \
  --timeout 300

# 정리
rm Dockerfile.friendly

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 진짜 친근한 AI 상담사 배포 완료!"
    echo "🌐 URL:"
    gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
    
    echo ""
    echo "🤗 이제 정말 친근하게 대화해요!"
    echo ""
    echo "🧪 꼭 테스트해보세요:"
    echo "  - '아우' → 진짜 공감하는 응답"
    echo "  - '뭐야' → 자연스러운 반응"
    echo "  - 'ㅋㅋ' → 함께 웃어주는 응답"
    echo "  - '안녕' → 따뜻한 인사"
    echo ""
else
    echo "❌ 배포 실패"
fi
