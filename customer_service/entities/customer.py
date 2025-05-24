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
"""Customer entity module."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class Address(BaseModel):
    """
    Represents a customer's address.
    """

    street: str
    city: str
    state: str
    zip: str
    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    """
    Represents a product in a customer's purchase history.
    """

    product_id: str
    name: str
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class Purchase(BaseModel):
    """
    Represents a customer's purchase.
    """

    date: str
    items: List[Product]
    total_amount: float
    model_config = ConfigDict(from_attributes=True)


class CommunicationPreferences(BaseModel):
    """
    Represents a customer's communication preferences.
    """

    email: bool = True
    sms: bool = True
    push_notifications: bool = True
    model_config = ConfigDict(from_attributes=True)


class BeautyProfile(BaseModel):
    """
    Represents a customer's beauty profile.
    """

    skin_type: str
    concerns: List[str]
    previous_treatments: List[str]
    preferred_treatment_time: str
    budget_range: str
    model_config = ConfigDict(from_attributes=True)


class Customer(BaseModel):
    """
    Represents a customer.
    """

    account_number: str
    customer_id: str
    customer_first_name: str
    customer_last_name: str
    email: str
    phone_number: str
    customer_start_date: str
    years_as_customer: int
    billing_address: Address
    treatment_history: List[Purchase]  # 시술 이력
    loyalty_points: int
    preferred_clinic: str  # 선호 클리닉
    communication_preferences: CommunicationPreferences
    beauty_profile: BeautyProfile  # 뷰티 프로필
    scheduled_appointments: Dict = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """
        Converts the Customer object to a JSON string.

        Returns:
            A JSON string representing the Customer object.
        """
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_customer(current_customer_id: str) -> Optional["Customer"]:
        """
        Retrieves a customer based on their ID.

        Args:
            customer_id: The ID of the customer to retrieve.

        Returns:
            The Customer object if found, None otherwise.
        """
        # In a real application, this would involve a database lookup.
        # For this example, we'll just return a dummy customer.
        return Customer(
            customer_id=current_customer_id,
            account_number="428765091",
            customer_first_name="민지",
            customer_last_name="김",
            email="minji.kim@example.com",
            phone_number="+82-10-1234-5678",
            customer_start_date="2022-06-10",
            years_as_customer=2,
            billing_address=Address(
                street="123 강남대로", city="서울", state="강남구", zip="06292"
            ),
            treatment_history=[  # Example treatment history
                Purchase(
                    date="2023-03-05",
                    items=[
                        Product(
                            product_id="botox-111",
                            name="보톡스 (이마)",
                            quantity=1,
                        ),
                        Product(
                            product_id="skincare-222",
                            name="하이드라페이셜",
                            quantity=1,
                        ),
                    ],
                    total_amount=350000,
                ),
                Purchase(
                    date="2023-07-12",
                    items=[
                        Product(
                            product_id="filler-333",
                            name="필러 (볼)",
                            quantity=1,
                        ),
                        Product(
                            product_id="laser-444",
                            name="레이저 토닝",
                            quantity=1,
                        ),
                    ],
                    total_amount=520000,
                ),
                Purchase(
                    date="2024-01-20",
                    items=[
                        Product(
                            product_id="peel-555",
                            name="화학적 필링",
                            quantity=1,
                        ),
                        Product(
                            product_id="massage-666",
                            name="얼굴 마사지",
                            quantity=1,
                        ),
                    ],
                    total_amount=180000,
                ),
            ],
            loyalty_points=1050,
            preferred_clinic="엘리트 뷰티 클리닉 강남점",
            communication_preferences=CommunicationPreferences(
                email=True, sms=True, push_notifications=True
            ),
            beauty_profile=BeautyProfile(
                skin_type="복합성",
                concerns=["색소침착", "주름", "모공"],
                previous_treatments=["보톡스", "필러", "레이저토닝"],
                preferred_treatment_time="오후",
                budget_range="월 30-50만원",
            ),
            scheduled_appointments={},
        )
