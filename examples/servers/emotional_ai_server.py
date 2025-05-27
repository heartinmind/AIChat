#!/usr/bin/env python3
"""
💖 진짜 감정을 읽는 AI - 재미와 감동이 있는 버전

사용자의 마음을 정말로 이해하고 공감하는 AI
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

app = FastAPI(title="감정을 읽는 뷰티 상담사")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    customer_id: str = "web_user"

class ChatResponse(BaseModel):
    response: str
    customer_id: str

class EmotionalAI:
    """진짜 감정을 읽고 공감하는 AI"""
    
    def __init__(self):
        # 깊은 감정 표현들
        self.deep_emotions = {
            # 그리움, 외로움
            "보고싶다": [
                "어머... 누군가 많이 그리우시나 봐요 💙",
                "그런 마음 정말 잘 알겠어요... 보고싶은 마음이 클 때가 있죠 😢",
                "아... 그리운 사람이 있으시군요. 마음이 아프시겠어요"
            ],
            "외롭다": [
                "혼자라는 느낌이 드시는군요... 정말 힘드시죠 😔",
                "외로운 마음, 저도 느껴져요. 괜찮으세요?",
                "그런 날이 있어요... 누구나 외로울 때가 있죠 💙"
            ],
            "슬프다": [
                "무슨 일이 있으셨나요? 마음이 많이 아프시겠어요 😢",
                "슬픈 일이 있으셨군요... 괜찮아지실 거예요",
                "힘든 시간을 보내고 계시는군요. 저도 마음이 아파요"
            ],
            
            # 스트레스, 화남
            "짜증나": [
                "아이고 무슨 일로 그렇게 짜증이 나셨어요? 😤",
                "오늘 하루 많이 힘드셨나 봐요! 스트레스 확 풀어야겠어요",
                "짜증날 일이 있으셨군요! 저한테 털어놓으세요"
            ],
            "화나": [
                "어머 무슨 일이 있으셨어요? 화가 많이 나시나 봐요 😠",
                "화날 일이 있으셨나 봐요! 속상하시겠어요",
                "화가 날 만한 일이 있으셨군요. 어떤 일인지 말씀해보세요"
            ],
            "스트레스": [
                "스트레스 정말 많이 받으시는군요! 😵‍💫",
                "요즘 스트레스가 심하시나 봐요. 힘드시죠?",
                "스트레스 받을 일이 많으시군요. 풀어드릴게요!"
            ],
            
            # 기쁨, 행복
            "기쁘다": [
                "와! 기쁜 일이 있으셨나 봐요! 😄 축하해요!",
                "어머 좋은 일이 있으셨군요! 저도 기뻐요 ✨",
                "기쁜 소식인가요? 들으니까 저도 행복해져요!"
            ],
            "행복하다": [
                "정말 행복해 보이세요! 😊 무슨 좋은 일이 있으셨어요?",
                "행복한 기운이 느껴져요! 저도 덩달아 기뻐요 💕",
                "행복하다니! 그 기분 오래오래 지속되면 좋겠어요"
            ],
            "신난다": [
                "우와! 정말 신나시나 봐요! 😆 뭔가 좋은 일 있으셨나요?",
                "신나는 일이 있으셨군요! 에너지가 넘쳐흘러요 ⚡",
                "신나는 기분이 여기까지 전해져요! 좋은 하루네요"
            ],
            
            # 피곤, 지침
            "피곤하다": [
                "어머 정말 피곤하시겠어요... 😴 얼마나 힘드셨을까",
                "피곤하실 때는 무리하지 마세요! 휴식이 필요해요",
                "하루 종일 고생하셨나 봐요. 푹 쉬세요!"
            ],
            "지쳤다": [
                "정말 많이 지치셨나 봐요... 😥 너무 무리하신 건 아니에요?",
                "지칠 만도 하죠! 이럴 때일수록 자기관리가 중요해요",
                "몸도 마음도 지치셨겠어요. 힐링이 필요한 시점이네요"
            ]
        }
        
        # 감정별 자연스러운 연결
        self.emotion_bridges = {
            "그리움": [
                "이럴 때 자기 자신을 더 예뻐해주는 시간이 필요해요 💄",
                "마음 아플 때일수록 셀프케어로 위로받으세요",
                "그리운 마음... 자신을 더 사랑해주는 건 어떨까요?"
            ],
            "외로움": [
                "외로울 때는 자신에게 더 잘해주세요! 뷰티케어로 힐링해요 💅",
                "혼자서도 충분히 소중한 분이에요. 자기관리로 기분 전환해봐요",
                "외로운 마음, 예쁜 자신을 만나면서 달래보세요"
            ],
            "스트레스": [
                "스트레스 받을 때는 뷰티케어가 최고예요! 😌",
                "피부도 스트레스 받잖아요. 같이 케어해드릴게요",
                "스트레스 풀기엔 역시 자기관리가 답이죠!"
            ],
            "기쁨": [
                "기쁜 날엔 더 예뻐져야죠! ✨",
                "좋은 일 있을 때 뷰티케어 받으면 기분이 더 좋아져요",
                "행복한 순간을 더 특별하게 만들어봐요!"
            ],
            "피곤": [
                "피곤할 때야말로 힐링케어가 필요해요! 🌸",
                "지친 몸과 마음을 달래드릴게요",
                "피곤한 하루, 나를 위한 시간을 가져보세요"
            ]
        }
        
        # 재미있는 반응들
        self.fun_reactions = {
            "ㅋㅋ": [
                "ㅋㅋㅋ 뭔가 재밌는 일 있으셨나요? 저도 웃음이 나네요! 😄",
                "ㅎㅎㅎ 웃음소리가 들리는 것 같아요! 기분 좋은 일 있으셨나 봐요 ✨"
            ],
            "ㅠㅠ": [
                "앗 뭔가 속상한 일이 있으셨나요? ㅠㅠ 괜찮으세요?",
                "어머 왜 울상이세요? 무슨 일인지 말씀해보세요 😢"
            ],
            "ㅗㅗ": [
                "아이고 많이 화나셨나 봐요! 😅 무슨 일로 그렇게 화가 나셨어요?",
                "어머 욕이 나올 정도로 열받으셨군요! 속상하시겠어요"
            ]
        }

    def analyze_deep_emotion(self, message: str) -> dict:
        """메시지에서 깊은 감정 분석"""
        msg = message.strip()
        
        # 감정 표현 직접 매칭
        for emotion_key, responses in self.deep_emotions.items():
            if emotion_key in msg:
                emotion_type = self._get_emotion_type(emotion_key)
                return {
                    "type": "deep_emotion",
                    "emotion": emotion_key,
                    "emotion_type": emotion_type,
                    "response": random.choice(responses),
                    "bridge": random.choice(self.emotion_bridges.get(emotion_type, []))
                }
        
        # 이모티콘/줄임말 반응
        for reaction_key, responses in self.fun_reactions.items():
            if reaction_key in msg:
                return {
                    "type": "fun_reaction",
                    "response": random.choice(responses)
                }
        
        # 기본 감정 키워드 분석
        if any(word in msg for word in ["힘들다", "우울하다", "아프다"]):
            return {
                "type": "deep_emotion",
                "emotion_type": "슬픔",
                "response": "많이 힘드시겠어요... 😔 괜찮으세요? 무슨 일인지 말씀해보세요",
                "bridge": random.choice(self.emotion_bridges["외로움"])
            }
        
        return None
    
    def _get_emotion_type(self, emotion_key: str) -> str:
        """감정 키워드를 감정 타입으로 변환"""
        emotion_map = {
            "보고싶다": "그리움",
            "외롭다": "외로움", 
            "슬프다": "슬픔",
            "짜증나": "스트레스",
            "화나": "스트레스",
            "스트레스": "스트레스",
            "기쁘다": "기쁨",
            "행복하다": "기쁨",
            "신난다": "기쁨",
            "피곤하다": "피곤",
            "지쳤다": "피곤"
        }
        return emotion_map.get(emotion_key, "일반")
    
    def generate_response(self, message: str, customer_id: str = "web_user") -> str:
        """감정을 읽고 공감하는 응답 생성"""
        
        # 깊은 감정 분석
        emotion_analysis = self.analyze_deep_emotion(message)
        
        if emotion_analysis:
            base_response = emotion_analysis["response"]
            
            # 감정에 따른 후속 제안
            if emotion_analysis["type"] == "deep_emotion":
                bridge = emotion_analysis.get("bridge", "")
                if bridge:
                    return f"{base_response}\n\n{bridge}"
                return base_response
            else:
                return base_response
        
        # 일반적인 친근한 응답
        general_responses = [
            "어떤 이야기든 편하게 해주세요! 😊",
            "오늘은 어떤 하루였나요? 들어볼게요~",
            "뭔가 하고 싶은 말씀이 있으신 것 같아요! 😌",
            "마음속 이야기를 털어놓으세요. 제가 들어드릴게요 💕",
            "어떤 기분이신지 알고 싶어요! 편하게 말씀해주세요"
        ]
        
        return random.choice(general_responses)

# AI 인스턴스 생성
emotional_ai = EmotionalAI()

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_request: ChatRequest):
    try:
        # 감정을 읽는 응답 생성
        ai_response = emotional_ai.generate_response(
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
            response="어머... 😅 제가 잠시 멈칫했네요. 다시 말씀해주실래요?",
            customer_id=chat_request.customer_id
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "감정을 읽는 뷰티 상담사",
        "version": "4.0.0 - 진짜 감정 읽기 버전",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    print(f"""
💖 감정을 읽는 뷰티 상담사 시작!
📍 URL: http://localhost:{port}
✨ 이제 진짜 마음을 읽어요!

테스트해볼 감정 표현들:
- "보고싶다" → 그리움에 공감
- "외롭다" → 외로움을 위로  
- "짜증나" → 스트레스 이해
- "기쁘다" → 함께 기뻐하기
- "ㅠㅠ" → 속상함에 공감
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
