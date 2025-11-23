package com.example.service;

import com.example.domain.User;
import com.example.dto.request.UserCreateRequest;
import com.example.dto.request.UserUpdateRequest;
import com.example.dto.response.PaginatedResponse;
import com.example.dto.response.UserResponse;
import com.example.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.*;

/**
 * UserService 테스트
 * 
 * <p>AAA 패턴(Arrange-Act-Assert)을 사용하여 테스트를 작성합니다.</p>
 * <p>테스트 메서드는 한글로 작성하여 의도를 명확히 합니다.</p>
 * 
 * @author kdy
 * @since 1.0
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("UserService 테스트")
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    private User 샘플_사용자;
    private UserCreateRequest 샘플_사용자_생성_요청;
    
    @BeforeEach
    void setUp() {
        // 테스트 데이터 초기화
        샘플_사용자 = User.builder()
                .id(1L)
                .name("홍길동")
                .email("hong@test.com")
                .active(true)
                .build();
        
        샘플_사용자_생성_요청 = UserCreateRequest.builder()
                .name("홍길동")
                .email("hong@test.com")
                .build();
    }
    
    @Nested
    @DisplayName("사용자 생성")
    class 사용자_생성_테스트 {
        
        @Test
        @DisplayName("사용자 생성이 정상적으로 동작한다")
        void 사용자_생성_성공() {
            // Given (준비)
            given(userRepository.existsByName(anyString())).willReturn(false);
            given(userRepository.save(any(User.class))).willReturn(샘플_사용자);
            
            // When (실행)
            User result = userService.사용자_생성(샘플_사용자_생성_요청);
            
            // Then (검증)
            assertThat(result).isNotNull();
            assertThat(result.getName()).isEqualTo("홍길동");
            assertThat(result.getEmail()).isEqualTo("hong@test.com");
            assertThat(result.isActive()).isTrue();
            
            // Mock 호출 검증
            verify(userRepository, times(1)).existsByName("홍길동");
            verify(userRepository, times(1)).save(any(User.class));
        }
        
        @Test
        @DisplayName("중복된 이름으로 사용자 생성 시 예외가 발생한다")
        void 중복_이름으로_사용자_생성시_예외_발생() {
            // Given
            given(userRepository.existsByName("홍길동")).willReturn(true);
            
            // When & Then
            assertThatThrownBy(() -> userService.사용자_생성(샘플_사용자_생성_요청))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("이미 존재하는 이름");
            
            // save는 호출되지 않아야 함
            verify(userRepository, never()).save(any(User.class));
        }
        
        @ParameterizedTest
        @ValueSource(strings = {"홍", "홍길"})
        @DisplayName("3자 미만의 이름으로 사용자 생성 시 예외가 발생한다")
        void 짧은_이름으로_사용자_생성시_예외_발생(String 짧은_이름) {
            // Given
            UserCreateRequest request = UserCreateRequest.builder()
                    .name(짧은_이름)
                    .email("test@test.com")
                    .build();
            
            // When & Then
            assertThatThrownBy(() -> userService.사용자_생성(request))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("3자 이상");
            
            // Repository 호출 없음
            verify(userRepository, never()).existsByName(anyString());
            verify(userRepository, never()).save(any(User.class));
        }
        
        @Test
        @DisplayName("50자 초과 이름으로 사용자 생성 시 예외가 발생한다")
        void 긴_이름으로_사용자_생성시_예외_발생() {
            // Given
            String 긴_이름 = "가".repeat(51);
            UserCreateRequest request = UserCreateRequest.builder()
                    .name(긴_이름)
                    .email("test@test.com")
                    .build();
            
            // When & Then
            assertThatThrownBy(() -> userService.사용자_생성(request))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("50자 이하");
        }
        
        @ParameterizedTest
        @ValueSource(strings = {"invalid-email", "test@", "@test.com", "test"})
        @DisplayName("잘못된 이메일 형식으로 사용자 생성 시 예외가 발생한다")
        void 잘못된_이메일로_사용자_생성시_예외_발생(String 잘못된_이메일) {
            // Given
            UserCreateRequest request = UserCreateRequest.builder()
                    .name("홍길동")
                    .email(잘못된_이메일)
                    .build();
            
            // When & Then
            assertThatThrownBy(() -> userService.사용자_생성(request))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("올바른 이메일 형식");
        }
        
        @Test
        @DisplayName("이름과 이메일이 정규화되어 저장된다")
        void 이름과_이메일_정규화() {
            // Given
            UserCreateRequest request = UserCreateRequest.builder()
                    .name("  홍길동  ")  // 앞뒤 공백
                    .email("HONG@TEST.COM")  // 대문자
                    .build();
            
            given(userRepository.existsByName(anyString())).willReturn(false);
            given(userRepository.save(any(User.class))).willAnswer(invocation -> {
                User savedUser = invocation.getArgument(0);
                return savedUser;
            });
            
            // When
            User result = userService.사용자_생성(request);
            
            // Then
            assertThat(result.getName()).isEqualTo("홍길동");  // trim
            assertThat(result.getEmail()).isEqualTo("hong@test.com");  // lowercase
        }
    }
    
    @Nested
    @DisplayName("사용자 조회")
    class 사용자_조회_테스트 {
        
        @Test
        @DisplayName("사용자 조회가 정상적으로 동작한다")
        void 사용자_조회_성공() {
            // Given
            given(userRepository.findById(1L)).willReturn(Optional.of(샘플_사용자));
            
            // When
            User result = userService.사용자_조회(1L);
            
            // Then
            assertThat(result).isNotNull();
            assertThat(result.getId()).isEqualTo(1L);
            assertThat(result.getName()).isEqualTo("홍길동");
            
            verify(userRepository, times(1)).findById(1L);
        }
        
        @Test
        @DisplayName("존재하지 않는 사용자 조회 시 예외가 발생한다")
        void 존재하지_않는_사용자_조회시_예외_발생() {
            // Given
            given(userRepository.findById(999L)).willReturn(Optional.empty());
            
            // When & Then
            assertThatThrownBy(() -> userService.사용자_조회(999L))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("사용자를 찾을 수 없습니다");
        }
    }
    
    @Nested
    @DisplayName("사용자 목록 조회")
    class 사용자_목록_조회_테스트 {
        
        @Test
        @DisplayName("사용자 목록 조회가 정상적으로 동작한다")
        void 사용자_목록_조회_성공() {
            // Given
            List<User> users = Arrays.asList(
                    User.builder().id(1L).name("홍길동").email("hong@test.com").build(),
                    User.builder().id(2L).name("김철수").email("kim@test.com").build()
            );
            
            Pageable pageable = PageRequest.of(0, 20);
            Page<User> userPage = new PageImpl<>(users, pageable, 2);
            
            given(userRepository.findAll(any(Pageable.class))).willReturn(userPage);
            
            // When
            PaginatedResponse<UserResponse> result = userService.사용자_목록_조회(0, 20);
            
            // Then
            assertThat(result).isNotNull();
            assertThat(result.getContent()).hasSize(2);
            assertThat(result.getTotalElements()).isEqualTo(2);
            assertThat(result.getTotalPages()).isEqualTo(1);
        }
        
        @Test
        @DisplayName("페이지 번호가 음수이면 예외가 발생한다")
        void 음수_페이지_번호로_조회시_예외_발생() {
            // When & Then
            assertThatThrownBy(() -> userService.사용자_목록_조회(-1, 20))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("페이지 번호는 0 이상");
            
            verify(userRepository, never()).findAll(any(Pageable.class));
        }
        
        @ParameterizedTest
        @CsvSource({
                "0, 1-100 사이",
                "101, 1-100 사이"
        })
        @DisplayName("페이지 크기가 범위를 벗어나면 예외가 발생한다")
        void 잘못된_페이지_크기로_조회시_예외_발생(int size, String 예상_메시지) {
            // When & Then
            assertThatThrownBy(() -> userService.사용자_목록_조회(0, size))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining(예상_메시지);
        }
    }
    
    @Nested
    @DisplayName("사용자 수정")
    class 사용자_수정_테스트 {
        
        @Test
        @DisplayName("사용자 수정이 정상적으로 동작한다")
        void 사용자_수정_성공() {
            // Given
            UserUpdateRequest request = UserUpdateRequest.builder()
                    .name("홍길순")
                    .email("hongsoon@test.com")
                    .build();
            
            given(userRepository.findById(1L)).willReturn(Optional.of(샘플_사용자));
            given(userRepository.existsByName("홍길순")).willReturn(false);
            
            // When
            User result = userService.사용자_수정(1L, request);
            
            // Then
            assertThat(result.getName()).isEqualTo("홍길순");
            assertThat(result.getEmail()).isEqualTo("hongsoon@test.com");
        }
        
        @Test
        @DisplayName("다른 사용자가 사용 중인 이름으로 수정 시 예외가 발생한다")
        void 중복_이름으로_수정시_예외_발생() {
            // Given
            UserUpdateRequest request = UserUpdateRequest.builder()
                    .name("김철수")
                    .build();
            
            given(userRepository.findById(1L)).willReturn(Optional.of(샘플_사용자));
            given(userRepository.existsByName("김철수")).willReturn(true);
            
            // When & Then
            assertThatThrownBy(() -> userService.사용자_수정(1L, request))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("이미 존재하는 이름");
        }
    }
    
    @Nested
    @DisplayName("사용자 삭제")
    class 사용자_삭제_테스트 {
        
        @Test
        @DisplayName("사용자 삭제가 정상적으로 동작한다")
        void 사용자_삭제_성공() {
            // Given
            given(userRepository.findById(1L)).willReturn(Optional.of(샘플_사용자));
            doNothing().when(userRepository).deleteById(1L);
            
            // When
            userService.사용자_삭제(1L);
            
            // Then
            verify(userRepository, times(1)).deleteById(1L);
        }
        
        @Test
        @DisplayName("존재하지 않는 사용자 삭제 시 예외가 발생한다")
        void 존재하지_않는_사용자_삭제시_예외_발생() {
            // Given
            given(userRepository.findById(999L)).willReturn(Optional.empty());
            
            // When & Then
            assertThatThrownBy(() -> userService.사용자_삭제(999L))
                    .isInstanceOf(IllegalArgumentException.class)
                    .hasMessageContaining("사용자를 찾을 수 없습니다");
            
            verify(userRepository, never()).deleteById(anyLong());
        }
        
        @Test
        @DisplayName("소프트 삭제가 정상적으로 동작한다")
        void 소프트_삭제_성공() {
            // Given
            given(userRepository.findById(1L)).willReturn(Optional.of(샘플_사용자));
            
            // When
            userService.사용자_소프트_삭제(1L);
            
            // Then
            assertThat(샘플_사용자.isActive()).isFalse();
        }
    }
    
    @Nested
    @DisplayName("경계값 테스트")
    class 경계값_테스트 {
        
        @ParameterizedTest
        @CsvSource({
                "홍, false",           // 1자 - 실패
                "홍길, false",         // 2자 - 실패
                "홍길동, true",        // 3자 - 성공
                "가나다라마바사아자차카타파하, true"  // 15자 - 성공
        })
        @DisplayName("다양한 이름 길이에 대한 검증 테스트")
        void 이름_길이_경계값_테스트(String 이름, boolean 예상_성공) {
            // Given
            UserCreateRequest request = UserCreateRequest.builder()
                    .name(이름)
                    .email("test@test.com")
                    .build();
            
            if (예상_성공) {
                given(userRepository.existsByName(anyString())).willReturn(false);
                given(userRepository.save(any(User.class))).willReturn(샘플_사용자);
            }
            
            // When & Then
            if (예상_성공) {
                assertThatCode(() -> userService.사용자_생성(request))
                        .doesNotThrowAnyException();
            } else {
                assertThatThrownBy(() -> userService.사용자_생성(request))
                        .isInstanceOf(IllegalArgumentException.class);
            }
        }
    }
}
