# Code Review Checklist

모든 코드는 이 체크리스트를 통과해야 합니다.

## When to Use

- 코드 작성 완료 후
- kdy에게 리뷰 요청하기 전
- PR 생성 전

## Review Categories

### 1. Functionality (기능) ⚙️

**체크 항목:**
- [ ] 요구사항을 정확히 구현했는가?
- [ ] 모든 엣지 케이스를 처리하는가?
- [ ] 에러 핸들링이 적절한가?
- [ ] 예상치 못한 입력에 대응하는가?

**검증 방법:**
```python
# ✅ Good: 엣지 케이스 처리
def 사용자_생성(이름: str | None) -> User:
    if not 이름:
        raise ValueError("이름은 필수입니다")
    if not 이름.strip():
        raise ValueError("이름은 공백일 수 없습니다")
    # 구현
```

### 2. Code Quality (코드 품질) 📝

**체크 항목:**
- [ ] Type hint가 모든 함수에 있는가?
- [ ] Docstring이 충분히 상세한가?
- [ ] 변수명/함수명이 명확한가?
- [ ] 중복 코드가 없는가?
- [ ] 각 함수가 단일 책임을 지는가?

**검증 방법:**
```python
# ✅ Good
def 페이지네이션_조회(
    페이지: int,
    페이지_크기: int,
    필터: dict | None = None
) -> PaginatedResponse[User]:
    """사용자 목록을 페이지네이션하여 조회합니다.
    
    Args:
        페이지: 페이지 번호 (1부터 시작)
        페이지_크기: 한 페이지당 항목 수
        필터: 선택적 필터 조건
    
    Returns:
        PaginatedResponse[User]: 페이지네이션된 결과
    """
    pass

# ❌ Bad: Type hint, docstring 없음
def get_users(page, size, filter=None):
    pass
```

### 3. Database (DB 최적화) 🗄️

**체크 항목:**
- [ ] N+1 쿼리가 없는가?
- [ ] Batch 처리를 사용했는가?
- [ ] SELECT 시 필요한 컬럼만 조회하는가?
- [ ] 인덱스를 고려했는가?

**검증 방법:**
```python
# ❌ Bad: N+1 쿼리
for user_id in user_ids:
    user = await repository.find_by_id(user_id)  # N번 쿼리
    users.append(user)

# ✅ Good: Batch 처리
users = await repository.find_by_ids(user_ids)  # 1번 쿼리

# ✅ Good: 필요한 컬럼만
users = await repository.find_all(
    select_fields=["id", "이름", "이메일"]
)
```

### 4. Testing (테스트) 🧪

**체크 항목:**
- [ ] 단위 테스트가 존재하는가?
- [ ] 테스트 커버리지가 충분한가? (Service 90%+)
- [ ] 모든 테스트가 통과하는가?
- [ ] 엣지 케이스 테스트가 있는가?

**검증 명령:**
```bash
# 테스트 실행
pytest tests/ -v

# 커버리지 확인
pytest --cov=src tests/
pytest --cov=src --cov-report=html tests/
```

**필수 테스트 케이스:**
- 정상 케이스
- 에러 케이스 (각 에러 타입별)
- 경계값 테스트
- null/empty 입력

### 5. Documentation (문서화) 📚

**체크 항목:**
- [ ] API 문서가 자동 생성되는가? (FastAPI)
- [ ] README 업데이트가 필요한가?
- [ ] 복잡한 로직에 주석이 있는가?
- [ ] 설정 파일에 설명이 있는가?

**검증 방법:**
```python
# ✅ Good: 복잡한 로직에 주석
def 할인_계산(금액: int, 고객_등급: str) -> int:
    """할인 금액을 계산합니다.
    
    할인율:
    - VIP: 20%
    - Gold: 10% 
    - Silver: 5%
    - 기본: 0%
    """
    discount_rates = {
        "VIP": 0.2,
        "Gold": 0.1,
        "Silver": 0.05
    }
    return int(금액 * discount_rates.get(고객_등급, 0))
```

### 6. Architecture (아키텍처) 🏛️

**체크 항목:**
- [ ] Service Layer 패턴을 따르는가?
- [ ] 관심사가 분리되어 있는가?
- [ ] 의존성 주입을 사용하는가?
- [ ] 추상화가 적절한가?

**검증 방법:**
```python
# ✅ Good: Service Layer 분리
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def 사용자_생성(self, dto: UserCreateDTO) -> User:
        # 비즈니스 로직
        self._validate(dto)
        return await self.repository.생성(dto)

# ❌ Bad: API에서 직접 DB 접근
@app.post("/users")
async def create_user(dto: UserCreateDTO):
    user = await db.execute(...)  # 직접 DB 접근
    return user
```

### 7. Performance (성능) ⚡

**체크 항목:**
- [ ] 불필요한 계산이 없는가?
- [ ] 메모리 사용이 효율적인가?
- [ ] 비동기 처리가 적절한가? (FastAPI)
- [ ] 캐싱이 필요한 부분은 없는가?

**검증 방법:**
```python
# ❌ Bad: 매번 계산
for item in items:
    total = calculate_heavy_operation()  # 반복 계산
    item.total = total

# ✅ Good: 한 번만 계산
total = calculate_heavy_operation()
for item in items:
    item.total = total

# ✅ Good: 비동기 처리 (FastAPI)
async def 사용자_목록_조회():
    users = await repository.find_all()  # 비동기
    return users
```

### 8. Security (보안) 🔒

**체크 항목:**
- [ ] SQL Injection 방어가 되는가?
- [ ] 민감 정보가 로그에 남지 않는가?
- [ ] 인증/인가가 적절한가?
- [ ] XSS, CSRF 방어가 되는가?

**검증 방법:**
```python
# ✅ Good: ORM 사용 (SQL Injection 방지)
users = await session.execute(
    select(User).where(User.name == name)
)

# ❌ Bad: Raw SQL
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✅ Good: 민감정보 마스킹
logger.info(f"User login: {email[:3]}***@***")

# ❌ Bad: 민감정보 노출
logger.info(f"User login: {email}, password: {password}")
```

## Review Process

### Step 1: Self Review
```markdown
## 📋 Self Review

### Functionality ⚙️
- [x] 요구사항 구현 완료
- [x] 엣지 케이스 처리
- [x] 에러 핸들링

### Code Quality 📝
- [x] Type hints 완비
- [x] Docstring 작성
- [x] 명확한 네이밍

[... 각 카테고리 체크]
```

### Step 2: Test Review
```bash
# 모든 테스트 실행
pytest tests/ -v

# 커버리지 확인
pytest --cov=src --cov-report=term-missing tests/

# 결과 확인
# ✅ 모든 테스트 통과
# ✅ Service 커버리지 90%+
```

### Step 3: Report to kdy

```markdown
## ✅ Code Review 완료

### 통과 항목
- ✅ Functionality: 모든 요구사항 구현
- ✅ Code Quality: Type hint, Docstring 완비
- ✅ Database: Batch 처리 적용, N+1 없음
- ✅ Testing: 커버리지 92%
- ✅ Architecture: Service Layer 적용

### 테스트 결과
```
tests/test_user_service.py::test_사용자_생성_성공 PASSED
tests/test_user_service.py::test_중복_이름_검증 PASSED
tests/test_user_service.py::test_이름_길이_검증 PASSED

Coverage: 92%
```

### 변경 파일
- src/service/user_service.py
- tests/test_user_service.py

진행해도 될까요?
```

## Quick Check Commands

```bash
# 전체 체크
pytest tests/ -v --cov=src --cov-report=term-missing

# 특정 파일만
pytest tests/test_user_service.py -v

# 린트 체크
ruff check src/
mypy src/

# 포맷 체크
black --check src/
```

## Red Flags (즉시 수정)

- 🚨 테스트 없음
- 🚨 테스트 실패
- 🚨 Type hint 없음
- 🚨 SQL Injection 취약점
- 🚨 N+1 쿼리
- 🚨 민감정보 로그 노출
- 🚨 500줄 이상 함수
- 🚨 비즈니스 로직이 Repository에

## Final Checklist

kdy에게 리뷰 요청 전:

- [ ] 8개 카테고리 모두 체크 완료
- [ ] 모든 테스트 통과
- [ ] 커버리지 목표 달성 (Service 90%+)
- [ ] Red Flag 없음
- [ ] 변경사항 요약 작성
- [ ] kdy에게 명확히 리포트
