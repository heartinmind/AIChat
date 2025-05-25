#!/usr/bin/env python3
"""
Firestore 초기 설정 및 데이터 생성 스크립트

뷰티 클리닉 AI 챗봇을 위한 Firestore 데이터베이스 초기화
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ImportError:
    print("❌ Google Cloud Firestore 라이브러리가 설치되지 않았습니다.")
    print("설치 명령어: pip install google-cloud-firestore")
    sys.exit(1)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirestoreSetup:
    """Firestore 초기 설정 클래스"""
    
    def __init__(self):
        self.project_id = "elite-cms-2025"
        self.credentials_path = "/Users/unipurple/gcp-mcp-key.json"
        self.db = None
        
    def initialize_firestore(self):
        """Firestore 클라이언트 초기화"""
        try:
            # 서비스 계정 키로 인증
            if os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self.db = firestore.Client(
                    project=self.project_id,
                    credentials=credentials
                )
            else:
                # 기본 인증 사용 (Cloud Run 환경)
                self.db = firestore.Client(project=self.project_id)
            
            logger.info(f"✅ Firestore 클라이언트 초기화 완료: {self.project_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Firestore 초기화 실패: {e}")
            return False
    
    def create_sample_customers(self):
        """샘플 고객 데이터 생성"""
        customers = [
            {
                "customer_id": "cust_001",
                "name": "김지영",
                "email": "jiyoung.kim@email.com",
                "phone": "010-1234-5678",
                "age": 28,
                "gender": "female",
                "skin_type": "건성",
                "previous_treatments": ["보톡스", "필러"],
                "preferences": ["자연스러운 효과", "빠른 회복"],
                "created_at": datetime.now(),
                "last_visit": datetime.now() - timedelta(days=30),
                "total_spent": 850000,
                "loyalty_points": 85,
                "notes": "첫 시술 후 만족도 높음. 정기 관리 희망"
            },
            {
                "customer_id": "cust_002", 
                "name": "박수진",
                "email": "sujin.park@email.com",
                "phone": "010-2345-6789",
                "age": 35,
                "gender": "female",
                "skin_type": "지성",
                "previous_treatments": ["레이저 토닝", "리프팅"],
                "preferences": ["확실한 효과", "프리미엄 서비스"],
                "created_at": datetime.now() - timedelta(days=60),
                "last_visit": datetime.now() - timedelta(days=15),
                "total_spent": 1200000,
                "loyalty_points": 120,
                "notes": "VIP 고객. 최신 시술에 관심 많음"
            },
            {
                "customer_id": "cust_003",
                "name": "이민정",
                "email": "minjeong.lee@email.com", 
                "phone": "010-3456-7890",
                "age": 42,
                "gender": "female",
                "skin_type": "복합성",
                "previous_treatments": [],
                "preferences": ["안전성", "자연스러움"],
                "created_at": datetime.now() - timedelta(days=7),
                "last_visit": None,
                "total_spent": 0,
                "loyalty_points": 0,
                "notes": "첫 방문 예정. 시술 경험 없음"
            }
        ]
        
        try:
            for customer in customers:
                doc_ref = self.db.collection('customers').document(customer['customer_id'])
                doc_ref.set(customer)
                logger.info(f"✅ 고객 데이터 생성: {customer['name']}")
            
            logger.info(f"✅ 총 {len(customers)}명의 샘플 고객 데이터 생성 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 고객 데이터 생성 실패: {e}")
            return False
    
    def create_sample_treatments(self):
        """샘플 시술 데이터 생성"""
        treatments = [
            {
                "treatment_id": "treat_001",
                "name": "보톡스",
                "category": "주사 시술",
                "price": 150000,
                "duration_minutes": 30,
                "description": "주름 개선 및 예방을 위한 보툴리눔 톡신 주사",
                "benefits": ["주름 개선", "예방 효과", "즉시 일상 복귀"],
                "side_effects": ["일시적 부종", "멍"],
                "recovery_days": 1,
                "suitable_age": [25, 60],
                "contraindications": ["임신", "수유", "근육 질환"],
                "popularity_score": 95,
                "created_at": datetime.now()
            },
            {
                "treatment_id": "treat_002",
                "name": "히알루론산 필러",
                "category": "주사 시술", 
                "price": 300000,
                "duration_minutes": 45,
                "description": "볼륨 개선 및 윤곽 정리를 위한 히알루론산 주입",
                "benefits": ["볼륨 증가", "윤곽 개선", "자연스러운 효과"],
                "side_effects": ["부종", "멍", "일시적 딱딱함"],
                "recovery_days": 3,
                "suitable_age": [25, 65],
                "contraindications": ["임신", "수유", "알레르기"],
                "popularity_score": 88,
                "created_at": datetime.now()
            },
            {
                "treatment_id": "treat_003",
                "name": "리프테라",
                "category": "레이저 시술",
                "price": 800000,
                "duration_minutes": 90,
                "description": "HIFU 기술을 이용한 비수술적 리프팅",
                "benefits": ["리프팅 효과", "콜라겐 재생", "지속적 개선"],
                "side_effects": ["일시적 부종", "따끔거림"],
                "recovery_days": 2,
                "suitable_age": [30, 70],
                "contraindications": ["임신", "수유", "금속 임플란트"],
                "popularity_score": 82,
                "created_at": datetime.now()
            }
        ]
        
        try:
            for treatment in treatments:
                doc_ref = self.db.collection('treatments').document(treatment['treatment_id'])
                doc_ref.set(treatment)
                logger.info(f"✅ 시술 데이터 생성: {treatment['name']}")
            
            logger.info(f"✅ 총 {len(treatments)}개의 샘플 시술 데이터 생성 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 시술 데이터 생성 실패: {e}")
            return False
    
    def create_sample_appointments(self):
        """샘플 예약 데이터 생성"""
        appointments = [
            {
                "appointment_id": "appt_001",
                "customer_id": "cust_001",
                "treatment_id": "treat_001",
                "doctor_name": "박지영 원장",
                "appointment_date": datetime.now() + timedelta(days=3),
                "duration_minutes": 30,
                "status": "confirmed",
                "price": 150000,
                "notes": "첫 보톡스 시술. 자연스러운 효과 희망",
                "created_at": datetime.now(),
                "reminder_sent": False
            },
            {
                "appointment_id": "appt_002", 
                "customer_id": "cust_002",
                "treatment_id": "treat_003",
                "doctor_name": "김수진 실장",
                "appointment_date": datetime.now() + timedelta(days=7),
                "duration_minutes": 90,
                "status": "pending",
                "price": 800000,
                "notes": "리프테라 2차 시술. VIP 고객",
                "created_at": datetime.now(),
                "reminder_sent": False
            }
        ]
        
        try:
            for appointment in appointments:
                doc_ref = self.db.collection('appointments').document(appointment['appointment_id'])
                doc_ref.set(appointment)
                logger.info(f"✅ 예약 데이터 생성: {appointment['appointment_id']}")
            
            logger.info(f"✅ 총 {len(appointments)}개의 샘플 예약 데이터 생성 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ 예약 데이터 생성 실패: {e}")
            return False
    
    def verify_setup(self):
        """설정 검증"""
        try:
            # 컬렉션별 문서 수 확인
            customers_count = len(list(self.db.collection('customers').stream()))
            treatments_count = len(list(self.db.collection('treatments').stream()))
            appointments_count = len(list(self.db.collection('appointments').stream()))
            
            logger.info("📊 Firestore 데이터 확인:")
            logger.info(f"  - 고객: {customers_count}명")
            logger.info(f"  - 시술: {treatments_count}개")
            logger.info(f"  - 예약: {appointments_count}개")
            
            return customers_count > 0 and treatments_count > 0
            
        except Exception as e:
            logger.error(f"❌ 설정 검증 실패: {e}")
            return False

def main():
    """메인 실행 함수"""
    print("🔥 Firestore 초기 설정을 시작합니다...")
    
    setup = FirestoreSetup()
    
    # 1. Firestore 초기화
    if not setup.initialize_firestore():
        print("❌ Firestore 초기화 실패")
        return False
    
    # 2. 샘플 데이터 생성
    success = True
    success &= setup.create_sample_customers()
    success &= setup.create_sample_treatments() 
    success &= setup.create_sample_appointments()
    
    # 3. 설정 검증
    if success and setup.verify_setup():
        print("🎉 Firestore 초기 설정 완료!")
        print("📱 Firebase 콘솔에서 데이터를 확인하세요:")
        print("   https://console.firebase.google.com/project/elite-cms-2025/firestore")
        return True
    else:
        print("❌ Firestore 설정 중 오류 발생")
        return False

if __name__ == "__main__":
    main()
