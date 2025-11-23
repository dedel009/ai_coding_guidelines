# AI Coding Guidelines

> AI 어시스턴트가 kdy와 협업할 때 따라야 할 핵심 규칙

## 🎯 MISSION

**1인 개발자가 비즈니스 로직, 인프라, 기획, 디자인까지 집중할 수 있도록 코딩 시간 최소화, 품질 극대화**

---

## ⚠️ CRITICAL RULES

### Rule 1: Test-First Development
```
❌ 테스트 없이 코드 작성 금지
✅ 항상 테스트 먼저 작성/확인
```

**실행:**
- 기존 코드 수정: 테스트 확인 → 수정 → 실행
- 신규 기능: 테스트 작성(Red) → 구현(Green) → 리팩토링
- 테스트 없으면 STOP → `/test-first` 실행

### Rule 2: Ask, Don't Assume
```
❌ 불명확한 부분 가정하고 진행
✅ 항상 질문하고 확인
```

**질문 필수 상황:**
- 요구사항이 애매할 때
- 여러 구현 방법이 가능할 때
- 기존 코드 의도를 모를 때
- 성능/보안/확장성 트레이드오프가 있을 때

### Rule 3: Break Down Big Tasks
```
❌ 큰 작업을 한 번에 처리
✅ 작은 단위로 분해
```

**분해 기준:**
- 파일 3개 이상 수정
- 100줄 이상 코드
- 여러 레이어 동시 수정
- 토큰 과다 사용 예상

**분해 방법:** `/plan-feature` 실행

### Rule 4: Developer Reviews
```
❌ 코드 작성 후 바로 다음 단계
✅ 개발자 리뷰 후 진행
```

**리뷰 요청 형식:**
```
변경 내용:
- [요약]

✅ 테스트 통과
📝 체크리스트 확인 완료

진행할까요?
```

---

## 🔄 WORKFLOWS

### Workflow Selection

```
기존 코드 수정? → Workflow 1
신규 기능? → Workflow 2  
대규모 기능? → Workflow 3
```

### Workflow 1: 기존 코드 수정

```
1. 요구사항 확인 (불명확하면 질문)
2. 기존 테스트 확인
3. 테스트 수정
4. 구현 수정
5. 테스트 실행
6. 개발자 리뷰
```

### Workflow 2: 신규 기능 (TDD)

```
1. 요구사항 확인
2. 테스트 작성 (Red)
3. 최소 구현 (Green)
4. 테스트 실행
5. 개발자 리뷰
6. 리팩토링 (필요시)
```

### Workflow 3: 대규모 기능

```
1. /plan-feature 실행
2. Phase별 분해
3. 각 Phase마다 Workflow 2 반복
4. 진행상황 보고
```

---

## 💬 COMMUNICATION PATTERN

### 응답 구조

```markdown
## 🎯 이해한 내용
[요구사항 재확인]

## ❓ 확인 필요 (있다면)
[구체적 질문]

## 📋 작업 계획
1. [단계별 계획]

## 🔨 구현
[코드/작업]

## ✅ 검증
- [ ] 테스트 통과
- [ ] 체크리스트 완료
```

### 질문 패턴

**✅ 좋은 질문:**
```
"UTM 파라미터 저장 위치를 선택해주세요:
1. 쿠키 (프론트엔드 접근)
2. 세션 (서버만 접근)
3. DB (영구 저장)

추천: 사용자 분석이 목적이면 3번"
```

**❌ 나쁜 질문:**
```
"어떻게 할까요?"
"저장 위치를 정해주세요."
```

---

## 🏗️ PROJECT CONTEXT

### Tech Stack
- **Backend:** FastAPI (Python 3.11+), Spring Boot (Java 17+)
- **Database:** PostgreSQL, MySQL
- **Testing:** pytest, JUnit 5

### Project Structure

**FastAPI:**
```
src/
├── domain/         # 도메인 모델
├── repository/     # 데이터 접근
├── service/        # 비즈니스 로직
├── api/            # API 엔드포인트
├── dto/            # DTO
└── core/           # 설정

tests/
├── unit/           # 단위 테스트
└── integration/    # 통합 테스트
```

---

## 📝 CODE STYLE

### Python (FastAPI)

**1. Type Hints (필수)**
```python
def 사용자_생성(이름: str, 이메일: str) -> User:
    pass
```

**2. Docstring (상세)**
```python
def 페이지네이션_조회(
    페이지: int,
    페이지_크기: int
) -> PaginatedResponse[User]:
    """사용자 목록을 페이지네이션하여 조회합니다.
    
    Args:
        페이지: 페이지 번호 (1부터 시작)
        페이지_크기: 한 페이지당 항목 수
    
    Returns:
        PaginatedResponse[User]: 페이지네이션된 사용자 목록
    
    Raises:
        ValueError: 페이지 번호가 0 이하인 경우
    """
    pass
```

**3. Service Layer**
```python
class UserService:
    """사용자 관리 서비스"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def 사용자_생성(self, dto: UserCreateDTO) -> User:
        # 비즈니스 로직
        await self._이름_중복_검증(dto.이름)
        return await self.repository.생성(dto)
```

**4. 한글 변수명 (비즈니스 로직)**
```python
# ✅ 비즈니스: 한글
총_금액 = sum(상품.가격 for 상품 in 상품_목록)
할인_금액 = await self._할인_계산(고객_ID)

# ✅ 기술: 영문
async def execute_query(query: str, params: dict):
    pass
```

**5. DB 최적화**
```python
# ✅ Batch 처리
users = await repository.find_by_ids(user_ids)

# ✅ Select 필드 최소화
users = await repository.find_all(
    select_fields=["id", "이름", "이메일"]
)
```

**6. 추상화**
```python
from abc import ABC, abstractmethod

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def 생성(self, entity: T) -> T:
        pass
```

**7. 중첩 클래스 지양**
```python
# ❌ Bad
class UserService:
    class UserValidator:  # 중첩
        pass

# ✅ Good
class UserValidator:
    pass

class UserService:
    def __init__(self, validator: UserValidator):
        pass
```

### Java (Spring Boot)

**Service + Repository**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    
    /**
     * 사용자를 생성합니다.
     */
    public User createUser(UserCreateDTO dto) {
        validateUserName(dto.getName());
        return userRepository.save(dto.toEntity());
    }
}
```

---

## ✅ CODE REVIEW CHECKLIST

모든 코드는 이 체크리스트를 통과해야 합니다:

### Functionality
- [ ] 요구사항 정확히 구현
- [ ] 엣지 케이스 처리
- [ ] 에러 핸들링

### Code Quality
- [ ] Type hint 완비
- [ ] Docstring 상세
- [ ] 변수/함수명 명확
- [ ] 중복 코드 없음
- [ ] 단일 책임 원칙

### Database
- [ ] N+1 쿼리 없음
- [ ] Batch 처리 사용
- [ ] 필요 컬럼만 SELECT
- [ ] 인덱스 고려

### Testing
- [ ] 단위 테스트 존재
- [ ] 커버리지 충분 (Service 90%+)
- [ ] 모든 테스트 통과
- [ ] 엣지 케이스 테스트

### Architecture
- [ ] Service Layer 패턴
- [ ] 관심사 분리
- [ ] 의존성 주입
- [ ] 적절한 추상화

### Performance
- [ ] 불필요한 계산 없음
- [ ] 메모리 효율적
- [ ] 비동기 처리 적절 (FastAPI)

### Security
- [ ] SQL Injection 방어
- [ ] 민감정보 로그 제외
- [ ] 인증/인가 적절

---

## 🧪 TESTING GUIDELINES

### AAA Pattern (Arrange-Act-Assert)

```python
def test_사용자_생성_성공():
    # Arrange
    repository = Mock(UserRepository)
    service = UserService(repository)
    dto = UserCreateDTO(이름="홍길동")
    
    # Act
    result = await service.사용자_생성(dto)
    
    # Assert
    assert result.이름 == "홍길동"
    repository.생성.assert_called_once()
```

### Test Coverage 목표
- Service: 90%+
- Repository: 80%+
- API: 80%+

### Test Naming
```python
# ✅ Good
def test_중복_이름으로_사용자_생성시_ValueError_발생():
    pass

# ❌ Bad
def test_user_create():
    pass
```

---

## 🚨 COMMON MISTAKES

### 1. 테스트 없이 코드 작성
```
❌ "먼저 구현하고 테스트 추가"
✅ "테스트 먼저"
```

### 2. 큰 PR
```
❌ 10개 파일 동시 수정
✅ 기능별 작은 단위
```

### 3. Repository에 비즈니스 로직
```python
# ❌ Bad
class UserRepository:
    async def create_user(self, dto):
        if len(dto.name) < 3:  # 비즈니스 로직
            raise ValueError("...")
        return await db.save(dto)

# ✅ Good
class UserService:
    async def create_user(self, dto):
        self._validate_name(dto.name)  # 비즈니스 로직
        return await self.repository.create(dto)
```

---

## 📚 CONTEXT MANAGEMENT

### Planning Documents
- 기능 요구사항은 `.claude/plans/` 에 Markdown으로 작성
- PRP (Product Requirements Prompt) 패턴 사용
- 각 세션 시작 시 관련 문서 확인

### Session Context
- 세션 종료 시 주요 학습 내용 요약
- 다음 세션을 위한 컨텍스트 기록
- `.claude/context.md` 활용 권장

---

## 🎓 LEARNING MODE

kdy가 새로운 개념 학습 요청 시:

```markdown
## 📖 개념 설명
[간단한 설명]

## 💡 kdy 프로젝트 활용
[실제 적용 예시]

## 📝 코드 예제
[FastAPI/Spring]

## ✅ 장단점
[trade-off]

## 🔗 참고 자료
[링크]
```

---

## 🔧 CUSTOM COMMANDS

### Available Commands
- `/test-first` - 테스트 우선 개발 강제
- `/review-code` - 코드 리뷰 체크리스트 실행
- `/check-workflow` - 워크플로우 준수 확인
- `/plan-feature` - 대규모 기능 계획 수립

### Adding Custom Commands
`.claude/commands/`에 Markdown 파일 추가:
```markdown
# /my-command

[커맨드 설명]

## Steps
1. [단계]

## Example
```
/my-command argument
```
```

---

## 📌 FINAL CHECKLIST

코드 완료 후:

- [ ] `/test-first` 실행
- [ ] 모든 테스트 통과
- [ ] `/review-code` 통과
- [ ] Type hint 완비
- [ ] Docstring 상세
- [ ] DB 쿼리 최적화
- [ ] Service Layer 적용
- [ ] 개발자 리뷰 요청

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-23  
**Maintainer:** kdy @ NEWEYE  
**Tech Stack:** FastAPI, Spring Boot, PostgreSQL, MySQL

---

## 💡 TIPS

### Context Engineering
- 관련 파일들을 먼저 읽어서 컨텍스트 구축
- examples/ 폴더의 패턴 참조
- 기존 코드 스타일 학습 후 적용

### Incremental Development
- 작은 단위로 자주 커밋
- 각 단계마다 테스트
- 지속적인 리팩토링

### Token Management
- 응답이 길어지면 단계별로 분할
- 각 단계 완료 후 계속 진행 여부 확인
- 불필요한 반복 설명 지양
