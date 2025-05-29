# CHANGELOG

## [1.0.0] - 2025-05-29

### 🎉 초기 릴리즈

#### ✨ 주요 기능
- **하이브리드 AI 채팅 시스템**
  - Claude AI 기반 자연스러운 대화
  - 근무 시간 자동 라우팅 (AI/상담원)
  - 실시간 메시지 전송

- **사용자 채팅 인터페이스**
  - 반응형 디자인 (모바일/데스크톱)
  - 부드러운 애니메이션
  - 실시간 타이핑 표시

- **관리자 대시보드**
  - 실시간 통계
  - 상담 내역 관리
  - 사용자/상담원 관리

#### 🛠️ 기술 스택
- **Backend**: FastAPI 0.104.1, Python 3.12
- **Frontend**: Next.js 14.0.3, React 18.2.0
- **Database**: SQLAlchemy 2.0.23, SQLite
- **AI**: Anthropic Claude 3.5 Sonnet
- **Auth**: JWT (python-jose 3.3.0)

#### 🐛 해결된 이슈
- Python 3.13 호환성 문제 → Python 3.12 권장
- Anthropic 라이브러리 proxies 오류 → v0.18.1 + httpx 0.24.1
- 프론트엔드 422 오류 → API 요청 포맷 수정
- AI 대화 부자연스러움 → 프롬프트 개선

#### 📝 환경 설정
- 개발: `.env.development`
- 스테이징: `.env.staging`  
- 프로덕션: `.env.production`

#### 👥 기여자
- 개발팀: Elite Beauty Tech Team

---

### 향후 계획
- [ ] WebSocket 실시간 상담원 채팅
- [ ] 이미지/파일 전송 기능
- [ ] 상담 예약 시스템
- [ ] 다국어 지원
- [ ] 모바일 앱
