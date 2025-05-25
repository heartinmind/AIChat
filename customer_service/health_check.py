# Copyright 2025 Google LLC
# Health Check System for Beauty Clinic Chatbot

"""헬스체크 시스템 - 서버 상태 모니터링"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
import psutil
import os

logger = logging.getLogger(__name__)

class HealthChecker:
    """시스템 상태 확인 클래스"""
    
    def __init__(self):
        self.last_check = None
        self.status = "unknown"
        self.check_count = 0
    
    async def check_system_health(self) -> Dict[str, Any]:
        """시스템 전체 상태 확인"""
        self.check_count += 1
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "check_count": self.check_count,
            "checks": {}
        }
        
        try:
            # 1. ADK 서비스 상태 확인
            health_status["checks"]["adk_service"] = await self._check_adk_service()
            
            # 2. 환경변수 확인
            health_status["checks"]["config"] = self._check_config()
            
            # 3. 메모리 사용량 확인
            health_status["checks"]["memory"] = self._check_memory()
            
            # 4. 디스크 사용량 확인
            health_status["checks"]["disk"] = self._check_disk()
            
            # 5. 전체 상태 판단
            health_status["status"] = self._determine_overall_status(health_status["checks"])
            
        except Exception as e:
            logger.error(f"헬스체크 중 오류 발생: {e}")
            health_status["status"] = "error"
            health_status["error"] = str(e)
        
        self.last_check = datetime.now()
        self.status = health_status["status"]
        
        return health_status
    
    async def _check_adk_service(self) -> Dict[str, Any]:
        """ADK 서비스 상태 확인"""
        try:
            from customer_service.agent import root_agent
            
            # 간단한 테스트 쿼리
            test_response = root_agent("system health check")
            
            return {
                "status": "healthy",
                "response_received": True,
                "message": "ADK 서비스 정상 작동"
            }
        except ImportError:
            return {
                "status": "warning",
                "response_received": False,
                "message": "ADK 라이브러리 없음 (Mock 모드)"
            }
        except Exception as e:
            logger.error(f"ADK 서비스 체크 실패: {e}")
            return {
                "status": "unhealthy",
                "response_received": False,
                "message": f"ADK 서비스 오류: {str(e)}"
            }
    
    def _check_config(self) -> Dict[str, Any]:
        """환경설정 확인"""
        try:
            from customer_service.config import Config
            config = Config()
            
            # 필수 설정 확인
            issues = []
            if not config.CLOUD_PROJECT or config.CLOUD_PROJECT == "my_project":
                issues.append("CLOUD_PROJECT 미설정")
            if not config.CLOUD_LOCATION:
                issues.append("CLOUD_LOCATION 미설정")
            
            if issues:
                return {
                    "status": "unhealthy",
                    "message": f"설정 문제: {', '.join(issues)}"
                }
            else:
                return {
                    "status": "healthy",
                    "message": "환경설정 정상",
                    "project": config.CLOUD_PROJECT,
                    "location": config.CLOUD_LOCATION
                }
        except Exception as e:
            logger.error(f"설정 체크 실패: {e}")
            return {
                "status": "unhealthy",
                "message": f"설정 오류: {str(e)}"
            }
    
    def _check_memory(self) -> Dict[str, Any]:
        """메모리 사용량 확인"""
        try:
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            available_gb = memory.available / (1024**3)
            
            if memory_percent > 95:
                status = "critical"
                message = f"메모리 사용량 위험: {memory_percent:.1f}%"
            elif memory_percent > 85:
                status = "warning"
                message = f"메모리 사용량 높음: {memory_percent:.1f}%"
            else:
                status = "healthy"
                message = f"메모리 사용량 정상: {memory_percent:.1f}%"
            
            return {
                "status": status,
                "usage_percent": memory_percent,
                "available_gb": round(available_gb, 2),
                "message": message
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"메모리 체크 실패: {str(e)}"
            }
    
    def _check_disk(self) -> Dict[str, Any]:
        """디스크 사용량 확인"""
        try:
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            free_gb = disk.free / (1024**3)
            
            if disk_percent > 95:
                status = "critical"
                message = f"디스크 사용량 위험: {disk_percent:.1f}%"
            elif disk_percent > 85:
                status = "warning"
                message = f"디스크 사용량 높음: {disk_percent:.1f}%"
            else:
                status = "healthy"
                message = f"디스크 사용량 정상: {disk_percent:.1f}%"
            
            return {
                "status": status,
                "usage_percent": round(disk_percent, 1),
                "free_gb": round(free_gb, 2),
                "message": message
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"디스크 체크 실패: {str(e)}"
            }
    
    def _determine_overall_status(self, checks: Dict[str, Any]) -> str:
        """전체 상태 판단"""
        statuses = [check.get("status", "unknown") for check in checks.values()]
        
        if "critical" in statuses:
            return "critical"
        elif "unhealthy" in statuses:
            return "unhealthy"
        elif "warning" in statuses:
            return "warning"
        elif all(status == "healthy" for status in statuses):
            return "healthy"
        else:
            return "degraded"
    
    def get_status_summary(self) -> Dict[str, Any]:
        """상태 요약 정보"""
        return {
            "current_status": self.status,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "total_checks": self.check_count
        }

# 전역 헬스체커 인스턴스
health_checker = HealthChecker()

# 간편 함수들
async def quick_health_check() -> str:
    """빠른 상태 확인"""
    result = await health_checker.check_system_health()
    return result["status"]

async def detailed_health_report() -> Dict[str, Any]:
    """상세 상태 리포트"""
    return await health_checker.check_system_health()

if __name__ == "__main__":
    # 테스트 실행
    async def test_health_check():
        print("🔍 헬스체크 시스템 테스트 시작...")
        result = await detailed_health_report()
        print(f"📊 전체 상태: {result['status']}")
        print("📋 상세 체크 결과:")
        for check_name, check_result in result["checks"].items():
            print(f"  - {check_name}: {check_result['status']} - {check_result.get('message', '')}")
    
    asyncio.run(test_health_check())
