"""
사용자 Repository

데이터 접근 로직만 담당하며, 비즈니스 로직은 포함하지 않습니다.
"""
from typing import Generic, TypeVar
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user import User


T = TypeVar('T')


class UserRepository:
    """사용자 데이터 접근 객체
    
    데이터베이스와의 모든 상호작용을 담당합니다.
    비즈니스 로직은 포함하지 않고, 순수하게 데이터 CRUD만 처리합니다.
    
    Attributes:
        session: SQLAlchemy 비동기 세션
    
    Example:
        >>> async with AsyncSession(engine) as session:
        ...     repository = UserRepository(session)
        ...     user = await repository.생성(User(...))
    """
    
    def __init__(self, session: AsyncSession):
        """
        Args:
            session: SQLAlchemy 비동기 세션
        """
        self.session = session
    
    async def 생성(self, user: User) -> User:
        """사용자를 생성합니다.
        
        Args:
            user: 생성할 사용자 엔티티
        
        Returns:
            User: 생성된 사용자 (ID 포함)
        
        Example:
            >>> user = User(이름="홍길동", 이메일="hong@test.com")
            >>> created = await repository.생성(user)
            >>> print(created.id)
            1
        """
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def 조회(self, user_id: int) -> User | None:
        """ID로 사용자를 조회합니다.
        
        Args:
            user_id: 사용자 ID
        
        Returns:
            User | None: 조회된 사용자 또는 None
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def 이름으로_조회(self, 이름: str) -> User | None:
        """이름으로 사용자를 조회합니다.
        
        Args:
            이름: 사용자 이름
        
        Returns:
            User | None: 조회된 사용자 또는 None
        """
        stmt = select(User).where(User.이름 == 이름)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def ID_목록으로_조회(
        self,
        user_ids: list[int],
        select_fields: list[str] | None = None
    ) -> list[User]:
        """여러 사용자를 한 번에 조회합니다 (Batch 처리).
        
        N+1 쿼리 문제를 방지하기 위해 IN 절을 사용합니다.
        
        Args:
            user_ids: 사용자 ID 목록
            select_fields: 조회할 필드 목록 (None이면 전체)
                예: ["id", "이름", "이메일"]
        
        Returns:
            list[User]: 조회된 사용자 목록
        
        Example:
            >>> # ❌ Bad: N+1 쿼리
            >>> users = []
            >>> for user_id in user_ids:
            ...     user = await repository.조회(user_id)
            ...     users.append(user)
            
            >>> # ✅ Good: Batch 처리
            >>> users = await repository.ID_목록으로_조회(user_ids)
        """
        if not user_ids:
            return []
        
        if select_fields:
            # 필요한 필드만 SELECT (성능 최적화)
            fields = [getattr(User, field) for field in select_fields]
            stmt = select(*fields).where(User.id.in_(user_ids))
        else:
            # 전체 필드 SELECT
            stmt = select(User).where(User.id.in_(user_ids))
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def 목록_조회(
        self,
        페이지: int,
        페이지_크기: int,
        활성화_여부: bool | None = None,
        정렬_필드: str = "생성일시",
        정렬_방향: str = "desc"
    ) -> tuple[list[User], int]:
        """페이지네이션된 사용자 목록을 조회합니다.
        
        Args:
            페이지: 페이지 번호 (1부터 시작)
            페이지_크기: 한 페이지당 항목 수
            활성화_여부: 활성화 상태 필터 (None이면 전체)
            정렬_필드: 정렬 기준 필드
            정렬_방향: 정렬 방향 ("asc" 또는 "desc")
        
        Returns:
            tuple[list[User], int]: (사용자 목록, 전체 개수)
        
        Example:
            >>> users, total = await repository.목록_조회(
            ...     페이지=1,
            ...     페이지_크기=20,
            ...     활성화_여부=True
            ... )
            >>> print(f"전체 {total}명 중 {len(users)}명 조회")
        """
        # 기본 쿼리
        query = select(User)
        
        # 필터 적용
        conditions = []
        if 활성화_여부 is not None:
            conditions.append(User.활성화 == 활성화_여부)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # 전체 개수 조회 (필터 적용 후)
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()
        
        # 정렬
        order_column = getattr(User, 정렬_필드)
        if 정렬_방향 == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
        
        # 페이지네이션
        offset = (페이지 - 1) * 페이지_크기
        query = query.offset(offset).limit(페이지_크기)
        
        # 실행
        result = await self.session.execute(query)
        users = list(result.scalars().all())
        
        return users, total
    
    async def 이름으로_검색(
        self,
        검색어: str,
        최대_개수: int = 10
    ) -> list[User]:
        """이름으로 사용자를 검색합니다 (부분 일치).
        
        Args:
            검색어: 검색할 이름 (부분 일치)
            최대_개수: 최대 반환 개수
        
        Returns:
            list[User]: 검색된 사용자 목록
        
        Example:
            >>> users = await repository.이름으로_검색("홍")
            >>> # "홍길동", "홍길순" 등 검색
        """
        stmt = (
            select(User)
            .where(User.이름.like(f"%{검색어}%"))
            .limit(최대_개수)
        )
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def 수정(self, user: User) -> User:
        """사용자 정보를 수정합니다.
        
        Args:
            user: 수정할 사용자 엔티티
        
        Returns:
            User: 수정된 사용자
        
        Note:
            세션에 이미 추가된 엔티티를 수정하는 경우,
            명시적으로 merge를 호출하지 않아도 자동으로 추적됩니다.
        """
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def 삭제(self, user_id: int) -> bool:
        """사용자를 삭제합니다.
        
        Args:
            user_id: 삭제할 사용자 ID
        
        Returns:
            bool: 삭제 성공 여부
        
        Note:
            Soft delete가 아닌 Hard delete입니다.
            Soft delete가 필요하면 활성화 필드를 False로 변경하세요.
        """
        user = await self.조회(user_id)
        
        if not user:
            return False
        
        await self.session.delete(user)
        await self.session.flush()
        return True
    
    async def 소프트_삭제(self, user_id: int) -> bool:
        """사용자를 소프트 삭제합니다 (활성화 = False).
        
        Args:
            user_id: 삭제할 사용자 ID
        
        Returns:
            bool: 삭제 성공 여부
        """
        user = await self.조회(user_id)
        
        if not user:
            return False
        
        user.활성화 = False
        await self.session.flush()
        return True
    
    async def 개수_조회(
        self,
        활성화_여부: bool | None = None
    ) -> int:
        """사용자 개수를 조회합니다.
        
        Args:
            활성화_여부: 활성화 상태 필터 (None이면 전체)
        
        Returns:
            int: 사용자 개수
        """
        query = select(func.count(User.id))
        
        if 활성화_여부 is not None:
            query = query.where(User.활성화 == 활성화_여부)
        
        result = await self.session.execute(query)
        return result.scalar_one()
    
    async def 일괄_생성(self, users: list[User]) -> list[User]:
        """여러 사용자를 한 번에 생성합니다 (Bulk Insert).
        
        대량의 데이터를 효율적으로 삽입할 때 사용합니다.
        
        Args:
            users: 생성할 사용자 목록
        
        Returns:
            list[User]: 생성된 사용자 목록
        
        Example:
            >>> users = [
            ...     User(이름="홍길동", 이메일="hong@test.com"),
            ...     User(이름="김철수", 이메일="kim@test.com"),
            ... ]
            >>> created = await repository.일괄_생성(users)
        """
        self.session.add_all(users)
        await self.session.flush()
        
        for user in users:
            await self.session.refresh(user)
        
        return users


# 추상 Repository 패턴 (선택적)

class BaseRepository(Generic[T]):
    """기본 Repository 추상 클래스
    
    공통 CRUD 로직을 제공합니다.
    실제 프로젝트에서는 이를 상속받아 사용할 수 있습니다.
    
    Type Parameters:
        T: 엔티티 타입
    """
    
    def __init__(self, session: AsyncSession, model: type[T]):
        """
        Args:
            session: SQLAlchemy 세션
            model: 엔티티 클래스
        """
        self.session = session
        self.model = model
    
    async def create(self, entity: T) -> T:
        """엔티티를 생성합니다."""
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity
    
    async def find_by_id(self, id: int) -> T | None:
        """ID로 엔티티를 조회합니다."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def find_all(self) -> list[T]:
        """모든 엔티티를 조회합니다."""
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def update(self, entity: T) -> T:
        """엔티티를 수정합니다."""
        await self.session.flush()
        await self.session.refresh(entity)
        return entity
    
    async def delete(self, id: int) -> bool:
        """엔티티를 삭제합니다."""
        entity = await self.find_by_id(id)
        
        if not entity:
            return False
        
        await self.session.delete(entity)
        await self.session.flush()
        return True
