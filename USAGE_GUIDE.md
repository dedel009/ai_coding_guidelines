# 실제 프로젝트 적용 가이드

> AI Coding Guidelines를 kdy의 실제 프로젝트에 적용하는 방법

## 📋 목차

1. [신규 프로젝트에 적용](#신규-프로젝트에-적용)
2. [기존 프로젝트에 적용](#기존-프로젝트에-적용)
3. [Claude Code 설정](#claude-code-설정)
4. [Cursor 설정](#cursor-설정)
5. [팀 프로젝트 적용](#팀-프로젝트-적용)
6. [실전 사용 예시](#실전-사용-예시)

---

## 신규 프로젝트에 적용

### 1. 프로젝트 생성

```bash
# FastAPI 프로젝트
mkdir my-fastapi-project
cd my-fastapi-project

# 또는 Spring Boot 프로젝트
mkdir my-spring-project
cd my-spring-project
```

### 2. 가이드라인 파일 복사

```bash
# Git clone으로 가져오기
git clone https://github.com/kdy/ai-coding-guidelines.git temp
cp temp/CLAUDE.md .
cp -r temp/.claude .
cp -r temp/examples . # 참조용
rm -rf temp

# 또는 직접 다운로드
# CLAUDE.md를 프로젝트 루트에 복사
# .claude/ 디렉토리를 프로젝트 루트에 복사
```

### 3. CLAUDE.md 커스터마이징

```bash
# CLAUDE.md 파일을 열고 PROJECT CONTEXT 섹션 수정
vi CLAUDE.md
```

```markdown
## 📚 PROJECT CONTEXT

### Tech Stack
- Framework: FastAPI 0.115.0
- Database: PostgreSQL 16
- ORM: SQLAlchemy 2.0
- Testing: pytest

### Project Structure
```
src/
├── domain/
├── repository/
├── service/
├── api/
├── dto/
└── core/
```

### Conventions
- API 버전: /api/v1
- 에러 코드: ERR_XXX_YYY 형식
- ...
```

### 4. Git 설정

```bash
# .gitignore에 추가 (선택사항)
echo "examples/" >> .gitignore  # 예시 코드는 커밋 안함

# Git 커밋
git add CLAUDE.md .claude/
git commit -m "feat: AI 코딩 가이드라인 추가"
```

---

## 기존 프로젝트에 적용

### 1. 현재 프로젝트 분석

```bash
cd /path/to/existing/project

# 프로젝트 구조 확인
tree -L 3 -I '__pycache__|*.pyc|node_modules'

# 테스트 디렉토리 확인
find . -name "test*.py" -o -name "*test.py"
```

### 2. 가이드라인 추가

```bash
# CLAUDE.md 복사
cp /path/to/ai-coding-guidelines/CLAUDE.md .

# .claude/ 디렉토리 복사
cp -r /path/to/ai-coding-guidelines/.claude .
```

### 3. 기존 코드 스타일 학습

```bash
# Claude Code를 실행하고 요청
claude
```

```
나: 현재 프로젝트의 코딩 스타일을 분석해서 
    .claude/project-style.md 파일을 만들어줘
    
    분석할 내용:
    - 네이밍 컨벤션
    - 디렉토리 구조
    - Import 순서
    - Docstring 스타일
    - 에러 핸들링 패턴

AI: [프로젝트 분석 시작...]
    
    분석 완료. .claude/project-style.md 파일을 생성했습니다.
```

### 4. CLAUDE.md 업데이트

기존 프로젝트 정보를 CLAUDE.md에 추가:

```markdown
## 📚 PROJECT CONTEXT

### Existing Project Info
- **프로젝트명**: TaxAI Backend
- **시작일**: 2024-01
- **레거시 코드 비율**: 약 60%
- **주요 기술 부채**: 
  - N+1 쿼리 다수 존재
  - 테스트 커버리지 낮음 (30%)

### Migration Plan
- Phase 1: 신규 기능은 가이드라인 준수
- Phase 2: 레거시 리팩토링 (우선순위별)
- Phase 3: 테스트 커버리지 80% 달성
```

---

## Claude Code 설정

### 1. Claude Code 설치

```bash
# Claude Code CLI 설치
npm install -g @anthropic-ai/claude-code

# 또는
brew install anthropic/tap/claude-code
```

### 2. 프로젝트에서 실행

```bash
cd /path/to/your/project

# Claude Code 실행
claude

# 또는 특정 작업 시작
claude "UTM 추적 기능 추가"
```

### 3. 커스텀 커맨드 사용

```bash
# 프로젝트에서 Claude Code 실행 후

# 테스트 우선 개발
/test-first

# 코드 리뷰
/review-code

# 워크플로우 확인
/check-workflow

# 대규모 기능 계획
/plan-feature
```

### 4. MCP 서버 설정 (선택사항)

`.mcp.json` 파일 생성:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "/path/to/project"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

---

## Cursor 설정

### 1. Cursor에서 프로젝트 열기

```bash
cursor /path/to/your/project
```

### 2. .cursorrules 파일 생성

`.cursorrules` 파일에 CLAUDE.md 내용 요약:

```bash
# CLAUDE.md 내용을 .cursorrules로 요약
cat > .cursorrules << 'EOF'
# AI Coding Rules

## Critical Rules
1. NO CODE WITHOUT TESTS
2. ASK, DON'T ASSUME
3. BREAK DOWN BIG TASKS
4. DEVELOPER ALWAYS REVIEWS

## Code Style (FastAPI)
- Type hints 필수
- 한글 변수명/함수명 (비즈니스 로직)
- Service Layer 패턴
- Docstring 상세 작성

## Read CLAUDE.md for full guidelines
EOF
```

### 3. Cursor 설정

Cursor Settings (Cmd/Ctrl + ,):

```json
{
  "cursor.rules": ".cursorrules",
  "cursor.chat.includePaths": [
    "CLAUDE.md",
    ".claude/commands/*.md"
  ]
}
```

---

## 팀 프로젝트 적용

### 1. Git 레포지토리에 추가

```bash
# 팀 프로젝트 레포지토리에서
git add CLAUDE.md .claude/
git commit -m "docs: AI 코딩 가이드라인 추가"
git push origin main
```

### 2. 팀 온보딩 문서 작성

`docs/AI_CODING_GUIDE.md`:

```markdown
# AI 코딩 어시스턴트 사용 가이드

## 시작하기

1. Claude Code 설치
2. 프로젝트 클론 후 `claude` 명령어 실행
3. CLAUDE.md 파일 읽기
4. `/test-first` 커맨드부터 시작

## 팀 규칙

- 모든 PR은 `/review-code` 체크리스트 통과 필수
- 대규모 기능은 `/plan-feature`로 계획 수립 후 진행
- 테스트 없는 코드는 리뷰 거부

## 문의

- Slack: #ai-coding 채널
- 담당자: @kdy
```

### 3. PR Template 업데이트

`.github/pull_request_template.md`:

```markdown
## 변경 사항

## AI 코딩 체크리스트

- [ ] `/test-first` 실행 완료
- [ ] `/review-code` 체크리스트 통과
- [ ] 모든 테스트 통과
- [ ] CLAUDE.md 가이드라인 준수

## 리뷰어 확인사항

- [ ] 테스트 커버리지 확인
- [ ] 아키텍처 패턴 준수
```

---

## 실전 사용 예시

### 예시 1: 신규 기능 개발 (UTM 추적)

```bash
# 1. Claude Code 실행
claude

# 2. 기능 요청
나: UTM 추적 기능을 추가하고 싶어.
    - UTM 파라미터를 첫 방문 시 DB에 저장
    - 90일 보관
    - 퍼널 분석 API 제공

# 3. AI가 질문
AI: /check-workflow를 실행합니다...
    
    → Workflow 3 (대규모 기능) 감지
    
    /plan-feature를 실행할까요?

나: 응

# 4. 기능 분해
AI: [Phase 분해 완료]
    
    Phase 1: Foundation
    - Task 1.1: UTM 도메인 모델 생성
    - Task 1.2: DB 마이그레이션
    
    Phase 2: Core
    - Task 2.1: UTMRepository 구현
    - Task 2.2: UTMService 구현
    - Task 2.3: API 엔드포인트
    
    Task 1.1부터 시작할까요?

나: 응

# 5. TDD로 개발
AI: /test-first 실행...
    
    tests/test_utm_model.py 생성:
    [테스트 코드]
    
    테스트 실행: FAILED
    
    이제 구현할까요?

나: 응

# 6. 각 Task 완료 후 리뷰
AI: Task 1.1 완료
    
    /review-code 결과:
    ✅ 모든 체크리스트 통과
    
    다음 Task 1.2 진행할까요?
```

### 예시 2: 기존 코드 수정 (버그 수정)

```bash
claude

나: user_service.py의 이름 검증을 2자에서 3자로 변경해줘

AI: /check-workflow 실행...
    → Workflow 1 (기존 코드 수정)
    
    /test-first 실행...
    
    기존 테스트 발견:
    - test_user_service.py::test_이름_길이_검증
    
    1. 테스트 수정 (2자 → 3자)
    2. 구현 수정
    3. 테스트 실행
    
    진행할까요?

나: 응

AI: [테스트 수정 완료]
    [구현 수정 완료]
    
    테스트 실행 결과:
    ✅ test_이름_길이_검증 PASSED
    ✅ test_사용자_생성_성공 PASSED
    
    /review-code 실행...
    ✅ 모든 항목 통과
    
    변경사항 리뷰 부탁드립니다.

나: 좋아, 커밋해줘

AI: [커밋 메시지 생성]
    feat: 사용자 이름 최소 길이 검증 변경 (2자 → 3자)
    
    - UserService.최소_이름_길이 상수 변경
    - 테스트 케이스 업데이트
    - 모든 테스트 통과 확인
    
    커밋할까요?
```

### 예시 3: 코드 리뷰 요청

```bash
claude

나: /review-code
    
    방금 작성한 order_service.py를 리뷰해줘

AI: 코드 리뷰 시작...

    ## ⚙️ Functionality
    ✅ 요구사항 구현 완료
    ✅ 엣지 케이스 처리
    
    ## 📝 Code Quality
    ✅ Type hints 완비
    ✅ Docstring 상세
    ⚠️ 주의: 함수 이름이 영문 (order_create)
       → 한글 권장: 주문_생성
    
    ## 🗄️ Database
    ❌ N+1 쿼리 발견!
       Line 45: for 문 안에서 repository 호출
       
       수정 제안:
       ```python
       # ❌ 현재 (N+1)
       for item in items:
           product = await repo.find_by_id(item.id)
       
       # ✅ 개선
       product_ids = [item.id for item in items]
       products = await repo.find_by_ids(product_ids)
       ```
    
    ## 🧪 Testing
    ⚠️ 테스트 커버리지 70%
       누락된 테스트:
       - 재고 부족 시나리오
       - 동시 주문 처리
    
    수정할까요?

나: 응, DB 부분이랑 테스트 추가해줘
```

---

## 일상 워크플로우

### 아침에 시작할 때

```bash
# 1. 프로젝트 디렉토리로 이동
cd ~/projects/taxai-backend

# 2. Claude Code 실행
claude

# 3. 오늘 할 일 확인
나: 오늘은 뭐 하면 되지?

AI: .claude/context.md를 확인했습니다.
    
    어제 진행 중이던 작업:
    - UTM 추적 기능 Phase 2 (50% 완료)
    - 다음: Task 2.3 API 엔드포인트
    
    시작할까요?
```

### 작업 종료 시

```bash
나: 오늘 작업 정리해줘

AI: 오늘 완료한 작업:
    ✅ Task 2.3: UTM API 엔드포인트
    ✅ Task 3.1: 퍼널 분석 뷰 생성
    
    .claude/context.md 업데이트 완료
    
    내일 할 일:
    - Task 3.2: 배치 처리 구현
    - UTM 기능 전체 테스트
```

---

## 문제 해결

### Q: AI가 테스트를 건너뛰려고 해요

```bash
나: /test-first
    
    CLAUDE.md의 Critical Rule 1을 다시 읽어줘
```

### Q: 작업이 너무 커서 어떻게 시작할지 모르겠어요

```bash
나: /plan-feature
    
    [기능 설명]
```

### Q: 코드 품질이 걱정돼요

```bash
나: /review-code
```

### Q: 어떤 워크플로우를 따라야 할지 모르겠어요

```bash
나: /check-workflow
```

---

## 추가 리소스

- [CLAUDE.md](../CLAUDE.md) - 전체 가이드라인
- [examples/](../examples/) - 코드 예시
- [.claude/commands/]../.claude/commands/) - 커스텀 커맨드

---

**Last Updated**: 2025-11-23  
**Author**: kdy @ NEWEYE
