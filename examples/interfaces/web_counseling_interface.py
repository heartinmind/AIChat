#!/usr/bin/env python3
"""
🌟 엘리트 뷰티 클리닉 AI 상담 인터페이스
Streamlit 기반의 친근한 뷰티 상담 시스템
"""

import streamlit as st
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# 페이지 설정
st.set_page_config(
    page_title="엘리트 뷰티 클리닉 AI 상담",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b9d, #c44569);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
        text-align: right;
    }
    
    .ai-message {
        background-color: #f3e5f5;
        margin-right: auto;
    }
    
    .treatment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #ff6b9d;
    }
    
    .sidebar-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class BeautyAIConsultant:
    """뷰티 클리닉 AI 상담사"""
    
    def __init__(self):
        self.name = "지수"
        self.treatments = {
            "보톡스": {
                "name": "보톡스 (이마/미간)",
                "price": 200000,
                "description": "이마 주름과 미간 주름을 자연스럽게 개선하는 시술입니다",
                "duration": "30분",
                "effect_period": "4-6개월",
                "emoji": "✨"
            },
            "필러": {
                "name": "히알루론산 필러",
                "price": 400000,
                "description": "볼륨 개선 및 윤곽 정리로 자연스러운 동안 효과를 만들어드려요",
                "duration": "45분",
                "effect_period": "8-12개월",
                "emoji": "💎"
            },
            "하이드라페이셜": {
                "name": "하이드라페이셜",
                "price": 150000,
                "description": "모든 피부 타입에 적합한 딥클렌징으로 깨끗하고 촉촉한 피부를 만들어드려요",
                "duration": "60분",
                "effect_period": "즉시 효과",
                "emoji": "🌊"
            },
            "레이저토닝": {
                "name": "레이저 토닝",
                "price": 120000,
                "description": "기미, 잡티 제거와 피부 톤 개선을 위한 안전한 레이저 시술입니다",
                "duration": "40분",
                "effect_period": "3-4주 후",
                "emoji": "⚡"
            },
            "리프팅": {
                "name": "울쎄라 리프팅",
                "price": 800000,
                "description": "수술 없이 탄력 있는 V라인을 만들어주는 프리미엄 리프팅 시술입니다",
                "duration": "90분",
                "effect_period": "6-12개월",
                "emoji": "🔥"
            }
        }
        
        self.promotions = [
            {
                "title": "🎉 신규 고객 특가",
                "description": "첫 방문 시 모든 시술 20% 할인",
                "valid_until": "2025년 6월 30일까지"
            },
            {
                "title": "💕 커플 패키지",
                "description": "2인 동시 예약 시 각각 15% 할인",
                "valid_until": "상시 진행"
            },
            {
                "title": "🌸 봄맞이 이벤트",
                "description": "하이드라페이셜 + 레이저토닝 패키지 30% 할인",
                "valid_until": "2025년 5월 31일까지"
            }
        ]
    
    def analyze_concern(self, message: str) -> Dict[str, Any]:
        """고객 메시지에서 고민과 감정 분석"""
        message_lower = message.lower()
        
        concerns = {
            "주름": ["주름", "이마", "미간", "눈가", "팔자", "나이"],
            "볼륨": ["볼", "턱", "입술", "볼륨", "꺼진", "패인"],
            "피부톤": ["기미", "잡티", "색소", "톤", "칙칙", "어두운"],
            "모공": ["모공", "블랙헤드", "각질", "트러블", "여드름"],
            "탄력": ["처짐", "탄력", "리프팅", "V라인", "이중턱"]
        }
        
        emotions = {
            "걱정": ["걱정", "불안", "무서워", "두려워", "괜찮을까"],
            "궁금": ["궁금", "어떻게", "방법", "과정", "절차"],
            "급함": ["빨리", "급해", "언제", "바로", "즉시"],
            "가격문의": ["가격", "비용", "얼마", "할인", "이벤트"],
            "피곤": ["피곤", "지쳐", "힘들어", "스트레스", "바빠"]
        }
        
        detected_concerns = []
        detected_emotions = []
        
        for concern, keywords in concerns.items():
            if any(keyword in message for keyword in keywords):
                detected_concerns.append(concern)
        
        for emotion, keywords in emotions.items():
            if any(keyword in message for keyword in keywords):
                detected_emotions.append(emotion)
        
        return {
            "concerns": detected_concerns,
            "emotions": detected_emotions,
            "message": message
        }
    
    def generate_response(self, analysis: Dict[str, Any]) -> str:
        """분석 결과를 바탕으로 맞춤 응답 생성"""
        concerns = analysis["concerns"]
        emotions = analysis["emotions"]
        message = analysis["message"]
        
        # 감정별 인사말
        greeting = ""
        if "피곤" in emotions:
            greeting = "아이고, 정말 고생 많으셨겠어요! 😅 이럴 때일수록 자기관리가 중요한데..."
        elif "걱정" in emotions:
            greeting = "걱정 마세요! 😌 저희가 안전하고 효과적인 방법으로 도와드릴게요."
        elif "급함" in emotions:
            greeting = "급하시군요! ⚡ 빠른 효과를 원하시는 분들을 위한 시술들이 있어요."
        else:
            greeting = "안녕하세요! 😊 뷰티 상담사 지수입니다."
        
        # 고민별 맞춤 추천
        recommendations = []
        if "주름" in concerns:
            recommendations.append(self._format_treatment_recommendation("보톡스"))
        if "볼륨" in concerns:
            recommendations.append(self._format_treatment_recommendation("필러"))
        if "피부톤" in concerns:
            recommendations.append(self._format_treatment_recommendation("레이저토닝"))
        if "모공" in concerns:
            recommendations.append(self._format_treatment_recommendation("하이드라페이셜"))
        if "탄력" in concerns:
            recommendations.append(self._format_treatment_recommendation("리프팅"))
        
        # 가격 문의 시 할인 정보 추가
        discount_info = ""
        if "가격문의" in emotions:
            discount_info = "\n\n💰 **현재 진행 중인 이벤트**\n"
            for promo in self.promotions[:2]:  # 상위 2개만
                discount_info += f"• {promo['title']}: {promo['description']}\n"
        
        # 응답 조합
        if recommendations:
            response = f"{greeting}\n\n고객님의 고민에 맞는 시술을 추천해드릴게요!\n\n"
            response += "\n\n".join(recommendations)
            response += discount_info
            response += "\n\n더 자세한 상담이나 예약을 원하시면 언제든 말씀해주세요! ✨"
        else:
            response = f"{greeting}\n\n어떤 부분이 가장 신경 쓰이시나요? 피부 고민을 자세히 말씀해주시면 맞춤 시술을 추천해드릴게요! 💕"
            response += discount_info
        
        return response
    
    def _format_treatment_recommendation(self, treatment_key: str) -> str:
        """시술 추천 포맷팅"""
        treatment = self.treatments[treatment_key]
        return f"""
{treatment['emoji']} **{treatment['name']}**
💰 가격: {treatment['price']:,}원
⏰ 소요시간: {treatment['duration']}
📅 효과 지속: {treatment['effect_period']}
📝 {treatment['description']}
        """.strip()

# AI 상담사 인스턴스 생성
if 'ai_consultant' not in st.session_state:
    st.session_state.ai_consultant = BeautyAIConsultant()

# 채팅 히스토리 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1>💄 엘리트 뷰티 클리닉</h1>
    <h3>AI 뷰티 상담사 지수와 함께하는 맞춤 상담</h3>
    <p>당신의 아름다움을 위한 전문적이고 친근한 상담을 제공합니다</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 - 클리닉 정보
with st.sidebar:
    st.markdown("### 🏥 클리닉 정보")
    
    st.markdown("""
    <div class="sidebar-info">
        <h4>📍 위치</h4>
        <p>서울 강남구 강남대로 123<br>
        지하철 2호선 강남역 3번 출구</p>
        
        <h4>📞 연락처</h4>
        <p>02-1234-5678</p>
        
        <h4>🕐 운영시간</h4>
        <p>평일: 10:00 - 19:00<br>
        토요일: 10:00 - 17:00<br>
        일요일: 휴무</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎉 현재 이벤트")
    for promo in st.session_state.ai_consultant.promotions:
        st.markdown(f"""
        **{promo['title']}**  
        {promo['description']}  
        *{promo['valid_until']}*
        """)
        st.markdown("---")
    
    if st.button("💬 채팅 기록 초기화"):
        st.session_state.chat_history = []
        st.rerun()

# 메인 채팅 영역
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 AI 상담사와 대화하기")
    
    # 채팅 히스토리 표시
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat['type'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>고객님:</strong> {chat['message']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message ai-message">
                    <strong>지수:</strong> {chat['message']}
                </div>
                """, unsafe_allow_html=True)
    
    # 메시지 입력
    user_input = st.text_input(
        "메시지를 입력하세요...",
        placeholder="예: 이마 주름이 신경 쓰여요. 어떤 시술이 좋을까요?",
        key="user_input"
    )
    
    col_send, col_example = st.columns([1, 2])
    
    with col_send:
        if st.button("💌 전송", type="primary"):
            if user_input:
                # 사용자 메시지 추가
                st.session_state.chat_history.append({
                    'type': 'user',
                    'message': user_input,
                    'timestamp': datetime.now()
                })
                
                # AI 응답 생성
                analysis = st.session_state.ai_consultant.analyze_concern(user_input)
                ai_response = st.session_state.ai_consultant.generate_response(analysis)
                
                # AI 응답 추가
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'message': ai_response,
                    'timestamp': datetime.now()
                })
                
                st.rerun()
    
    with col_example:
        st.markdown("**💡 예시 질문들:**")
        example_questions = [
            "이마 주름이 신경 쓰여요",
            "볼이 꺼져 보여서 고민이에요",
            "기미 때문에 스트레스받아요",
            "가격이 궁금해요",
            "빠른 효과를 원해요"
        ]
        
        for question in example_questions:
            if st.button(f"'{question}'", key=f"example_{question}"):
                # 예시 질문으로 바로 대화 시작
                st.session_state.chat_history.append({
                    'type': 'user',
                    'message': question,
                    'timestamp': datetime.now()
                })
                
                # AI 응답 생성
                analysis = st.session_state.ai_consultant.analyze_concern(question)
                ai_response = st.session_state.ai_consultant.generate_response(analysis)
                
                # AI 응답 추가
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'message': ai_response,
                    'timestamp': datetime.now()
                })
                
                st.rerun()

with col2:
    st.markdown("### 🌟 인기 시술")
    
    popular_treatments = ["보톡스", "필러", "하이드라페이셜"]
    
    for treatment_key in popular_treatments:
        treatment = st.session_state.ai_consultant.treatments[treatment_key]
        
        st.markdown(f"""
        <div class="treatment-card">
            <h4>{treatment['emoji']} {treatment['name']}</h4>
            <p><strong>💰 {treatment['price']:,}원</strong></p>
            <p>⏰ {treatment['duration']} | 📅 {treatment['effect_period']}</p>
            <p>{treatment['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 실시간 상담 현황")
    st.metric("오늘 상담 건수", "47건", "↗️ +12")
    st.metric("평균 만족도", "4.8/5.0", "↗️ +0.2")
    st.metric("예약 가능 시간", "오후 3시 이후", "")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>💄 엘리트 뷰티 클리닉 | AI 상담사 지수가 24시간 상담해드립니다</p>
    <p>⚠️ 본 상담은 참고용이며, 정확한 진단은 전문의와 상담 후 결정해주세요</p>
</div>
""", unsafe_allow_html=True) 