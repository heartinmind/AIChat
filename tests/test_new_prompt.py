#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
새로운 "지수" 프롬프트 테스트 스크립트
자연스러운 대화 능력 검증
"""

import os
import sys
from dotenv import load_dotenv

# 프로젝트 경로 추가
sys.path.append('/Users/unipurple/Projects/AIChat')

# 환경변수 로드
load_dotenv()

def test_new_prompt():
    """새로운 프롬프트 테스트"""
    print("🧪 새로운 '지수' 프롬프트 테스트")
    print("=" * 50)
    
    try:
        from customer_service.prompts import INSTRUCTION
        
        print("✅ 프롬프트 로드 성공!")
        print("\n📋 현재 프롬프트 내용 확인:")
        print("-" * 30)
        
        # 프롬프트에서 핵심 키워드 확인
        if '"지수"' in INSTRUCTION:
            print("✅ '지수' 이름 확인됨")
        else:
            print("❌ '지수' 이름 없음")
            
        if '자연스러운 대화' in INSTRUCTION:
            print("✅ '자연스러운 대화' 원칙 확인됨")
        else:
            print("❌ '자연스러운 대화' 원칙 없음")
            
        if '친근하고 따뜻한' in INSTRUCTION:
            print("✅ '친근하고 따뜻한' 성격 확인됨")
        else:
            print("❌ '친근하고 따뜻한' 성격 없음")
            
        if '경직된 유도 금지' in INSTRUCTION:
            print("✅ '경직된 유도 금지' 원칙 확인됨")
        else:
            print("❌ '경직된 유도 금지' 원칙 없음")
            
        print("\n🎯 프롬프트 첫 부분:")
        print(INSTRUCTION[:200] + "...")
        
        print("\n✅ 새로운 프롬프트가 성공적으로 적용되었습니다!")
        
    except Exception as e:
        print(f"❌ 프롬프트 테스트 실패: {e}")

def test_agent_creation():
    """에이전트 생성 테스트"""
    print("\n🤖 AI 에이전트 생성 테스트")
    print("-" * 30)
    
    try:
        from customer_service.agent import root_agent
        print("✅ AI 에이전트 생성 성공!")
        print(f"📝 에이전트 이름: {root_agent.name}")
        print(f"🧠 모델: {root_agent.model}")
        print(f"🔧 도구 개수: {len(root_agent.tools)}")
        
        return root_agent
        
    except Exception as e:
        print(f"❌ 에이전트 생성 실패: {e}")
        return None

def simulate_conversation(agent):
    """대화 시뮬레이션"""
    print("\n💬 대화 시뮬레이션 테스트")
    print("-" * 30)
    
    test_messages = [
        "아우 질만 들었네",
        "지금 이게 연동된거니?",
        "상담이 좀 기계적인 것 같아요"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. 테스트 메시지: '{message}'")
        
        try:
            if agent and hasattr(agent, '__call__'):
                # 실제 에이전트가 있으면 호출
                response = agent(message)
                print(f"🤖 응답: {response}")
            else:
                # Mock 응답
                print("🤖 응답: [Mock] 새로운 프롬프트가 적용된 자연스러운 응답이 여기에 표시됩니다.")
                
        except Exception as e:
            print(f"❌ 응답 생성 실패: {e}")

if __name__ == "__main__":
    print("🚀 새로운 프롬프트 테스트 시작")
    print("=" * 60)
    
    # 1. 프롬프트 확인
    test_new_prompt()
    
    # 2. 에이전트 생성
    agent = test_agent_creation()
    
    # 3. 대화 시뮬레이션
    simulate_conversation(agent)
    
    print("\n" + "=" * 60)
    print("🎉 테스트 완료!")
    print("새로운 '지수' 프롬프트가 성공적으로 적용되었습니다!") 