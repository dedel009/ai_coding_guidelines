package com.example.service;

import com.example.domain.User;
import com.example.dto.request.UserCreateRequest;
import com.example.dto.request.UserUpdateRequest;
import com.example.dto.response.UserResponse;
import com.example.dto.response.PaginatedResponse;
import com.example.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.regex.Pattern;

/**
 * 사용자 관리 서비스
 * 
 * <p>사용자의 생명주기를 관리하고 비즈니스 로직을 처리합니다.</p>
 * 
 * <p>비즈니스 규칙:</p>
 * <ul>
 *   <li>이름은 3-50자 사이여야 합니다</li>
 *   <li>이름은 중복될 수 없습니다</li>
 *   <li>이메일은 유효한 형식이어야 합니다</li>
 * </ul>
 * 
 * @author kdy
 * @since 1.0
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {
    
    private final UserRepository userRepository;
    
    // 비즈니스 규칙 상수
    private static final int 최소_이름_길이 = 3;
    private static final int 최대_이름_길이 = 50;
    private static final Pattern EMAIL_PATTERN = 
        Pattern.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$");
    
    /**
     * 사용자를 생성합니다.
     * 
     * @param request 사용자 생성 요청
     *                <ul>
     *                  <li>이름: 3-50자</li>
     *                  <li>이메일: 유효한 이메일 형식</li>
     *                </ul>
     * @return 생성된 사용자
     * @throws IllegalArgumentException 검증 실패 시
     *                                  <ul>
     *                                    <li>이름이 3자 미만</li>
     *                                    <li>이름이 50자 초과</li>
     *                                    <li>이메일 형식 오류</li>
     *                                    <li>이름 중복</li>
     *                                  </ul>
     */
    @Transactional
    public User 사용자_생성(UserCreateRequest request) {
        // 1. 입력 검증
        이름_길이_검증(request.getName());
        이메일_형식_검증(request.getEmail());
        
        // 2. 비즈니스 규칙 검증
        이름_중복_검증(request.getName());
        
        // 3. 엔티티 생성
        User user = User.builder()
                .name(request.getName().trim())
                .email(request.getEmail().toLowerCase())
                .active(true)
                .build();
        
        // 4. 저장
        return userRepository.save(user);
    }
    
    /**
     * 사용자를 조회합니다.
     * 
     * @param userId 사용자 ID
     * @return 조회된 사용자
     * @throws IllegalArgumentException 사용자가 존재하지 않는 경우
     */
    public User 사용자_조회(Long userId) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException(
                        "사용자를 찾을 수 없습니다: " + userId));
    }
    
    /**
     * 페이지네이션된 사용자 목록을 조회합니다.
     * 
     * @param page 페이지 번호 (0부터 시작)
     * @param size 페이지 크기 (기본: 20, 최대: 100)
     * @return 페이지네이션된 사용자 목록
     *         <ul>
     *           <li>content: 사용자 목록</li>
     *           <li>totalElements: 전체 항목 수</li>
     *           <li>totalPages: 전체 페이지 수</li>
     *           <li>number: 현재 페이지</li>
     *           <li>size: 페이지 크기</li>
     *         </ul>
     * @throws IllegalArgumentException 페이지 번호가 음수이거나 페이지 크기가 범위를 벗어난 경우
     */
    public PaginatedResponse<UserResponse> 사용자_목록_조회(int page, int size) {
        // 입력 검증
        if (page < 0) {
            throw new IllegalArgumentException("페이지 번호는 0 이상이어야 합니다");
        }
        
        if (size < 1 || size > 100) {
            throw new IllegalArgumentException("페이지 크기는 1-100 사이여야 합니다");
        }
        
        // 조회
        Pageable pageable = PageRequest.of(page, size);
        Page<User> userPage = userRepository.findAll(pageable);
        
        // DTO 변환
        Page<UserResponse> responsePage = userPage.map(UserResponse::from);
        
        // 페이지네이션 응답 생성
        return PaginatedResponse.<UserResponse>builder()
                .content(responsePage.getContent())
                .totalElements(responsePage.getTotalElements())
                .totalPages(responsePage.getTotalPages())
                .number(responsePage.getNumber())
                .size(responsePage.getSize())
                .build();
    }
    
    /**
     * 사용자 정보를 수정합니다.
     * 
     * @param userId 사용자 ID
     * @param request 수정할 정보
     * @return 수정된 사용자
     * @throws IllegalArgumentException 사용자가 없거나 검증 실패 시
     */
    @Transactional
    public User 사용자_수정(Long userId, UserUpdateRequest request) {
        // 기존 사용자 조회
        User user = 사용자_조회(userId);
        
        // 수정할 필드 검증 및 업데이트
        if (request.getName() != null) {
            이름_길이_검증(request.getName());
            
            // 다른 사용자가 사용 중인지 확인
            if (!request.getName().equals(user.getName())) {
                이름_중복_검증(request.getName());
            }
            
            user.updateName(request.getName().trim());
        }
        
        if (request.getEmail() != null) {
            이메일_형식_검증(request.getEmail());
            user.updateEmail(request.getEmail().toLowerCase());
        }
        
        // JPA dirty checking으로 자동 저장
        return user;
    }
    
    /**
     * 사용자를 삭제합니다.
     * 
     * @param userId 사용자 ID
     * @throws IllegalArgumentException 사용자가 존재하지 않는 경우
     */
    @Transactional
    public void 사용자_삭제(Long userId) {
        // 존재 여부 확인
        사용자_조회(userId);
        
        // 삭제
        userRepository.deleteById(userId);
    }
    
    /**
     * 사용자를 소프트 삭제합니다 (활성화 = false).
     * 
     * @param userId 사용자 ID
     * @throws IllegalArgumentException 사용자가 존재하지 않는 경우
     */
    @Transactional
    public void 사용자_소프트_삭제(Long userId) {
        User user = 사용자_조회(userId);
        user.deactivate();
    }
    
    // Private 검증 메서드들
    
    /**
     * 이름 길이를 검증합니다.
     * 
     * @param name 검증할 이름
     * @throws IllegalArgumentException 이름 길이가 범위를 벗어난 경우
     */
    private void 이름_길이_검증(String name) {
        int nameLength = name.trim().length();
        
        if (nameLength < 최소_이름_길이) {
            throw new IllegalArgumentException(
                    String.format("이름은 %d자 이상이어야 합니다", 최소_이름_길이));
        }
        
        if (nameLength > 최대_이름_길이) {
            throw new IllegalArgumentException(
                    String.format("이름은 %d자 이하여야 합니다", 최대_이름_길이));
        }
    }
    
    /**
     * 이메일 형식을 검증합니다.
     * 
     * @param email 검증할 이메일
     * @throws IllegalArgumentException 이메일 형식이 올바르지 않은 경우
     */
    private void 이메일_형식_검증(String email) {
        if (!EMAIL_PATTERN.matcher(email).matches()) {
            throw new IllegalArgumentException(
                    "올바른 이메일 형식이 아닙니다: " + email);
        }
    }
    
    /**
     * 이름 중복을 검증합니다.
     * 
     * @param name 검증할 이름
     * @throws IllegalArgumentException 이름이 이미 존재하는 경우
     */
    private void 이름_중복_검증(String name) {
        if (userRepository.existsByName(name)) {
            throw new IllegalArgumentException(
                    "이미 존재하는 이름입니다: " + name);
        }
    }
}
