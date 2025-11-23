package com.example.repository;

import com.example.domain.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 사용자 Repository
 * 
 * <p>데이터 접근 로직만 담당하며, 비즈니스 로직은 포함하지 않습니다.</p>
 * <p>Spring Data JPA를 사용하여 기본 CRUD와 커스텀 쿼리를 제공합니다.</p>
 * 
 * @author kdy
 * @since 1.0
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    /**
     * 이름으로 사용자를 조회합니다.
     * 
     * @param name 사용자 이름
     * @return 조회된 사용자 (Optional)
     */
    Optional<User> findByName(String name);
    
    /**
     * 이름 존재 여부를 확인합니다.
     * 
     * @param name 확인할 이름
     * @return 존재 여부
     */
    boolean existsByName(String name);
    
    /**
     * 여러 ID로 사용자를 한 번에 조회합니다 (Batch).
     * 
     * <p>N+1 쿼리 문제를 방지하기 위해 IN 절을 사용합니다.</p>
     * 
     * @param ids 사용자 ID 목록
     * @return 조회된 사용자 목록
     * 
     * @example
     * <pre>
     * // ❌ Bad: N+1 쿼리
     * List&lt;User&gt; users = new ArrayList&lt;&gt;();
     * for (Long id : ids) {
     *     User user = userRepository.findById(id).orElse(null);
     *     if (user != null) users.add(user);
     * }
     * 
     * // ✅ Good: Batch 처리
     * List&lt;User&gt; users = userRepository.findAllByIdIn(ids);
     * </pre>
     */
    List<User> findAllByIdIn(List<Long> ids);
    
    /**
     * 활성화 상태로 사용자를 필터링하여 조회합니다.
     * 
     * @param active 활성화 상태
     * @param pageable 페이지네이션 정보
     * @return 페이지네이션된 사용자 목록
     */
    Page<User> findAllByActive(boolean active, Pageable pageable);
    
    /**
     * 이름으로 사용자를 검색합니다 (부분 일치).
     * 
     * @param keyword 검색어 (부분 일치)
     * @param pageable 페이지네이션 정보
     * @return 검색된 사용자 목록
     * 
     * @example
     * <pre>
     * Pageable pageable = PageRequest.of(0, 10);
     * Page&lt;User&gt; users = userRepository.findByNameContaining("홍", pageable);
     * // "홍길동", "홍길순" 등 검색
     * </pre>
     */
    Page<User> findByNameContaining(String keyword, Pageable pageable);
    
    /**
     * 활성화된 사용자 수를 조회합니다.
     * 
     * @return 활성화된 사용자 수
     */
    long countByActive(boolean active);
    
    /**
     * 필요한 필드만 선택하여 조회합니다 (성능 최적화).
     * 
     * <p>DTO Projection을 사용하여 필요한 필드만 SELECT합니다.</p>
     * 
     * @param ids 사용자 ID 목록
     * @return 사용자 정보 DTO 목록
     * 
     * @example
     * <pre>
     * // ❌ Bad: 모든 필드 조회
     * SELECT * FROM users WHERE id IN (...)
     * 
     * // ✅ Good: 필요한 필드만
     * SELECT id, name, email FROM users WHERE id IN (...)
     * </pre>
     */
    @Query("SELECT new com.example.dto.UserSimpleDto(u.id, u.name, u.email) " +
           "FROM User u WHERE u.id IN :ids")
    List<UserSimpleDto> findSimpleByIds(@Param("ids") List<Long> ids);
    
    /**
     * 이메일로 사용자를 조회합니다 (대소문자 무시).
     * 
     * @param email 이메일
     * @return 조회된 사용자 (Optional)
     */
    Optional<User> findByEmailIgnoreCase(String email);
    
    /**
     * 활성화 상태와 이름으로 검색합니다.
     * 
     * @param active 활성화 상태
     * @param keyword 검색어
     * @param pageable 페이지네이션
     * @return 검색 결과
     */
    @Query("SELECT u FROM User u " +
           "WHERE u.active = :active " +
           "AND u.name LIKE %:keyword%")
    Page<User> searchByActiveAndName(
            @Param("active") boolean active,
            @Param("keyword") String keyword,
            Pageable pageable);
    
    /**
     * 일괄 삭제를 수행합니다.
     * 
     * <p>여러 사용자를 효율적으로 삭제합니다.</p>
     * 
     * @param ids 삭제할 사용자 ID 목록
     */
    @Query("DELETE FROM User u WHERE u.id IN :ids")
    void deleteAllByIdIn(@Param("ids") List<Long> ids);
    
    /**
     * 일괄 소프트 삭제를 수행합니다.
     * 
     * @param ids 소프트 삭제할 사용자 ID 목록
     */
    @Query("UPDATE User u SET u.active = false WHERE u.id IN :ids")
    void deactivateAllByIdIn(@Param("ids") List<Long> ids);
    
    /**
     * Fetch Join을 사용하여 연관 엔티티를 함께 조회합니다.
     * 
     * <p>N+1 문제 해결을 위해 Fetch Join을 사용합니다.</p>
     * 
     * @param userId 사용자 ID
     * @return 사용자와 연관 엔티티
     * 
     * @example
     * <pre>
     * // ❌ Bad: N+1 쿼리
     * User user = userRepository.findById(1L).get();
     * List&lt;Order&gt; orders = user.getOrders(); // 추가 쿼리 발생
     * 
     * // ✅ Good: Fetch Join
     * User user = userRepository.findByIdWithOrders(1L).get();
     * List&lt;Order&gt; orders = user.getOrders(); // 이미 로딩됨
     * </pre>
     */
    @Query("SELECT u FROM User u " +
           "LEFT JOIN FETCH u.orders " +
           "WHERE u.id = :userId")
    Optional<User> findByIdWithOrders(@Param("userId") Long userId);
}

/**
 * 사용자 간단 정보 DTO
 * 
 * <p>필요한 필드만 조회할 때 사용하는 Projection DTO입니다.</p>
 */
class UserSimpleDto {
    private final Long id;
    private final String name;
    private final String email;
    
    public UserSimpleDto(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Getters
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}
