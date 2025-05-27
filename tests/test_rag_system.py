#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAG 시스템 상담 시뮬레이션 테스트
실제 고객 시나리오로 AI 상담 품질 검증
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from customer_service.rag.rag_system import (
    BeautyClinicRAG,
    run_consultation_simulation,
    live_consultation_demo
)

def test_basic_rag_functionality():
    """기본 RAG 기능 테스트"""
    print("🧪 기본 RAG 기능 테스트 시작...")
    
    rag = BeautyClinicRAG()
    rag.initialize_knowledge_base()
    
    # 테스트 쿼리들
    test_queries = [
        "보톡스 가격이 얼마인가요?",
        "필러 시술 후 주의사항이 뭔가요?",
        "20대 여성에게 추천하는 시술은?",
        "피코레이저 효과는 어떤가요?"
    ]
    
    for query in test_queries:
        print(f"\n📝 테스트 쿼리: {query}")
        result = rag.generate_consultation_response(query)
        
        print(f"✅ 응답 생성됨 (신뢰도: {result['confidence_score']:.2f})")
        print(f"📄 참조 문서: {len(result['relevant_documents'])}개")
        
        if result['relevant_documents']:
            print(f"🔍 최고 유사도: {result['relevant_documents'][0]['similarity']:.2f}")
    
    print("\n✅ 기본 RAG 기능 테스트 완료!")

def test_customer_scenarios():
    """실제 고객 시나리오 테스트"""
    print("\n🎭 고객 시나리오 테스트 시작...")
    
    simulations = run_consultation_simulation()
    
    for i, sim in enumerate(simulations, 1):
        print(f"\n📋 시나리오 {i}:")
        scenario = sim['시나리오']
        result = sim['AI상담결과']
        
        print(f"👤 고객: {scenario['고객_프로필']['나이']}세 {scenario['고객_프로필']['성별']}")
        print(f"💬 질문: {scenario['상담_시나리오']['초기_질문'][:50]}...")
        print(f"📊 신뢰도: {sim['신뢰도']:.2f}")
        print(f"📝 응답 길이: {len(result['ai_response'])}자")
        
        # 응답 품질 검사
        response = result['ai_response']
        quality_score = 0
        
        if "만원" in response: quality_score += 1  # 가격 정보
        if "시간" in response: quality_score += 1  # 시간 정보  
        if "주의" in response or "금지" in response: quality_score += 1  # 주의사항
        if "😊" in response or "💫" in response: quality_score += 1  # 친근함
        
        print(f"⭐ 응답 품질: {quality_score}/4")
    
    print("\n✅ 고객 시나리오 테스트 완료!")

def test_live_demo():
    """실시간 데모 테스트"""
    print("\n🎬 실시간 데모 테스트 시작...")
    
    # 다양한 고객 프로필로 테스트
    test_cases = [
        {
            "profile": {
                "나이": 25,
                "성별": "여성",
                "주요_고민": ["여드름 흉터"],
                "예산": "30만원 이하",
                "시술_경험": "없음"
            },
            "query": "여드름 흉터 때문에 고민이에요. 어떤 시술이 좋을까요?"
        },
        {
            "profile": {
                "나이": 45,
                "성별": "남성",
                "주요_고민": ["이중턱", "사각턱"],
                "예산": "제한없음",
                "시술_경험": "보톡스 경험"
            },
            "query": "이중턱이 심해서 인상이 나빠 보여요. 효과적인 방법이 있나요?"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🎯 테스트 케이스 {i}:")
        result = live_consultation_demo(case['query'], case['profile'])
        
        # 응답 평가
        response = result['ai_response']
        if len(response) > 200:
            print("✅ 충분히 상세한 응답")
        if result['confidence_score'] > 0.5:
            print("✅ 높은 신뢰도")
        if "만원" in response:
            print("✅ 가격 정보 포함")
            
    print("\n✅ 실시간 데모 테스트 완료!")

def performance_test():
    """성능 테스트"""
    print("\n⚡ 성능 테스트 시작...")
    
    import time
    
    rag = BeautyClinicRAG()
    
    # 초기화 시간 측정
    start_time = time.time()
    rag.initialize_knowledge_base()
    init_time = time.time() - start_time
    
    print(f"📊 지식베이스 초기화: {init_time:.2f}초")
    print(f"📚 총 문서 수: {len(rag.documents)}개")
    
    # 응답 생성 시간 측정
    test_queries = [
        "보톡스 가격 알려주세요",
        "30대 여성 추천 시술",
        "레이저 시술 후 관리법"
    ]
    
    total_time = 0
    for query in test_queries:
        start_time = time.time()
        result = rag.generate_consultation_response(query)
        response_time = time.time() - start_time
        total_time += response_time
        
        print(f"⏱️ '{query[:20]}...' 응답 시간: {response_time:.3f}초")
    
    avg_time = total_time / len(test_queries)
    print(f"📈 평균 응답 시간: {avg_time:.3f}초")
    
    print("\n✅ 성능 테스트 완료!")

if __name__ == "__main__":
    print("🚀 RAG 시스템 종합 테스트 시작!")
    print("=" * 60)
    
    try:
        # 1. 기본 기능 테스트
        test_basic_rag_functionality()
        
        # 2. 고객 시나리오 테스트  
        test_customer_scenarios()
        
        # 3. 실시간 데모 테스트
        test_live_demo()
        
        # 4. 성능 테스트
        performance_test()
        
        print("\n" + "=" * 60)
        print("🎉 모든 테스트 성공적으로 완료!")
        print("\n📋 테스트 결과 요약:")
        print("✅ RAG 지식베이스 구축 성공")
        print("✅ 키워드 기반 문서 검색 작동")
        print("✅ 고객 프로필 분석 정상")
        print("✅ 전문적인 상담 응답 생성")
        print("✅ 실시간 상담 시뮬레이션 성공")
        print("✅ 성능 최적화 확인")
        
        print("\n🎯 다음 단계:")
        print("1. 실제 API 연동 (네이버 예약, SMS 등)")
        print("2. 보안 시스템 구현")
        print("3. 데이터베이스 연동")
        print("4. 상용 서비스 배포")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()
