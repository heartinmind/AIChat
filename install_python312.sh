#!/bin/bash

# Python 3.12 설치 도우미 스크립트

echo "🐍 Python 3.12 설치 가이드"
echo "========================="
echo ""

# OS 확인
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS 환경입니다."
    
    # Homebrew 확인
    if command -v brew &> /dev/null; then
        echo "✅ Homebrew가 설치되어 있습니다."
        echo ""
        echo "Python 3.12 설치:"
        echo "brew install python@3.12"
        echo ""
        echo "Python 3.12를 기본으로 설정:"
        echo "brew link python@3.12"
    else
        echo "❌ Homebrew가 설치되어 있지 않습니다."
        echo ""
        echo "Homebrew 설치:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    fi
    
    # pyenv 옵션
    echo ""
    echo "또는 pyenv 사용 (여러 Python 버전 관리):"
    echo "brew install pyenv"
    echo "pyenv install 3.12.1"
    echo "pyenv local 3.12.1"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux 환경입니다."
    echo ""
    echo "Ubuntu/Debian:"
    echo "sudo apt update"
    echo "sudo apt install python3.12 python3.12-venv python3.12-dev"
    echo ""
    echo "RHEL/CentOS/Fedora:"
    echo "sudo dnf install python3.12 python3.12-devel"
else
    echo "알 수 없는 OS입니다."
fi

echo ""
echo "설치 후 프로젝트에서 Python 3.12 사용:"
echo ""
echo "1. 가상환경 재생성:"
echo "   rm -rf venv"
echo "   python3.12 -m venv venv"
echo ""
echo "2. test_backend_local.sh 실행"
echo "   bash test_backend_local.sh"
