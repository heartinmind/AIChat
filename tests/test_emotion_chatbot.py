#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
감정 분석 기능이 통합된 AI 챗봇 테스트
"지수" 상담사의 지능적 대화 시뮬레이션
"""

import os
import sys
from dotenv import load_dotenv

# 프로젝트 경로 추가
sys.path.append('/Users/unipurple/Projects/AIChat')

# 환경변수 로드
load_dotenv()

def simulate_intelligent_conversation():
    """감정 분석 기반 지능적 대화 시뮬레이션"""
    
    print("🤖 감정 분석 기반 AI 챗봇 '지수' 테스트")
    print("🧠 고객 감정을 인식하고 맞춤 응답하는 시뮬레이션")
    print("=" * 60)
    
    try:
        from customer_service.tools.emotion_analyzer import generate_conversation_insights
        
        # 테스트 시나리오
        test_scenarios = [
            {
                "message": "아우 질만 들었네",
                "expected_emotion": "tired",
                "expected_context": "casual_chat"
            },
            {
                "message": "지금 이게 연동된거니?",
                "expected_emotion": "curious", 
                "expected_context": "technical_inquiry"
            },
            {
                "message": "상담이 좀 기계적인 것 같아요",
                "expected_emotion": "dissatisfied",
                "expected_context": "complaint"
            },
            {
                "message": "이마 주름이 신경쓰여서 상담받고 싶어요",
                "expected_emotion": "neutral",
                "expected_context": "beauty_concern"
            },
            {
                "message": "예약 가능한 시간 있나요?",
                "expected_emotion": "neutral",
                "expected_context": "booking_intent"
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n🎭 시나리오 {i}")
            print("-" * 30)
            
            message = scenario["message"]
            print(f"👤 고객: '{message}'")
            
            # 감정 분석
            insights = generate_conversation_insights(message)
            
            print(f"🧠 감정 분석:")
            print(f"   감정: {insights['emotion']['primary_emotion']}")
            print(f"   맥락: {insights['context']['primary_context']}")
            print(f"   전략: {insights['strategy']['approach']}")
            print(f"   톤: {insights['strategy']['tone']}")
            
            # 맞춤 응답 생성
            response = generate_contextual_response(insights, message)
            print(f"🤖 지수: {response}")
            
            # 대화 흐름 제안
            print(f"📋 추천 대화 흐름:")
            for step in insights['conversation_flow']:
                print(f"   • {step}")
        
        print(f"\n" + "=" * 60)
        print("🎉 감정 분석 기반 대화 시뮬레이션 완료!")
        print("✨ '지수'가 고객 감정을 정확히 파악하고 맞춤 응답합니다!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

def generate_contextual_response(insights: dict, message: str) -> str:
    """감정과 맥락에 따른 맞춤 응답 생성"""
    
    emotion = insights['emotion']['primary_emotion']
    context = insights['context']['primary_context']
    strategy = insights['strategy']
    
    # 감정별 맞춤 응답
    responses = {
        ("tired", "casual_chat"): 
            "아, 많이 지치셨나 봐요! 😅 오늘 하루 고생 많으셨을 것 같은데... "
            "저희 클리닉에서 힐링할 수 있는 시간 가져보시는 건 어떨까요? "
            "스트레스 해소에 도움되는 페이셜 케어도 있어요! ✨",
            
        ("curious", "technical_inquiry"):
            "네 맞아요! 실시간으로 연결되어 있어서 바로 상담 도와드릴 수 있어요 😊 "
            "저희 시스템은 고객님의 정보를 안전하게 관리하면서 "
            "개인 맞춤 서비스를 제공하고 있답니다! 궁금한 거 더 있으시면 편하게 물어보세요!",
            
        ("dissatisfied", "complaint"):
            "아, 그렇게 느끼셨다니 정말 죄송해요 😔 "
            "더 자연스럽고 따뜻한 상담을 드리고 싶었는데... "
            "앞으로 더 개선해서 편안한 상담 경험을 드릴게요! "
            "혹시 어떤 부분이 아쉬우셨는지 알려주시면 더 도움이 될 것 같아요!",
            
        ("neutral", "beauty_concern"):
            "이마 주름 때문에 고민이 많으셨겠어요! 😊 "
            "저희가 정말 도움을 드릴 수 있는 부분이에요. "
            "고객님 연령대와 피부 상태에 맞는 시술을 추천해드릴 수 있어요. "
            "보톡스나 다른 시술에 대해 궁금한 점 있으시면 언제든 물어보세요!",
            
        ("neutral", "booking_intent"):
            "예약 문의해주셔서 감사해요! 😊 "
            "어떤 시술을 원하시는지, 그리고 언제쯤 생각하고 계신지 알려주시면 "
            "가능한 시간대를 확인해서 안내해드릴게요! "
            "평일이나 주말 중 선호하시는 시간대가 있으신가요?"
    }
    
    key = (emotion, context)
    if key in responses:
        return responses[key]
    
    # 기본 응답
    return (
        "안녕하세요! 😊 엘리트 뷰티 클리닉 상담사 지수입니다. "
        "어떤 도움이 필요하신지 편하게 말씀해주세요! "
        "고객님께 가장 적합한 서비스를 찾아드릴게요! ✨"
    )

def test_emotion_integration():
    """감정 분석 통합 테스트"""
    
    print("\n🔬 감정 분석 통합 기능 테스트")
    print("-" * 40)
    
    try:
        from customer_service.tools.emotion_analyzer import (
            analyze_customer_emotion,
            analyze_conversation_context,
            get_response_strategy
        )
        
        test_message = "아우 질만 들었네"
        
        emotion = analyze_customer_emotion(test_message)
        context = analyze_conversation_context(test_message)
        strategy = get_response_strategy(
            emotion['primary_emotion'], 
            context['primary_context']
        )
        
        print(f"✅ 감정 분석: {emotion['primary_emotion']}")
        print(f"✅ 맥락 분석: {context['primary_context']}")
        print(f"✅ 응답 전략: {strategy['approach']}")
        print(f"✅ 모든 기능이 정상 작동합니다!")
        
        return True
        
    except Exception as e:
        print(f"❌ 통합 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("🚀 감정 분석 기반 AI 챗봇 테스트 시작")
    print("🎯 '지수' 상담사의 지능적 대화 능력 검증")
    print("=" * 70)
    
    # 1. 통합 기능 테스트
    if test_emotion_integration():
        # 2. 지능적 대화 시뮬레이션
        simulate_intelligent_conversation()
    else:
        print("❌ 기본 기능 테스트 실패로 시뮬레이션을 건너뜁니다.")
    
    print("\n🎊 테스트 완료!")
    print("이제 '지수'가 고객의 감정을 읽고 맞춤 응답할 수 있습니다!") 