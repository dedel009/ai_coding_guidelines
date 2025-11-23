# Test-First Development

테스트 없이는 코드를 작성하지 않습니다. 이것은 협상 불가능한 규칙입니다.

## When to Use

- 모든 코드 작성/수정 작업 시작 전
- kdy가 코드 변경을 요청할 때
- 새로운 기능을 추가할 때

## Workflow

### 1. 기존 코드 수정 시

```
1. 관련 테스트 파일 확인
   └─ tests/ 디렉토리에서 검색
   
2. 테스트가 있는가?
   ├─ YES → 테스트 읽고 이해
   │         └─ 테스트 수정 필요 여부 확인
   │         └─ 테스트 먼저 수정
   │         └─ 구현 수정
   │         └─ 테스트 실행
   │
   └─ NO → STOP
             └─ kdy에게 알림: "테스트가 없습니다. 테스트를 먼저 작성할까요?"
             └─ 승인 받은 후 테스트 작성
             └─ 그 다음 구현 수정
```

### 2. 신규 기능 개발 시 (TDD)

```
1. Red: 실패하는 테스트 작성
   └─ 요구사항을 테스트로 표현
   └─ 테스트 실행 → 실패 확인
   
2. Green: 최소 구현
   └─ 테스트를 통과하는 최소한의 코드
   └─ 테스트 실행 → 통과 확인
   
3. Refactor: 코드 개선
   └─ 중복 제거
   └─ 가독성 향상
   └─ 테스트 실행 → 통과 유지
   
4. Developer Review
   └─ kdy에게 리뷰 요청
```

## Response Template

### 기존 테스트가 있을 때

```markdown
## 🔍 테스트 확인

기존 테스트를 찾았습니다:
- `tests/test_user_service.py::test_사용자_생성`
- `tests/test_user_service.py::test_이름_중복_검증`

## 📝 수정 계획

1. 테스트 수정:
   - test_이름_중복_검증: 2자 → 3자로 변경
   
2. 구현 수정:
   - user_service.py: _이름_길이_검증 함수 수정

진행할까요?
```

### 기존 테스트가 없을 때

```markdown
## ⚠️ 테스트 없음

관련 테스트를 찾지 못했습니다.

## 📝 제안

다음 테스트를 먼저 작성하겠습니다:

```python
# tests/test_user_service.py

def test_사용자_생성_성공():
    """사용자 생성이 정상적으로 동작하는지 테스트"""
    # Arrange
    # Act
    # Assert
    pass

def test_중복_이름_검증():
    """중복된 이름으로 생성 시 에러 발생 테스트"""
    pass
```

테스트를 먼저 작성할까요?
```

## Example Usage

```
kdy: "사용자 이름 검증을 2자에서 3자로 변경해줘"

AI: /test-first를 실행합니다...

## 🔍 테스트 확인
기존 테스트: tests/test_user_service.py::test_이름_길이_검증

## 📝 수정 계획
1. 테스트 수정 (2자 → 3자)
2. 구현 수정

진행할까요?
```

## Rules

1. **절대 테스트를 건너뛰지 않음**
2. **테스트가 없으면 코드를 작성하지 않음**
3. **kdy의 승인 없이 테스트를 생략하지 않음**
4. **"나중에 테스트 추가"는 허용되지 않음**

## Test File Locations

### FastAPI
```
tests/
├── unit/
│   ├── service/
│   │   └── test_user_service.py
│   └── repository/
│       └── test_user_repository.py
└── integration/
    └── api/
        └── test_user_api.py
```

### Spring Boot
```
src/test/java/
└── com/company/project/
    ├── service/
    │   └── UserServiceTest.java
    └── controller/
        └── UserControllerTest.java
```

## Quick Test Template (pytest)

```python
import pytest
from unittest.mock import AsyncMock

class Test사용자서비스:
    """사용자 서비스 테스트"""
    
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()
    
    @pytest.fixture
    def user_service(self, mock_repository):
        return UserService(mock_repository)
    
    @pytest.mark.asyncio
    async def test_사용자_생성_성공(self, user_service, mock_repository):
        """사용자 생성 성공 케이스"""
        # Arrange
        dto = UserCreateDTO(이름="홍길동")
        mock_repository.이름으로_조회.return_value = None
        mock_repository.생성.return_value = User(id=1, 이름="홍길동")
        
        # Act
        result = await user_service.사용자_생성(dto)
        
        # Assert
        assert result.이름 == "홍길동"
        mock_repository.생성.assert_called_once()
```

## Final Checklist

작업 시작 전:
- [ ] 관련 테스트 파일 검색 완료
- [ ] 테스트 존재 여부 확인 완료
- [ ] 테스트 없으면 kdy에게 알림
- [ ] 테스트 먼저 작성/수정
- [ ] kdy 승인 후 구현 진행
