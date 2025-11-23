"""
사용자 관리 서비스

비즈니스 로직을 캡슐화하고 Repository를 통해 데이터에 접근합니다.
"""
from typing import Protocol

from src.domain.user import User
from src.dto.request.user import UserCreateDTO, UserUpdateDTO
from src.dto.response.user import UserResponse, PaginatedResponse


class IUserRepository(Protocol):
    """UserRepository 인터페이스
    
    의존성 역전 원칙(DIP)을 위한 Protocol 정의
    """
    
    async def 생성(self, user: User) -> User:
        """사용자를 생성합니다."""
        ...
    
    async def 조회(self, user_id: int) -> User | None:
        """ID로 사용자를 조회합니다."""
        ...
    
    async def 이름으로_조회(self, 이름: str) -> User | None:
        """이름으로 사용자를 조회합니다."""
        ...
    
    async def 목록_조회(
        self,
        페이지: int,
        페이지_크기: int
    ) -> tuple[list[User], int]:
        """페이지네이션된 사용자 목록을 조회합니다."""
        ...
    
    async def 수정(self, user: User) -> User:
        """사용자 정보를 수정합니다."""
        ...
    
    async def 삭제(self, user_id: int) -> bool:
        """사용자를 삭제합니다."""
        ...


class UserService:
    """사용자 관리 서비스
    
    사용자 생명주기를 관리하고 비즈니스 로직을 처리합니다.
    
    Attributes:
        repository: 사용자 데이터 접근 객체
    
    Example:
        >>> repository = UserRepository(session)
        >>> service = UserService(repository)
        >>> user = await service.사용자_생성(dto)
    """
    
    # 비즈니스 규칙 상수
    최소_이름_길이 = 3
    최대_이름_길이 = 50
    
    def __init__(self, repository: IUserRepository):
        """
        Args:
            repository: 사용자 Repository
        """
        self.repository = repository
    
    async def 사용자_생성(self, dto: UserCreateDTO) -> User:
        """사용자를 생성합니다.
        
        Args:
            dto: 사용자 생성 요청 DTO
                - 이름: 3-50자
                - 이메일: 유효한 이메일 형식
        
        Returns:
            User: 생성된 사용자 엔티티
        
        Raises:
            ValueError: 검증 실패 시
                - 이름이 3자 미만
                - 이름이 50자 초과
                - 이메일 형식 오류
                - 이름 중복
        
        Example:
            >>> dto = UserCreateDTO(이름="홍길동", 이메일="hong@test.com")
            >>> user = await service.사용자_생성(dto)
            >>> print(user.이름)
            '홍길동'
        """
        # 1. 입력 검증
        self._이름_길이_검증(dto.이름)
        self._이메일_형식_검증(dto.이메일)
        
        # 2. 비즈니스 규칙 검증
        await self._이름_중복_검증(dto.이름)
        
        # 3. 엔티티 생성
        user = User(
            이름=dto.이름.strip(),
            이메일=dto.이메일.lower(),
            활성화=True
        )
        
        # 4. 저장
        return await self.repository.생성(user)
    
    async def 사용자_조회(self, user_id: int) -> User:
        """사용자를 조회합니다.
        
        Args:
            user_id: 사용자 ID
        
        Returns:
            User: 조회된 사용자
        
        Raises:
            ValueError: 사용자가 존재하지 않는 경우
        """
        user = await self.repository.조회(user_id)
        
        if not user:
            raise ValueError(f"사용자를 찾을 수 없습니다: {user_id}")
        
        return user
    
    async def 사용자_목록_조회(
        self,
        페이지: int = 1,
        페이지_크기: int = 20
    ) -> PaginatedResponse[UserResponse]:
        """페이지네이션된 사용자 목록을 조회합니다.
        
        Args:
            페이지: 페이지 번호 (1부터 시작)
            페이지_크기: 한 페이지당 항목 수 (기본: 20, 최대: 100)
        
        Returns:
            PaginatedResponse[UserResponse]: 페이지네이션된 사용자 목록
                - items: 사용자 목록
                - total: 전체 항목 수
                - page: 현재 페이지
                - page_size: 페이지 크기
                - pages: 전체 페이지 수
        
        Raises:
            ValueError: 페이지 번호가 0 이하이거나 페이지 크기가 범위를 벗어난 경우
        """
        # 입력 검증
        if 페이지 < 1:
            raise ValueError("페이지 번호는 1 이상이어야 합니다")
        
        if not (1 <= 페이지_크기 <= 100):
            raise ValueError("페이지 크기는 1-100 사이여야 합니다")
        
        # 조회
        users, total = await self.repository.목록_조회(페이지, 페이지_크기)
        
        # DTO 변환
        items = [UserResponse.from_entity(user) for user in users]
        
        # 페이지네이션 응답 생성
        return PaginatedResponse(
            items=items,
            total=total,
            page=페이지,
            page_size=페이지_크기,
            pages=(total + 페이지_크기 - 1) // 페이지_크기
        )
    
    async def 사용자_수정(
        self,
        user_id: int,
        dto: UserUpdateDTO
    ) -> User:
        """사용자 정보를 수정합니다.
        
        Args:
            user_id: 사용자 ID
            dto: 수정할 정보
        
        Returns:
            User: 수정된 사용자
        
        Raises:
            ValueError: 사용자가 없거나 검증 실패 시
        """
        # 기존 사용자 조회
        user = await self.사용자_조회(user_id)
        
        # 수정할 필드 검증 및 업데이트
        if dto.이름:
            self._이름_길이_검증(dto.이름)
            
            # 다른 사용자가 사용 중인지 확인
            if dto.이름 != user.이름:
                await self._이름_중복_검증(dto.이름)
            
            user.이름 = dto.이름.strip()
        
        if dto.이메일:
            self._이메일_형식_검증(dto.이메일)
            user.이메일 = dto.이메일.lower()
        
        # 저장
        return await self.repository.수정(user)
    
    async def 사용자_삭제(self, user_id: int) -> bool:
        """사용자를 삭제합니다.
        
        Args:
            user_id: 사용자 ID
        
        Returns:
            bool: 삭제 성공 여부
        
        Raises:
            ValueError: 사용자가 존재하지 않는 경우
        """
        # 존재 여부 확인
        await self.사용자_조회(user_id)
        
        # 삭제
        return await self.repository.삭제(user_id)
    
    # Private 검증 메서드들
    
    def _이름_길이_검증(self, 이름: str) -> None:
        """이름 길이를 검증합니다.
        
        Args:
            이름: 검증할 이름
        
        Raises:
            ValueError: 이름 길이가 범위를 벗어난 경우
        """
        이름_길이 = len(이름.strip())
        
        if 이름_길이 < self.최소_이름_길이:
            raise ValueError(
                f"이름은 {self.최소_이름_길이}자 이상이어야 합니다"
            )
        
        if 이름_길이 > self.최대_이름_길이:
            raise ValueError(
                f"이름은 {self.최대_이름_길이}자 이하여야 합니다"
            )
    
    def _이메일_형식_검증(self, 이메일: str) -> None:
        """이메일 형식을 검증합니다.
        
        Args:
            이메일: 검증할 이메일
        
        Raises:
            ValueError: 이메일 형식이 올바르지 않은 경우
        """
        import re
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, 이메일):
            raise ValueError(f"올바른 이메일 형식이 아닙니다: {이메일}")
    
    async def _이름_중복_검증(self, 이름: str) -> None:
        """이름 중복을 검증합니다.
        
        Args:
            이름: 검증할 이름
        
        Raises:
            ValueError: 이름이 이미 존재하는 경우
        """
        existing = await self.repository.이름으로_조회(이름)
        
        if existing:
            raise ValueError(f"이미 존재하는 이름입니다: {이름}")
