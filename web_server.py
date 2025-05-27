#!/usr/bin/env python3
"""
웹 인터페이스용 FastAPI 서버

뷰티 클리닉 AI 챗봇의 웹 버전을 제공합니다.
"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

# 현재 프로젝트의 customer_service 임포트
try:
    from customer_service.agent import root_agent
    from customer_service.tools.tools import access_cart_information
    AGENT_AVAILABLE = True
except ImportError:
    print("⚠️ customer_service 모듈을 찾을 수 없습니다. Mock 모드로 실행됩니다.")
    AGENT_AVAILABLE = False

# FastAPI 앱 생성
app = FastAPI(
    title="엘리트 뷰티 클리닉 AI 챗봇",
    description="친근하고 전문적인 AI 뷰티 상담사",
    version="2.0.0"
)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# API 요청 모델
class ChatRequest(BaseModel):
    message: str
    customer_id: str = "web_user"

class ChatResponse(BaseModel):
    response: str
    customer_id: str

# 루트 경로 - 메인 웹 인터페이스
@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    """메인 채팅 인터페이스 제공"""
    return templates.TemplateResponse("index.html", {"request": request})

# 채팅 API 엔드포인트
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_request: ChatRequest):
    """AI와 채팅하는 API"""
    
    if AGENT_AVAILABLE:
        try:
            # 실제 AI 에이전트 호출
            ai_response = root_agent(
                chat_request.message,
                customer_id=chat_request.customer_id
            )
            
            # AI 응답이 문자열이 아닌 경우 처리
            if hasattr(ai_response, 'content'):
                response_text = ai_response.content
            elif isinstance(ai_response, dict):
                response_text = ai_response.get('content', str(ai_response))
            else:
                response_text = str(ai_response)
                
        except Exception as e:
            print(f"AI 에이전트 오류: {e}")
            response_text = "죄송합니다. 잠시 기술적인 문제가 발생했어요. 곧 해결하고 다시 답변드릴게요! 😅"
    else:
        # Mock 응답 (개발/테스트용)
        response_text = f"안녕하세요! 말씀하신 '{chat_request.message}'에 대해 상담해드릴게요. 현재는 테스트 모드로 실행 중입니다. 😊"
    
    return ChatResponse(
        response=response_text,
        customer_id=chat_request.customer_id
    )

# 고객 정보 API (옵션)
@app.get("/api/customer/{customer_id}")
async def get_customer_info(customer_id: str):
    """고객 정보 조회 API"""
    
    if AGENT_AVAILABLE:
        try:
            customer_info = access_cart_information(customer_id)
            return customer_info
        except Exception as e:
            return {"error": str(e)}
    else:
        return {
            "customer_id": customer_id,
            "message": "Mock 데이터입니다.",
            "items": [],
            "subtotal": 0
        }

# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """서비스 상태 확인"""
    return {
        "status": "healthy",
        "service": "Beauty Clinic AI Chatbot",
        "version": "2.0.0",
        "agent_available": AGENT_AVAILABLE
    }

# 개발용 실행
if __name__ == "__main__":
    # 환경변수에서 포트 설정 (Cloud Run 호환)
    port = int(os.environ.get("PORT", 8080))
    
    print(f"""
🚀 엘리트 뷰티 클리닉 AI 챗봇 서버 시작
📍 URL: http://localhost:{port}
🤖 AI 에이전트: {'활성화' if AGENT_AVAILABLE else '테스트 모드'}
    """)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
