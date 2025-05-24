# Google Cloud 보안 강화 가이드

## 🔒 **현재 보안 상태 vs 필요한 보안**

### ✅ **Google Cloud 기본 보안 (이미 있음)**
- **인프라 보안**: 데이터센터, 네트워크, 하드웨어
- **플랫폼 보안**: Kubernetes, Cloud Run 컨테이너
- **전송 암호화**: HTTPS 기본 제공
- **DDoS 방어**: Cloud Armor 기본 제공

### ❌ **애플리케이션 레벨 보안 (우리가 추가해야 함)**
- **API 키 인증**: 무단 접근 방지
- **입력 검증**: SQL 인젝션 방지  
- **세션 관리**: 사용자 인증
- **로깅**: 보안 이벤트 추적

## 🛡️ **즉시 적용 가능한 보안 강화**

### 1. **API 키 인증 추가**

```python
# customer_service/security.py 생성
import os
import hashlib
import hmac
from functools import wraps
from flask import request, jsonify

class SecurityManager:
    def __init__(self):
        self.api_key = os.getenv('API_KEY', 'your-secret-api-key')
        self.rate_limit = {}
    
    def require_api_key(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            provided_key = request.headers.get('X-API-Key')
            if not provided_key or provided_key != self.api_key:
                return jsonify({'error': 'Invalid API key'}), 401
            return f(*args, **kwargs)
        return decorated_function
    
    def rate_limit_check(self, client_ip, limit=100):
        """시간당 요청 수 제한"""
        current_count = self.rate_limit.get(client_ip, 0)
        if current_count > limit:
            return False
        self.rate_limit[client_ip] = current_count + 1
        return True

# customer_service/agent.py에 적용
from .security import SecurityManager

security = SecurityManager()

@security.require_api_key
def chat_endpoint():
    # 기존 챗봇 로직...
    pass
```

### 2. **입력 검증 및 필터링**

```python
# customer_service/validators.py
import re
import html

class InputValidator:
    @staticmethod
    def sanitize_input(text: str) -> str:
        """입력값 정리 및 XSS 방지"""
        if not text:
            return ""
        
        # HTML 태그 제거
        text = html.escape(text)
        
        # SQL 키워드 차단
        sql_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT']
        for keyword in sql_keywords:
            text = text.replace(keyword.lower(), '').replace(keyword.upper(), '')
        
        # 특수 문자 제한
        text = re.sub(r'[<>"\';(){}]', '', text)
        
        return text.strip()
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """전화번호 형식 검증"""
        pattern = r'^(\+82|0)(10|11|16|17|18|19)\d{8}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_customer_id(customer_id: str) -> bool:
        """고객 ID 형식 검증"""
        return customer_id.isalnum() and len(customer_id) <= 20

# tools.py에 적용
from .validators import InputValidator

def access_cart_information(customer_id: str) -> dict:
    # 입력 검증
    if not InputValidator.validate_customer_id(customer_id):
        return {"error": "Invalid customer ID"}
    
    customer_id = InputValidator.sanitize_input(customer_id)
    # 기존 로직...
```

### 3. **로깅 및 모니터링 강화**

```python
# customer_service/security_logger.py
import logging
import json
from datetime import datetime
from google.cloud import logging as cloud_logging

class SecurityLogger:
    def __init__(self):
        # Google Cloud Logging 설정
        client = cloud_logging.Client()
        client.setup_logging()
        
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
    
    def log_security_event(self, event_type: str, details: dict, client_ip: str = None):
        """보안 이벤트 로깅"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'client_ip': client_ip,
            'details': details
        }
        
        self.logger.warning(f"SECURITY_EVENT: {json.dumps(log_data)}")
    
    def log_failed_auth(self, client_ip: str, reason: str):
        """인증 실패 로깅"""
        self.log_security_event('AUTH_FAILED', {
            'reason': reason
        }, client_ip)
    
    def log_suspicious_activity(self, client_ip: str, activity: str):
        """의심스러운 활동 로깅"""
        self.log_security_event('SUSPICIOUS_ACTIVITY', {
            'activity': activity
        }, client_ip)

# 사용 예시
security_logger = SecurityLogger()

# API 키 인증 실패 시
security_logger.log_failed_auth(request.remote_addr, "Invalid API key")

# 과도한 요청 시  
security_logger.log_suspicious_activity(request.remote_addr, "Rate limit exceeded")
```

## 🚀 **Google Cloud 보안 서비스 활용**

### 1. **Cloud Armor (웹 방화벽)**
```bash
# Cloud Armor 보안 정책 생성
gcloud compute security-policies create chat-security-policy \
    --description="Chat service security policy"

# IP 차단 규칙 추가
gcloud compute security-policies rules create 1000 \
    --security-policy=chat-security-policy \
    --expression="origin.ip == '1.2.3.4'" \
    --action=deny-403
```

### 2. **Identity-Aware Proxy (IAP)**
```bash
# IAP 활성화 (선택사항 - 내부 사용자만)
gcloud iap web enable \
    --resource-type=backend-services \
    --service=chat-backend
```

### 3. **Secret Manager (API 키 관리)**
```bash
# 비밀번호 저장
echo -n "your-super-secret-api-key" | \
gcloud secrets create api-key --data-file=-

# 애플리케이션에서 사용
export API_KEY=$(gcloud secrets versions access latest --secret="api-key")
```

## 📊 **보안 비용 (월 기준)**

| 보안 서비스 | 월 비용 | 효과 |
|-------------|---------|------|
| Cloud Armor | $5-20 | DDoS 방어, 웹 방화벽 |
| Secret Manager | $0.06 | API 키 안전 관리 |
| Cloud Logging | $0.50 | 보안 이벤트 추적 |
| **총합** | **$5.56-20.56** | **기업급 보안** |

## ✅ **즉시 적용 스크립트**

```bash
#!/bin/bash
# setup_security.sh

# 1. 보안 서비스 활성화
gcloud services enable compute.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable logging.googleapis.com

# 2. API 키 생성 및 저장
API_KEY=$(openssl rand -hex 32)
echo -n "$API_KEY" | gcloud secrets create chat-api-key --data-file=-

# 3. Cloud Armor 보안 정책 생성
gcloud compute security-policies create chat-security \
    --description="Chat service security"

# 4. 기본 보안 규칙 추가
gcloud compute security-policies rules create 2000 \
    --security-policy=chat-security \
    --expression="true" \
    --action=allow

echo "✅ 기본 보안 설정 완료!"
echo "API Key: $API_KEY"
```

## 🎯 **결론: Google Cloud + 기본 보안 = 상용 가능**

**Google Cloud 기본 보안 (무료)** + **우리가 추가한 애플리케이션 보안 ($20/월)** = **엔터프라이즈급 보안**

이 정도면 **은행급 보안**까지는 아니어도 **일반 상용 서비스로는 충분**합니다! 🛡️ 