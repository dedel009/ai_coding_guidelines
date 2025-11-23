# AI Coding Guidelines

> AI와 협업하여 높은 품질의 코드를 빠르고 안정적으로 작성하기 위한 가이드라인

## 📋 목차

- [개요](#개요)
- [시작하기](#시작하기)
- [프로젝트 구조](#프로젝트-구조)
- [사용 방법](#사용-방법)
- [워크플로우](#워크플로우)
- [커맨드 참조](#커맨드-참조)
- [예시 코드](#예시-코드)
- [기여 방법](#기여-방법)

## 개요

이 가이드라인은 AI 코딩 어시스턴트(Claude Code, Cursor, 등)와 효과적으로 협업하여 생산성을 극대화하면서도 코드 품질과 안정성을 보장하기 위한 체계적인 워크플로우를 제공합니다.

### 핵심 원칙

1. **TDD (Test-Driven Development) 우선**
   - 테스트 없는 코드는 작성하지 않음
   - AI가 생성한 코드의 정확성을 검증

2. **명확한 의사소통**
   - 애매한 부분은 항상 질문
   - 가정하지 않고 확인

3. **점진적 개발**
   - 큰 작업은 작은 단위로 분해
   - 각 단계마다 검증

4. **품질 보증**
   - 모든 코드는 리뷰 체크리스트 통과
   - 지속적인 테스트와 검증

### 목표

**1인 개발자가 비즈니스 로직, 인프라, 기획, 디자인까지 광범위하게 집중할 수 있도록 코딩 시간을 최소화하고 품질을 극대화**

## 시작하기

### 필수 조건

- Python 3.11+ (FastAPI 프로젝트)
- Java 17+ (Spring Boot 프로젝트)
- Claude Code 또는 다른 AI 코딩 어시스턴트
- Git

### 설치

1. **가이드라인 복사**
   ```bash
   # CLAUDE.md를 프로젝트 루트에 복사
   cp CLAUDE.md /your/project/root/
   ```

2. **커스텀 커맨드 설정**
   ```bash
   # .claude 디렉토리 복사
   cp -r .claude /your/project/root/
   ```

3. **예시 코드 참조**
   ```bash
   # examples 디렉토리를 참조용으로 유지
   # 실제 프로젝트에 복사할 필요는 없음
   ```

### 빠른 시작

1. **Claude Code 실행**
   ```bash
   cd /your/project
   claude
   ```

2. **워크플로우 확인**
   ```
   /check-workflow
   ```

3. **테스트 우선 개발**
   ```
   /test-first
   ```

## 프로젝트 구조

```
.
├── CLAUDE.md                    # 메인 가이드라인 문서
├── .claude/                     # Claude Code 설정
│   └── commands/               # 커스텀 커맨드
│       ├── test-first.md       # TDD 강제 커맨드
│       ├── review-code.md      # 코드 리뷰 커맨드
│       ├── check-workflow.md   # 워크플로우 확인
│       └── plan-feature.md     # 기능 계획 수립
├── examples/                    # 코드 패턴 예시
│   ├── README.md
│   ├── fastapi/                # FastAPI 예시
│   │   ├── services/
│   │   ├── repositories/
│   │   └── tests/
│   └── spring/                 # Spring Boot 예시
│       ├── services/
│       ├── repositories/
│       └── tests/
└── README.md                    # 이 파일
```

## 사용 방법

### CLAUDE.md 커스터마이징

`CLAUDE.md` 파일의 프로젝트 특화 섹션을 수정하세요:

```markdown
## 📚 PROJECT CONTEXT

### Tech Stack
- Framework: [Your framework]
- Database: [Your database]
- ...

### Project Structure
```
[Your structure]
```

### Conventions
...
```

### 커스텀 커맨드 추가

`.claude/commands/` 디렉토리에 새로운 Markdown 파일을 추가:

```bash
# 새 커맨드 생성
touch .claude/commands/my-custom-command.md
```

```markdown
# My Custom Command

[Command description and steps]

## Example Usage
```
/my-custom-command
```
```

## 워크플로우

### Workflow 1: 기존 코드 수정

```
1. 기존 코드 분석
   ↓
2. 테스트 확인/생성 ← 테스트 없으면 STOP
   ↓
3. 코드 수정
   ↓
4. 테스트 실행 및 검증
   ↓
5. 개발자 리뷰
```

**사용 예:**
```
나: 사용자 이름 검증 로직을 2자 이상에서 3자 이상으로 변경해줘

AI: /test-first를 실행합니다...
    
    기존 테스트를 찾았습니다:
    - tests/test_user_service.py::test_validate_user_name
    
    테스트를 수정해야 합니다:
    - 2자 → 3자로 변경
    
    진행할까요?

나: 응, 진행해

AI: [테스트 수정 → 구현 수정 → 테스트 실행]
    
    ✅ 모든 테스트 통과
    변경사항 리뷰 부탁드립니다.
```

### Workflow 2: 신규 기능 개발

```
1. 요구사항 이해 ← 불명확하면 질문
   ↓
2. 테스트 작성 (TDD)
   ↓
3. API 개발
   ↓
4. 개발자 리뷰
   ↓
5. 리팩토링
   ↓
6. 2-5 반복
```

**사용 예:**
```
나: UTM 추적 기능 추가해줘
    - UTM 파라미터 저장
    - 분석 API 제공

AI: 몇 가지 확인이 필요합니다:
    
    1. UTM 파라미터는 쿠키에 저장할까요, 아니면 첫 방문 시에만?
    2. 데이터 보관 기간은 얼마나 되나요?
    3. 실시간 분석이 필요한가요?

나: 1. 첫 방문 시에만
    2. 90일
    3. 배치 처리로 충분해

AI: 알겠습니다. 테스트부터 작성하겠습니다...
```

### Workflow 3: 대규모 기능 개발

```
1. 기능 분석 및 분해
   ↓
2. 태스크 우선순위 지정
   ↓
3. 태스크별 개발 (Workflow 2)
   ↓
4. 진행 상황 추적
```

**사용 예:**
```
나: /plan-feature
    
    완전한 사용자 관리 시스템을 구축해줘

AI: 이 기능을 다음과 같이 분해했습니다:
    
    Phase 1: Foundation
    - [ ] Task 1: User 모델 생성 (Small)
    - [ ] Task 2: DB 마이그레이션 (Small)
    
    Phase 2: Core
    - [ ] Task 3: UserService 구현 (Medium)
    - [ ] Task 4: API 엔드포인트 (Medium)
    
    Phase 3: Enhancement
    - [ ] Task 5: 권한 시스템 (Medium)
    
    진행할까요?
```

## 커맨드 참조

### `/test-first`
테스트 우선 개발 강제

```bash
/test-first
```

- 테스트 존재 여부 확인
- 테스트 없으면 생성 유도
- 구현 전 테스트 실행

### `/review-code`
코드 품질 체크리스트 실행

```bash
/review-code
```

체크 항목:
- ✅ 기능 동작
- ✅ 코드 품질
- ✅ DB 최적화
- ✅ 테스트 커버리지
- ✅ 문서화
- ✅ 아키텍처
- ✅ 성능
- ✅ 보안

### `/check-workflow`
워크플로우 준수 확인

```bash
/check-workflow
```

- 현재 워크플로우 식별
- 단계별 완료 상태 확인
- Critical Rules 준수 검증

### `/plan-feature`
대규모 기능 계획 수립

```bash
/plan-feature
```

- 기능 분해
- 의존성 매핑
- 태스크 우선순위
- 리스크 식별

## 예시 코드

`examples/` 디렉토리에서 다음 패턴을 참조할 수 있습니다:

### FastAPI

- **Service Layer**: `examples/fastapi/services/user_service.py`
  - 의존성 주입
  - 비즈니스 로직 캡슐화
  - 에러 핸들링

- **Repository**: `examples/fastapi/repositories/user_repository.py`
  - 데이터 접근 패턴
  - 쿼리 최적화
  - 배치 작업

- **Tests**: `examples/fastapi/tests/test_user_service.py`
  - AAA 패턴
  - Mocking
  - 픽스처 활용

### Spring Boot

- **Service Layer**: `examples/spring/services/UserService.java`
  - `@Service`, `@Transactional` 어노테이션
  - Lombok `@RequiredArgsConstructor` 사용
  - 상세한 JavaDoc
  - 한글 메서드명
  - 검증 로직 분리

- **Repository**: `examples/spring/repositories/UserRepository.java`
  - Spring Data JPA 사용
  - 커스텀 쿼리 메서드
  - `@Query` 어노테이션 활용
  - Fetch Join으로 N+1 방지
  - DTO Projection 예시

- **Tests**: `examples/spring/tests/UserServiceTest.java`
  - JUnit 5 + Mockito
  - `@Nested` 클래스로 테스트 그룹핑
  - `@DisplayName` 한글 테스트명
  - `@ParameterizedTest` 경계값 테스트
  - AssertJ 사용
  - BDDMockito 스타일

## 기여 방법

### 새로운 패턴 추가

1. `examples/` 디렉토리에 예시 코드 작성
2. `examples/README.md` 업데이트
3. CLAUDE.md에 패턴 설명 추가

### 워크플로우 개선

1. 문제점 식별
2. 개선안 작성
3. CLAUDE.md 업데이트

### 커맨드 추가

1. `.claude/commands/`에 새 커맨드 작성
2. 이 README에 사용법 추가
3. 테스트

## 문제 해결

### AI가 테스트를 건너뛰려고 함

```
/test-first를 실행하고 Critical Rule 1을 상기시키세요
```

### AI가 가정을 하고 있음

```
CLAUDE.md의 "AI COMMUNICATION RULES"를 참조하고
명확한 질문을 요청하세요
```

### 태스크가 너무 큼

```
/plan-feature를 실행하여 분해하세요
```

### 코드 품질이 낮음

```
/review-code를 실행하고 체크리스트를 확인하세요
```

## FAQ

**Q: Claude Code 없이도 사용 가능한가요?**
A: 네, Cursor, Windsurf 등 다른 AI 코딩 어시스턴트에서도 CLAUDE.md를 참조할 수 있습니다.

**Q: 기존 프로젝트에 적용할 수 있나요?**
A: 네, CLAUDE.md를 프로젝트 루트에 복사하고 프로젝트별 섹션을 수정하면 됩니다.

**Q: 팀에서 사용할 수 있나요?**
A: 네, Git으로 버전 관리하여 팀 전체가 공유할 수 있습니다.

**Q: 다른 언어/프레임워크를 추가하려면?**
A: CLAUDE.md의 PROJECT CONTEXT 섹션에 새로운 하위 섹션을 추가하면 됩니다.

## 라이선스

MIT License

## 연락처

- **Maintainer**: kdy
- **Company**: NEWEYE
- **Location**: Busan, South Korea

---

**Last Updated**: 2025-11-23  
**Version**: 1.0.0
