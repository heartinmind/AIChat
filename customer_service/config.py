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
"""Configuration module for the customer service agent."""

import os
import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentModel(BaseModel):
    """Agent model settings."""

    name: str = Field(default="customer_service_agent")
    model: str = Field(default="gemini-2.0-flash-001")


class Config(BaseSettings):
    """Configuration settings for the customer service agent."""

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../.env"
        ),
        env_prefix="GOOGLE_",
        case_sensitive=True,
        extra="ignore",  # 추가 환경변수 허용
    )
    agent_settings: AgentModel = Field(default=AgentModel())
    app_name: str = "customer_service_app"
    CLOUD_PROJECT: str = Field(default="my_project")
    CLOUD_LOCATION: str = Field(default="us-central1")
    GENAI_USE_VERTEXAI: str = Field(default="1")
    API_KEY: Optional[str] = Field(default="")
    agent_language: str = "ko-KR"
    
    def __post_init__(self):
        """환경변수 검증 로직"""
        if not self.CLOUD_PROJECT or self.CLOUD_PROJECT == "my_project":
            raise ValueError("❌ GOOGLE_CLOUD_PROJECT 환경변수를 실제 프로젝트 ID로 설정해주세요!")
        if not self.CLOUD_LOCATION:
            raise ValueError("❌ GOOGLE_CLOUD_LOCATION 환경변수를 설정해주세요!")
        logger.info(f"✅ 설정 검증 완료: Project={self.CLOUD_PROJECT}, Location={self.CLOUD_LOCATION}")
