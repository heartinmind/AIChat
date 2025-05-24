@echo off
echo 🚀 뷰티 클리닉 AI 챗봇 개발 환경을 설정합니다...

REM Python 버전 확인
echo 📋 Python 버전 확인 중...
python --version
python3 --version

REM Python 의존성 설치
echo 📦 Python 의존성 설치 중...
pip install pydantic-settings
pip install jsonschema
pip install pytest

REM Node.js 버전 확인
echo 📋 Node.js 버전 확인 중...
node --version
npm --version

REM Node.js 의존성 설치
echo 📦 Node.js 의존성 설치 중...
npm install

echo ✅ 환경 설정 완료!
echo.
echo 🧪 테스트 실행 방법:
echo   Python 테스트: python -m pytest tests/unit/ -v
echo   Node.js 테스트: npm test
echo.
echo 🎯 프로젝트 실행 준비 완료!
pause 