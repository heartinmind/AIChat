#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
대화 맥락 기억 시스템
고객과의 대화 히스토리와 라포 관리
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class ConversationContext:
    """대화 맥락 정보"""
    customer_id: str
    current_mood: str = "neutral"
    topics_mentioned: List[str] = None
    rapport_level: int = 5  # 1-10 scale
    preferred_call: str = "고객님"  # 선호 호칭
    conversation_style: str = "formal"  # formal, friendly, casual
    last_interaction: str = ""
    session_start: datetime = None
    total_interactions: int = 0
    
    def __post_init__(self):
        if self.topics_mentioned is None:
            self.topics_mentioned = []
        if self.session_start is None:
            self.session_start = datetime.now()

class ConversationMemory:
    """대화 기억 관리 클래스"""
    
    def __init__(self):
        self.contexts: Dict[str, ConversationContext] = {}
        self.mood_transitions = {
            "tired": {"positive_response": "relaxed", "negative_response": "frustrated"},
            "curious": {"positive_response": "satisfied", "negative_response": "confused"},
            "dissatisfied": {"positive_response": "neutral", "negative_response": "angry"},
            "worried": {"positive_response": "relieved", "negative_response": "anxious"},
            "happy": {"positive_response": "delighted", "negative_response": "disappointed"}
        }
    
    def get_or_create_context(self, customer_id: str) -> ConversationContext:
        """고객 맥락 정보 가져오기 또는 생성"""
        if customer_id not in self.contexts:
            self.contexts[customer_id] = ConversationContext(customer_id=customer_id)
        return self.contexts[customer_id]
    
    def update_mood(self, customer_id: str, new_mood: str, response_quality: str = "positive"):
        """고객 기분 업데이트"""
        context = self.get_or_create_context(customer_id)
        
        # 기분 전환 로직
        if context.current_mood in self.mood_transitions:
            transitions = self.mood_transitions[context.current_mood]
            if response_quality in transitions:
                context.current_mood = transitions[response_quality]
            else:
                context.current_mood = new_mood
        else:
            context.current_mood = new_mood
        
        # 라포 레벨 조정
        if response_quality == "positive":
            context.rapport_level = min(10, context.rapport_level + 1)
        elif response_quality == "negative":
            context.rapport_level = max(1, context.rapport_level - 1)
    
    def add_topic(self, customer_id: str, topic: str):
        """언급된 주제 추가"""
        context = self.get_or_create_context(customer_id)
        if topic not in context.topics_mentioned:
            context.topics_mentioned.append(topic)
            # 최근 5개 주제만 유지
            if len(context.topics_mentioned) > 5:
                context.topics_mentioned = context.topics_mentioned[-5:]
    
    def update_interaction(self, customer_id: str, message: str):
        """상호작용 업데이트"""
        context = self.get_or_create_context(customer_id)
        context.last_interaction = message
        context.total_interactions += 1
        
        # 대화 스타일 학습
        if any(word in message for word in ["죄송", "부탁", "실례"]):
            context.conversation_style = "formal"
        elif any(word in message for word in ["ㅋㅋ", "ㅎㅎ", "그냥", "막"]):
            context.conversation_style = "casual"
        else:
            context.conversation_style = "friendly"
    
    def get_personalized_greeting(self, customer_id: str) -> str:
        """개인화된 인사말 생성"""
        context = self.get_or_create_context(customer_id)
        
        greetings = {
            "formal": f"안녕하세요, {context.preferred_call}! 😊",
            "friendly": f"안녕하세요! 😊 오늘도 좋은 하루 보내고 계신가요?",
            "casual": f"안녕하세요! 😄 어떻게 지내세요?"
        }
        
        base_greeting = greetings.get(context.conversation_style, greetings["friendly"])
        
        # 라포 레벨에 따른 추가 메시지
        if context.rapport_level >= 8:
            base_greeting += " 항상 저희를 찾아주셔서 감사해요! ✨"
        elif context.rapport_level >= 6:
            base_greeting += " 다시 만나뵙게 되어 반가워요!"
        
        return base_greeting
    
    def get_contextual_response_modifier(self, customer_id: str) -> Dict:
        """맥락 기반 응답 수정자 반환"""
        context = self.get_or_create_context(customer_id)
        
        return {
            "tone_adjustment": self._get_tone_adjustment(context),
            "formality_level": context.conversation_style,
            "rapport_bonus": context.rapport_level >= 7,
            "mood_consideration": context.current_mood,
            "recent_topics": context.topics_mentioned[-3:],  # 최근 3개 주제
            "preferred_call": context.preferred_call
        }
    
    def _get_tone_adjustment(self, context: ConversationContext) -> str:
        """기분에 따른 톤 조정"""
        tone_map = {
            "tired": "더욱 부드럽고 위로하는 톤",
            "frustrated": "차분하고 해결 중심적인 톤",
            "happy": "밝고 에너지 넘치는 톤",
            "worried": "안심시키고 신뢰감 주는 톤",
            "curious": "친근하고 설명적인 톤",
            "relaxed": "편안하고 자연스러운 톤"
        }
        return tone_map.get(context.current_mood, "따뜻하고 전문적인 톤")

def add_appropriate_emoji(message: str, emotion: str, rapport_level: int = 5) -> str:
    """상황별 이모지 자동 추가"""
    
    emoji_map = {
        "tired": ["😅", "💤", "🌙"],
        "happy": ["😊", "✨", "🌟", "💕"],
        "curious": ["🤔", "💡", "🔍"],
        "worried": ["😌", "💕", "🤗"],
        "dissatisfied": ["😔", "💙", "🙏"],
        "excited": ["🎉", "✨", "😄"],
        "relaxed": ["😊", "🌸", "☺️"],
        "neutral": ["😊", "✨"]
    }
    
    # 라포 레벨에 따른 이모지 개수 조정
    emoji_count = 1 if rapport_level < 6 else 2
    emojis = emoji_map.get(emotion, emoji_map["neutral"])[:emoji_count]
    
    return message + " " + "".join(emojis)

def learn_preferred_call(customer_id: str, customer_response: str, memory: ConversationMemory):
    """고객 응답에서 선호 호칭 학습"""
    
    context = memory.get_or_create_context(customer_id)
    
    # 고객이 사용하는 호칭 패턴 분석
    if "님" in customer_response and "고객님" not in customer_response:
        context.preferred_call = "님"
        context.conversation_style = "friendly"
    elif any(formal in customer_response for formal in ["존댓말", "정중", "공손"]):
        context.preferred_call = "고객님"
        context.conversation_style = "formal"
    elif any(casual in customer_response for casual in ["편하게", "자연스럽게", "친근"]):
        context.preferred_call = "씨" if "씨" in customer_response else "님"
        context.conversation_style = "casual"

def generate_memory_enhanced_response(
    customer_id: str, 
    message: str, 
    base_response: str, 
    emotion: str,
    memory: ConversationMemory
) -> str:
    """기억 기반 향상된 응답 생성"""
    
    # 맥락 업데이트
    memory.update_interaction(customer_id, message)
    
    # 주제 추출 및 추가
    topics = extract_topics_from_message(message)
    for topic in topics:
        memory.add_topic(customer_id, topic)
    
    # 맥락 기반 수정자 가져오기
    modifier = memory.get_contextual_response_modifier(customer_id)
    context = memory.get_or_create_context(customer_id)
    
    # 응답 개인화
    personalized_response = base_response
    
    # 호칭 교체
    if "고객님" in personalized_response:
        personalized_response = personalized_response.replace("고객님", context.preferred_call)
    
    # 이전 주제 참조
    if modifier["recent_topics"] and any(topic in message for topic in modifier["recent_topics"]):
        personalized_response = "아, 전에 말씀하신 " + modifier["recent_topics"][-1] + " 관련해서 더 궁금한 점이 있으신가요? " + personalized_response
    
    # 라포 보너스
    if modifier["rapport_bonus"]:
        rapport_phrases = [
            "항상 좋은 질문 해주시네요! ",
            "역시 센스가 좋으시네요! ",
            "정말 꼼꼼하게 생각해주시는군요! "
        ]
        import random
        personalized_response = random.choice(rapport_phrases) + personalized_response
    
    # 이모지 추가
    final_response = add_appropriate_emoji(
        personalized_response, 
        emotion, 
        context.rapport_level
    )
    
    return final_response

def extract_topics_from_message(message: str) -> List[str]:
    """메시지에서 주제 추출"""
    
    topic_keywords = {
        "피부관리": ["피부", "관리", "케어", "스킨"],
        "주름": ["주름", "라인", "노화"],
        "시술": ["시술", "치료", "트리트먼트"],
        "예약": ["예약", "스케줄", "시간"],
        "가격": ["가격", "비용", "할인", "프로모션"],
        "부작용": ["부작용", "위험", "안전"],
        "효과": ["효과", "결과", "변화"]
    }
    
    detected_topics = []
    for topic, keywords in topic_keywords.items():
        if any(keyword in message for keyword in keywords):
            detected_topics.append(topic)
    
    return detected_topics

# 테스트 함수
def test_conversation_memory():
    """대화 기억 시스템 테스트"""
    
    print("🧠 대화 기억 시스템 테스트")
    print("=" * 50)
    
    memory = ConversationMemory()
    customer_id = "test_customer_001"
    
    # 시나리오 1: 첫 대화
    print("\n📝 시나리오 1: 첫 대화")
    message1 = "아우 질만 들었네"
    base_response1 = "많이 지치셨나 봐요! 저희 클리닉에서 힐링 시간 가져보세요."
    
    enhanced_response1 = generate_memory_enhanced_response(
        customer_id, message1, base_response1, "tired", memory
    )
    print(f"👤 고객: {message1}")
    print(f"🤖 지수: {enhanced_response1}")
    
    # 시나리오 2: 두 번째 대화 (맥락 기억)
    print("\n📝 시나리오 2: 두 번째 대화")
    message2 = "피부 관리는 어떤 게 좋을까요?"
    base_response2 = "피부 타입에 맞는 관리를 추천해드릴게요."
    
    enhanced_response2 = generate_memory_enhanced_response(
        customer_id, message2, base_response2, "curious", memory
    )
    print(f"👤 고객: {message2}")
    print(f"🤖 지수: {enhanced_response2}")
    
    # 맥락 정보 출력
    context = memory.get_or_create_context(customer_id)
    print(f"\n📊 현재 맥락 정보:")
    print(f"   기분: {context.current_mood}")
    print(f"   라포 레벨: {context.rapport_level}/10")
    print(f"   언급된 주제: {context.topics_mentioned}")
    print(f"   대화 스타일: {context.conversation_style}")
    print(f"   선호 호칭: {context.preferred_call}")

if __name__ == "__main__":
    test_conversation_memory() 