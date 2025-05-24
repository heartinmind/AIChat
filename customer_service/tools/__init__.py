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

"""
Customer Service Tools Package
뷰티 클리닉 고객 서비스 도구 패키지
"""

from .tools import (
    # Communication tools
    send_call_companion_link,
    
    # Discount and approval tools
    approve_discount,
    sync_ask_for_approval,
    
    # CRM and data tools
    update_salesforce_crm,
    access_cart_information,
    modify_cart,
    
    # Recommendation and product tools
    get_product_recommendations,
    check_product_availability,
    
    # Appointment scheduling tools
    schedule_planting_service,
    get_available_planting_times,
    check_upcoming_appointments,
    
    # Customer care and instructions
    send_care_instructions,
    send_satisfaction_survey,
    collect_feedback,
    get_satisfaction_statistics,
    
    # Notification and reminder tools
    send_appointment_reminder,
    set_appointment_notifications,
    
    # Mobile app tools
    send_mobile_app_notification,
    generate_mobile_deep_link,
    sync_customer_data_to_app,
    get_mobile_app_analytics,
    
    # QR code and promotion tools
    generate_qr_code,
)

# 패키지 메타데이터
__version__ = "1.0.0"
__author__ = "Elite Beauty Clinic"
__description__ = "Customer service tools for beauty clinic chatbot"

# 모든 export된 함수들
__all__ = [
    # Communication
    "send_call_companion_link",
    
    # Discount and approval
    "approve_discount", 
    "sync_ask_for_approval",
    
    # CRM and data
    "update_salesforce_crm",
    "access_cart_information", 
    "modify_cart",
    
    # Recommendations and products
    "get_product_recommendations",
    "check_product_availability",
    
    # Appointments
    "schedule_planting_service",
    "get_available_planting_times", 
    "check_upcoming_appointments",
    
    # Customer care
    "send_care_instructions",
    "send_satisfaction_survey",
    "collect_feedback",
    "get_satisfaction_statistics",
    
    # Notifications
    "send_appointment_reminder",
    "set_appointment_notifications",
    
    # Mobile app
    "send_mobile_app_notification",
    "generate_mobile_deep_link", 
    "sync_customer_data_to_app",
    "get_mobile_app_analytics",
    
    # Promotions
    "generate_qr_code",
]
