#!/usr/bin/env python3
"""
🤗 진짜 친근한 AI 응답기 - 완전히 새로운 버전

사용자의 감정과 상황에 진짜로 공감하는 AI
"""

import os
import json
import random
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="진짜 친근한 뷰티 상담사")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    customer_id: str = "web_user"

class ChatResponse(BaseModel):
    response: str
    customer_id: str

class SuperFriendlyAI:
    """진짜 친근한 AI 상담사"""
    
    def __init__(self):
        # 자연스러운 반응들
        self.reactions = {
            # 한숨, 피곤함
            "아우": [
                "아이고 😅 많이 피곤하시나 봐요!",
                "하루 고생 많으셨어요~ 힘드시죠?",
                "어머 무슨 일 있으셨나요? 😊"
            ],
            
            # 의문, 당황
            "뭐야": [
                "어? 뭔가 이상한가요? 😄",
                "아 깜짝이야! 무슨 일이세요? ㅎㅎ",
                "어머 어떻게 된 거예요? 😊"
            ],
            
            # 웃음
            "ㅋㅋ": [
                "ㅎㅎㅎ 뭔가 재밌는 일 있으셨나요? 😄",
                "아 웃으시네요! 좋은 일 있으셨나 봐요 ✨",
                "ㅋㅋㅋ 기분 좋아 보이셔서 저도 기뻐요! 😊"
            ],
            
            # 짧은 반응들
            "네": [
                "네네! 뭐든 말씀하세요 😊",
                "네! 듣고 있어요~ 편하게 말씀해주세요!",
                "넵! 어떤 도움이 필요하신가요?"
            ],
            
            # 문의
            "안녕": [
                "안녕하세요! 😊 반가워요!",
                "안녕하세요~ 오늘 어떤 일로 오셨어요?",
                "네 안녕하세요! 편하게 대화해요 ✨"
            ]
        }
        
        # 상황별 자연스러운 연결
        self.natural_transitions = {
            "피곤함": [
                "이럴 때일수록 셀프케어가 중요한데요!",
                "스트레스 받으시면 피부에도 영향 있잖아요 😅",
                "힐링이 필요한 시점인 것 같아요!"
            ],
            "호기심": [
                "궁금한 게 많으시군요! 뭐든 물어보세요~",
                "설명해드릴게요! 어떤 부분이 궁금하신가요?",
                "이것저것 알아보고 계시는군요 😊"
            ],
            "기분좋음": [
                "오늘 좋은 하루 보내고 계시는 것 같아요!",
                "기분 좋을 때 뷰티 케어 받으면 더 좋아져요 ✨",
                "좋은 에너지가 느껴져요! 😄"
            ]
        }
        
        # 시술 정보
        self.treatments = {
            "보톡스": "💉 보톡스 - 주름 개선의 대표 시술! 자연스러운 효과로 인기 만점이에요 ✨",
            "필러": "💎 필러 - 볼륨업과 윤곽 개선! 즉각적인 효과를 볼 수 있어요 😍",
            "레이저": "⚡ 레이저 - 색소침착과 모공 개선! 깨끗한 피부로 변신해요 🌟"
        }

    def analyze_message(self, message: str) -> dict:
        """메시지 분석하여 감정과 의도 파악"""
        msg = message.strip().lower()
        
        # 직접 매칭되는 키워드들
        for keyword, responses in self.reactions.items():
            if keyword in msg:
                return {
                    "type": "direct_reaction",
                    "keyword": keyword,
                    "emotion": self._get_emotion_from_keyword(keyword),
                    "response": random.choice(responses)
                }
        
        # 감정 키워드 분석
        if any(word in msg for word in ["피곤", "힘들", "지쳐", "스트레스"]):
            return {
                "type": "emotion",
                "emotion": "피곤함",
                "response": "정말 고생 많으셨겠어요! 😅 " + random.choice(self.natural_transitions["피곤함"])
            }
        
        if any(word in msg for word in ["궁금", "뭐", "어떻게", "연동"]):
            return {
                "type": "emotion", 
                "emotion": "호기심",
                "response": "오, 궁금한 게 있으시군요! 😊 " + random.choice(self.natural_transitions["호기심"])
            }
        
        if any(word in msg for word in ["시술", "보톡스", "필러", "레이저", "추천"]):
            return {
                "type": "treatment_inquiry",
                "response": self._generate_treatment_response(msg)
            }
        
        # 기본 친근한 응답
        friendly_responses = [
            "네네! 어떤 얘기든 편하게 해주세요 😊",
            "오호 그렇군요! 더 자세히 말씀해주세요~",
            "아 그래요? 흥미롭네요! 😄",
            "네! 듣고 있어요~ 뭐든 말씀하세요!",
            "어머 그렇구나! 어떤 도움이 필요하세요?"
        ]
        
        return {
            "type": "general",
            "response": random.choice(friendly_responses)
        }
    
    def _get_emotion_from_keyword(self, keyword: str) -> str:
        emotion_map = {
            "아우": "피곤함",
            "뭐야": "호기심", 
            "ㅋㅋ": "기분좋음",
            "네": "중립",
            "안녕": "인사"
        }
        return emotion_map.get(keyword, "중립")
    
    def _generate_treatment_response(self, message: str) -> str:
        """시술 관련 친근한 응답 생성"""
        responses = [
            "오! 시술에 관심 있으시군요! 😍",
            "어떤 고민이 있으신지 듣고 싶어요!",
            "피부 고민 상담해드릴게요~ 편하게 말씀하세요!"
        ]
        
        base_response = random.choice(responses)
        
        # 구체적 시술 언급 시
        for treatment, description in self.treatments.items():
            if treatment in message:
                return f"{base_response}\n\n{description}"
        
        return f"{base_response}\n\n어떤 부분이 가장 신경 쓰이시나요? 주름? 색소침착? 모공? 😊"
    
    def generate_response(self, message: str, customer_id: str = "web_user") -> str:
        """진짜 친근한 응답 생성"""
        
        analysis = self.analyze_message(message)
        base_response = analysis["response"]
        
        # 상황에 맞는 후속 제안 추가
        if analysis.get("emotion") == "피곤함":
            follow_up = "\n\n스트레스 풀 수 있는 힐링 케어 어때요? 😌"
            return base_response + follow_up
        
        elif analysis.get("emotion") == "호기심":
            follow_up = "\n\n뭐든 물어보세요! 궁금한 거 다 알려드릴게요 ✨"
            return base_response + follow_up
        
        elif analysis.get("emotion") == "기분좋음":
            follow_up = "\n\n좋은 기분일 때 뷰티 케어 받으면 더 좋아져요! 😄"
            return base_response + follow_up
        
        # 기본적으로 친근한 마무리
        if analysis["type"] == "general":
            endings = [
                "\n\n저희가 도와드릴 수 있는 건 뭐든 말씀하세요! 💕",
                "\n\n편하게 대화해요~ 어떤 이야기든 좋아요! 😊",
                "\n\n뭐가 필요하신지 천천히 말씀해주세요! ✨"
            ]
            return base_response + random.choice(endings)
        
        return base_response

# AI 인스턴스 생성
super_friendly_ai = SuperFriendlyAI()

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_request: ChatRequest):
    try:
        # 진짜 친근한 응답 생성
        ai_response = super_friendly_ai.generate_response(
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
            response="어머! 😅 잠시 문제가 생겼어요. 다시 말씀해주실래요?",
            customer_id=chat_request.customer_id
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "진짜 친근한 뷰티 상담사",
        "version": "3.0.0 - 완전 친근한 버전",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    print(f"""
🤗 진짜 친근한 뷰티 상담사 시작!
📍 URL: http://localhost:{port}
✨ 이제 정말 자연스럽게 대화해요!

테스트해볼 문장들:
- "아우" → 진짜 공감하는 응답
- "뭐야" → 자연스러운 반응  
- "ㅋㅋ" → 함께 웃어주는 응답
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
