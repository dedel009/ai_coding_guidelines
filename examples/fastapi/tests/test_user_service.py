"""
사용자 서비스 테스트

AAA 패턴(Arrange-Act-Assert)을 사용하여 테스트를 작성합니다.
"""
import pytest
from unittest.mock import AsyncMock, Mock

from src.service.user_service import UserService
from src.domain.user import User
from src.dto.request.user import UserCreateDTO, UserUpdateDTO
from src.dto.response.user import PaginatedResponse


class Test사용자서비스:
    """UserService 테스트 클래스
    
    테스트 케이스는 한글로 작성하여 의도를 명확히 합니다.
    """
    
    # Fixtures
    
    @pytest.fixture
    def mock_repository(self):
        """Mock Repository 픽스처
        
        AsyncMock을 사용하여 비동기 메서드를 모킹합니다.
        """
        return AsyncMock()
    
    @pytest.fixture
    def user_service(self, mock_repository):
        """UserService 픽스처
        
        의존성 주입을 통해 Mock Repository를 주입합니다.
        """
        return UserService(mock_repository)
    
    @pytest.fixture
    def 샘플_사용자_DTO(self):
        """샘플 UserCreateDTO 픽스처"""
        return UserCreateDTO(
            이름="홍길동",
            이메일="hong@test.com"
        )
    
    @pytest.fixture
    def 샘플_사용자(self):
        """샘플 User 엔티티 픽스처"""
        return User(
            id=1,
            이름="홍길동",
            이메일="hong@test.com",
            활성화=True
        )
    
    # 사용자 생성 테스트
    
    @pytest.mark.asyncio
    async def test_사용자_생성_성공(
        self,
        user_service,
        mock_repository,
        샘플_사용자_DTO,
        샘플_사용자
    ):
        """사용자 생성이 정상적으로 동작하는 경우
        
        AAA 패턴:
        - Arrange: 테스트 데이터 준비
        - Act: 테스트 대상 실행
        - Assert: 결과 검증
        """
        # Arrange (준비)
        mock_repository.이름으로_조회.return_value = None  # 중복 없음
        mock_repository.생성.return_value = 샘플_사용자
        
        # Act (실행)
        result = await user_service.사용자_생성(샘플_사용자_DTO)
        
        # Assert (검증)
        assert result.이름 == "홍길동"
        assert result.이메일 == "hong@test.com"
        assert result.활성화 is True
        
        # Mock 호출 검증
        mock_repository.이름으로_조회.assert_called_once_with("홍길동")
        mock_repository.생성.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_중복_이름으로_사용자_생성시_ValueError_발생(
        self,
        user_service,
        mock_repository,
        샘플_사용자_DTO,
        샘플_사용자
    ):
        """중복된 이름으로 사용자 생성 시 ValueError 발생"""
        # Arrange
        mock_repository.이름으로_조회.return_value = 샘플_사용자  # 중복 있음
        
        # Act & Assert
        with pytest.raises(ValueError, match="이미 존재하는 이름"):
            await user_service.사용자_생성(샘플_사용자_DTO)
        
        # 생성 메서드는 호출되지 않아야 함
        mock_repository.생성.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_짧은_이름으로_사용자_생성시_ValueError_발생(
        self,
        user_service,
        mock_repository
    ):
        """3자 미만의 이름으로 사용자 생성 시 ValueError 발생"""
        # Arrange
        짧은_이름_DTO = UserCreateDTO(
            이름="홍",  # 1자
            이메일="hong@test.com"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="3자 이상"):
            await user_service.사용자_생성(짧은_이름_DTO)
        
        # Repository 호출 없음
        mock_repository.이름으로_조회.assert_not_called()
        mock_repository.생성.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_긴_이름으로_사용자_생성시_ValueError_발생(
        self,
        user_service,
        mock_repository
    ):
        """50자 초과 이름으로 사용자 생성 시 ValueError 발생"""
        # Arrange
        긴_이름_DTO = UserCreateDTO(
            이름="가" * 51,  # 51자
            이메일="hong@test.com"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="50자 이하"):
            await user_service.사용자_생성(긴_이름_DTO)
    
    @pytest.mark.asyncio
    async def test_잘못된_이메일_형식으로_사용자_생성시_ValueError_발생(
        self,
        user_service,
        mock_repository
    ):
        """잘못된 이메일 형식으로 사용자 생성 시 ValueError 발생"""
        # Arrange
        잘못된_이메일_DTO = UserCreateDTO(
            이름="홍길동",
            이메일="invalid-email"  # 잘못된 형식
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="올바른 이메일 형식"):
            await user_service.사용자_생성(잘못된_이메일_DTO)
    
    @pytest.mark.asyncio
    async def test_이름과_이메일이_정규화되어_저장됨(
        self,
        user_service,
        mock_repository,
        샘플_사용자
    ):
        """이름은 trim, 이메일은 소문자로 정규화되어 저장"""
        # Arrange
        공백_포함_DTO = UserCreateDTO(
            이름="  홍길동  ",  # 앞뒤 공백
            이메일="HONG@TEST.COM"  # 대문자
        )
        mock_repository.이름으로_조회.return_value = None
        mock_repository.생성.return_value = 샘플_사용자
        
        # Act
        await user_service.사용자_생성(공백_포함_DTO)
        
        # Assert - 생성 메서드에 전달된 인자 확인
        call_args = mock_repository.생성.call_args[0][0]
        assert call_args.이름 == "홍길동"  # 공백 제거
        assert call_args.이메일 == "hong@test.com"  # 소문자 변환
    
    # 사용자 조회 테스트
    
    @pytest.mark.asyncio
    async def test_사용자_조회_성공(
        self,
        user_service,
        mock_repository,
        샘플_사용자
    ):
        """사용자 조회가 정상적으로 동작하는 경우"""
        # Arrange
        mock_repository.조회.return_value = 샘플_사용자
        
        # Act
        result = await user_service.사용자_조회(1)
        
        # Assert
        assert result.id == 1
        assert result.이름 == "홍길동"
        mock_repository.조회.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_존재하지_않는_사용자_조회시_ValueError_발생(
        self,
        user_service,
        mock_repository
    ):
        """존재하지 않는 사용자 조회 시 ValueError 발생"""
        # Arrange
        mock_repository.조회.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="사용자를 찾을 수 없습니다"):
            await user_service.사용자_조회(999)
    
    # 사용자 목록 조회 테스트
    
    @pytest.mark.asyncio
    async def test_사용자_목록_조회_성공(
        self,
        user_service,
        mock_repository
    ):
        """사용자 목록 조회가 정상적으로 동작하는 경우"""
        # Arrange
        users = [
            User(id=1, 이름="홍길동", 이메일="hong@test.com"),
            User(id=2, 이름="김철수", 이메일="kim@test.com"),
        ]
        mock_repository.목록_조회.return_value = (users, 2)
        
        # Act
        result = await user_service.사용자_목록_조회(페이지=1, 페이지_크기=20)
        
        # Assert
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) == 2
        assert result.total == 2
        assert result.page == 1
        assert result.pages == 1
    
    @pytest.mark.asyncio
    async def test_페이지_번호_0_이하로_조회시_ValueError_발생(
        self,
        user_service,
        mock_repository
    ):
        """페이지 번호가 0 이하인 경우 ValueError 발생"""
        # Act & Assert
        with pytest.raises(ValueError, match="페이지 번호는 1 이상"):
            await user_service.사용자_목록_조회(페이지=0)
        
        mock_repository.목록_조회.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_페이지_크기_범위_벗어나면_ValueError_발생(
        self,
        user_service,
        mock_repository
    ):
        """페이지 크기가 1-100 범위를 벗어나면 ValueError 발생"""
        # Act & Assert
        with pytest.raises(ValueError, match="페이지 크기는 1-100 사이"):
            await user_service.사용자_목록_조회(페이지=1, 페이지_크기=0)
        
        with pytest.raises(ValueError, match="페이지 크기는 1-100 사이"):
            await user_service.사용자_목록_조회(페이지=1, 페이지_크기=101)
    
    # 사용자 수정 테스트
    
    @pytest.mark.asyncio
    async def test_사용자_수정_성공(
        self,
        user_service,
        mock_repository,
        샘플_사용자
    ):
        """사용자 수정이 정상적으로 동작하는 경우"""
        # Arrange
        수정_DTO = UserUpdateDTO(
            이름="홍길순",
            이메일="hongsoon@test.com"
        )
        수정된_사용자 = User(
            id=1,
            이름="홍길순",
            이메일="hongsoon@test.com"
        )
        
        mock_repository.조회.return_value = 샘플_사용자
        mock_repository.이름으로_조회.return_value = None
        mock_repository.수정.return_value = 수정된_사용자
        
        # Act
        result = await user_service.사용자_수정(1, 수정_DTO)
        
        # Assert
        assert result.이름 == "홍길순"
        mock_repository.수정.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_다른_사용자가_사용중인_이름으로_수정시_ValueError_발생(
        self,
        user_service,
        mock_repository,
        샘플_사용자
    ):
        """다른 사용자가 이미 사용 중인 이름으로 수정 시 ValueError 발생"""
        # Arrange
        수정_DTO = UserUpdateDTO(이름="김철수")
        다른_사용자 = User(id=2, 이름="김철수", 이메일="kim@test.com")
        
        mock_repository.조회.return_value = 샘플_사용자
        mock_repository.이름으로_조회.return_value = 다른_사용자
        
        # Act & Assert
        with pytest.raises(ValueError, match="이미 존재하는 이름"):
            await user_service.사용자_수정(1, 수정_DTO)
        
        mock_repository.수정.assert_not_called()
    
    # 사용자 삭제 테스트
    
    @pytest.mark.asyncio
    async def test_사용자_삭제_성공(
        self,
        user_service,
        mock_repository,
        샘플_사용자
    ):
        """사용자 삭제가 정상적으로 동작하는 경우"""
        # Arrange
        mock_repository.조회.return_value = 샘플_사용자
        mock_repository.삭제.return_value = True
        
        # Act
        result = await user_service.사용자_삭제(1)
        
        # Assert
        assert result is True
        mock_repository.삭제.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_존재하지_않는_사용자_삭제시_ValueError_발생(
        self,
        user_service,
        mock_repository
    ):
        """존재하지 않는 사용자 삭제 시 ValueError 발생"""
        # Arrange
        mock_repository.조회.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="사용자를 찾을 수 없습니다"):
            await user_service.사용자_삭제(999)
        
        mock_repository.삭제.assert_not_called()


# 통합 테스트 예시 (선택적)

class Test사용자서비스_통합:
    """실제 DB를 사용한 통합 테스트
    
    Mock 대신 실제 데이터베이스를 사용하여 테스트합니다.
    테스트 DB는 각 테스트마다 초기화됩니다.
    """
    
    @pytest.fixture
    async def db_session(self):
        """테스트용 DB 세션
        
        실제 프로젝트에서는 conftest.py에 정의합니다.
        """
        # 테스트 DB 연결 설정
        # session = await create_test_session()
        # yield session
        # await session.close()
        pass
    
    @pytest.fixture
    def user_repository(self, db_session):
        """실제 UserRepository"""
        # return UserRepository(db_session)
        pass
    
    @pytest.fixture
    def user_service(self, user_repository):
        """실제 UserService"""
        # return UserService(user_repository)
        pass
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_사용자_생성_및_조회_통합(self, user_service):
        """사용자 생성 후 조회까지의 전체 플로우 테스트"""
        # Arrange
        dto = UserCreateDTO(이름="홍길동", 이메일="hong@test.com")
        
        # Act
        created = await user_service.사용자_생성(dto)
        retrieved = await user_service.사용자_조회(created.id)
        
        # Assert
        assert created.id == retrieved.id
        assert created.이름 == retrieved.이름
        assert created.이메일 == retrieved.이메일


# Parametrize 예시

class Test이름_검증:
    """Parametrize를 사용한 경계값 테스트"""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("이름,예상_결과", [
        ("홍", False),           # 1자 - 실패
        ("홍길", False),         # 2자 - 실패
        ("홍길동", True),        # 3자 - 성공
        ("가" * 50, True),       # 50자 - 성공
        ("가" * 51, False),      # 51자 - 실패
    ])
    async def test_이름_길이_검증(
        self,
        이름,
        예상_결과,
        user_service,
        mock_repository
    ):
        """다양한 이름 길이에 대한 검증 테스트"""
        # Arrange
        dto = UserCreateDTO(이름=이름, 이메일="test@test.com")
        mock_repository.이름으로_조회.return_value = None
        mock_repository.생성.return_value = User(id=1, 이름=이름, 이메일="test@test.com")
        
        # Act & Assert
        if 예상_결과:
            result = await user_service.사용자_생성(dto)
            assert result is not None
        else:
            with pytest.raises(ValueError):
                await user_service.사용자_생성(dto)
