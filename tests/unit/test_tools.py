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

from customer_service.tools.tools import (
    send_call_companion_link,
    approve_discount,
    update_salesforce_crm,
    access_cart_information,
    modify_cart,
    get_product_recommendations,
    check_product_availability,
    schedule_planting_service,
    get_available_planting_times,
    send_care_instructions,
    generate_qr_code,
)
from datetime import datetime, timedelta
import logging

# Configure logging for the test file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_send_call_companion_link():
    phone_number = "+1-555-123-4567"
    result = send_call_companion_link(phone_number)
    assert result == {
        "status": "success",
        "message": f"Link sent to {phone_number}",
    }


def test_approve_discount_small():
    result = approve_discount(
        discount_type="percentage", value=10.0, reason="Test discount"
    )
    assert result == {"status": "ok"}


def test_approve_discount_large():
    result = approve_discount(
        discount_type="percentage", value=15.0, reason="Test large discount"
    )
    assert result["status"]=="rejected"

def test_update_salesforce_crm():
    customer_id = "123"
    details = "Updated customer details"
    result = update_salesforce_crm(customer_id, details)
    assert result == {
        "status": "success",
        "message": "Salesforce record updated.",
    }


def test_access_cart_information():
    customer_id = "123"
    result = access_cart_information(customer_id)
    assert result == {
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


def test_modify_cart_add_and_remove():
    customer_id = "123"
    items_to_add = [{"product_id": "beauty-003", "quantity": 1}]
    items_to_remove = [{"product_id": "beauty-001"}]
    result = modify_cart(customer_id, items_to_add, items_to_remove)
    assert result == {
        "status": "success",
        "message": "Cart updated successfully.",
        "items_added": True,
        "items_removed": True,
    }


def test_get_product_recommendations_skincare():
    treatment_type = "skincare"
    customer_id = "123"
    result = get_product_recommendations(treatment_type, customer_id)
    assert result == {
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


def test_get_product_recommendations_other():
    treatment_type = "other"
    customer_id = "123"
    result = get_product_recommendations(treatment_type, customer_id)
    assert result == {
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


def test_check_product_availability():
    product_id = "beauty-001"
    store_id = "Beauty Clinic Main"
    result = check_product_availability(product_id, store_id)
    assert result == {"available": True, "quantity": 10, "store": store_id}


def test_schedule_planting_service():
    customer_id = "123"
    date = "2024-07-29"
    time_range = "9-12"
    details = "Facial Treatment Session"
    result = schedule_planting_service(customer_id, date, time_range, details)
    assert result["status"] == "success"
    assert result["date"] == date
    assert result["time"] == time_range
    assert "appointment_id" in result
    assert "confirmation_time" in result


def test_get_available_planting_times():
    date = "2024-07-29"
    result = get_available_planting_times(date)
    assert result == ["9-11", "11-13", "14-16", "16-18", "18-20"]


def test_send_care_instructions():
    customer_id = "123"
    treatment_type = "Facial Treatment"
    delivery_method = "email"
    result = send_care_instructions(customer_id, treatment_type, delivery_method)
    assert result == {
        "status": "success",
        "message": "Facial Treatment 시술 후 관리 안내를 이메일로 발송했습니다.",
    }


def test_generate_qr_code():
    customer_id = "123"
    discount_value = 10.0
    discount_type = "percentage"
    expiration_days = 30
    result = generate_qr_code(
        customer_id, discount_value, discount_type, expiration_days
    )
    assert result["status"] == "success"
    assert result["qr_code_data"] == "MOCK_QR_CODE_DATA"
    assert "expiration_date" in result
    expiration_date = datetime.now() + timedelta(days=expiration_days)
    assert result["expiration_date"] == expiration_date.strftime("%Y-%m-%d")
