#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고객 감정/의도 분석 모듈
자연스러운 대화를 위한 감정 인식 시스템
"""

import re
from typing import Dict, List, Tuple

def analyze_customer_emotion(message: str) -> dict:
    """고객 감정/의도 분석"""
    emotions = {
        "tired": ["질만", "피곤", "지쳐", "힘들어", "스트레스"],
        "curious": ["연동", "어떻게", "시스템", "방법"],
        "dissatisfied": ["별루", "아쉬워", "기계적", "로봇"],
        "happy": ["좋아", "만족", "감사", "최고"],
        "worried": ["걱정", "괜찮나", "안전한가", "부작용"]
    }
    
    detected_emotions = []
    for emotion, keywords in emotions.items():
        if any(keyword in message for keyword in keywords):
            detected_emotions.append(emotion)
    
    return {
        "primary_emotion": detected_emotions[0] if detected_emotions else "neutral",
        "all_emotions": detected_emotions,
        "confidence": len(detected_emotions) / len(emotions)
    }

def analyze_conversation_context(message: str) -> dict:
    """대화 맥락 분석 - 고객이 무엇을 원하는지 파악"""
    
    contexts = {
        "greeting": ["안녕", "처음", "반가워", "hello", "hi"],
        "technical_inquiry": ["연동", "시스템", "어떻게", "작동", "기능"],
        "complaint": ["불만", "별루", "아쉬워", "문제", "이상해"],
        "beauty_concern": ["주름", "피부", "시술", "관리", "뷰티"],
        "booking_intent": ["예약", "언제", "시간", "가능", "스케줄"],
        "price_inquiry": ["가격", "비용", "얼마", "할인", "프로모션"],
        "casual_chat": ["질만", "피곤", "오늘", "날씨", "그냥"]
    }
    
    detected_contexts = []
    for context, keywords in contexts.items():
        if any(keyword in message for keyword in keywords):
            detected_contexts.append(context)
    
    return {
        "primary_context": detected_contexts[0] if detected_contexts else "general",
        "all_contexts": detected_contexts,
        "is_beauty_related": "beauty_concern" in detected_contexts or "booking_intent" in detected_contexts
    }

def get_response_strategy(emotion: str, context: str) -> dict:
    """감정과 맥락에 따른 응답 전략 제안"""
    
    strategies = {
        ("tired", "casual_chat"): {
            "approach": "empathy_first",
            "tone": "warm_caring",
            "suggestion": "힐링 서비스 자연스럽게 제안"
        },
        ("curious", "technical_inquiry"): {
            "approach": "informative_friendly",
            "tone": "helpful_professional",
            "suggestion": "기술 설명 후 서비스 소개"
        },
        ("dissatisfied", "complaint"): {
            "approach": "apologetic_solution",
            "tone": "understanding_proactive",
            "suggestion": "문제 해결 후 개선된 서비스 제안"
        },
        ("happy", "beauty_concern"): {
            "approach": "enthusiastic_supportive",
            "tone": "positive_encouraging",
            "suggestion": "맞춤 시술 적극 추천"
        },
        ("worried", "beauty_concern"): {
            "approach": "reassuring_detailed",
            "tone": "calm_professional",
            "suggestion": "안전성 설명 후 단계별 안내"
        }
    }
    
    key = (emotion, context)
    if key in strategies:
        return strategies[key]
    
    # 기본 전략
    return {
        "approach": "friendly_adaptive",
        "tone": "warm_professional",
        "suggestion": "고객 상황에 맞춰 자연스럽게 대응"
    }

def generate_conversation_insights(message: str) -> dict:
    """종합적인 대화 인사이트 생성"""
    
    emotion_analysis = analyze_customer_emotion(message)
    context_analysis = analyze_conversation_context(message)
    
    primary_emotion = emotion_analysis["primary_emotion"]
    primary_context = context_analysis["primary_context"]
    
    strategy = get_response_strategy(primary_emotion, primary_context)
    
    # 추가 인사이트
    urgency_keywords = ["급해", "빨리", "지금", "당장", "오늘"]
    is_urgent = any(keyword in message for keyword in urgency_keywords)
    
    politeness_keywords = ["부탁", "죄송", "실례", "괜찮다면"]
    is_polite = any(keyword in message for keyword in politeness_keywords)
    
    return {
        "emotion": emotion_analysis,
        "context": context_analysis,
        "strategy": strategy,
        "urgency": is_urgent,
        "politeness": is_polite,
        "recommended_response_type": _get_response_type(primary_emotion, primary_context),
        "conversation_flow": _suggest_conversation_flow(primary_emotion, primary_context)
    }

def _get_response_type(emotion: str, context: str) -> str:
    """응답 유형 결정"""
    
    if emotion == "tired" and context == "casual_chat":
        return "empathetic_transition"
    elif emotion == "curious" and context == "technical_inquiry":
        return "informative_engaging"
    elif emotion == "dissatisfied":
        return "problem_solving"
    elif context == "beauty_concern":
        return "professional_consultation"
    elif context == "booking_intent":
        return "service_facilitation"
    else:
        return "adaptive_friendly"

def _suggest_conversation_flow(emotion: str, context: str) -> List[str]:
    """대화 흐름 제안"""
    
    flows = {
        ("tired", "casual_chat"): [
            "공감 표현",
            "위로 메시지",
            "힐링 서비스 자연스럽게 제안",
            "구체적 혜택 안내"
        ],
        ("curious", "technical_inquiry"): [
            "질문 확인",
            "친근한 설명",
            "서비스 연결",
            "추가 도움 제안"
        ],
        ("dissatisfied", "complaint"): [
            "사과 및 공감",
            "문제 파악",
            "해결책 제시",
            "개선된 경험 제안"
        ]
    }
    
    key = (emotion, context)
    if key in flows:
        return flows[key]
    
    return [
        "친근한 인사",
        "상황 파악",
        "적절한 서비스 제안",
        "후속 지원"
    ]

# 테스트 함수
def test_emotion_analyzer():
    """감정 분석기 테스트"""
    
    test_messages = [
        "아우 질만 들었네",
        "지금 이게 연동된거니?",
        "상담이 좀 기계적인 것 같아요",
        "이마 주름이 신경쓰여요",
        "예약 가능한 시간 있나요?"
    ]
    
    print("🧪 감정 분석기 테스트")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. 메시지: '{message}'")
        insights = generate_conversation_insights(message)
        
        print(f"   감정: {insights['emotion']['primary_emotion']}")
        print(f"   맥락: {insights['context']['primary_context']}")
        print(f"   전략: {insights['strategy']['approach']}")
        print(f"   응답 유형: {insights['recommended_response_type']}")

if __name__ == "__main__":
    test_emotion_analyzer() 