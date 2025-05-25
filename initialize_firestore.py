#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firestore 초기 데이터 생성 스크립트
실제 뷰티 클리닉 데이터로 Firestore 설정
"""

import os
import sys
from datetime import datetime, timedelta
import uuid
import json

# 프로젝트 경로 추가
sys.path.append('/Users/unipurple/Projects/AIChat')

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

def setup_firestore():
    """Firestore 초기화 및 데이터 생성"""
    try:
        print("🔥 Firestore 초기화 시작...")
        
        # Firebase Admin SDK 초기화
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        # 서비스 계정 키 파일 확인
        key_path = os.getenv('GCS_CREDENTIALS_PATH')
        if not key_path or not os.path.exists(key_path):
            print(f"❌ 서비스 계정 키 파일을 찾을 수 없습니다: {key_path}")
            print("📋 다음 단계를 완료해주세요:")
            print("1. Google Cloud Console → IAM 및 관리자 → 서비스 계정")
            print("2. 서비스 계정 키 다운로드 (JSON)")
            print("3. 파일을 /Users/unipurple/Projects/AIChat/service-account-key.json 에 저장")
            return False
        
        # Firebase 앱 초기화
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred, {
                'projectId': os.getenv('GOOGLE_CLOUD_PROJECT', 'elite-cms-2025')
            })
        
        db = firestore.client()
        print("✅ Firestore 연결 성공!")
        
        # 1. 시술 카테고리 생성
        print("📂 시술 카테고리 생성 중...")
        categories = [
            {
                'name': '주사 시술',
                'description': '보톡스, 필러 등 주사를 이용한 시술',
                'displayOrder': 1,
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'name': '레이저 시술', 
                'description': '피코, IPL, 프락셔널 등 레이저 시술',
                'displayOrder': 2,
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'name': '스킨케어',
                'description': '하이드라페이셜, 아쿠아필 등 기본 관리',
                'displayOrder': 3,
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            }
        ]
        
        for category in categories:
            doc_ref = db.collection('treatmentCategories').add(category)
            print(f"  ✅ 카테고리 추가: {category['name']}")
        
        # 2. 시술 정보 생성
        print("💉 시술 정보 생성 중...")
        treatments = [
            {
                'code': 'BTX001',
                'name': '보톡스 (이마)',
                'description': '이마 주름 개선을 위한 보톡스 시술입니다. 안전하고 효과적인 시술로 자연스러운 결과를 얻을 수 있습니다.',
                'shortDescription': '이마 주름 개선 보톡스',
                'category': 'injection',
                'price': 200000,
                'discountedPrice': 180000,
                'duration': 15,
                'targetArea': '이마',
                'recommendedAgeMin': 25,
                'recommendedAgeMax': 60,
                'suitableSkinTypes': ['oily', 'dry', 'combination', 'normal'],
                'postCareInstructions': '시술 후 4시간 동안 눕지 마세요. 24시간 사우나 금지.',
                'isActive': True,
                'popularityScore': 95,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'code': 'BTX002',
                'name': '보톡스 (눈가)',
                'description': '눈가 주름(까치발) 개선을 위한 보톡스 시술입니다.',
                'shortDescription': '눈가 주름 개선 보톡스',
                'category': 'injection',
                'price': 250000,
                'discountedPrice': 220000,
                'duration': 15,
                'targetArea': '눈가',
                'recommendedAgeMin': 25,
                'recommendedAgeMax': 65,
                'suitableSkinTypes': ['all'],
                'postCareInstructions': '시술 후 눈 비비지 마세요. 4시간 동안 눕지 마세요.',
                'isActive': True,
                'popularityScore': 90,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'code': 'FILL001',
                'name': '필러 (볼)',
                'description': '볼 볼륨 개선을 위한 히알루론산 필러 시술입니다.',
                'shortDescription': '볼 볼륨 개선 필러',
                'category': 'injection',
                'price': 400000,
                'discountedPrice': 360000,
                'duration': 30,
                'targetArea': '볼',
                'recommendedAgeMin': 25,
                'recommendedAgeMax': 55,
                'suitableSkinTypes': ['all'],
                'postCareInstructions': '시술 후 2-3일간 부기 있을 수 있습니다. 마사지 금지.',
                'isActive': True,
                'popularityScore': 85,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'code': 'LASER001',
                'name': '피코레이저',
                'description': '색소 침착, 기미, 주근깨 개선을 위한 피코레이저 시술입니다.',
                'shortDescription': '색소 개선 피코레이저',
                'category': 'laser',
                'price': 150000,
                'discountedPrice': 130000,
                'duration': 20,
                'targetArea': '전체',
                'recommendedAgeMin': 20,
                'recommendedAgeMax': 70,
                'suitableSkinTypes': ['oily', 'combination', 'normal'],
                'postCareInstructions': '시술 후 3-5일간 딱지 생길 수 있습니다. 자외선 차단 필수.',
                'isActive': True,
                'popularityScore': 88,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'code': 'FACIAL001',
                'name': '하이드라페이셜',
                'description': '모든 피부 타입에 적합한 딥클렌징 + 수분 공급 시술입니다.',
                'shortDescription': '딥클렌징 + 수분공급',
                'category': 'skincare',
                'price': 180000,
                'discountedPrice': 150000,
                'duration': 60,
                'targetArea': '전체',
                'recommendedAgeMin': 18,
                'recommendedAgeMax': 80,
                'suitableSkinTypes': ['all'],
                'postCareInstructions': '시술 후 24시간 메이크업 지양. 충분한 수분 공급.',
                'isActive': True,
                'popularityScore': 92,
                'createdAt': firestore.SERVER_TIMESTAMP
            }
        ]
        
        for treatment in treatments:
            doc_ref = db.collection('treatments').add(treatment)
            print(f"  ✅ 시술 추가: {treatment['name']}")
        
        # 3. 직원 정보 생성
        print("👩‍⚕️ 직원 정보 생성 중...")
        staff_members = [
            {
                'staffCode': 'DOC001',
                'name': '김미용',
                'role': 'doctor',
                'specialization': ['botox', 'filler', 'thread_lift'],
                'phone': '02-1234-5678',
                'email': 'dr.kim@elitebeauty.co.kr',
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'staffCode': 'DOC002',
                'name': '이성형',
                'role': 'doctor',
                'specialization': ['laser', 'ipl', 'picosure'],
                'phone': '02-1234-5679',
                'email': 'dr.lee@elitebeauty.co.kr',
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'staffCode': 'NUR001',
                'name': '박간호',
                'role': 'nurse',
                'specialization': ['skincare', 'basic_treatment'],
                'phone': '02-1234-5680',
                'email': 'nurse.park@elitebeauty.co.kr',
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            }
        ]
        
        for staff in staff_members:
            doc_ref = db.collection('staff').add(staff)
            print(f"  ✅ 직원 추가: {staff['name']} ({staff['role']})")
        
        # 4. 샘플 고객 생성
        print("👤 샘플 고객 생성 중...")
        sample_customers = [
            {
                'customerCode': 'BC2024001',
                'name': '김지수',
                'phone': '010-1234-5678',
                'email': 'jisu.kim@example.com',
                'birthDate': datetime(1995, 3, 15),
                'gender': 'female',
                'skinType': 'combination',
                'skinConcerns': ['wrinkles', 'pigmentation'],
                'membershipLevel': 'silver',
                'totalSpent': 800000,
                'pointBalance': 8000,
                'marketingConsent': True,
                'smsConsent': True,
                'emailConsent': True,
                'createdAt': firestore.SERVER_TIMESTAMP,
                'lastVisit': datetime.now() - timedelta(days=15),
                'status': 'active'
            },
            {
                'customerCode': 'BC2024002',
                'name': '이민정',
                'phone': '010-2345-6789',
                'email': 'minjeong.lee@example.com',
                'birthDate': datetime(1988, 7, 22),
                'gender': 'female',
                'skinType': 'dry',
                'skinConcerns': ['wrinkles', 'volume_loss'],
                'membershipLevel': 'gold',
                'totalSpent': 1500000,
                'pointBalance': 15000,
                'marketingConsent': True,
                'smsConsent': True,
                'emailConsent': True,
                'createdAt': firestore.SERVER_TIMESTAMP,
                'lastVisit': datetime.now() - timedelta(days=7),
                'status': 'active'
            }
        ]
        
        customer_refs = []
        for customer in sample_customers:
            doc_ref = db.collection('customers').add(customer)
            customer_refs.append(doc_ref[1])
            print(f"  ✅ 고객 추가: {customer['name']} ({customer['customerCode']})")
        
        # 5. 프로모션 생성
        print("🎁 프로모션 생성 중...")
        promotions = [
            {
                'code': 'WELCOME10',
                'name': '신규 고객 10% 할인',
                'description': '첫 방문 고객 대상 10% 할인 혜택',
                'discountType': 'percentage',
                'discountValue': 10,
                'minPurchaseAmount': 100000,
                'usageLimitPerCustomer': 1,
                'totalUsageLimit': 100,
                'currentUsageCount': 5,
                'startDate': datetime.now(),
                'endDate': datetime.now() + timedelta(days=30),
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            },
            {
                'code': 'VIP20',
                'name': 'VIP 고객 20% 할인',
                'description': 'VIP 멤버십 고객 대상 특별 할인',
                'discountType': 'percentage',
                'discountValue': 20,
                'minPurchaseAmount': 200000,
                'customerSegments': ['vip'],
                'usageLimitPerCustomer': 3,
                'startDate': datetime.now(),
                'endDate': datetime.now() + timedelta(days=365),
                'isActive': True,
                'createdAt': firestore.SERVER_TIMESTAMP
            }
        ]
        
        for promotion in promotions:
            doc_ref = db.collection('promotions').add(promotion)
            print(f"  ✅ 프로모션 추가: {promotion['name']}")
        
        # 6. 샘플 예약 생성
        print("📅 샘플 예약 생성 중...")
        if customer_refs:
            appointment_data = {
                'appointmentNumber': f"APT{datetime.now().strftime('%Y%m%d')}001",
                'customerId': customer_refs[0].id,
                'treatmentDetails': '보톡스 (이마) 시술',
                'appointmentDate': datetime.now() + timedelta(days=3),
                'startTime': '14:00',
                'endTime': '14:15',
                'status': 'scheduled',
                'finalPrice': 200000,
                'paymentStatus': 'pending',
                'createdAt': firestore.SERVER_TIMESTAMP,
                'createdBy': 'ai_chatbot',
                'location': '엘리트 뷰티 클리닉 강남점'
            }
            
            doc_ref = db.collection('appointments').add(appointment_data)
            print(f"  ✅ 예약 추가: {appointment_data['appointmentNumber']}")
        
        print("\n🎉 Firestore 초기 데이터 생성 완료!")
        print("📊 생성된 데이터:")
        print("  - 시술 카테고리: 3개")
        print("  - 시술 정보: 5개")
        print("  - 직원 정보: 3명")
        print("  - 샘플 고객: 2명")
        print("  - 프로모션: 2개")
        print("  - 샘플 예약: 1개")
        
        return True
        
    except ImportError as e:
        print(f"❌ 필요한 라이브러리가 설치되지 않았습니다: {e}")
        print("📦 다음 명령어로 설치해주세요:")
        print("pip install firebase-admin google-cloud-firestore")
        return False
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("🔍 문제 해결 방법:")
        print("1. 서비스 계정 키 파일 경로 확인")
        print("2. 프로젝트 ID 확인") 
        print("3. Firestore API 활성화 확인")
        return False

def test_connection():
    """Firestore 연결 테스트"""
    try:
        print("\n🧪 Firestore 연결 테스트 중...")
        
        import firebase_admin
        from firebase_admin import firestore
        
        db = firestore.client()
        
        # 테스트 쿼리
        treatments = db.collection('treatments').limit(3).get()
        customers = db.collection('customers').limit(2).get()
        
        print("✅ 연결 테스트 성공!")
        print(f"📊 시술 정보: {len(treatments)}개")
        print(f"👤 고객 정보: {len(customers)}개")
        
        # 샘플 데이터 출력
        print("\n📋 샘플 데이터:")
        for treatment in treatments:
            data = treatment.to_dict()
            print(f"  - {data.get('name')}: {data.get('price'):,}원")
        
        return True
        
    except Exception as e:
        print(f"❌ 연결 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("🔥 Firestore 초기화 스크립트 실행")
    print("=" * 50)
    
    # 초기 데이터 생성
    if setup_firestore():
        # 연결 테스트
        test_connection()
        
        print("\n🚀 다음 단계:")
        print("1. 실제 함수 테스트 실행")
        print("2. AI 챗봇과 연동 테스트")
        print("3. 웹 인터페이스 구축")
        
    else:
        print("\n❌ 초기화 실패")
        print("위 안내에 따라 문제를 해결한 후 다시 실행해주세요.")
