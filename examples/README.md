# Code Examples

AI 어시스턴트가 참조할 수 있는 코드 패턴 예시 모음입니다.

## 📁 Structure

```
examples/
├── README.md           # 이 파일
└── fastapi/            # FastAPI 예시
    ├── services/       # Service Layer 패턴
    ├── repositories/   # Repository 패턴
    └── tests/          # 테스트 패턴
```

## 🎯 Purpose

이 예시들은:
1. **AI 학습용**: AI가 kdy의 코딩 스타일을 학습
2. **참조용**: 새 코드 작성 시 패턴 참조
3. **템플릿**: 복사해서 수정 가능

## 📚 Examples Overview

### FastAPI Examples

#### Services (`examples/fastapi/services/`)
- **user_service.py**: 사용자 관리 서비스
  - 의존성 주입 패턴
  - 비즈니스 로직 캡슐화
  - 에러 핸들링
  - Docstring 예시

#### Repositories (`examples/fastapi/repositories/`)
- **user_repository.py**: 사용자 데이터 접근
  - 추상 Repository 패턴
  - Batch 처리
  - 쿼리 최적화
  - Type hints

#### Tests (`examples/fastapi/tests/`)
- **test_user_service.py**: Service 테스트
  - AAA 패턴 (Arrange-Act-Assert)
  - Mocking 패턴
  - Fixture 활용
  - 엣지 케이스 테스트

## 🔍 How to Use

### For AI Assistant

코드 작성 시:
```python
# 1. 관련 예시 파일 읽기
view examples/fastapi/services/user_service.py

# 2. 패턴 학습
# - Docstring 스타일
# - Type hints 사용법
# - 에러 핸들링 방식

# 3. 패턴 적용
# - 동일한 스타일로 새 코드 작성
```

### For Developers

kdy가 직접 참조:
```bash
# 서비스 레이어 패턴 확인
cat examples/fastapi/services/user_service.py

# 테스트 패턴 확인
cat examples/fastapi/tests/test_user_service.py
```

## 📋 Pattern Checklist

각 예시 파일은 다음을 포함:
- [ ] Type hints (모든 함수)
- [ ] 상세한 Docstring
- [ ] 한글 변수명 (비즈니스 로직)
- [ ] 에러 핸들링
- [ ] 테스트 가능한 구조

## 🎓 Key Patterns

### 1. Service Layer
```python
class UserService:
    """비즈니스 로직을 캡슐화"""
    
    def __init__(self, repository: UserRepository):
        """의존성 주입"""
        self.repository = repository
    
    async def 사용자_생성(self, dto: UserCreateDTO) -> User:
        """한글 함수명 + Type hints + Docstring"""
        # 검증
        await self._이름_중복_검증(dto.이름)
        
        # 저장
        return await self.repository.생성(dto)
```

### 2. Repository Pattern
```python
class UserRepository:
    """데이터 접근만 담당"""
    
    async def find_by_ids(self, ids: list[int]) -> list[User]:
        """Batch 처리로 N+1 방지"""
        stmt = select(User).where(User.id.in_(ids))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
```

### 3. Test Pattern
```python
@pytest.mark.asyncio
async def test_사용자_생성_성공():
    """AAA 패턴"""
    # Arrange
    mock_repo = AsyncMock()
    service = UserService(mock_repo)
    
    # Act
    result = await service.사용자_생성(dto)
    
    # Assert
    assert result.이름 == "홍길동"
```

## 🚀 Quick Start

### 새 Service 작성 시

```bash
# 1. 예시 파일 복사
cp examples/fastapi/services/user_service.py src/service/my_service.py

# 2. 이름 변경
# UserService → MyService

# 3. 로직 구현

# 4. 테스트 복사
cp examples/fastapi/tests/test_user_service.py tests/test_my_service.py
```

## 📝 Notes

- **예시는 최소한으로 유지**: 핵심 패턴만
- **실제 프로젝트 코드 아님**: 학습/참조용
- **kdy 스타일 반영**: 실제 사용하는 패턴
- **정기 업데이트**: 새로운 패턴 추가

## 🔄 Updates

새로운 패턴 추가 시:
1. 예시 파일 작성
2. 이 README 업데이트
3. CLAUDE.md에 언급 (필요시)

---

**Last Updated**: 2025-11-23  
**Maintainer**: kdy @ NEWEYE
