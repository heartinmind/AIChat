#!/usr/bin/env python3
"""
🤖 ChatGPT 스타일 뷰티 전문 AI

감정팔이 그만하고 제대로 된 답변을 하는 AI
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

app = FastAPI(title="뷰티 전문 AI 상담사")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    customer_id: str = "web_user"

class ChatResponse(BaseModel):
    response: str
    customer_id: str

class BeautyExpertAI:
    """ChatGPT 스타일의 뷰티 전문 AI"""
    
    def __init__(self):
        # 시술별 전문 정보
        self.treatments = {
            "보톡스": {
                "description": "보툴리눔 톡신을 주입하여 근육의 움직임을 일시적으로 제한해 주름을 개선하는 시술",
                "areas": ["이마", "눈가", "미간", "턱"],
                "price_range": "15만원~30만원 (부위별)",
                "duration": "15-30분",
                "effects": "시술 후 3-7일 후부터 효과 나타남, 3-6개월 지속",
                "pros": ["즉각적 효과", "시술 시간 짧음", "일상생활 바로 가능"],
                "cons": ["일시적 효과", "반복 시술 필요", "개인차 존재"],
                "care": ["시술 후 4시간 눕지 말 것", "24시간 사우나 금지", "1주일간 음주 금지"]
            },
            "필러": {
                "description": "히알루론산 등을 주입하여 볼륨을 채우고 윤곽을 개선하는 시술",
                "areas": ["볼", "입술", "코", "턱", "이마"],
                "price_range": "30만원~80만원 (부위/양에 따라)",
                "duration": "30-60분",
                "effects": "즉시 효과 확인 가능, 6개월~2년 지속",
                "pros": ["즉각적 볼륨 개선", "자연스러운 결과", "긴 지속 기간"],
                "cons": ["부기 가능", "비용 부담", "숙련된 의사 필요"],
                "care": ["2-3일간 부기 가능", "얼음찜질 권장", "딱딱한 음식 피하기"]
            },
            "레이저토닝": {
                "description": "레이저를 이용해 멜라닌 색소를 분해하여 색소침착을 개선하는 시술",
                "areas": ["전체 얼굴", "목", "손등"],
                "price_range": "10만원~20만원 (1회)",
                "duration": "20-30분",
                "effects": "5-10회 시술 후 개선 효과, 지속적 관리 필요",
                "pros": ["색소침착 개선", "피부톤 균일화", "모공 개선"],
                "cons": ["여러 번 시술 필요", "일시적 홍조", "자외선 차단 필수"],
                "care": ["시술 후 자외선 차단", "보습 관리", "각질 제거 금지"]
            },
            "하이드라페이셜": {
                "description": "특수 장비로 각질 제거, 모공 청소, 수분 공급을 동시에 하는 시술",
                "areas": ["전체 얼굴"],
                "price_range": "15만원~25만원 (1회)",
                "duration": "45-60분",
                "effects": "즉시 피부 개선 효과, 월 1-2회 권장",
                "pros": ["즉각적 효과", "모든 피부 타입 가능", "다운타임 없음"],
                "cons": ["지속 기간 짧음", "정기적 관리 필요"],
                "care": ["시술 후 24시간 화장 자제", "충분한 수분 공급"]
            }
        }
        
        # 피부 고민별 추천
        self.skin_concerns = {
            "주름": ["보톡스", "필러"],
            "색소침착": ["레이저토닝", "화학적필링"],
            "모공": ["하이드라페이셜", "레이저토닝"],
            "여드름": ["아쿠아필", "LED광치료"],
            "탄력": ["울쎄라", "써마지"],
            "볼륨": ["필러", "실리프팅"]
        }

    def analyze_query(self, message: str) -> dict:
        """사용자 질문 분석 및 카테고리 분류"""
        msg = message.lower().strip()
        
        # 구체적인 시술 문의
        for treatment_name in self.treatments.keys():
            if treatment_name in msg:
                return {
                    "type": "treatment_specific",
                    "treatment": treatment_name,
                    "query_type": self._get_query_type(msg)
                }
        
        # 피부 고민 상담
        for concern in self.skin_concerns.keys():
            if concern in msg:
                return {
                    "type": "skin_concern",
                    "concern": concern
                }
        
        # 일반 문의 키워드
        if any(keyword in msg for keyword in ["가격", "비용", "얼마"]):
            return {"type": "price_inquiry"}
        
        if any(keyword in msg for keyword in ["예약", "시간", "언제"]):
            return {"type": "booking_inquiry"}
        
        if any(keyword in msg for keyword in ["추천", "좋은", "어떤"]):
            return {"type": "recommendation_request"}
        
        # 일반 대화
        return {"type": "general_chat"}
    
    def _get_query_type(self, message: str) -> str:
        """시술 관련 질문 유형 분석"""
        if any(word in message for word in ["가격", "비용", "얼마"]):
            return "price"
        elif any(word in message for word in ["효과", "결과", "어떤"]):
            return "effects"
        elif any(word in message for word in ["아픈", "아프", "통증"]):
            return "pain"
        elif any(word in message for word in ["관리", "주의", "케어"]):
            return "aftercare"
        else:
            return "general"
    
    def generate_treatment_info(self, treatment: str, query_type: str = "general") -> str:
        """시술 정보 생성"""
        if treatment not in self.treatments:
            return "죄송합니다. 해당 시술에 대한 정보를 찾을 수 없습니다."
        
        info = self.treatments[treatment]
        
        if query_type == "price":
            return f"""💰 **{treatment} 가격 정보**

📋 **비용**: {info['price_range']}
⏰ **시술 시간**: {info['duration']}
📍 **시술 부위**: {', '.join(info['areas'])}

💡 **가격은 시술 부위와 범위에 따라 달라질 수 있습니다.**
정확한 견적은 상담을 통해 안내해드립니다!"""

        elif query_type == "effects":
            return f"""✨ **{treatment} 효과 정보**

📝 **시술 원리**: {info['description']}
⏱️ **효과 지속**: {info['effects']}

👍 **장점**:
{chr(10).join(f"• {pro}" for pro in info['pros'])}

⚠️ **고려사항**:
{chr(10).join(f"• {con}" for con in info['cons'])}"""

        elif query_type == "aftercare":
            return f"""🔧 **{treatment} 시술 후 관리법**

📋 **주의사항**:
{chr(10).join(f"• {care}" for care in info['care'])}

💡 **관리 팁**: 시술 후 관리가 결과에 큰 영향을 미치니 꼭 지켜주세요!"""

        else:  # general
            return f"""💎 **{treatment} 시술 정보**

📝 **개요**: {info['description']}
📍 **시술 부위**: {', '.join(info['areas'])}
💰 **가격대**: {info['price_range']}
⏰ **시술 시간**: {info['duration']}
⏱️ **효과**: {info['effects']}

더 자세한 정보나 상담을 원하시면 말씀해주세요! 😊"""

    def generate_recommendation(self, concern: str) -> str:
        """피부 고민별 추천"""
        if concern not in self.skin_concerns:
            return "어떤 피부 고민이 있으신지 더 자세히 말씀해주세요!"
        
        recommended = self.skin_concerns[concern]
        
        response = f"💡 **{concern} 개선 추천 시술**\n\n"
        
        for i, treatment in enumerate(recommended, 1):
            if treatment in self.treatments:
                info = self.treatments[treatment]
                response += f"{i}. **{treatment}**\n"
                response += f"   • {info['description']}\n"
                response += f"   • 가격: {info['price_range']}\n\n"
        
        response += "어떤 시술에 대해 더 자세히 알고 싶으신가요? 😊"
        return response

    def generate_response(self, message: str, customer_id: str = "web_user") -> str:
        """ChatGPT 스타일 응답 생성"""
        
        analysis = self.analyze_query(message)
        
        if analysis["type"] == "treatment_specific":
            return self.generate_treatment_info(
                analysis["treatment"], 
                analysis["query_type"]
            )
        
        elif analysis["type"] == "skin_concern":
            return self.generate_recommendation(analysis["concern"])
        
        elif analysis["type"] == "price_inquiry":
            return """💰 **시술 가격 안내**

주요 시술 가격표:
• 보톡스: 15만원~30만원 (부위별)
• 필러: 30만원~80만원 (부위/양별)  
• 레이저토닝: 10만원~20만원 (1회)
• 하이드라페이셜: 15만원~25만원 (1회)

구체적인 시술명을 말씀해주시면 더 자세한 가격을 안내해드릴게요! 😊"""

        elif analysis["type"] == "booking_inquiry":
            return """📅 **예약 안내**

**운영시간**:
• 평일: 오전 10시 ~ 오후 8시
• 토요일: 오전 10시 ~ 오후 6시
• 일요일: 휴무

**예약 방법**:
• 전화: 02-1234-5678
• 온라인 예약: 홈페이지 또는 앱

원하시는 시술을 먼저 정하시고 예약하시면 더 정확한 상담이 가능합니다! ✨"""

        elif analysis["type"] == "recommendation_request":
            return """💡 **맞춤 추천을 위해 알려주세요**

어떤 부분이 가장 신경 쓰이시나요?
• 주름 (이마, 눈가, 입가)
• 색소침착 (기미, 잡티)  
• 모공 (넓어진 모공, 블랙헤드)
• 여드름 (성인 여드름, 흉터)
• 탄력 (처진 피부, 이중턱)
• 볼륨 (꺼진 볼, 납작한 코)

구체적인 고민을 말씀해주시면 최적의 시술을 추천해드릴게요! 😊"""

        else:  # general_chat
            # 간단한 친근한 응답
            if any(greet in message.lower() for greet in ["안녕", "hi", "hello"]):
                return "안녕하세요! 뷰티 시술 상담이 필요하시면 언제든 말씀해주세요! 😊"
            
            elif any(word in message.lower() for word in ["고마워", "감사", "thanks"]):
                return "천만에요! 더 궁금한 게 있으시면 언제든 물어보세요! ✨"
            
            else:
                return """뷰티 시술에 관한 어떤 질문이든 도움드릴게요! 😊

**문의 가능한 내용**:
• 시술 정보 (보톡스, 필러, 레이저 등)
• 가격 문의
• 효과 및 후기
• 예약 안내
• 시술 후 관리법

구체적으로 어떤 도움이 필요하신가요?"""

# AI 인스턴스 생성
beauty_expert_ai = BeautyExpertAI()

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_request: ChatRequest):
    try:
        # ChatGPT 스타일 응답 생성
        ai_response = beauty_expert_ai.generate_response(
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
            response="죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.",
            customer_id=chat_request.customer_id
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "뷰티 전문 AI 상담사",
        "version": "5.0.0 - ChatGPT 스타일",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    print(f"""
🤖 뷰티 전문 AI 상담사 (ChatGPT 스타일)
📍 URL: http://localhost:{port}
✨ 이제 제대로 된 전문 상담을 해드려요!

테스트해볼 질문들:
- "보톡스" → 전문적인 시술 정보
- "주름 고민" → 맞춤 시술 추천  
- "가격 알려줘" → 상세 가격 안내
- "예약하고 싶어" → 예약 방법 안내
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
