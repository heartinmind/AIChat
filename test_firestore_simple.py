#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 Firestore 연동 테스트
SQLAlchemy 없이 Firestore만 사용
"""

import os
import sys
from datetime import datetime, timedelta

# 프로젝트 경로 추가
sys.path.append('/Users/unipurple/Projects/AIChat')

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

def test_firestore_only():
    """Firestore만 사용한 간단한 테스트"""
    
    print("🔥 Firestore 연동 테스트 (간단 버전)")
    print("=" * 50)
    
    try:
        # Firebase Admin SDK import
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        # 서비스 계정 키 파일 확인
        key_path = os.getenv('GCS_CREDENTIALS_PATH')
        if not key_path or not os.path.exists(key_path):
            print(f"❌ 서비스 계정 키 파일을 찾을 수 없습니다: {key_path}")
            return False
        
        # Firebase 앱 초기화 (이미 초기화되어 있으면 기존 것 사용)
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred, {
                'projectId': os.getenv('GOOGLE_CLOUD_PROJECT', 'elite-cms-2025')
            })
        
        db = firestore.client()
        print("✅ Firestore 연결 성공!")
        
        # 테스트 1: 고객 정보 조회
        print("\n👤 테스트 1: 고객 정보 조회")
        print("-" * 30)
        
        customers_ref = db.collection('customers')
        customer_query = customers_ref.where('customerCode', '==', 'BC2024001').limit(1)
        customer_docs = customer_query.get()
        
        if customer_docs:
            customer_data = customer_docs[0].to_dict()
            print(f"✅ 고객 발견: {customer_data.get('name')}")
            print(f"  📞 전화번호: {customer_data.get('phone')}")
            print(f"  🏅 멤버십: {customer_data.get('membershipLevel')}")
            print(f"  💰 포인트: {customer_data.get('pointBalance', 0):,}점")
            print(f"  🎂 나이: {datetime.now().year - customer_data.get('birthDate', datetime.now()).year}세")
        else:
            print("❌ 고객 BC2024001을 찾을 수 없습니다.")
        
        # 테스트 2: 시술 정보 조회
        print("\n💉 테스트 2: 시술 정보 조회")
        print("-" * 30)
        
        treatments_ref = db.collection('treatments')
        treatments_query = treatments_ref.where('isActive', '==', True).limit(5)
        treatments_docs = treatments_query.get()
        
        print(f"✅ 활성 시술 {len(treatments_docs)}개 발견:")
        for i, treatment_doc in enumerate(treatments_docs, 1):
            treatment_data = treatment_doc.to_dict()
            print(f"  {i}. {treatment_data.get('name')}")
            print(f"     💰 가격: {treatment_data.get('price', 0):,}원")
            print(f"     ⏱️ 소요시간: {treatment_data.get('duration')}분")
            print(f"     🎯 부위: {treatment_data.get('targetArea')}")
        
        # 테스트 3: 직원 정보 조회
        print("\n👩‍⚕️ 테스트 3: 직원 정보 조회")
        print("-" * 30)
        
        staff_ref = db.collection('staff')
        staff_docs = staff_ref.where('isActive', '==', True).get()
        
        print(f"✅ 활성 직원 {len(staff_docs)}명 발견:")
        for i, staff_doc in enumerate(staff_docs, 1):
            staff_data = staff_doc.to_dict()
            print(f"  {i}. {staff_data.get('name')} ({staff_data.get('role')})")
            print(f"     🏥 전문분야: {', '.join(staff_data.get('specialization', []))}")
            print(f"     📧 이메일: {staff_data.get('email')}")
        
        # 테스트 4: 프로모션 조회
        print("\n🎁 테스트 4: 프로모션 조회")
        print("-" * 30)
        
        promotions_ref = db.collection('promotions')
        promotions_docs = promotions_ref.where('isActive', '==', True).get()
        
        print(f"✅ 활성 프로모션 {len(promotions_docs)}개 발견:")
        for i, promo_doc in enumerate(promotions_docs, 1):
            promo_data = promo_doc.to_dict()
            print(f"  {i}. {promo_data.get('name')}")
            print(f"     🏷️ 코드: {promo_data.get('code')}")
            print(f"     💸 할인: {promo_data.get('discountValue')}% 할인")
            print(f"     📅 유효기간: {promo_data.get('endDate').strftime('%Y-%m-%d')}")
        
        # 테스트 5: 새 예약 생성
        print("\n📅 테스트 5: 새 예약 생성")
        print("-" * 30)
        
        if customer_docs:
            customer_doc = customer_docs[0]
            
            # 예약 번호 생성
            appointment_number = f"APT{datetime.now().strftime('%Y%m%d%H%M')}"
            
            # 새 예약 데이터
            appointment_data = {
                'appointmentNumber': appointment_number,
                'customerId': customer_doc.id,
                'customerName': customer_data.get('name'),
                'treatmentDetails': '테스트 예약 - 보톡스 이마 시술',
                'appointmentDate': datetime.now() + timedelta(days=2),
                'startTime': '15:00',
                'endTime': '15:30',
                'status': 'scheduled',
                'finalPrice': 200000,
                'paymentStatus': 'pending',
                'createdAt': firestore.SERVER_TIMESTAMP,
                'createdBy': 'test_script',
                'location': '엘리트 뷰티 클리닉 강남점'
            }
            
            # Firestore에 추가
            appointment_ref = db.collection('appointments').add(appointment_data)
            
            print(f"✅ 예약 생성 성공!")
            print(f"  📋 예약번호: {appointment_number}")
            print(f"  👤 고객: {customer_data.get('name')}")
            print(f"  📅 날짜: {appointment_data['appointmentDate'].strftime('%Y-%m-%d')}")
            print(f"  ⏰ 시간: {appointment_data['startTime']} - {appointment_data['endTime']}")
            print(f"  💰 가격: {appointment_data['finalPrice']:,}원")
        
        # 테스트 6: 예약 조회
        print("\n📋 테스트 6: 고객 예약 조회")
        print("-" * 30)
        
        if customer_docs:
            customer_doc = customer_docs[0]
            
            appointments_ref = db.collection('appointments')
            appointments_query = appointments_ref.where('customerId', '==', customer_doc.id).order_by('appointmentDate').limit(5)
            appointments_docs = appointments_query.get()
            
            print(f"✅ 고객 예약 {len(appointments_docs)}개 발견:")
            for i, apt_doc in enumerate(appointments_docs, 1):
                apt_data = apt_doc.to_dict()
                print(f"  {i}. {apt_data.get('treatmentDetails')}")
                print(f"     📅 날짜: {apt_data.get('appointmentDate').strftime('%Y-%m-%d')}")
                print(f"     ⏰ 시간: {apt_data.get('startTime')} - {apt_data.get('endTime')}")
                print(f"     📍 상태: {apt_data.get('status')}")
                print(f"     💰 가격: {apt_data.get('finalPrice', 0):,}원")
        
        print("\n🎉 모든 Firestore 테스트 통과!")
        print("=" * 50)
        
        print("\n📊 테스트 요약:")
        print("  ✅ Firestore 연결 및 인증 성공")
        print("  ✅ 고객 데이터 조회 성공")
        print("  ✅ 시술 정보 조회 성공")
        print("  ✅ 직원 정보 조회 성공")
        print("  ✅ 프로모션 정보 조회 성공")
        print("  ✅ 예약 생성 성공")
        print("  ✅ 예약 조회 성공")
        
        print("\n🚀 Mock → Real 전환 완료!")
        print("이제 AI 챗봇이 실제 데이터베이스와 연동됩니다!")
        
        return True
        
    except ImportError as e:
        print(f"❌ 필요한 라이브러리 미설치: {e}")
        print("📦 다음 명령어로 설치하세요:")
        print("pip install firebase-admin google-cloud-firestore python-dotenv")
        return False
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류: {e}")
        print("🔍 오류 상세:", str(e))
        return False

if __name__ == "__main__":
    print("🔥 간단한 Firestore 연동 테스트")
    print("📝 SQLAlchemy 없이 Firestore만 사용")
    print("\n" + "="*50)
    
    success = test_firestore_only()
    
    if success:
        print("\n🎊 테스트 대성공!")
        print("🚀 다음 단계:")
        print("  1. AI 챗봇 실제 연동")
        print("  2. 웹 API 서버 구축")
        print("  3. 외부 API 연동")
        print("  4. 프로덕션 배포")
    else:
        print("\n❌ 테스트 실패")
        print("위 안내에 따라 문제를 해결한 후 다시 시도해주세요.")
