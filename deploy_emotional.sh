#!/bin/bash

# 💖 감정을 읽는 AI 배포 - 재미와 감동 버전

echo "💖 진짜 감정을 읽는 AI 상담사 배포!"

PROJECT_ID="elite-cms-2025"
SERVICE_NAME="beauty-clinic-ai"
REGION="us-central1"

gcloud config set project $PROJECT_ID

echo "🚀 감정 읽기 버전 배포 중..."

# 감정 AI용 Dockerfile
cat > Dockerfile.emotional << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements_minimal.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY emotional_ai_server.py .
COPY templates/ templates/
ENV PYTHONPATH=/app
ENV PORT=8080
CMD exec python emotional_ai_server.py
EOF

gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --dockerfile Dockerfile.emotional \
  --set-env-vars="PORT=8080" \
  --timeout 300

rm Dockerfile.emotional

if [ $? -eq 0 ]; then
    echo ""
    echo "💖 감정을 읽는 AI 배포 완료!"
    echo "🌐 URL:"
    gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
    
    echo ""
    echo "🎭 이제 진짜 재미와 감동이 있어요!"
    echo ""
    echo "🧪 감정 테스트:"
    echo "  - '보고싶다' → 그리움에 진짜 공감"
    echo "  - '외롭다' → 외로움을 따뜻하게 위로"  
    echo "  - '짜증나' → 스트레스를 이해하고 풀어줌"
    echo "  - 'ㅠㅠ' → 속상함에 진심으로 공감"
    echo "  - 'ㅋㅋ' → 함께 웃어주며 기뻐함"
    echo ""
    echo "💄 그리고 자연스럽게 뷰티케어로 연결!"
    echo ""
else
    echo "❌ 배포 실패"
fi
