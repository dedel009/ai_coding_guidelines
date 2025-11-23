# Check Workflow

현재 작업이 올바른 워크플로우를 따르고 있는지 확인합니다.

## When to Use

- 작업 시작 전
- 작업 중간에 방향성 확인 필요할 때
- kdy가 워크플로우를 확인하고 싶을 때

## Workflow Types

### Workflow 1: 기존 코드 수정

**특징:**
- 이미 존재하는 코드를 변경
- 기존 테스트가 있어야 함
- 작은 변경사항

**단계:**
```
1. 요구사항 확인 ← 불명확하면 질문
2. 기존 테스트 확인 ← 없으면 STOP
3. 테스트 수정
4. 구현 수정
5. 테스트 실행
6. kdy 리뷰
```

**체크리스트:**
- [ ] 요구사항 명확히 이해했는가?
- [ ] 기존 테스트를 찾았는가?
- [ ] 테스트를 먼저 수정했는가?
- [ ] 구현을 수정했는가?
- [ ] 모든 테스트가 통과하는가?
- [ ] kdy에게 리뷰를 요청했는가?

### Workflow 2: 신규 기능 개발

**특징:**
- 새로운 기능 추가
- TDD 사이클 적용
- 중간 크기 작업

**단계:**
```
1. 요구사항 확인 ← 불명확하면 질문
2. Red: 테스트 작성
3. Green: 최소 구현
4. 테스트 실행
5. kdy 리뷰
6. Refactor (필요시)
```

**체크리스트:**
- [ ] 요구사항 명확히 이해했는가?
- [ ] 실패하는 테스트를 작성했는가?
- [ ] 테스트가 실패하는 것을 확인했는가?
- [ ] 최소한의 구현으로 테스트를 통과했는가?
- [ ] kdy에게 리뷰를 요청했는가?
- [ ] 리팩토링이 필요한가?

### Workflow 3: 대규모 기능 개발

**특징:**
- 여러 파일/레이어 수정
- Phase별 분해 필요
- 복잡한 작업

**단계:**
```
1. /plan-feature 실행
2. Phase별 분해
3. 각 Phase마다:
   ├─ Task 선택
   ├─ Workflow 2 실행
   └─ 진행상황 보고
4. 전체 완료 확인
```

**체크리스트:**
- [ ] `/plan-feature`를 실행했는가?
- [ ] Phase별로 분해했는가?
- [ ] 현재 Phase/Task가 명확한가?
- [ ] 각 Task마다 Workflow 2를 따랐는가?
- [ ] 진행상황을 kdy에게 보고하는가?

## Identification Guide

### 어떤 Workflow인가?

```
┌─ 기존 코드를 수정하는가?
│   ├─ YES
│   │   └─ 파일이 3개 미만인가?
│   │       ├─ YES → Workflow 1
│   │       └─ NO → Workflow 3
│   │
│   └─ NO (신규 기능)
│       └─ 여러 레이어를 건드리는가?
│           ├─ YES → Workflow 3
│           └─ NO → Workflow 2
```

## Critical Rules Check

### Rule 1: Test-First
```
현재 상태:
- [ ] 테스트가 있는가?
- [ ] 테스트를 먼저 작성/수정했는가?
- [ ] 테스트가 통과하는가?

❌ 위반 시: 즉시 STOP → /test-first 실행
```

### Rule 2: Ask, Don't Assume
```
현재 상태:
- [ ] 요구사항이 명확한가?
- [ ] 불명확한 부분을 질문했는가?
- [ ] kdy의 확인을 받았는가?

❌ 위반 시: 진행 중단 → kdy에게 질문
```

### Rule 3: Break Down
```
현재 상태:
- [ ] 작업이 적절한 크기인가?
- [ ] 파일 3개 미만인가?
- [ ] 100줄 미만인가?

❌ 위반 시: /plan-feature 실행
```

### Rule 4: Review
```
현재 상태:
- [ ] kdy에게 리뷰를 요청했는가?
- [ ] 리뷰 없이 다음 단계로 진행하지 않았는가?

❌ 위반 시: 즉시 리뷰 요청
```

## Status Report Template

### Workflow 1 진행 중

```markdown
## 📊 Workflow Status: 기존 코드 수정

### 현재 단계: 3/6
- [x] 1. 요구사항 확인
- [x] 2. 기존 테스트 확인
- [x] 3. 테스트 수정 ← 현재 여기
- [ ] 4. 구현 수정
- [ ] 5. 테스트 실행
- [ ] 6. kdy 리뷰

### Critical Rules
- ✅ Test-First
- ✅ Ask, Don't Assume
- ✅ Break Down (파일 1개)
- ⏳ Review (아직 안함)

### 다음 단계
구현 수정 → 테스트 실행 → 리뷰 요청
```

### Workflow 2 진행 중

```markdown
## 📊 Workflow Status: 신규 기능 개발

### TDD 사이클: Green
- [x] Red: 테스트 작성 완료
- [x] Green: 구현 완료 ← 현재 여기
- [ ] Refactor: 리팩토링 예정

### Critical Rules
- ✅ Test-First (테스트 먼저 작성)
- ✅ Ask, Don't Assume
- ✅ Break Down
- ⏳ Review (다음 단계)

### 테스트 결과
```
tests/test_user_service.py::test_사용자_생성 PASSED
```

### 다음 단계
kdy 리뷰 → 필요시 리팩토링
```

### Workflow 3 진행 중

```markdown
## 📊 Workflow Status: 대규모 기능

### 전체 진행률: Phase 1/3
- [x] Phase 1: Foundation (완료)
- [ ] Phase 2: Core ← 현재 여기
- [ ] Phase 3: Enhancement

### Phase 2 진행률: 2/4 tasks
- [x] Task 1: UserService 구현
- [x] Task 2: API 엔드포인트 ← 완료
- [ ] Task 3: 권한 시스템
- [ ] Task 4: 테스트 추가

### Critical Rules
- ✅ Test-First (각 Task마다)
- ✅ Ask, Don't Assume
- ✅ Break Down (Phase별 분해)
- ✅ Review (매 Task마다)

### 다음 단계
Phase 2, Task 3 시작 → 테스트 작성
```

## Quick Check

### 1분 체크리스트

```bash
# 어떤 워크플로우?
□ Workflow 1 (기존 코드 수정)
□ Workflow 2 (신규 기능)
□ Workflow 3 (대규모)

# Critical Rules 준수?
□ Test-First ✅
□ Ask, Don't Assume ✅
□ Break Down ✅
□ Review ✅

# 현재 단계?
□ 요구사항 확인
□ 테스트 작성/수정
□ 구현
□ 테스트 실행
□ 리뷰 대기
```

## Common Violations

### ❌ 테스트 없이 구현
```
위반: Rule 1 (Test-First)
현재 단계: 구현 중
문제: 테스트 없음

조치:
1. 구현 중단
2. /test-first 실행
3. 테스트 작성
4. 다시 구현
```

### ❌ 불명확한 요구사항 가정
```
위반: Rule 2 (Ask, Don't Assume)
현재 단계: 테스트 작성 중
문제: 요구사항 불명확

조치:
1. 작업 중단
2. kdy에게 질문
3. 확인 후 재개
```

### ❌ 큰 작업을 한 번에
```
위반: Rule 3 (Break Down)
현재 단계: 구현 중
문제: 10개 파일 수정 예정

조치:
1. /plan-feature 실행
2. Phase별 분해
3. 작은 단위로 진행
```

### ❌ 리뷰 없이 진행
```
위반: Rule 4 (Review)
현재 단계: 다음 기능 시작
문제: 이전 작업 리뷰 안받음

조치:
1. 다음 작업 중단
2. 이전 작업 리뷰 요청
3. 승인 후 진행
```

## Auto-Check Questions

AI가 스스로 확인해야 할 질문들:

```
□ 지금 어떤 워크플로우를 따르고 있는가?
□ 현재 어느 단계에 있는가?
□ 4가지 Critical Rules를 모두 준수하는가?
□ 다음 단계로 넘어가도 되는가?
□ kdy의 승인이 필요한가?
```

## Example Session

```
kdy: "사용자 이름 검증을 2자에서 3자로 변경해줘"

AI: /check-workflow 실행...

## 📊 Workflow 식별
→ Workflow 1 (기존 코드 수정)

## 현재 단계: 1/6
- [x] 요구사항 확인 ← 명확함
- [ ] 기존 테스트 확인
- [ ] 테스트 수정
- [ ] 구현 수정
- [ ] 테스트 실행
- [ ] kdy 리뷰

## Critical Rules
- ⏳ Test-First (다음 단계)
- ✅ Ask, Don't Assume (요구사항 명확)
- ✅ Break Down (파일 1개)
- ⏳ Review (마지막 단계)

다음: 기존 테스트 확인 → /test-first 실행
```

## Final Reminder

- 워크플로우는 **가이드**이지 **감옥**이 아님
- 상황에 따라 유연하게 적용
- 하지만 **Critical Rules는 절대 위반 금지**
- 불확실하면 **항상 kdy에게 물어보기**
