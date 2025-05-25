# customer_service/rag/rag_system.py
"""
RAG (Retrieval-Augmented Generation) 시스템 통합
실제 뷰티 클리닉 데이터로 상담 시뮬레이션
"""

import os
import json
from typing import List, Dict, Any
import logging

from .beauty_clinic_data import (
    REAL_BEAUTY_TREATMENTS,
    CUSTOMER_CONSULTATION_SCENARIOS, 
    CLINIC_POLICIES,
    generate_rag_documents,
    simulate_customer_consultation
)

logger = logging.getLogger(__name__)

# 간단한 키워드 기반 검색 시스템 (실제로는 SentenceTransformer 사용)
class SimpleKeywordMatcher:
    """키워드 기반 단순 검색 시스템 (임베딩 모델 대체용)"""
    
    def __init__(self):
        self.documents = []
        self.keywords_map = {}
        
    def add_documents(self, documents):
        self.documents = documents
        # 각 문서에서 키워드 추출
        for i, doc in enumerate(documents):
            keywords = set()
            # 한국어 키워드 추출 (간단한 버전)
            for word in ["보톡스", "필러", "레이저", "피코", "IPL", "하이드라", "아쿠아", 
                        "이마", "눈가", "볼", "턱", "주름", "색소", "모공", "여드름",
                        "20대", "30대", "40대", "50대", "지성", "건성", "복합성", "민감성"]:
                if word in doc:
                    keywords.add(word)
            self.keywords_map[i] = keywords
    
    def search(self, query, top_k=3):
        scores = []
        query_keywords = set()
        for word in ["보톡스", "필러", "레이저", "피코", "IPL", "하이드라", "아쿠아", 
                    "이마", "눈가", "볼", "턱", "주름", "색소", "모공", "여드름",
                    "20대", "30대", "40대", "50대", "지성", "건성", "복합성", "민감성"]:
            if word in query:
                query_keywords.add(word)
        
        for i, doc_keywords in self.keywords_map.items():
            # 교집합 크기로 점수 계산
            score = len(query_keywords.intersection(doc_keywords))
            if score > 0:
                scores.append((i, score))
        
        # 점수 순으로 정렬
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for i, score in scores[:top_k]:
            results.append({
                "document": self.documents[i],
                "similarity": score / max(len(query_keywords), 1),
                "index": i
            })
        
        return results

class BeautyClinicRAG:
    def __init__(self):
        """간소화된 RAG 시스템 초기화 (의존성 최소화)"""
        self.matcher = SimpleKeywordMatcher()
        self.documents = []
        self.is_initialized = False
        
    def initialize_knowledge_base(self):
        """실제 뷰티 클리닉 지식베이스 구축"""
        logger.info("뷰티 클리닉 지식베이스 구축 중...")
        
        # 실제 데이터로 문서 생성
        self.documents = generate_rag_documents()
        
        # 추가 전문 지식 문서
        expert_knowledge = [
            """
            보톡스 시술 가이드:
            - 이마 주름: 15-20 유닛, 15만원
            - 눈가 주름: 12-16 유닛, 20만원  
            - 사각근: 40-60 유닛, 25만원
            - 시술 후 4시간 눕지 말기
            - 효과는 3-5일 후부터 나타남
            - 지속기간 4-6개월
            """,
            
            """
            필러 시술 가이드:
            - 히알루론산 필러가 가장 안전
            - 볼: 1-2cc, 40만원
            - 법령선: 0.5-1cc, 30만원
            - 입술: 0.5cc, 35만원
            - 시술 후 2-3일 붓기 정상
            - 마사지 금지, 얼음찜질 권장
            """,
            
            """
            피부 타입별 맞춤 관리:
            - 지성 피부: IPL + 피코레이저 조합
            - 건성 피부: 하이드라페이셜 + 수분케어
            - 민감성 피부: 아쿠아필 + 진정케어
            - 복합성 피부: 부위별 차별 관리
            """,
            
            """
            연령대별 추천 시술:
            - 20대: 스킨케어 위주, 예방 보톡스
            - 30대: 보톡스 + 필러 시작
            - 40대: 리프팅 + 레이저 조합
            - 50대 이상: 종합적 안티에이징
            """
        ]
        
        self.documents.extend(expert_knowledge)
        
        # 검색 시스템에 문서 추가
        self.matcher.add_documents(self.documents)
        self.is_initialized = True
        
        logger.info(f"✅ RAG 지식베이스 구축 완료! (총 {len(self.documents)}개 문서)")
        
    def search_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """질문과 관련된 문서 검색"""
        if not self.is_initialized:
            self.initialize_knowledge_base()
            
        return self.matcher.search(query, top_k)
    
    def generate_consultation_response(self, customer_query: str, customer_profile: Dict = None) -> Dict:
        """고객 질문에 대한 전문적인 상담 응답 생성"""
        
        # 관련 문서 검색
        relevant_docs = self.search_relevant_documents(customer_query, top_k=3)
        
        # 고객 프로필 분석
        if customer_profile:
            profile_analysis = self._analyze_customer_profile(customer_profile)
        else:
            profile_analysis = "고객 프로필 정보가 없어 일반적인 상담을 진행합니다."
        
        # 컨텍스트 구성
        context = ""
        for doc in relevant_docs:
            context += f"관련정보: {doc['document']}\n"
        
        # 전문적인 응답 생성
        response = self._generate_expert_response(customer_query, context, profile_analysis)
        
        return {
            "customer_query": customer_query,
            "ai_response": response,
            "relevant_documents": relevant_docs,
            "customer_analysis": profile_analysis,
            "confidence_score": max([doc['similarity'] for doc in relevant_docs]) if relevant_docs else 0
        }
    
    def _analyze_customer_profile(self, profile: Dict) -> str:
        """고객 프로필 분석"""
        age = profile.get('나이', 0)
        concerns = profile.get('주요_고민', [])
        budget = profile.get('예산', '')
        experience = profile.get('시술_경험', '')
        
        analysis = f"고객 분석: {age}세, 주요 고민 {concerns}"
        
        if age < 30:
            analysis += " → 예방 중심 관리 추천"
        elif age < 40:  
            analysis += " → 초기 안티에이징 관리"
        else:
            analysis += " → 본격적인 안티에이징 필요"
            
        if '없음' in experience:
            analysis += " → 시술 초보자, 안전한 시술부터 시작"
        else:
            analysis += " → 시술 경험자, 고급 시술 가능"
            
        return analysis
    
    def _generate_expert_response(self, query: str, context: str, profile_analysis: str) -> str:
        """전문가 수준의 응답 생성"""
        
        if "보톡스" in query:
            return f"""
안녕하세요! 보톡스 상담 문의해주셔서 감사합니다. 😊

{profile_analysis}

보톡스는 주름 개선에 매우 효과적인 시술입니다:

🎯 **추천 부위 및 비용**:
- 이마 주름: 15-20 유닛 (15만원)
- 눈가 주름: 12-16 유닛 (20만원)
- 미간 주름: 8-12 유닛 (12만원)

⏰ **시술 정보**:
- 시술 시간: 10-15분
- 마취: 마취크림 도포
- 효과 발현: 3-5일 후
- 지속 기간: 4-6개월

⚠️ **주의사항**:
- 시술 후 4시간 눕지 말기
- 24시간 사우나/찜질방 금지
- 음주 일주일 금지

📅 **예약 안내**:
다음 주 화요일, 목요일 오후 시간대 예약 가능합니다.
상담 후 당일 시술도 가능하니 편안하게 방문해주세요!

추가 궁금한 점이 있으시면 언제든 말씀해주세요. 💫
            """
        
        elif "필러" in query:
            return f"""
필러 상담 문의 감사합니다! 🌟

{profile_analysis}

히알루론산 필러로 자연스럽고 안전한 볼륨 개선이 가능합니다:

💉 **추천 시술**:
- 볼 필러: 1-2cc (40만원)
- 법령선: 0.5-1cc (30만원)  
- 입술 필러: 0.5cc (35만원)

✨ **예상 효과**:
- 즉시 볼륨 개선 확인
- 자연스러운 동안 효과
- 12-18개월 지속

🔒 **안전성**:
- FDA 승인 정품 히알루론산만 사용
- 숙련된 전문의 직접 시술
- 사후관리 1개월 무료

언제든 상담 예약 가능하니 편하실 때 방문해주세요! 💕
            """
        
        elif "레이저" in query or "피코" in query or "IPL" in query:
            return f"""
레이저 시술 상담 문의 감사드립니다! ✨

{profile_analysis}

고객님의 피부 고민에 맞는 레이저 치료를 추천해드리겠습니다:

🔥 **레이저 시술 종류**:
- 피코레이저: 색소 개선 (15만원/회)
- 프락셔널: 흉터/모공 (30만원/회)
- IPL: 홍조/색소 (12만원/회)

📈 **치료 계획**:
- 세션 수: 5-8회 (상태에 따라)
- 간격: 2-4주
- 효과: 70-90% 개선

⏱️ **회복 기간**:
- 피코레이저: 3-5일
- 프락셔널: 5-7일
- IPL: 1-2일

정확한 진단을 위해 피부 상태 확인 후 맞춤 치료 계획을 세워드리겠습니다! 🎯
            """
        
        else:
            return f"""
상담 문의 감사합니다! 😊

{profile_analysis}

고객님의 고민에 맞는 맞춤 솔루션을 제안해드리겠습니다.
정확한 상담을 위해 직접 방문하셔서 피부 상태를 확인해보시는 것을 추천드립니다.

🏥 **엘리트 뷰티 클리닉**
📞 예약 문의: 02-1234-5678
📍 위치: 강남구 강남대로 123 엘리트빌딩 5층
🕒 운영시간: 월-금 10:00-20:00, 토 10:00-17:00

언제든 편하게 연락주세요! 💫
            """

# 실제 상담 시뮬레이션 함수들
def run_consultation_simulation():
    """실제 데이터로 상담 시뮬레이션 실행"""
    
    rag_system = BeautyClinicRAG()
    rag_system.initialize_knowledge_base()
    
    # 시뮬레이션 시나리오들
    simulations = []
    
    for scenario in CUSTOMER_CONSULTATION_SCENARIOS:
        customer_profile = scenario['고객_프로필']
        initial_question = scenario['상담_시나리오']['초기_질문']
        
        # RAG 시스템으로 응답 생성
        consultation_result = rag_system.generate_consultation_response(
            initial_question, 
            customer_profile
        )
        
        simulations.append({
            "시나리오": scenario,
            "AI상담결과": consultation_result,
            "신뢰도": consultation_result['confidence_score']
        })
    
    return simulations

def live_consultation_demo(user_query: str, user_profile: Dict = None):
    """실시간 상담 데모"""
    
    rag_system = BeautyClinicRAG()
    
    print("🏥 엘리트 뷰티 클리닉 AI 상담사입니다!")
    print("=" * 50)
    
    result = rag_system.generate_consultation_response(user_query, user_profile)
    
    print(f"👤 고객님: {user_query}")
    print("-" * 50)  
    print(f"🤖 AI 상담사: {result['ai_response']}")
    print("-" * 50)
    print(f"📊 응답 신뢰도: {result['confidence_score']:.2f}")
    print(f"🔍 참조 문서 수: {len(result['relevant_documents'])}")
    
    return result

# 글로벌 RAG 인스턴스
beauty_rag = BeautyClinicRAG()

# 사용 예시
if __name__ == "__main__":
    # 1. 전체 시뮬레이션 실행
    print("🧪 상담 시뮬레이션 실행 중...")
    simulations = run_consultation_simulation()
    
    for i, sim in enumerate(simulations, 1):
        print(f"\n📋 시나리오 {i}:")
        print(f"신뢰도: {sim['신뢰도']:.2f}")
        print(f"AI 응답 길이: {len(sim['AI상담결과']['ai_response'])}자")
    
    # 2. 실시간 상담 데모
    print("\n" + "="*50)
    print("🎭 실시간 상담 데모")
    
    # 예시 상담
    demo_profile = {
        "나이": 32,
        "성별": "여성",
        "주요_고민": ["눈가 주름", "입가 주름"],
        "예산": "50만원 이하",
        "시술_경험": "없음"
    }
    
    demo_query = "처음 시술받는데 눈가 주름이 신경쓰여요. 보톡스 맞으면 얼마나 걸리나요?"
    
    live_consultation_demo(demo_query, demo_profile)
