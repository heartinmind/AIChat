#!/bin/bash
# Python 3.10+ 문법을 Python 3.9 호환으로 변경

echo "🔍 Python 3.10+ 문법 찾기 및 수정..."

# str | None 패턴 찾기
echo "📋 수정이 필요한 파일들:"
grep -r "str | None\|int | None\|float | None\|dict | None\|list | None" --include="*.py" .

echo ""
echo "🔧 해결 방법:"
echo "1. Python 3.9를 사용 중이므로 Union 타입 문법을 변경해야 합니다."
echo "2. 'str | None' → 'Optional[str]' 또는 'Union[str, None]'"
echo "3. 파일 상단에 'from typing import Optional, Union' 추가"

echo ""
echo "📝 수정 예시:"
echo "변경 전: API_KEY: str | None = Field(default=\"\")"
echo "변경 후: API_KEY: Optional[str] = Field(default=\"\")"

echo ""
echo "🚀 또는 Python 3.10+ 설치:"
echo "brew install python@3.11"
echo "python3.11 -m venv venv311"
echo "source venv311/bin/activate"
echo "pip install -r requirements.txt"
