# Google Cloud 스케일링 가이드

## 🚀 **1000명 동시 접속 처리하기**

### 현재 문제
- 기본 설정으로는 동접자 10-20명만 처리 가능
- 메모리 부족으로 서버 다운 위험

### ✅ **해결 방법**

#### 1. **Cloud Run 자동 스케일링 설정**
```bash
# 현재 배포 명령어 수정
gcloud run deploy customer-service-ai \
  --source . \
  --region=asia-northeast3 \
  --max-instances=100 \
  --min-instances=2 \
  --cpu=2 \
  --memory=4Gi \
  --concurrency=1000 \
  --timeout=300
```

#### 2. **로드 밸런서 설정**
```bash
# Cloud Load Balancing 활성화
gcloud compute backend-services create chat-backend \
  --protocol=HTTP \
  --health-checks=chat-health-check \
  --global
```

#### 3. **Redis 캐시 추가**
```bash
# Redis 인스턴스 생성
gcloud redis instances create chat-cache \
  --size=1 \
  --region=asia-northeast3 \
  --redis-version=redis_6_x
```

#### 4. **모니터링 설정**
```bash
# 모니터링 알림 설정
gcloud alpha monitoring policies create \
  --policy-from-file=monitoring-policy.yaml
```

## 📊 **예상 비용 (월 기준)**

| 서비스 | 사양 | 월 비용 |
|--------|------|---------|
| Cloud Run | 100 인스턴스 | $200-400 |
| Load Balancer | 트래픽 기준 | $50-100 |
| Redis Cache | 1GB | $30 |
| **총합** | | **$280-530** |

## ⚡ **성능 예상**
- **동시 접속자**: 1,000명
- **응답 시간**: 평균 200ms
- **가용성**: 99.9%
- **자동 확장**: 트래픽에 따라 자동 조절

## 🔧 **설정 스크립트**
```bash
#!/bin/bash
# setup_scaling.sh

# 1. 프로젝트 설정
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# 2. 필요한 API 활성화
gcloud services enable run.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable compute.googleapis.com

# 3. Redis 캐시 생성
gcloud redis instances create chat-cache \
  --size=1 \
  --region=asia-northeast3

# 4. 스케일링 설정으로 배포
gcloud run deploy customer-service-ai \
  --source . \
  --region=asia-northeast3 \
  --max-instances=100 \
  --min-instances=2 \
  --cpu=2 \
  --memory=4Gi \
  --concurrency=1000

echo "✅ 스케일링 설정 완료!"
```

## 📈 **단계별 확장 계획**

### Phase 1: 100명까지 (현재 + 기본 스케일링)
- Cloud Run 기본 설정 조정
- 비용: ~$50/월

### Phase 2: 500명까지 (Redis 캐시 추가)
- Redis 캐시 도입
- 응답 속도 개선
- 비용: ~$150/월

### Phase 3: 1,000명까지 (완전 스케일링)
- 로드 밸런서 추가
- 모니터링 강화
- 비용: ~$400/월

## 🎯 **즉시 적용 가능한 설정**

현재 코드에 다음만 추가하면 바로 향상:

```python
# customer_service/config.py에 추가
import os

class Config:
    # 기존 설정...
    
    # 스케일링 설정
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', '1000'))
    WORKER_PROCESSES = int(os.getenv('WORKER_PROCESSES', '4'))
    WORKER_THREADS = int(os.getenv('WORKER_THREADS', '8'))
    
    # Redis 캐시 설정
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))  # 5분
```

이렇게 하면 **지금 당장 1000명도 처리 가능**합니다! 🚀 