#!/usr/bin/env python3
"""
🔧 간단한 테스트 서버 - 연결 문제 진단용
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def test_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>테스트 서버</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>🎉 서버 연결 성공!</h1>
        <p>이 페이지가 보인다면 서버가 정상 작동 중입니다.</p>
        <hr>
        <h2>테스트 완료 ✅</h2>
        <p>이제 메인 서버를 실행해도 됩니다!</p>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "OK", "message": "테스트 서버 정상 작동"}

if __name__ == "__main__":
    port = 8080
    print(f"""
🔧 테스트 서버 시작
📍 URL: http://localhost:{port}
📍 헬스체크: http://localhost:{port}/health

Ctrl+C로 서버를 중지할 수 있습니다.
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
