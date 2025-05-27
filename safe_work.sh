#!/bin/bash
# AIChat 프로젝트 안전 작업 스크립트

set -e  # 에러 발생 시 즉시 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 현재 디렉토리 확인
if [ ! -f "package.json" ] || [ ! -d "customer_service" ]; then
    echo -e "${RED}❌ AIChat 프로젝트 루트 디렉토리에서 실행해주세요!${NC}"
    exit 1
fi

# 메뉴 표시
show_menu() {
    echo -e "\n${BLUE}=== AIChat 안전 작업 도구 ===${NC}"
    echo "1) 📦 중요 파일 백업"
    echo "2) 🔍 작업 전 상태 확인"
    echo "3) 🧪 테스트 실행"
    echo "4) 📤 안전하게 커밋 & 푸시"
    echo "5) 🧹 캐시 파일 정리"
    echo "6) 🔄 MCP 설정 백업"
    echo "7) 📋 일일 체크리스트"
    echo "8) 🚨 긴급 복구"
    echo "0) 종료"
    echo -n "선택: "
}

# 중요 파일 백업
backup_important_files() {
    echo -e "\n${YELLOW}📦 중요 파일 백업 중...${NC}"
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # 백업할 파일 목록
    files_to_backup=(
        ".env"
        "package.json"
        "requirements.txt"
        "claude_desktop_config.json"
        "service-account-key.json"
    )
    
    for file in "${files_to_backup[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "$BACKUP_DIR/" 2>/dev/null || true
            echo -e "  ✅ $file"
        fi
    done
    
    # MCP 설정 백업 (Mac)
    if [ -f "$HOME/Library/Application Support/Claude/claude_desktop_config.json" ]; then
        cp "$HOME/Library/Application Support/Claude/claude_desktop_config.json" "$BACKUP_DIR/claude_desktop_config_system.json"
        echo -e "  ✅ MCP 설정 (시스템)"
    fi
    
    echo -e "${GREEN}✅ 백업 완료: $BACKUP_DIR${NC}"
}

# 작업 전 상태 확인
check_status() {
    echo -e "\n${YELLOW}🔍 프로젝트 상태 확인 중...${NC}"
    
    # Git 상태
    echo -e "\n${BLUE}Git 상태:${NC}"
    git status --short
    
    # 현재 브랜치
    echo -e "\n${BLUE}현재 브랜치:${NC}"
    git branch --show-current
    
    # Python 환경
    echo -e "\n${BLUE}Python 환경:${NC}"
    python --version
    if [ -d "venv" ]; then
        echo "  ✅ 가상환경 존재"
    else
        echo "  ⚠️  가상환경 없음"
    fi
    
    # Node 환경
    echo -e "\n${BLUE}Node 환경:${NC}"
    node --version
    npm --version
    
    # 포트 사용 확인
    echo -e "\n${BLUE}포트 사용 현황:${NC}"
    lsof -i :5000 2>/dev/null || echo "  ✅ 5000번 포트 사용 가능"
    lsof -i :3000 2>/dev/null || echo "  ✅ 3000번 포트 사용 가능"
}

# 테스트 실행
run_tests() {
    echo -e "\n${YELLOW}🧪 테스트 실행 중...${NC}"
    
    # Python 테스트
    if [ -f "test_server.py" ]; then
        echo -e "\n${BLUE}Python 테스트:${NC}"
        python -m pytest tests/ -v || echo -e "${YELLOW}⚠️  일부 테스트 실패${NC}"
    fi
    
    # JavaScript 테스트
    if [ -f "package.json" ] && grep -q "test" package.json; then
        echo -e "\n${BLUE}JavaScript 테스트:${NC}"
        npm test || echo -e "${YELLOW}⚠️  일부 테스트 실패${NC}"
    fi
}

# 안전한 커밋 & 푸시
safe_commit_push() {
    echo -e "\n${YELLOW}📤 안전한 커밋 & 푸시${NC}"
    
    # 변경사항 확인
    echo -e "\n${BLUE}변경된 파일:${NC}"
    git status --short
    
    # 보호 파일 체크
    echo -e "\n${BLUE}보호 파일 확인:${NC}"
    protected_files=(".env" "service-account-key.json" "*.pem" "*.key")
    for pattern in "${protected_files[@]}"; do
        if git status --short | grep -q "$pattern"; then
            echo -e "${RED}⚠️  경고: 보호 파일이 변경되었습니다: $pattern${NC}"
            echo -n "계속하시겠습니까? (y/N): "
            read -r response
            if [ "$response" != "y" ]; then
                echo "취소되었습니다."
                return
            fi
        fi
    done
    
    # 커밋 메시지 입력
    echo -e "\n${BLUE}커밋 타입 선택:${NC}"
    echo "1) [기능] 새로운 기능"
    echo "2) [수정] 버그 수정"
    echo "3) [개선] 기능 개선"
    echo "4) [리팩토링] 코드 정리"
    echo "5) [문서] 문서 업데이트"
    echo -n "선택 (1-5): "
    read -r commit_type
    
    case $commit_type in
        1) prefix="[기능]" ;;
        2) prefix="[수정]" ;;
        3) prefix="[개선]" ;;
        4) prefix="[리팩토링]" ;;
        5) prefix="[문서]" ;;
        *) prefix="[기타]" ;;
    esac
    
    echo -n "커밋 메시지: $prefix "
    read -r message
    
    # 커밋 실행
    git add .
    git commit -m "$prefix $message"
    
    # 푸시 확인
    echo -n "GitHub에 푸시하시겠습니까? (y/N): "
    read -r push_response
    if [ "$push_response" = "y" ]; then
        git push origin "$(git branch --show-current)"
        echo -e "${GREEN}✅ 푸시 완료!${NC}"
    fi
}

# 캐시 정리
clean_cache() {
    echo -e "\n${YELLOW}🧹 캐시 파일 정리 중...${NC}"
    
    # Python 캐시
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    echo "  ✅ Python 캐시 삭제"
    
    # Node 캐시
    if [ -d "node_modules/.cache" ]; then
        rm -rf node_modules/.cache
        echo "  ✅ Node 캐시 삭제"
    fi
    
    # 기타 임시 파일
    find . -name ".DS_Store" -delete 2>/dev/null || true
    find . -name "*.log" -delete 2>/dev/null || true
    echo "  ✅ 임시 파일 삭제"
    
    echo -e "${GREEN}✅ 정리 완료!${NC}"
}

# MCP 설정 백업
backup_mcp() {
    echo -e "\n${YELLOW}🔄 MCP 설정 백업 중...${NC}"
    
    MCP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    if [ -f "$MCP_CONFIG" ]; then
        BACKUP_PATH="$HOME/Desktop/claude_desktop_config_$(date +%Y%m%d_%H%M%S).json"
        cp "$MCP_CONFIG" "$BACKUP_PATH"
        echo -e "${GREEN}✅ MCP 설정이 백업되었습니다: $BACKUP_PATH${NC}"
    else
        echo -e "${RED}❌ MCP 설정 파일을 찾을 수 없습니다.${NC}"
    fi
}

# 일일 체크리스트
daily_checklist() {
    echo -e "\n${BLUE}📋 일일 체크리스트${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    checklist=(
        "Git pull 실행"
        "환경변수 확인"
        "테스트 실행"
        "Claude와 작업 논의"
        "중요 파일 백업"
        "브랜치 확인"
        "의존성 업데이트 확인"
    )
    
    for item in "${checklist[@]}"; do
        echo -n "[ ] $item - 완료했나요? (y/N): "
        read -r response
        if [ "$response" = "y" ]; then
            echo -e "    ${GREEN}✅ 완료${NC}"
        else
            echo -e "    ${YELLOW}⏳ 대기${NC}"
        fi
    done
}

# 긴급 복구
emergency_recovery() {
    echo -e "\n${RED}🚨 긴급 복구 메뉴${NC}"
    echo "1) Git 변경사항 모두 취소"
    echo "2) 마지막 커밋 취소"
    echo "3) MCP 설정 복원"
    echo "4) 백업에서 파일 복원"
    echo "0) 취소"
    echo -n "선택: "
    read -r recovery_choice
    
    case $recovery_choice in
        1)
            echo -n "정말로 모든 변경사항을 취소하시겠습니까? (yes 입력): "
            read -r confirm
            if [ "$confirm" = "yes" ]; then
                git checkout .
                git clean -fd
                echo -e "${GREEN}✅ 변경사항이 취소되었습니다.${NC}"
            fi
            ;;
        2)
            git reset --soft HEAD~1
            echo -e "${GREEN}✅ 마지막 커밋이 취소되었습니다.${NC}"
            ;;
        3)
            echo "사용 가능한 MCP 백업:"
            ls -la ~/Desktop/claude_desktop_config_*.json 2>/dev/null || echo "백업 없음"
            ;;
        4)
            echo "사용 가능한 백업:"
            ls -la backups/
            ;;
        *)
            echo "취소되었습니다."
            ;;
    esac
}

# 메인 루프
while true; do
    show_menu
    read -r choice
    
    case $choice in
        1) backup_important_files ;;
        2) check_status ;;
        3) run_tests ;;
        4) safe_commit_push ;;
        5) clean_cache ;;
        6) backup_mcp ;;
        7) daily_checklist ;;
        8) emergency_recovery ;;
        0) 
            echo -e "${GREEN}안녕히 가세요! Claude와 함께 즐거운 코딩하세요! 🚀${NC}"
            exit 0 
            ;;
        *) echo -e "${RED}잘못된 선택입니다.${NC}" ;;
    esac
    
    echo -e "\n${YELLOW}계속하려면 엔터를 누르세요...${NC}"
    read -r
done
