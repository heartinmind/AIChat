# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# add docstring to this module
"""Tools module for the customer service agent."""

import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Conditional import for google.adk with fallback
try:
    from google.adk.tools import ToolContext
except ImportError:
    # Mock ToolContext for testing environments
    class ToolContext:
        """Mock ToolContext for environments where google.adk is not available."""
        pass

logger = logging.getLogger(__name__)


def send_call_companion_link(phone_number: str) -> str:
    """
    Sends a link to the user's phone number to start a video session.

    Args:
        phone_number (str): The phone number to send the link to.

    Returns:
        dict: A dictionary with the status and message.

    Example:
        >>> send_call_companion_link(phone_number='+12065550123')
        {'status': 'success', 'message': 'Link sent to +12065550123'}
    """

    logger.info("Sending call companion link to %s", phone_number)

    return {"status": "success", "message": f"Link sent to {phone_number}"}


def approve_discount(discount_type: str, value: float, reason: str) -> dict:
    """
    Approve the flat rate or percentage discount requested by the user.

    Args:
        discount_type (str): The type of discount, either "percentage" or "flat".
        value (float): The value of the discount.
        reason (str): The reason for the discount.

    Returns:
        dict: A dictionary indicating the status of the approval.

    Example:
        >>> approve_discount(type='percentage', value=10.0, reason='Customer loyalty')
        {"status": "ok"}
    """
    if value > 10:
        logger.info("Denying %s discount of %s", discount_type, value)
        # Send back a reason for the error so that the model can recover.
        return {"status": "rejected",
                "message": "discount too large. Must be 10 or less."}
    logger.info(
        "Approving a %s discount of %s because %s", discount_type, value, reason
    )
    return {"status": "ok"}

def sync_ask_for_approval(discount_type: str, value: float, reason: str) -> dict:
    """
    Asks the manager for approval for a discount.

    Args:
        discount_type (str): The type of discount, either "percentage" or "flat".
        value (float): The value of the discount.
        reason (str): The reason for the discount.

    Returns:
        dict: A dictionary indicating the status of the approval.

    Example:
        >>> sync_ask_for_approval(type='percentage', value=15, reason='Customer loyalty')
        {"status": "approved"}
    """
    logger.info(
        "Asking for approval for a %s discount of %s because %s",
        discount_type,
        value,
        reason,
    )
    return {"status": "approved"}


def update_salesforce_crm(customer_id: str, details: dict) -> dict:
    """
    Updates the Salesforce CRM with customer details.

    Args:
        customer_id (str): The ID of the customer.
        details (str): A dictionary of details to update in Salesforce.

    Returns:
        dict: A dictionary with the status and message.

    Example:
        >>> update_salesforce_crm(customer_id='123', details={
            'appointment_date': '2024-07-25',
            'appointment_time': '9-12',
            'services': 'Planting',
            'discount': '15% off planting',
            'qr_code': '10% off next in-store purchase'})
        {'status': 'success', 'message': 'Salesforce record updated.'}
    """
    logger.info(
        "Updating Salesforce CRM for customer ID %s with details: %s",
        customer_id,
        details,
    )
    return {"status": "success", "message": "Salesforce record updated."}


def access_cart_information(customer_id: str) -> dict:
    """
    Args:
        customer_id (str): The ID of the customer.

    Returns:
        dict: A dictionary representing the appointment/reservation contents.

    Example:
        >>> access_cart_information(customer_id='123')
        {'items': [{'product_id': 'botox-123', 'name': '보톡스 (눈가)', 'quantity': 1}, {'product_id': 'facial-456', 'name': '딥클렌징 페이셜', 'quantity': 1}], 'subtotal': 450000}
    """
    logger.info("Accessing appointment information for customer ID: %s", customer_id)

    # MOCK API RESPONSE - Replace with actual API call
    mock_appointments = {
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
    }
    return mock_appointments


def modify_cart(
    customer_id: str, items_to_add: list[dict], items_to_remove: list[dict]
) -> dict:
    """Modifies the user's shopping cart by adding and/or removing items.

    Args:
        customer_id (str): The ID of the customer.
        items_to_add (list): A list of dictionaries, each with 'product_id' and 'quantity'.
        items_to_remove (list): A list of product_ids to remove.

    Returns:
        dict: A dictionary indicating the status of the cart modification.
    Example:
        >>> modify_cart(customer_id='123', items_to_add=[{'product_id': 'soil-456', 'quantity': 1}, {'product_id': 'fert-789', 'quantity': 1}], items_to_remove=[{'product_id': 'fert-112', 'quantity': 1}])
        {'status': 'success', 'message': 'Cart updated successfully.', 'items_added': True, 'items_removed': True}
    """

    logger.info("Modifying cart for customer ID: %s", customer_id)
    logger.info("Adding items: %s", items_to_add)
    logger.info("Removing items: %s", items_to_remove)
    # MOCK API RESPONSE - Replace with actual API call
    return {
        "status": "success",
        "message": "Cart updated successfully.",
        "items_added": True,
        "items_removed": True,
    }


def get_product_recommendations(skin_concern: str, customer_id: str) -> dict:
    """Provides treatment recommendations based on the customer's skin concerns.

    Args:
        skin_concern: The skin concern (e.g., '주름', '색소침착', '여드름').
        customer_id: Optional customer ID for personalized recommendations.

    Returns:
        A dictionary of recommended treatments. Example:
        {'recommendations': [
            {'product_id': 'botox-456', 'name': '보톡스 (이마)', 'description': '이마 주름 개선에 효과적'},
            {'product_id': 'laser-789', 'name': '피코 레이저', 'description': '색소침착 개선 전문 시술'}
        ]}
    """
    logger.info(
        "Getting treatment recommendations for skin concern: %s and customer %s",
        skin_concern,
        customer_id,
    )
    # MOCK API RESPONSE - Replace with actual API call or recommendation engine
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
    return recommendations


def check_product_availability(product_id: str, store_id: str) -> dict:
    """Checks the availability of a product at a specified store (or for pickup).

    Args:
        product_id: The ID of the product to check.
        store_id: The ID of the store (or 'pickup' for pickup availability).

    Returns:
        A dictionary indicating availability.  Example:
        {'available': True, 'quantity': 10, 'store': 'Main Store'}

    Example:
        >>> check_product_availability(product_id='soil-456', store_id='pickup')
        {'available': True, 'quantity': 10, 'store': 'pickup'}
    """
    logger.info(
        "Checking availability of product ID: %s at store: %s",
        product_id,
        store_id,
    )
    # MOCK API RESPONSE - Replace with actual API call
    return {"available": True, "quantity": 10, "store": store_id}


def schedule_planting_service(
    customer_id: str, date: str, time_range: str, details: str
) -> dict:
    """Schedules a beauty treatment appointment.

    Args:
        customer_id: The ID of the customer.
        date:  The desired date (YYYY-MM-DD).
        time_range: The desired time range (e.g., "9-12").
        details: Any additional details (e.g., "보톡스 이마 시술").

    Returns:
        A dictionary indicating the status of the scheduling. Example:
        {'status': 'success', 'appointment_id': '12345', 'date': '2024-07-29', 'time': '9:00 AM - 12:00 PM'}

    Example:
        >>> schedule_planting_service(customer_id='123', date='2024-07-29', time_range='9-12', details='보톡스 이마 시술')
        {'status': 'success', 'appointment_id': 'some_uuid', 'date': '2024-07-29', 'time': '9-12', 'confirmation_time': '2024-07-29 9:00'}
    """
    logger.info(
        "Scheduling beauty treatment for customer ID: %s on %s (%s)",
        customer_id,
        date,
        time_range,
    )
    logger.info("Treatment details: %s", details)
    # MOCK API RESPONSE - Replace with actual API call to your scheduling system
    # Calculate confirmation time based on date and time_range
    start_time_str = time_range.split("-")[0]  # Get the start time (e.g., "9")
    confirmation_time_str = (
        f"{date} {start_time_str}:00"  # e.g., "2024-07-29 9:00"
    )

    return {
        "status": "success",
        "appointment_id": str(uuid.uuid4()),
        "date": date,
        "time": time_range,
        "treatment": details,
        "confirmation_time": confirmation_time_str,  # formatted time for calendar
        "location": "엘리트 뷰티 클리닉 강남점"
    }


def get_available_planting_times(date: str) -> list:
    """Retrieves available beauty treatment time slots for a given date.

    Args:
        date: The date to check (YYYY-MM-DD).

    Returns:
        A list of available time ranges.

    Example:
        >>> get_available_planting_times(date='2024-07-29')
        ['9-11', '11-13', '14-16', '16-18']
    """
    logger.info("Retrieving available treatment times for %s", date)
    # MOCK API RESPONSE - Replace with actual API call
    # Generate beauty clinic time slots
    return ["9-11", "11-13", "14-16", "16-18", "18-20"]


def send_care_instructions(
    customer_id: str, treatment_type: str, delivery_method: str
) -> dict:
    """Sends an email or SMS with aftercare instructions for a specific beauty treatment.

    Args:
        customer_id:  The ID of the customer.
        treatment_type: The type of treatment (e.g., '보톡스', '필러', '레이저').
        delivery_method: 'email' (default) or 'sms'.

    Returns:
        A dictionary indicating the status.

    Example:
        >>> send_care_instructions(customer_id='123', treatment_type='보톡스', delivery_method='email')
        {'status': 'success', 'message': '보톡스 시술 후 관리 안내를 이메일로 발송했습니다.'}
    """
    logger.info(
        "Sending aftercare instructions for %s to customer: %s via %s",
        treatment_type,
        customer_id,
        delivery_method,
    )
    # MOCK API RESPONSE - Replace with actual API call or email/SMS sending logic
    delivery_method_kr = "이메일" if delivery_method == "email" else "SMS"
    return {
        "status": "success",
        "message": f"{treatment_type} 시술 후 관리 안내를 {delivery_method_kr}로 발송했습니다.",
    }


def generate_qr_code(
    customer_id: str,
    discount_value: float,
    discount_type: str,
    expiration_days: int,
) -> dict:
    """Generates a QR code for a discount.

    Args:
        customer_id: The ID of the customer.
        discount_value: The value of the discount (e.g., 10 for 10%).
        discount_type: "percentage" (default) or "fixed".
        expiration_days: Number of days until the QR code expires.

    Returns:
        A dictionary containing the QR code data (or a link to it). Example:
        {'status': 'success', 'qr_code_data': '...', 'expiration_date': '2024-08-28'}

    Example:
        >>> generate_qr_code(customer_id='123', discount_value=10.0, discount_type='percentage', expiration_days=30)
        {'status': 'success', 'qr_code_data': 'MOCK_QR_CODE_DATA', 'expiration_date': '2024-08-24'}
    """
    
    # Guardrails to validate the amount of discount is acceptable for a auto-approved discount.
    # Defense-in-depth to prevent malicious prompts that could circumvent system instructions and
    # be able to get arbitrary discounts.
    if discount_type == "" or discount_type == "percentage":
        if discount_value > 10:
            return "cannot generate a QR code for this amount, must be 10% or less"
    if discount_type == "fixed" and discount_value > 20:
        return "cannot generate a QR code for this amount, must be 20 or less"
    
    logger.info(
        "Generating QR code for customer: %s with %s - %s discount.",
        customer_id,
        discount_value,
        discount_type,
    )
    # MOCK API RESPONSE - Replace with actual QR code generation library
    expiration_date = (
        datetime.now() + timedelta(days=expiration_days)
    ).strftime("%Y-%m-%d")
    return {
        "status": "success",
        "qr_code_data": "MOCK_QR_CODE_DATA",  # Replace with actual QR code
        "expiration_date": expiration_date,
    }


def send_satisfaction_survey(
    customer_id: str, treatment_type: str, delivery_method: str = "email"
) -> dict:
    """Sends a satisfaction survey to the customer after treatment.

    Args:
        customer_id: The ID of the customer.
        treatment_type: The type of treatment completed.
        delivery_method: 'email' (default) or 'sms'.

    Returns:
        A dictionary indicating the status.

    Example:
        >>> send_satisfaction_survey(customer_id='123', treatment_type='보톡스', delivery_method='email')
        {'status': 'success', 'message': '보톡스 시술 만족도 조사를 이메일로 발송했습니다.'}
    """
    logger.info(
        "Sending satisfaction survey for %s to customer: %s via %s",
        treatment_type,
        customer_id,
        delivery_method,
    )
    delivery_method_kr = "이메일" if delivery_method == "email" else "SMS"
    return {
        "status": "success",
        "message": f"{treatment_type} 시술 만족도 조사를 {delivery_method_kr}로 발송했습니다.",
        "survey_link": f"https://survey.elitebeauty.com/{customer_id}/{treatment_type}",
    }


def collect_feedback(
    customer_id: str, rating: int, feedback: str, treatment_type: str
) -> dict:
    """Collects customer feedback and rating.

    Args:
        customer_id: The ID of the customer.
        rating: Rating from 1-5 stars.
        feedback: Customer's written feedback.
        treatment_type: The type of treatment rated.

    Returns:
        A dictionary indicating the status.

    Example:
        >>> collect_feedback(customer_id='123', rating=5, feedback='매우 만족', treatment_type='보톡스')
        {'status': 'success', 'message': '피드백이 성공적으로 저장되었습니다.'}
    """
    logger.info(
        "Collecting feedback from customer %s: %d stars for %s",
        customer_id,
        rating,
        treatment_type,
    )
    
    # Validate rating
    if rating < 1 or rating > 5:
        return {
            "status": "error",
            "message": "평점은 1~5점 사이여야 합니다."
        }
    
    return {
        "status": "success",
        "message": "피드백이 성공적으로 저장되었습니다.",
        "rating": rating,
        "feedback": feedback,
        "treatment": treatment_type,
    }


def get_satisfaction_statistics(clinic_id: str = "gangnam") -> dict:
    """Gets satisfaction statistics for the clinic.

    Args:
        clinic_id: The ID of the clinic.

    Returns:
        A dictionary with satisfaction statistics.

    Example:
        >>> get_satisfaction_statistics(clinic_id='gangnam')
        {'average_rating': 4.8, 'total_reviews': 150, 'satisfaction_rate': 96}
    """
    logger.info("Getting satisfaction statistics for clinic: %s", clinic_id)
    
    # MOCK DATA - Replace with actual database query
    return {
        "average_rating": 4.8,
        "total_reviews": 150,
        "satisfaction_rate": 96,
        "top_rated_treatments": [
            {"name": "보톡스", "rating": 4.9},
            {"name": "필러", "rating": 4.7},
            {"name": "레이저토닝", "rating": 4.8}
        ]
    }

def send_appointment_reminder(
    customer_id: str, appointment_id: str, reminder_type: str = "24h"
) -> dict:
    """Sends appointment reminder to customer.

    Args:
        customer_id: The ID of the customer.
        appointment_id: The ID of the appointment.
        reminder_type: Type of reminder ('24h', '2h', '30min').

    Returns:
        A dictionary indicating the status.

    Example:
        >>> send_appointment_reminder(customer_id='123', appointment_id='apt123', reminder_type='24h')
        {'status': 'success', 'message': '24시간 전 예약 알림을 발송했습니다.'}
    """
    logger.info(
        "Sending %s reminder for appointment %s to customer %s",
        reminder_type,
        appointment_id,
        customer_id,
    )
    
    reminder_messages = {
        "24h": "24시간 전 예약 알림을 발송했습니다.",
        "2h": "2시간 전 예약 알림을 발송했습니다.",
        "30min": "30분 전 예약 알림을 발송했습니다."
    }
    
    return {
        "status": "success",
        "message": reminder_messages.get(reminder_type, "예약 알림을 발송했습니다."),
        "appointment_id": appointment_id,
        "reminder_type": reminder_type,
    }


def set_appointment_notifications(
    customer_id: str, 
    appointment_id: str,
    notifications: dict
) -> dict:
    """Sets up notification preferences for an appointment.

    Args:
        customer_id: The ID of the customer.
        appointment_id: The ID of the appointment.
        notifications: Dictionary with notification settings.

    Returns:
        A dictionary indicating the status.

    Example:
        >>> set_appointment_notifications(customer_id='123', appointment_id='apt123', 
        ...     notifications={'email': True, 'sms': True, 'push': False})
        {'status': 'success', 'message': '알림 설정이 완료되었습니다.'}
    """
    logger.info(
        "Setting notification preferences for appointment %s, customer %s: %s",
        appointment_id,
        customer_id,
        notifications,
    )
    
    return {
        "status": "success",
        "message": "알림 설정이 완료되었습니다.",
        "appointment_id": appointment_id,
        "notifications": notifications,
    }


def check_upcoming_appointments(customer_id: str) -> dict:
    """Checks for upcoming appointments for a customer.

    Args:
        customer_id: The ID of the customer.

    Returns:
        A dictionary with upcoming appointments.

    Example:
        >>> check_upcoming_appointments(customer_id='123')
        {'appointments': [{'date': '2024-05-25', 'time': '14-16', 'treatment': '보톡스'}]}
    """
    logger.info("Checking upcoming appointments for customer: %s", customer_id)
    
    # MOCK DATA - Replace with actual database query
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
        ]
    }

def send_mobile_app_notification(
    customer_id: str, message: str, notification_type: str = "general"
) -> dict:
    """Sends push notification to customer's mobile app.

    Args:
        customer_id: The ID of the customer.
        message: The notification message.
        notification_type: Type of notification ('appointment', 'promotion', 'general').

    Returns:
        A dictionary indicating the status.

    Example:
        >>> send_mobile_app_notification(customer_id='123', message='예약 확인', notification_type='appointment')
        {'status': 'success', 'message': '모바일 앱 알림이 발송되었습니다.'}
    """
    logger.info(
        "Sending mobile app notification to customer %s: %s (type: %s)",
        customer_id,
        message,
        notification_type,
    )
    
    return {
        "status": "success",
        "message": "모바일 앱 알림이 발송되었습니다.",
        "notification_id": str(uuid.uuid4()),
        "customer_id": customer_id,
        "type": notification_type,
    }


def generate_mobile_deep_link(
    customer_id: str, target_screen: str, parameters: Optional[dict] = None
) -> dict:
    """Generates a deep link for the mobile app.

    Args:
        customer_id: The ID of the customer.
        target_screen: Target screen in the app ('appointment', 'profile', 'treatments').
        parameters: Additional parameters for the deep link.

    Returns:
        A dictionary with the deep link.

    Example:
        >>> generate_mobile_deep_link(customer_id='123', target_screen='appointment', 
        ...     parameters={'appointment_id': 'apt123'})
        {'deep_link': 'elitebeauty://appointment?customer_id=123&appointment_id=apt123'}
    """
    logger.info(
        "Generating deep link for customer %s to %s with params: %s",
        customer_id,
        target_screen,
        parameters,
    )
    
    base_url = f"elitebeauty://{target_screen}?customer_id={customer_id}"
    
    if parameters:
        for key, value in parameters.items():
            base_url += f"&{key}={value}"
    
    return {
        "status": "success",
        "deep_link": base_url,
        "qr_code": f"https://api.qrserver.com/v1/create-qr-code/?data={base_url}",
    }


def sync_customer_data_to_app(customer_id: str) -> dict:
    """Syncs customer data to mobile app.

    Args:
        customer_id: The ID of the customer.

    Returns:
        A dictionary indicating the sync status.

    Example:
        >>> sync_customer_data_to_app(customer_id='123')
        {'status': 'success', 'message': '고객 데이터가 모바일 앱에 동기화되었습니다.'}
    """
    logger.info("Syncing customer data to mobile app for customer: %s", customer_id)
    
    return {
        "status": "success",
        "message": "고객 데이터가 모바일 앱에 동기화되었습니다.",
        "sync_timestamp": datetime.now().isoformat(),
        "customer_id": customer_id,
    }


def get_mobile_app_analytics(customer_id: str) -> dict:
    """Gets mobile app usage analytics for customer.

    Args:
        customer_id: The ID of the customer.

    Returns:
        A dictionary with app analytics.

    Example:
        >>> get_mobile_app_analytics(customer_id='123')
        {'last_login': '2024-05-23', 'sessions': 15, 'most_used_feature': 'appointment_booking'}
    """
    logger.info("Getting mobile app analytics for customer: %s", customer_id)
    
    # MOCK DATA - Replace with actual analytics data
    return {
        "last_login": "2024-05-23T10:30:00",
        "total_sessions": 15,
        "most_used_feature": "appointment_booking",
        "app_version": "2.1.0",
        "device_type": "iOS",
        "push_notifications_enabled": True,
        "preferences": {
            "language": "ko",
            "theme": "light",
            "notifications": {
                "appointments": True,
                "promotions": False,
                "news": True
            }
        }
    }
