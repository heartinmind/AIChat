#!/bin/bash
# 대체 포트로 서버 실행

PORT=8081
echo "🚀 포트 $PORT로 서버 실행 중..."
echo "📍 URL: http://localhost:$PORT"
echo ""

PORT=$PORT python web_server.py
