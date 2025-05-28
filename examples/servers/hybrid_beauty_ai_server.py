#!/usr/bin/env python3
"""
🏥💬 하이브리드 뷰티 클리닉 AI 서버

병원 관련 질문 → RAG 기반 정확한 정보
일상 대화 → 감정 공감 AI
"""

import os
import json
import random
import re
from datetime import datetime
from typing import Dict, List, Tuple
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="하이브리드 뷰티 클리닉 AI")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    customer_id: str = "web_user"

class ChatResponse(BaseModel):
    response: str
    customer_id: str
    response_type: str = "general"  # "medical", "emotional", "general"

class HybridBeautyAI:
    """병원 정보 + 감정 공감 하이브리드 AI"""
    
    def __init__(self):
        # 뷰티/의료 관련 키워드
        self.medical_keywords = {
            "시술": ["보톡스", "필러", "레이저", "리프팅", "피부관리", "여드름", "기미", "주름"],
            "가격": ["비용", "얼마", "가격", "금액", "할인", "이벤트", "프로모션"],
            "예약": ["예약", "방문", "상담", "시간", "언제", "스케줄"],
            "정보": ["효과", "부작용", "기간", "회복", "관리", "추천", "어떤"],
            "부위": ["이마", "미간", "눈가", "팔자", "볼", "턱", "목"],
        }
        
        # 뷰티 클리닉 정보 (RAG 대신 간단한 DB)
        self.clinic_info = {
            "보톡스": {
                "가격": {
                    "이마": "15만원",
                    "미간": "10만원", 
                    "눈가": "15만원",
                    "전체": "35만원 (패키지 할인)"
                },
                "설명": "근육의 움직임을 일시적으로 마비시켜 주름을 개선하는 시술",
                "효과기간": "4-6개월",
                "시술시간": "10-15분"
            },
            "필러": {
                "가격": {
                    "팔자주름": "40만원",
                    "볼": "60만원",
                    "턱": "50만원",
                    "입술": "35만원"
                },
                "설명": "히알루론산을 주입하여 볼륨을 채우고 주름을 개선하는 시술",
                "효과기간": "12-18개월",
                "시술시간": "20-30분"
            },
            "레이저": {
                "가격": {
                    "기미레이저": "회당 20만원",
                    "모공레이저": "회당 30만원",
                    "리프팅레이저": "회당 50만원"
                },
                "설명": "레이저를 이용한 피부 개선 시술",
                "효과": "즉시 ~ 1개월 후 최대 효과",
                "시술시간": "30-60분"
            },
            "영업시간": "평일 10:00-20:00, 토요일 10:00-17:00, 일요일 휴무",
            "위치": "서울시 강남구 청담동 엘리트타워 5층",
            "예약": "전화: 02-1234-5678, 카톡: elitebeauty"
        }
        
        # 감정 응답 (기존 감정 AI 부분)
        self.emotion_responses = {
            "피곤": [
                "정말 피곤하시겠어요... 😔 푹 쉬셔야겠어요",
                "하루 종일 고생하셨나봐요. 피부도 피곤하면 칙칙해져요",
                "피곤할 때는 충분한 수면이 최고의 피부 관리예요!"
            ],
            "스트레스": [
                "스트레스가 많으시군요 😣 피부에도 안 좋아요",
                "스트레스는 피부의 적이에요! 관리가 필요하시겠어요",
                "힘든 일이 있으셨나봐요. 이럴 때일수록 자기관리가 중요해요"
            ],
            "기쁘": [
                "와! 좋은 일 있으셨나봐요! 😊",
                "기쁜 마음이 느껴져요! 피부도 빛나실 것 같아요 ✨",
                "행복한 기운이 여기까지 전해져요!"
            ]
        }
    
    def classify_intent(self, message: str) -> str:
        """메시지 의도 분류: medical, emotional, general"""
        msg_lower = message.lower()
        
        # 의료/뷰티 관련 체크
        medical_score = 0
        for category, keywords in self.medical_keywords.items():
            for keyword in keywords:
                if keyword in msg_lower:
                    medical_score += 1
        
        # 감정 관련 체크
        emotion_keywords = ["피곤", "힘들", "우울", "기쁘", "행복", "스트레스", 
                          "외로", "슬프", "화나", "짜증"]
        emotion_score = sum(1 for keyword in emotion_keywords if keyword in msg_lower)
        
        if medical_score > 0:
            return "medical"
        elif emotion_score > 0:
            return "emotional"
        else:
            return "general"
    
    def get_medical_response(self, message: str) -> str:
        """병원/시술 관련 응답 생성"""
        msg_lower = message.lower()
        
        # 보톡스 관련
        if "보톡스" in msg_lower:
            if any(word in msg_lower for word in ["가격", "비용", "얼마"]):
                prices = self.clinic_info["보톡스"]["가격"]
                response = "💉 보톡스 가격 안내\n\n"
                for part, price in prices.items():
                    response += f"• {part}: {price}\n"
                response += f"\n⏰ 시술시간: {self.clinic_info['보톡스']['시술시간']}"
                response += f"\n✨ 효과기간: {self.clinic_info['보톡스']['효과기간']}"
                response += "\n\n📞 자세한 상담은 예약 후 방문해주세요!"
                return response
            else:
                return f"보톡스는 {self.clinic_info['보톡스']['설명']}입니다. 효과는 {self.clinic_info['보톡스']['효과기간']} 지속되며, 시술 시간은 {self.clinic_info['보톡스']['시술시간']} 정도예요! 😊"
        
        # 필러 관련
        elif "필러" in msg_lower:
            if any(word in msg_lower for word in ["가격", "비용", "얼마"]):
                prices = self.clinic_info["필러"]["가격"]
                response = "💧 필러 가격 안내\n\n"
                for part, price in prices.items():
                    response += f"• {part}: {price}\n"
                response += f"\n⏰ 시술시간: {self.clinic_info['필러']['시술시간']}"
                response += f"\n✨ 효과기간: {self.clinic_info['필러']['효과기간']}"
                return response
            else:
                return f"필러는 {self.clinic_info['필러']['설명']}입니다. 효과는 {self.clinic_info['필러']['효과기간']} 정도 유지돼요!"
        
        # 레이저 관련
        elif "레이저" in msg_lower:
            prices = self.clinic_info["레이저"]["가격"]
            response = "🔬 레이저 시술 안내\n\n"
            for treatment, price in prices.items():
                response += f"• {treatment}: {price}\n"
            response += f"\n{self.clinic_info['레이저']['설명']}"
            return response
        
        # 예약 관련
        elif any(word in msg_lower for word in ["예약", "상담", "방문"]):
            return f"📅 예약 안내\n\n영업시간: {self.clinic_info['영업시간']}\n위치: {self.clinic_info['위치']}\n{self.clinic_info['예약']}\n\n편하신 시간에 연락 주세요! 😊"
        
        # 영업시간
        elif any(word in msg_lower for word in ["영업", "시간", "언제"]):
            return f"⏰ 영업시간 안내\n\n{self.clinic_info['영업시간']}\n\n토요일은 5시까지, 일요일은 휴무입니다!"
        
        # 위치
        elif any(word in msg_lower for word in ["위치", "어디", "찾아"]):
            return f"📍 오시는 길\n\n{self.clinic_info['위치']}\n\n지하철 7호선 청담역 3번 출구에서 도보 5분이에요!"
        
        # 일반 의료 질문
        else:
            return "어떤 시술에 대해 궁금하신가요? 보톡스, 필러, 레이저 등 다양한 시술을 제공하고 있어요! 💝"
    
    def get_emotional_response(self, message: str) -> str:
        """감정 관련 응답 생성"""
        msg_lower = message.lower()
        
        for emotion, responses in self.emotion_responses.items():
            if emotion in msg_lower:
                base_response = random.choice(responses)
                # 뷰티 관련 조언 추가
                beauty_tips = [
                    "\n\n💆‍♀️ 이럴 때 페이셜 마사지 받으시면 기분도 좋아지고 피부도 좋아져요!",
                    "\n\n✨ 피부 관리로 기분 전환해보는 건 어떠세요?",
                    "\n\n🌸 셀프케어로 스스로에게 선물을 주세요!"
                ]
                return base_response + random.choice(beauty_tips)
        
        return "마음이 복잡하신가 봐요. 어떤 이야기든 들어드릴게요 💕"
    
    def get_general_response(self, message: str) -> str:
        """일반 대화 응답"""
        msg_lower = message.lower()
        
        if any(word in msg_lower for word in ["안녕", "하이", "헬로"]):
            return "안녕하세요! 엘리트 뷰티 클리닉입니다 😊\n무엇을 도와드릴까요?"
        elif "고마" in msg_lower or "감사" in msg_lower:
            return "별말씀을요! 도움이 되었다니 기뻐요 💕"
        else:
            suggestions = [
                "오늘은 어떤 도움이 필요하신가요? 시술 상담이나 예약 도와드릴게요!",
                "피부 고민이 있으시면 편하게 말씀해주세요 😊",
                "저희 클리닉의 시술이나 가격이 궁금하신가요?",
                "무엇이든 물어보세요! 뷰티 상담부터 예약까지 도와드려요 ✨"
            ]
            return random.choice(suggestions)
    
    def generate_response(self, message: str, customer_id: str) -> Tuple[str, str]:
        """하이브리드 응답 생성"""
        # 의도 분류
        intent = self.classify_intent(message)
        
        # 의도에 따른 응답 생성
        if intent == "medical":
            response = self.get_medical_response(message)
        elif intent == "emotional":
            response = self.get_emotional_response(message)
        else:
            response = self.get_general_response(message)
        
        return response, intent

# AI 인스턴스 생성
hybrid_ai = HybridBeautyAI()

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_request: ChatRequest):
    try:
        # 하이브리드 응답 생성
        response, response_type = hybrid_ai.generate_response(
            chat_request.message,
            chat_request.customer_id
        )
        
        return ChatResponse(
            response=response,
            customer_id=chat_request.customer_id,
            response_type=response_type
        )
        
    except Exception as e:
        print(f"응답 생성 오류: {e}")
        return ChatResponse(
            response="죄송해요, 잠시 문제가 발생했어요. 다시 한 번 말씀해주실래요? 😅",
            customer_id=chat_request.customer_id,
            response_type="error"
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "하이브리드 뷰티 클리닉 AI",
        "version": "1.0.0",
        "features": ["medical_info", "emotional_support", "general_chat"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/intents")
async def get_supported_intents():
    """지원하는 의도 목록 반환 (디버깅용)"""
    return {
        "medical": list(hybrid_ai.medical_keywords.keys()),
        "emotional": list(hybrid_ai.emotion_responses.keys()),
        "examples": {
            "medical": ["보톡스 가격이 얼마예요?", "필러 효과가 얼마나 가나요?", "예약하고 싶어요"],
            "emotional": ["오늘 너무 피곤해", "스트레스 받아", "기분이 좋아!"],
            "general": ["안녕하세요", "감사합니다", "뭘 도와주시나요?"]
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    print(f"""
🏥💬 하이브리드 뷰티 클리닉 AI 시작!
📍 URL: http://localhost:{port}
✨ 기능: 의료정보 + 감정공감 + 일반대화

테스트 예시:
📌 의료: "보톡스 가격이 얼마예요?"
📌 감정: "오늘 너무 피곤해"
📌 일반: "안녕하세요"
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
