#!/bin/bash
# 실행 권한 부여: chmod +x clean_customer_service.sh
# customer_service 디렉토리 정리 스크립트

echo "🧹 customer_service 디렉토리 정리 시작..."

# 1. __pycache__ 디렉토리 삭제
echo "📦 Python 캐시 파일 삭제 중..."
find /Users/unipurple/Projects/AIChat/customer_service -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# 2. tools 파일 백업
echo "💾 tools 파일 백업 중..."
cp /Users/unipurple/Projects/AIChat/customer_service/tools/tools.py /Users/unipurple/Projects/AIChat/customer_service/tools/tools_original.py.bak
cp /Users/unipurple/Projects/AIChat/customer_service/tools/tools_real.py /Users/unipurple/Projects/AIChat/customer_service/tools/tools_real.py.bak

# 3. beauty_clinic_data.py 이동 (옵션)
# echo "📍 beauty_clinic_data.py를 상위 디렉토리로 이동..."
# mkdir -p /Users/unipurple/Projects/AIChat/beauty_clinic
# mv /Users/unipurple/Projects/AIChat/customer_service/rag/beauty_clinic_data.py /Users/unipurple/Projects/AIChat/beauty_clinic/

echo "✅ 정리 완료!"
echo ""
echo "📋 정리 결과:"
echo "- __pycache__ 디렉토리 삭제됨"
echo "- tools 파일 백업됨 (.bak 파일)"
echo ""
echo "🔧 추가 작업 필요:"
echo "1. tools.py와 tools_real.py 통합"
echo "2. beauty_clinic_data.py 위치 재검토"
