#!/usr/bin/env python3
"""
🚀 독립형 웹 서버 - Google ADK 없이도 작동

Google Cloud Run에서 안전하게 배포되는 버전
"""

import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

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

# 개선된 AI 응답 생성기
class FriendlyAIResponder:
    """친근한 AI 응답 생성기"""
    
    def __init__(self):
        self.customer_data = {
            "web_user": {
                "name": "고객님",
                "membership": "BASIC",
                "visit_count": 1
            }
        }
        
        # 감정별 응답 템플릿
        self.emotion_responses = {
            "tired": [
                "아이고, 정말 고생 많으셨겠어요! 😅",
                "하루 종일 바쁘셨나 봐요?",
                "이럴 때일수록 자기관리 시간이 필요한데...",
                "혹시 스트레스 받으실 때 피부에도 영향 있지 않으세요?"
            ],
            "curious": [
                "네 맞아요! 실시간으로 연결되어 있어서",
                "바로바로 답해드릴 수 있어요 😊", 
                "신기하죠? 요즘 기술이 정말 발전해서",
                "궁금한 거 있으시면 편하게 물어보세요!"
            ],
            "dissatisfied": [
                "아, 죄송해요! 😅",
                "제가 아직 좀 어색했나 봐요...",
                "더 편하고 자연스럽게 대화하고 싶은데",
                "고객님께 정말 도움이 되는 상담사가 되고 싶거든요 💪"
            ],
            "treatment_inquiry": [
                "시술에 관심 있으시군요! ✨",
                "고객님의 피부 고민에 맞는 시술을 추천해드릴게요",
                "어떤 부분이 가장 신경 쓰이시나요?"
            ],
            "booking": [
                "예약 도와드릴게요! 📅",
                "원하시는 날짜와 시간을 알려주세요",
                "인기 시술들은 빨리 예약이 차니까 서둘러주세요!"
            ]
        }
        
        # 시술 정보
        self.treatments = {
            "보톡스": {
                "name": "보톡스 (이마)",
                "price": 200000,
                "description": "이마 주름 개선에 효과적인 시술입니다",
                "duration": "30분"
            },
            "필러": {
                "name": "히알루론산 필러",
                "price": 400000,
                "description": "볼륨 개선 및 윤곽 정리를 위한 시술입니다",
                "duration": "45분"
            },
            "하이드라페이셜": {
                "name": "하이드라페이셜",
                "price": 150000,
                "description": "모든 피부 타입에 적합한 딥클렌징 시술입니다",
                "duration": "60분"
            }
        }
    
    def analyze_emotion(self, message: str) -> str:
        """메시지에서 감정/의도 분석"""
        message_lower = message.lower()
        
        # 피곤함 표현
        tired_keywords = ["질만", "피곤", "지쳐", "힘들어", "스트레스", "바빠"]
        if any(keyword in message for keyword in tired_keywords):
            return "tired"
        
        # 궁금함/기술 문의
        curious_keywords = ["연동", "어떻게", "시스템", "방법", "작동"]
        if any(keyword in message for keyword in curious_keywords):
            return "curious"
        
        # 불만 표현
        dissatisfied_keywords = ["별루", "아쉬워", "기계적", "로봇", "딱딱"]
        if any(keyword in message for keyword in dissatisfied_keywords):
            return "dissatisfied"
        
        # 시술 문의
        treatment_keywords = ["시술", "추천", "보톡스", "필러", "레이저", "피부", "주름"]
        if any(keyword in message for keyword in treatment_keywords):
            return "treatment_inquiry"
        
        # 예약 관련
        booking_keywords = ["예약", "날짜", "시간", "언제", "가능"]
        if any(keyword in message for keyword in booking_keywords):
            return "booking"
        
        return "general"
    
    def generate_response(self, message: str, customer_id: str = "web_user") -> str:
        """친근한 응답 생성"""
        
        emotion = self.analyze_emotion(message)
        
        # 감정별 맞춤 응답
        if emotion in self.emotion_responses:
            base_response = " ".join(self.emotion_responses[emotion])
            
            # 시술 추천 카드 추가
            if emotion == "treatment_inquiry":
                treatment_cards = self._generate_treatment_cards()
                return base_response + "\n\n" + treatment_cards
            
            # 예약 정보 추가  
            elif emotion == "booking":
                booking_info = self._generate_booking_info()
                return base_response + "\n\n" + booking_info
                
            return base_response
        
        # 일반적인 친근한 응답
        friendly_responses = [
            "네네, 말씀해주세요! 😊",
            "어떤 도움이 필요하신지 알려주세요!",
            "궁금한 게 있으시면 편하게 물어보세요~",
            "더 자세히 말씀해주시면 정확히 도움드릴 수 있어요!",
            "저희 클리닉에서 어떤 서비스가 필요하신가요?"
        ]
        
        import random
        return random.choice(friendly_responses)
    
    def _generate_treatment_cards(self) -> str:
        """시술 추천 카드 생성"""
        cards = []
        for key, treatment in self.treatments.items():
            card = f"""
💎 **{treatment['name']}**
💰 가격: {treatment['price']:,}원
⏰ 소요시간: {treatment['duration']}
📝 {treatment['description']}
            """.strip()
            cards.append(card)
        
        return "\n\n".join(cards[:2])  # 상위 2개만 표시
    
    def _generate_booking_info(self) -> str:
        """예약 정보 생성"""
        return """
📅 **예약 가능 시간**
• 평일: 오전 10시 ~ 오후 7시
• 토요일: 오전 10시 ~ 오후 5시  
• 일요일: 휴무

📞 **예약 문의**: 02-1234-5678
📍 **위치**: 서울 강남구 강남대로 123

원하시는 시술과 날짜를 말씀해주시면 
실시간으로 예약 도와드릴게요! ✨
        """.strip()

# AI 응답기 인스턴스
ai_responder = FriendlyAIResponder()

# 루트 경로 - 메인 웹 인터페이스
@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    """메인 채팅 인터페이스 제공"""
    return templates.TemplateResponse("index.html", {"request": request})

# 채팅 API 엔드포인트
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_request: ChatRequest):
    """AI와 채팅하는 API"""
    
    try:
        # 친근한 AI 응답 생성
        ai_response = ai_responder.generate_response(
            chat_request.message,
            chat_request.customer_id
        )
        
        return ChatResponse(
            response=ai_response,
            customer_id=chat_request.customer_id
        )
        
    except Exception as e:
        print(f"응답 생성 오류: {e}")
        return ChatResponse(
            response="죄송해요! 잠시 기술적인 문제가 발생했어요. 곧 해결하고 다시 답변드릴게요! 😅",
            customer_id=chat_request.customer_id
        )

# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """서비스 상태 확인"""
    return {
        "status": "healthy",
        "service": "Beauty Clinic AI Chatbot",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "message": "독립형 웹서버 정상 작동 중"
    }

# 개발용 실행
if __name__ == "__main__":
    # 환경변수에서 포트 설정 (Cloud Run 호환)
    port = int(os.environ.get("PORT", 8080))
    
    print(f"""
🚀 엘리트 뷰티 클리닉 AI 챗봇 서버 시작
📍 URL: http://localhost:{port}
🤖 독립형 AI 시스템: 활성화
💪 친근한 상담사 모드: ON
    """)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
