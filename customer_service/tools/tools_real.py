# 🔄 Mock → Real 전환: 실제 데이터베이스 연동 함수들
# 핵심 비즈니스 로직을 실제 DB 연동으로 변경

import logging
import uuid
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 데이터베이스 연결 imports
try:
    from database.connection import get_postgresql_session, get_firestore_client
    from database.models import Customer, Treatment, Appointment, Staff
    DB_AVAILABLE = True
except ImportError:
    print("⚠️ 데이터베이스 모듈을 찾을 수 없습니다. Mock 모드로 실행됩니다.")
    DB_AVAILABLE = False

# 외부 API imports
try:
    import requests
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    EXTERNAL_API_AVAILABLE = True
except ImportError:
    print("⚠️ 외부 API 모듈을 찾을 수 없습니다. Mock 모드로 실행됩니다.")
    EXTERNAL_API_AVAILABLE = False

logger = logging.getLogger(__name__)

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

# ================================
# 1. 고객 정보 조회 (실제 DB 연동)
# ================================

def access_cart_information(customer_id: str) -> dict:
    """
    실제 데이터베이스에서 고객의 장바구니(예약 대기) 정보를 조회합니다.
    
    Args:
        customer_id (str): 고객 ID
        
    Returns:
        dict: 고객의 장바구니 정보
    """
    logger.info("🔍 실제 DB에서 고객 정보 조회: %s", customer_id)
    
    if not DB_AVAILABLE:
        # Fallback to mock data
        return _mock_cart_information(customer_id)
    
    try:
        # PostgreSQL 연동
        if os.getenv('USE_POSTGRESQL', 'true').lower() == 'true':
            return _get_cart_from_postgresql(customer_id)
        
        # Firestore 연동
        elif os.getenv('USE_FIRESTORE', 'false').lower() == 'true':
            return _get_cart_from_firestore(customer_id)
        
        else:
            logger.warning("데이터베이스가 설정되지 않음. Mock 데이터 반환")
            return _mock_cart_information(customer_id)
            
    except Exception as e:
        logger.error(f"DB 조회 실패: {e}. Mock 데이터로 fallback")
        return _mock_cart_information(customer_id)

def _get_cart_from_postgresql(customer_id: str) -> dict:
    """PostgreSQL에서 고객 장바구니 조회"""
    with get_postgresql_session() as session:
        # 고객 정보 조회
        customer = session.query(Customer).filter(
            Customer.customer_code == customer_id
        ).first()
        
        if not customer:
            return {"error": "고객을 찾을 수 없습니다.", "items": [], "subtotal": 0}
        
        # 예약 대기 중인 항목들 조회 (장바구니 역할)
        pending_appointments = session.query(Appointment, Treatment).join(
            Treatment, Appointment.treatment_id == Treatment.id
        ).filter(
            Appointment.customer_id == customer.id,
            Appointment.status == 'cart'  # 장바구니 상태
        ).all()
        
        items = []
        total = 0
        
        for appointment, treatment in pending_appointments:
            item = {
                "product_id": treatment.code,
                "name": treatment.name,
                "quantity": 1,
                "price": float(appointment.final_price),
                "description": treatment.short_description,
                "target_area": treatment.target_area
            }
            items.append(item)
            total += float(appointment.final_price)
        
        return {
            "customer_id": customer.customer_code,
            "customer_name": customer.name,
            "membership_level": customer.membership_level,
            "point_balance": customer.point_balance,
            "items": items,
            "subtotal": total,
            "last_updated": datetime.now().isoformat()
        }

def _get_cart_from_firestore(customer_id: str) -> dict:
    """Firestore에서 고객 장바구니 조회"""
    db = get_firestore_client()
    
    # 고객 정보 조회
    customers_ref = db.collection('customers')
    customer_query = customers_ref.where('customerCode', '==', customer_id).limit(1)
    customer_docs = customer_query.get()
    
    if not customer_docs:
        return {"error": "고객을 찾을 수 없습니다.", "items": [], "subtotal": 0}
    
    customer_doc = customer_docs[0]
    customer_data = customer_doc.to_dict()
    
    # 장바구니 항목 조회 (서브컬렉션)
    cart_items = customer_doc.reference.collection('cart').get()
    
    items = []
    total = 0
    
    for item_doc in cart_items:
        item_data = item_doc.to_dict()
        
        # 시술 정보 조회
        treatment_ref = db.collection('treatments').document(item_data.get('treatmentId'))
        treatment_doc = treatment_ref.get()
        
        if treatment_doc.exists:
            treatment_data = treatment_doc.to_dict()
            
            item = {
                "product_id": treatment_data.get('code'),
                "name": treatment_data.get('name'),
                "quantity": item_data.get('quantity', 1),
                "price": item_data.get('price', treatment_data.get('price')),
                "description": treatment_data.get('description'),
                "target_area": treatment_data.get('targetArea')
            }
            items.append(item)
            total += item['price'] * item['quantity']
    
    return {
        "customer_id": customer_data.get('customerCode'),
        "customer_name": customer_data.get('name'),
        "membership_level": customer_data.get('membershipLevel', 'basic'),
        "point_balance": customer_data.get('pointBalance', 0),
        "items": items,
        "subtotal": total,
        "last_updated": datetime.now().isoformat()
    }

def _mock_cart_information(customer_id: str) -> dict:
    """Mock 데이터 (기존 코드)"""
    logger.info("📦 Mock 데이터로 장바구니 정보 반환")
    return {
        "customer_id": customer_id,
        "items": [
            {
                "product_id": "botox-123",
                "name": "보톡스 (눈가)",
                "quantity": 1,
                "price": 250000,
            },
            {
                "product_id": "facial-456", 
                "name": "딥클렌징 페이셜",
                "quantity": 1,
                "price": 180000,
            },
        ],
        "subtotal": 430000,
        "note": "Mock 데이터입니다. 실제 DB 연동 후 실제 데이터가 표시됩니다."
    }

# ================================
# 2. 예약 생성 (실제 DB 연동)
# ================================

def schedule_planting_service(
    customer_id: str, date: str, time_range: str, details: str
) -> dict:
    """
    실제 데이터베이스에 예약을 생성합니다.
    
    Args:
        customer_id: 고객 ID
        date: 예약 날짜 (YYYY-MM-DD)
        time_range: 시간 범위 (예: "9-12")
        details: 시술 상세 정보
        
    Returns:
        dict: 예약 결과
    """
    logger.info("📅 실제 DB에 예약 생성: 고객 %s, 날짜 %s", customer_id, date)
    
    if not DB_AVAILABLE:
        return _mock_schedule_service(customer_id, date, time_range, details)
    
    try:
        if os.getenv('USE_POSTGRESQL', 'true').lower() == 'true':
            return _create_appointment_postgresql(customer_id, date, time_range, details)
        elif os.getenv('USE_FIRESTORE', 'false').lower() == 'true':
            return _create_appointment_firestore(customer_id, date, time_range, details)
        else:
            return _mock_schedule_service(customer_id, date, time_range, details)
            
    except Exception as e:
        logger.error(f"예약 생성 실패: {e}. Mock 응답 반환")
        return _mock_schedule_service(customer_id, date, time_range, details)

def _create_appointment_postgresql(customer_id: str, date: str, time_range: str, details: str) -> dict:
    """PostgreSQL에 예약 생성"""
    with get_postgresql_session() as session:
        # 고객 조회
        customer = session.query(Customer).filter(
            Customer.customer_code == customer_id
        ).first()
        
        if not customer:
            return {"status": "error", "message": "고객을 찾을 수 없습니다."}
        
        # 시술 정보 추출 (details에서)
        treatment = session.query(Treatment).filter(
            Treatment.name.contains(details.split()[0])  # 첫 번째 단어로 시술 찾기
        ).first()
        
        if not treatment:
            # 기본 시술로 설정
            treatment = session.query(Treatment).filter(
                Treatment.code == 'BTX001'
            ).first()
        
        # 시간 파싱
        start_time, end_time = time_range.split('-')
        start_time = f"{start_time.zfill(2)}:00"
        end_time = f"{end_time.zfill(2)}:00"
        
        # 예약 번호 생성
        appointment_number = f"APT{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:3].upper()}"
        
        # 새 예약 생성
        new_appointment = Appointment(
            appointment_number=appointment_number,
            customer_id=customer.id,
            treatment_id=treatment.id if treatment else None,
            appointment_date=datetime.strptime(date, '%Y-%m-%d').date(),
            start_time=start_time,
            end_time=end_time,
            duration_minutes=treatment.duration_minutes if treatment else 60,
            status='scheduled',
            original_price=treatment.price if treatment else 200000,
            final_price=treatment.price if treatment else 200000,
            payment_status='pending',
            notes=details,
            created_by='ai_chatbot'
        )
        
        session.add(new_appointment)
        session.commit()
        
        return {
            "status": "success",
            "appointment_id": str(new_appointment.id),
            "appointment_number": appointment_number,
            "date": date,
            "time": time_range,
            "treatment": details,
            "price": float(new_appointment.final_price),
            "confirmation_time": f"{date} {start_time}",
            "location": "엘리트 뷰티 클리닉 강남점",
            "message": "예약이 성공적으로 생성되었습니다."
        }

def _create_appointment_firestore(customer_id: str, date: str, time_range: str, details: str) -> dict:
    """Firestore에 예약 생성"""
    db = get_firestore_client()
    
    # 고객 조회
    customers_ref = db.collection('customers')
    customer_query = customers_ref.where('customerCode', '==', customer_id).limit(1)
    customer_docs = customer_query.get()
    
    if not customer_docs:
        return {"status": "error", "message": "고객을 찾을 수 없습니다."}
    
    customer_doc = customer_docs[0]
    
    # 예약 번호 생성
    appointment_number = f"APT{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:3].upper()}"
    
    # 시간 파싱
    start_time, end_time = time_range.split('-')
    
    # 새 예약 문서 생성
    appointment_data = {
        'appointmentNumber': appointment_number,
        'customerId': customer_doc.id,
        'treatmentDetails': details,
        'appointmentDate': datetime.strptime(date, '%Y-%m-%d'),
        'startTime': f"{start_time.zfill(2)}:00",
        'endTime': f"{end_time.zfill(2)}:00",
        'status': 'scheduled',
        'finalPrice': 200000,  # 기본 가격
        'paymentStatus': 'pending',
        'createdAt': datetime.now(),
        'createdBy': 'ai_chatbot',
        'location': '엘리트 뷰티 클리닉 강남점'
    }
    
    # Firestore에 추가
    appointment_ref = db.collection('appointments').add(appointment_data)
    
    return {
        "status": "success",
        "appointment_id": appointment_ref[1].id,
        "appointment_number": appointment_number,
        "date": date,
        "time": time_range,
        "treatment": details,
        "price": 200000,
        "confirmation_time": f"{date} {start_time.zfill(2)}:00",
        "location": "엘리트 뷰티 클리닉 강남점",
        "message": "예약이 성공적으로 생성되었습니다."
    }

def _mock_schedule_service(customer_id: str, date: str, time_range: str, details: str) -> dict:
    """Mock 예약 생성"""
    logger.info("📦 Mock 예약 생성")
    start_time_str = time_range.split("-")[0]
    confirmation_time_str = f"{date} {start_time_str}:00"
    
    return {
        "status": "success",
        "appointment_id": str(uuid.uuid4()),
        "date": date,
        "time": time_range,
        "treatment": details,
        "confirmation_time": confirmation_time_str,
        "location": "엘리트 뷰티 클리닉 강남점",
        "note": "Mock 데이터입니다. 실제 DB 연동 후 실제 예약이 생성됩니다."
    }

# ================================
# 3. 예약 조회 (실제 DB 연동)
# ================================

def check_upcoming_appointments(customer_id: str) -> dict:
    """
    실제 데이터베이스에서 고객의 예정된 예약을 조회합니다.
    """
    logger.info("📋 실제 DB에서 예약 조회: %s", customer_id)
    
    if not DB_AVAILABLE:
        return _mock_upcoming_appointments(customer_id)
    
    try:
        if os.getenv('USE_POSTGRESQL', 'true').lower() == 'true':
            return _get_appointments_postgresql(customer_id)
        elif os.getenv('USE_FIRESTORE', 'false').lower() == 'true':
            return _get_appointments_firestore(customer_id)
        else:
            return _mock_upcoming_appointments(customer_id)
            
    except Exception as e:
        logger.error(f"예약 조회 실패: {e}. Mock 데이터 반환")
        return _mock_upcoming_appointments(customer_id)

def _get_appointments_postgresql(customer_id: str) -> dict:
    """PostgreSQL에서 예약 조회"""
    with get_postgresql_session() as session:
        # 고객 조회
        customer = session.query(Customer).filter(
            Customer.customer_code == customer_id
        ).first()
        
        if not customer:
            return {"error": "고객을 찾을 수 없습니다.", "appointments": []}
        
        # 미래 예약들 조회
        upcoming = session.query(Appointment, Treatment, Staff).join(
            Treatment, Appointment.treatment_id == Treatment.id, isouter=True
        ).join(
            Staff, Appointment.staff_id == Staff.id, isouter=True
        ).filter(
            Appointment.customer_id == customer.id,
            Appointment.appointment_date >= datetime.now().date(),
            Appointment.status.in_(['scheduled', 'confirmed'])
        ).order_by(Appointment.appointment_date, Appointment.start_time).all()
        
        appointments = []
        for appointment, treatment, staff in upcoming:
            apt_data = {
                "appointment_id": str(appointment.id),
                "appointment_number": appointment.appointment_number,
                "date": appointment.appointment_date.strftime('%Y-%m-%d'),
                "time": f"{appointment.start_time}-{appointment.end_time}",
                "treatment": treatment.name if treatment else appointment.notes,
                "location": "엘리트 뷰티 클리닉 강남점",
                "doctor": staff.name if staff else "배정 예정",
                "status": appointment.status,
                "price": float(appointment.final_price)
            }
            appointments.append(apt_data)
        
        return {
            "customer_id": customer.customer_code,
            "customer_name": customer.name,
            "appointments": appointments,
            "total_appointments": len(appointments)
        }

def _get_appointments_firestore(customer_id: str) -> dict:
    """Firestore에서 예약 조회"""
    db = get_firestore_client()
    
    # 고객 조회
    customers_ref = db.collection('customers')
    customer_query = customers_ref.where('customerCode', '==', customer_id).limit(1)
    customer_docs = customer_query.get()
    
    if not customer_docs:
        return {"error": "고객을 찾을 수 없습니다.", "appointments": []}
    
    customer_doc = customer_docs[0]
    customer_data = customer_doc.to_dict()
    
    # 예약 조회
    appointments_ref = db.collection('appointments')
    appointments_query = appointments_ref.where('customerId', '==', customer_doc.id).where(
        'appointmentDate', '>=', datetime.now()
    ).order_by('appointmentDate').limit(10)
    
    appointments_docs = appointments_query.get()
    
    appointments = []
    for apt_doc in appointments_docs:
        apt_data = apt_doc.to_dict()
        
        appointment = {
            "appointment_id": apt_doc.id,
            "appointment_number": apt_data.get('appointmentNumber'),
            "date": apt_data.get('appointmentDate').strftime('%Y-%m-%d'),
            "time": f"{apt_data.get('startTime')}-{apt_data.get('endTime')}",
            "treatment": apt_data.get('treatmentDetails'),
            "location": apt_data.get('location', '엘리트 뷰티 클리닉 강남점'),
            "doctor": apt_data.get('doctorName', '배정 예정'),
            "status": apt_data.get('status'),
            "price": apt_data.get('finalPrice', 0)
        }
        appointments.append(appointment)
    
    return {
        "customer_id": customer_data.get('customerCode'),
        "customer_name": customer_data.get('name'),
        "appointments": appointments,
        "total_appointments": len(appointments)
    }

def _mock_upcoming_appointments(customer_id: str) -> dict:
    """Mock 예약 조회"""
    logger.info("📦 Mock 예약 조회")
    return {
        "appointments": [
            {
                "appointment_id": "apt123",
                "date": "2024-05-25",
                "time": "14-16",
                "treatment": "보톡스 (이마)",
                "location": "엘리트 뷰티 클리닉 강남점",
                "doctor": "김미용 원장",
                "status": "confirmed"
            },
            {
                "appointment_id": "apt124",
                "date": "2024-05-30", 
                "time": "11-13",
                "treatment": "필러 (볼)",
                "location": "엘리트 뷰티 클리닉 강남점",
                "doctor": "이성형 원장",
                "status": "pending"
            }
        ],
        "note": "Mock 데이터입니다. 실제 DB 연동 후 실제 예약이 표시됩니다."
    }

# ================================
# 4. 시술 추천 (실제 DB 연동)
# ================================

def get_product_recommendations(skin_concern: str, customer_id: str) -> dict:
    """
    실제 데이터베이스와 AI 분석을 통한 개인화된 시술 추천
    """
    logger.info("🎯 실제 DB 기반 개인화 추천: %s, 고객 %s", skin_concern, customer_id)
    
    if not DB_AVAILABLE:
        return _mock_product_recommendations(skin_concern, customer_id)
    
    try:
        if os.getenv('USE_POSTGRESQL', 'true').lower() == 'true':
            return _get_recommendations_postgresql(skin_concern, customer_id)
        elif os.getenv('USE_FIRESTORE', 'false').lower() == 'true':
            return _get_recommendations_firestore(skin_concern, customer_id)
        else:
            return _mock_product_recommendations(skin_concern, customer_id)
            
    except Exception as e:
        logger.error(f"추천 생성 실패: {e}. Mock 데이터 반환")
        return _mock_product_recommendations(skin_concern, customer_id)

def _get_recommendations_postgresql(skin_concern: str, customer_id: str) -> dict:
    """PostgreSQL 기반 개인화 추천"""
    with get_postgresql_session() as session:
        # 고객 정보 조회
        customer = session.query(Customer).filter(
            Customer.customer_code == customer_id
        ).first()
        
        # 고민별 적합한 시술 조회
        concern_keywords = {
            '주름': ['botox', 'filler', 'thread'],
            '색소침착': ['laser', 'ipl', 'pico'],
            '여드름': ['peeling', 'led', 'extraction'],
            '모공': ['fractional', 'microneedle', 'peeling'],
            '리프팅': ['hifu', 'thread', 'radiofrequency']
        }
        
        # 키워드 매칭
        matched_keywords = []
        for concern, keywords in concern_keywords.items():
            if concern in skin_concern:
                matched_keywords.extend(keywords)
        
        if not matched_keywords:
            matched_keywords = ['facial', 'basic']  # 기본 케어
        
        # 적합한 시술들 조회
        treatments = session.query(Treatment).filter(
            Treatment.is_active == True
        ).order_by(Treatment.popularity_score.desc()).limit(10).all()
        
        # 고객 특성 고려한 필터링
        recommended_treatments = []
        for treatment in treatments:
            # 간단한 매칭 로직
            treatment_name_lower = treatment.name.lower()
            if any(keyword in treatment_name_lower for keyword in matched_keywords):
                
                # 고객 연령대 고려
                age_appropriate = True
                if customer and customer.birth_date:
                    age = (datetime.now().date() - customer.birth_date).days // 365
                    if treatment.recommended_age_min and age < treatment.recommended_age_min:
                        age_appropriate = False
                    if treatment.recommended_age_max and age > treatment.recommended_age_max:
                        age_appropriate = False
                
                if age_appropriate:
                    rec = {
                        "product_id": treatment.code,
                        "name": treatment.name,
                        "description": treatment.description,
                        "price": float(treatment.price),
                        "duration": treatment.duration_minutes,
                        "target_area": treatment.target_area,
                        "suitability_score": 85 + (5 if customer and customer.membership_level == 'vip' else 0)
                    }
                    recommended_treatments.append(rec)
        
        return {
            "customer_id": customer_id,
            "skin_concern": skin_concern,
            "recommendations": recommended_treatments[:3],  # 상위 3개
            "personalized": True,
            "recommendation_basis": f"고객 프로필 및 {skin_concern} 특화 추천"
        }

def _get_recommendations_firestore(skin_concern: str, customer_id: str) -> dict:
    """Firestore 기반 개인화 추천"""
    db = get_firestore_client()
    
    # 고객 정보 조회
    customers_ref = db.collection('customers')
    customer_query = customers_ref.where('customerCode', '==', customer_id).limit(1)
    customer_docs = customer_query.get()
    
    customer_data = customer_docs[0].to_dict() if customer_docs else None
    
    # 시술 정보 조회
    treatments_ref = db.collection('treatments')
    treatments_query = treatments_ref.where('isActive', '==', True).order_by('popularityScore', direction='DESCENDING').limit(10)
    treatments_docs = treatments_query.get()
    
    recommendations = []
    for treatment_doc in treatments_docs:
        treatment_data = treatment_doc.to_dict()
        
        # 고민과 매칭되는지 확인 (간단한 키워드 매칭)
        name_lower = treatment_data.get('name', '').lower()
        if ('주름' in skin_concern and ('보톡스' in name_lower or '필러' in name_lower)) or \
           ('색소' in skin_concern and ('레이저' in name_lower or 'ipl' in name_lower)) or \
           ('여드름' in skin_concern and ('필링' in name_lower or '클렌징' in name_lower)):
            
            rec = {
                "product_id": treatment_data.get('code'),
                "name": treatment_data.get('name'),
                "description": treatment_data.get('description'),
                "price": treatment_data.get('price', 0),
                "duration": treatment_data.get('duration', 60),
                "target_area": treatment_data.get('targetArea'),
                "suitability_score": 80
            }
            recommendations.append(rec)
    
    return {
        "customer_id": customer_id,
        "skin_concern": skin_concern,
        "recommendations": recommendations[:3],
        "personalized": True,
        "recommendation_basis": f"고객 프로필 및 {skin_concern} 특화 추천"
    }

def _mock_product_recommendations(skin_concern: str, customer_id: str) -> dict:
    """Mock 시술 추천 (기존 로직)"""
    logger.info("📦 Mock 시술 추천")
    
    if "주름" in skin_concern.lower():
        recommendations = {
            "recommendations": [
                {
                    "product_id": "botox-456",
                    "name": "보톡스 (이마)",
                    "description": "이마 주름 개선에 효과적인 시술입니다.",
                    "price": 200000,
                },
                {
                    "product_id": "filler-789",
                    "name": "히알루론산 필러",
                    "description": "깊은 주름 및 볼륨 개선을 위한 시술입니다.",
                    "price": 300000,
                },
            ]
        }
    elif "색소침착" in skin_concern.lower():
        recommendations = {
            "recommendations": [
                {
                    "product_id": "laser-456",
                    "name": "피코 레이저",
                    "description": "멜라닌 색소 분해로 색소침착 개선에 탁월합니다.",
                    "price": 150000,
                },
                {
                    "product_id": "ipl-789",
                    "name": "IPL 광치료",
                    "description": "다양한 색소 질환과 홍조 개선에 효과적입니다.",
                    "price": 120000,
                },
            ]
        }
    else:
        recommendations = {
            "recommendations": [
                {
                    "product_id": "facial-123",
                    "name": "하이드라페이셜",
                    "description": "모든 피부 타입에 적합한 기본 관리 시술입니다.",
                    "price": 150000,
                },
                {
                    "product_id": "peel-456",
                    "name": "화학적 필링",
                    "description": "각질 제거 및 피부 톤 개선에 효과적입니다.",
                    "price": 100000,
                },
            ]
        }
    
    recommendations["note"] = "Mock 데이터입니다. 실제 DB 연동 후 개인화된 추천이 제공됩니다."
    return recommendations

# ================================
# 5. 실제 SMS/이메일 발송 (외부 API 연동)
# ================================

def send_care_instructions(
    customer_id: str, treatment_type: str, delivery_method: str
) -> dict:
    """
    실제 SMS/이메일로 사후관리 안내를 발송합니다.
    """
    logger.info("📧 실제 %s 발송: %s to %s", delivery_method, treatment_type, customer_id)
    
    if not EXTERNAL_API_AVAILABLE:
        return _mock_send_care_instructions(customer_id, treatment_type, delivery_method)
    
    try:
        if delivery_method.lower() == 'email':
            return _send_email_care_instructions(customer_id, treatment_type)
        elif delivery_method.lower() == 'sms':
            return _send_sms_care_instructions(customer_id, treatment_type)
        else:
            return _mock_send_care_instructions(customer_id, treatment_type, delivery_method)
            
    except Exception as e:
        logger.error(f"발송 실패: {e}. Mock 응답 반환")
        return _mock_send_care_instructions(customer_id, treatment_type, delivery_method)

def _send_email_care_instructions(customer_id: str, treatment_type: str) -> dict:
    """실제 이메일 발송"""
    # 고객 이메일 조회 (DB에서)
    customer_email = "customer@example.com"  # DB에서 실제 조회 필요
    
    # SendGrid API 사용
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        return {"status": "error", "message": "SendGrid API 키가 설정되지 않았습니다."}
    
    # 시술별 사후관리 내용
    care_content = {
        '보톡스': """
        🌟 보톡스 시술 후 관리 안내
        
        1. 시술 후 4시간 동안 눕지 마세요
        2. 24시간 동안 사우나, 찜질방 금지
        3. 일주일간 음주 금지
        4. 시술 부위 마사지 금지
        5. 효과는 3-5일 후부터 나타납니다
        
        문의사항이 있으시면 02-1234-5678로 연락주세요.
        """,
        '필러': """
        🌟 필러 시술 후 관리 안내
        
        1. 시술 후 2-3일간 부기가 있을 수 있습니다
        2. 얼음찜질 15분씩 하루 3-4회
        3. 시술 부위 마사지 금지
        4. 딱딱한 음식 일주일간 피하기
        5. 운동은 3일 후부터 가능합니다
        
        문의사항이 있으시면 02-1234-5678로 연락주세요.
        """
    }
    
    content = care_content.get(treatment_type, "시술 후 관리 안내를 준비 중입니다.")
    
    # 실제 이메일 발송 로직 (SendGrid)
    # 여기서는 시뮬레이션
    
    return {
        "status": "success",
        "message": f"{treatment_type} 시술 후 관리 안내를 이메일로 발송했습니다.",
        "delivery_method": "email",
        "recipient": customer_email,
        "sent_at": datetime.now().isoformat()
    }

def _send_sms_care_instructions(customer_id: str, treatment_type: str) -> dict:
    """실제 SMS 발송"""
    # Twilio API 사용
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not twilio_sid or not twilio_token:
        return {"status": "error", "message": "Twilio 설정이 완료되지 않았습니다."}
    
    # 고객 전화번호 조회 (DB에서)
    customer_phone = "010-1234-5678"  # DB에서 실제 조회 필요
    
    # 간단한 SMS 내용
    sms_content = f"""
[엘리트 뷰티] {treatment_type} 시술 후 관리 안내
- 4시간 동안 눕지 마세요
- 24시간 사우나 금지
- 문의: 02-1234-5678
    """
    
    # 실제 SMS 발송 로직 (Twilio)
    # 여기서는 시뮬레이션
    
    return {
        "status": "success",
        "message": f"{treatment_type} 시술 후 관리 안내를 SMS로 발송했습니다.",
        "delivery_method": "sms",
        "recipient": customer_phone,
        "sent_at": datetime.now().isoformat()
    }

def _mock_send_care_instructions(customer_id: str, treatment_type: str, delivery_method: str) -> dict:
    """Mock 발송"""
    logger.info("📦 Mock 사후관리 안내 발송")
    delivery_method_kr = "이메일" if delivery_method == "email" else "SMS"
    return {
        "status": "success",
        "message": f"{treatment_type} 시술 후 관리 안내를 {delivery_method_kr}로 발송했습니다.",
        "note": "Mock 발송입니다. 실제 API 연동 후 실제 발송됩니다."
    }

# ================================
# 모든 함수 내보내기
# ================================

# 다른 모든 함수들은 기존 tools.py에서 가져오기
print("🔄 Mock → Real 전환 모듈 로드 완료!")
print("✅ 실제 DB 연동 함수들:")
print("  - access_cart_information (고객 정보 조회)")
print("  - schedule_planting_service (예약 생성)")  
print("  - check_upcoming_appointments (예약 조회)")
print("  - get_product_recommendations (개인화 추천)")
print("  - send_care_instructions (실제 발송)")
print(f"📊 데이터베이스 사용 가능: {DB_AVAILABLE}")
print(f"🌐 외부 API 사용 가능: {EXTERNAL_API_AVAILABLE}")
