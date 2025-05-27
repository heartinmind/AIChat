#!/bin/bash
# AIChat 프로젝트 정리 스크립트

echo "🧹 AIChat 프로젝트 정리 시작..."
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# 1. 백업 디렉토리 생성
BACKUP_DIR="project_backup_$(date +%Y%m%d_%H%M%S)"
echo "📦 백업 디렉토리 생성: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# 2. 디렉토리 구조 생성
echo ""
echo "📁 디렉토리 구조 생성 중..."
mkdir -p tests
mkdir -p examples
mkdir -p examples/demos
mkdir -p examples/interfaces
mkdir -p examples/servers
mkdir -p examples/utils
mkdir -p docs

# 3. 테스트 파일 이동
echo ""
echo "🧪 테스트 파일 정리..."
for file in test_*.py test-*.cjs; do
    if [ -f "$file" ]; then
        mv "$file" tests/
        echo "  ✅ $file → tests/"
    fi
done

# 4. 데모 파일 이동
echo ""
echo "🎮 데모 파일 정리..."
for file in *demo.py *_demo.py; do
    if [ -f "$file" ]; then
        mv "$file" examples/demos/
        echo "  ✅ $file → examples/demos/"
    fi
done

# 5. 인터페이스 파일 이동
echo ""
echo "🖥️  인터페이스 파일 정리..."
for file in *interface.py *_interface.py; do
    if [ -f "$file" ]; then
        mv "$file" examples/interfaces/
        echo "  ✅ $file → examples/interfaces/"
    fi
done

# 6. 서버 파일 이동
echo ""
echo "🌐 서버 파일 정리..."
for file in *server.py *_server.py; do
    if [ -f "$file" ] && [ "$file" != "web_server.py" ]; then
        mv "$file" examples/servers/
        echo "  ✅ $file → examples/servers/"
    fi
done

# 7. 문서 파일 이동 (README 제외)
echo ""
echo "📚 문서 파일 정리..."
for file in *.md; do
    if [ -f "$file" ] && [ "$file" != "README.md" ]; then
        mv "$file" docs/
        echo "  ✅ $file → docs/"
    fi
done

# 8. 유틸리티 파일 이동
echo ""
echo "🔧 유틸리티 파일 정리..."
if [ -f "check_path.py" ]; then
    mv check_path.py examples/utils/
    echo "  ✅ check_path.py → examples/utils/"
fi

# 9. 오래된 설정 파일 백업 후 삭제
echo ""
echo "⚙️  오래된 설정 파일 정리..."
for file in setup_development.bat setup_development.sh; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/"
        rm "$file"
        echo "  ✅ $file → 백업 후 삭제"
    fi
done

# 10. TypeScript 설정 파일 처리 (Python 프로젝트에서는 불필요)
if [ -f "tsconfig.json" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  tsconfig.json 파일 발견${NC}"
    echo "Python 프로젝트에서는 일반적으로 불필요합니다."
    echo -n "삭제하시겠습니까? (y/N): "
    read -r response
    if [ "$response" = "y" ]; then
        cp tsconfig.json "$BACKUP_DIR/"
        rm tsconfig.json
        echo "  ✅ tsconfig.json → 백업 후 삭제"
    fi
fi

# 11. 임시 파일 정리
echo ""
echo "🗑️  임시 파일 정리..."
if [ -f "test_claude_desktop.txt" ]; then
    rm test_claude_desktop.txt
    echo "  ✅ test_claude_desktop.txt 삭제"
fi

# 12. __pycache__ 정리
echo ""
echo "🧹 캐시 파일 정리..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "  ✅ __pycache__ 디렉토리 삭제"

# 13. 정리 완료 보고서
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ 프로젝트 정리 완료!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 정리 결과:"
echo "  - 테스트 파일: tests/ 디렉토리로 이동"
echo "  - 데모/예제: examples/ 디렉토리로 이동"
echo "  - 문서: docs/ 디렉토리로 이동"
echo "  - 백업: $BACKUP_DIR/ 디렉토리에 저장"
echo ""
echo "💡 다음 단계:"
echo "1. git status로 변경사항 확인"
echo "2. git add . && git commit -m '[정리] 프로젝트 구조 개선'"
echo "3. 불필요한 파일 추가 삭제"
echo ""
echo "📁 새로운 프로젝트 구조:"
tree -L 2 -d 2>/dev/null || ls -la
