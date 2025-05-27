# 🤖 Cursor IDE 사용자를 위한 최종 지시사항

## ⚠️ 절대 규칙 (MUST FOLLOW)

### 1. **대화 금지**
- Cursor AI와 대화하지 마세요
- "이 코드 설명해줘", "버그 찾아줘" 등 금지
- 모든 질문은 Claude에게!

### 2. **파일 보호**
```bash
# 이 파일들은 절대 건드리지 마세요:
~/Library/Application Support/Claude/claude_desktop_config.json  # MCP 설정
.env                                                            # 환경변수
service-account-key.json                                        # 인증 키
*.pem, *.key                                                   # 인증서
```

### 3. **작업 순서**
1. Claude와 계획 수립
2. `./safe_work.sh` 실행하여 백업
3. Cursor에서 코딩 (자동완성만)
4. Claude에게 검증 요청
5. Git commit & push

## 🛡️ Cursor 설정

### 1. **settings.json 추가**
```json
{
  "cursor.chat.enabled": false,  // AI 채팅 비활성화 권장
  "cursor.aiAutoComplete": true,  // 자동완성만 사용
  "files.autoSave": "off",       // 자동저장 끄기 (안전)
  "git.confirmSync": true        // Git 동기화 확인
}
```

### 2. **단축키 비활성화**
- `Cmd+K` (AI 채팅) → 사용하지 않기
- 대신 `Cmd+P` (파일 검색) 사용

## 📝 코딩 규칙

### Python 파일
```python
# 항상 파일 상단에 인코딩 명시
# -*- coding: utf-8 -*-

# 의미 있는 주석 작성
# TODO: Claude와 확인 필요
# FIXME: 버그 수정 필요
```

### JavaScript/TypeScript
```typescript
// 명확한 타입 정의
interface Props {
  // ...
}

// 주석은 한국어로 작성 가능
// Claude가 검토할 예정
```

## 🚨 위험 신호 감지

다음 상황이 발생하면 즉시 중단하고 Claude에게 알리세요:

1. **Cursor가 대량의 코드를 한번에 생성하려 할 때**
2. **설정 파일을 자동으로 수정하려 할 때**
3. **node_modules나 venv 폴더를 건드리려 할 때**
4. **import 문을 대량으로 변경하려 할 때**

## 💡 유용한 팁

### 1. **파일 탐색**
```bash
# 빠른 파일 찾기
Cmd+P → 파일명 입력

# 심볼 찾기
Cmd+Shift+O → 함수/클래스명 입력
```

### 2. **코드 정리**
```bash
# 포맷팅
Option+Shift+F

# import 정리
Option+Shift+O
```

### 3. **Git 통합**
- Source Control 탭 사용
- 하지만 커밋은 `./safe_work.sh` 사용 권장

## 📋 체크리스트

### 코딩 시작 전:
- [ ] Claude와 작업 내용 확인
- [ ] `./safe_work.sh` 실행 → 2번 (상태 확인)
- [ ] 필요시 백업 생성

### 코딩 중:
- [ ] 자동완성만 사용
- [ ] 의심스러우면 Claude에게 확인
- [ ] 주기적으로 저장 (Cmd+S)

### 코딩 후:
- [ ] Claude에게 코드 리뷰 요청
- [ ] 테스트 실행
- [ ] `./safe_work.sh` 실행 → 4번 (커밋 & 푸시)

## 🆘 도움말

### 문제 발생 시:
1. **먼저 시도**: `./safe_work.sh` → 8번 (긴급 복구)
2. **Claude에게 상황 설명**
3. **백업에서 복원**

### 자주 하는 실수:
- ❌ Cursor AI와 대화
- ❌ 설정 파일 직접 수정
- ❌ 확인 없이 대량 변경
- ❌ .env 파일 커밋

### 올바른 방법:
- ✅ Claude와 먼저 상의
- ✅ 작은 단위로 작업
- ✅ 자주 백업
- ✅ 테스트 후 커밋

## 🎯 기억하세요!

> **"Cursor는 똑똑한 타자기일 뿐입니다."**
> 
> 모든 결정은 당신과 Claude가 함께 내립니다.
> Cursor는 그저 타이핑을 도와줄 뿐입니다.

---

## 빠른 참조

```bash
# 작업 시작
./safe_work.sh  # 메뉴 선택

# 백업
./safe_work.sh → 1

# 상태 확인  
./safe_work.sh → 2

# 테스트
./safe_work.sh → 3

# 커밋 & 푸시
./safe_work.sh → 4

# 긴급 복구
./safe_work.sh → 8
```

**항상 안전하게, 천천히, Claude와 함께!** 🚀
