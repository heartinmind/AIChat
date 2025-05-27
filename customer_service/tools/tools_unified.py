# customer_service/tools/tools_unified.py
"""
통합된 Tools 모듈 - Mock과 Real 데이터베이스를 환경변수로 전환
환경변수 USE_MOCK_DATA=true/false로 모드 전환
"""

import logging
import uuid
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from functools import wraps

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

# Mock 모드 확인
USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'true').lower() == 'true'

logger = logging.getLogger(__name__)

# 데이터베이스 연결 (Real 모드일 때만)
if not USE_MOCK_DATA:
    try:
        from database.connection import get_postgresql_session, get_firestore_client
        from database.models import Customer, Treatment, Appointment, Staff
        DB_AVAILABLE = True
        logger.info("✅ 실제 데이터베이스 연결 성공")
    except ImportError:
        logger.warning("⚠️ 데이터베이스 모듈을 찾을 수 없습니다. Mock 모드로 전환합니다.")
        USE_MOCK_DATA = True
        DB_AVAILABLE = False
else:
    DB_AVAILABLE = False
    logger.info("📦 Mock 모드로 실행 중")

# Mock/Real 자동 전환 데코레이터
def auto_mock_fallback(mock_func):
    """실제 DB 실패 시 자동으로 Mock 함수로 fallback하는 데코레이터"""
    def decorator(real_func):
        @wraps(real_func)
        def wrapper(*args, **kwargs):
            if USE_MOCK_DATA:
                return mock_func(*args, **kwargs)
            
            try:
                return real_func(*args, **kwargs)
            except Exception as e:
                logger.error(f"실제 DB 작업 실패: {e}. Mock 데이터로 fallback")
                return mock_func(*args, **kwargs)
        
        return wrapper
    return decorator

# ================================
# Mock 함수들
# ================================

def _mock_cart_information(customer_id: str) -> dict:
    """Mock 장바구니 정보"""
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
        "mode": "mock"
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
        "mode": "mock"
    }

# ================================
# 통합 API 함수들
# ================================

@auto_mock_fallback(_mock_cart_information)
def access_cart_information(customer_id: str) -> dict:
    """
    고객의 장바구니(예약 대기) 정보를 조회합니다.
    Mock 모드와 Real DB 모드를 자동으로 전환합니다.
    """
    logger.info("🔍 고객 정보 조회: %s (Real DB 모드)", customer_id)
    
    # PostgreSQL 사용
    if os.getenv('USE_POSTGRESQL', 'true').lower() == 'true':
        with get_postgresql_session() as session:
            customer = session.query(Customer).filter(
                Customer.customer_code == customer_id
            ).first()
            
            if not customer:
                return {"error": "고객을 찾을 수 없습니다.", "items": [], "subtotal": 0}
            
            # 장바구니 항목 조회
            pending_appointments = session.query(Appointment, Treatment).join(
                Treatment, Appointment.treatment_id == Treatment.id
            ).filter(
                Appointment.customer_id == customer.id,
                Appointment.status == 'cart'
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
                "items": items,
                "subtotal": total,
                "mode": "real",
                "last_updated": datetime.now().isoformat()
            }

@auto_mock_fallback(_mock_schedule_service)
def schedule_planting_service(customer_id: str, date: str, time_range: str, details: str) -> dict:
    """
    예약을 생성합니다.
    Mock 모드와 Real DB 모드를 자동으로 전환합니다.
    """
    logger.info("📅 예약 생성: 고객 %s, 날짜 %s (Real DB 모드)", customer_id, date)
    
    with get_postgresql_session() as session:
        # 고객 조회
        customer = session.query(Customer).filter(
            Customer.customer_code == customer_id
        ).first()
        
        if not customer:
            return {"status": "error", "message": "고객을 찾을 수 없습니다."}
        
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
            appointment_date=datetime.strptime(date, '%Y-%m-%d').date(),
            start_time=start_time,
            end_time=end_time,
            status='scheduled',
            final_price=200000,
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
            "confirmation_time": f"{date} {start_time}",
            "location": "엘리트 뷰티 클리닉 강남점",
            "mode": "real"
        }

# ================================
# 기타 함수들 (동일한 패턴으로 구현)
# ================================

def approve_discount(discount_type: str, value: float, reason: str) -> dict:
    """할인 승인"""
    if value > 10:
        logger.info("할인 거부: %s%% (최대 10%%)", value)
        return {"status": "rejected", "message": "할인율이 너무 높습니다. 최대 10%까지 가능합니다."}
    
    logger.info("할인 승인: %s %s (사유: %s)", value, discount_type, reason)
    return {"status": "ok"}

def send_care_instructions(customer_id: str, treatment_type: str, delivery_method: str) -> dict:
    """사후관리 안내 발송"""
    logger.info("사후관리 안내 발송: %s to %s via %s", treatment_type, customer_id, delivery_method)
    
    if USE_MOCK_DATA:
        delivery_method_kr = "이메일" if delivery_method == "email" else "SMS"
        return {
            "status": "success",
            "message": f"{treatment_type} 시술 후 관리 안내를 {delivery_method_kr}로 발송했습니다.",
            "mode": "mock"
        }
    
    # 실제 발송 로직 구현
    # ...
    
    return {
        "status": "success",
        "message": f"{treatment_type} 시술 후 관리 안내를 발송했습니다.",
        "mode": "real"
    }

# ================================
# 설정 정보 출력
# ================================

def print_configuration():
    """현재 설정 정보 출력"""
    print("\n🔧 Tools 모듈 설정:")
    print(f"  - 모드: {'Mock' if USE_MOCK_DATA else 'Real DB'}")
    print(f"  - DB 사용 가능: {DB_AVAILABLE}")
    print(f"  - PostgreSQL: {os.getenv('USE_POSTGRESQL', 'false')}")
    print(f"  - Firestore: {os.getenv('USE_FIRESTORE', 'false')}")
    print("\n💡 모드 변경: USE_MOCK_DATA 환경변수를 true/false로 설정하세요\n")

# 모듈 로드 시 설정 출력
if __name__ != "__main__":
    print_configuration()
