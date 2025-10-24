# Trading Ecosystem Multi-Repo Workflow Guide

## Overview

This guide documents the comprehensive workflow for productive development in the Trading Ecosystem multi-repo project. It synthesizes patterns used across multiple sessions and provides a structured approach to managing complex, multi-service feature development.

## Workflow Visualization

See `WORKFLOW.dot` for the complete flowchart. Generate visual diagram with:

```bash
# Install graphviz
sudo apt-get install graphviz  # Ubuntu/Debian
brew install graphviz          # macOS

# Generate PNG
dot -Tpng WORKFLOW.dot -o WORKFLOW.png

# Generate SVG (better for documentation)
dot -Tsvg WORKFLOW.dot -o WORKFLOW.svg

# Generate PDF
dot -Tpdf WORKFLOW.dot -o WORKFLOW.pdf
```

## Workflow Phases

### Phase 1: Session Initialization

**Objective**: Load context and understand project state

#### 1.1 Load Configuration
```bash
# Global skills are in your home directory
~/.claude/skills/
  ├── go-development/
  ├── python-development/
  ├── typescript-development/
  ├── docker-deployment/
  ├── security-audit/
  └── testing-protocols/

# Local project configuration
./project-plan/.claude/
  ├── settings.json
  ├── epic-templates/
  └── conventions.md
```

**Action**: Claude loads both global and local configurations to understand available capabilities and project-specific conventions.

#### 1.2 Assess Project State
```bash
# Read master TODO
cat ./project-plan/TODO-MASTER.md
```

**Three Possible States**:

1. **Mid-Epic**: Work in progress from previous session
   - Continue with in-progress tasks
   - Check for blockers or completed dependencies

2. **Ready Epic**: Defined epic ready to start
   - Review epic requirements
   - Begin planning phase

3. **New Epic Needed**: Brainstorm new features
   - Define user stories
   - Break down into epics
   - Add to TODO-MASTER.md

**Example from Our Work**:
```markdown
# From TODO-MASTER.md
## Epic 3: Frontend Development [IN_PROGRESS]
- [x] Initialize Next.js project
- [x] Configure Clean Architecture
- [in_progress] Implement SSE real-time updates
- [ ] Add user authentication
```

### Phase 2: Session Planning

**Objective**: Define clear outcomes for today's session

#### 2.1 Define Session Outcome

**Questions to Answer**:
- What will we complete today?
- Which repositories will be affected?
- Are there cross-repo dependencies?
- What's the definition of done?

**Example Session Outcomes**:
- "Implement SSE client and integrate into market data adapter"
- "Add gRPC health check service to all Go simulators"
- "Create audit correlation service with PostgreSQL persistence"

#### 2.2 Identify Required Components

**9 Component Repositories**:
```
Go Services (4):
  ├── audit-correlator-go
  ├── custodian-simulator-go
  ├── exchange-simulator-go
  └── market-data-simulator-go

Python Services (3):
  ├── risk-monitor-py
  ├── trading-system-engine-py
  └── test-coordinator-py

Infrastructure:
  ├── protobuf-schemas
  └── simulator-ui-js
```

**Example**: SSE implementation required changes to:
- `protobuf-schemas` (not needed, REST-based)
- `simulator-ui-js` (main work)
- Backend services would need SSE endpoints (future work)

### Phase 3: Multi-Repo Coordination

**Objective**: Ensure all repositories are in correct state for work

#### 3.1 Analyze Cross-Dependencies

**Key Questions**:
- Does Service A depend on Service B's new endpoint?
- Do we need to update protobuf schemas?
- Will changes break existing consumers?
- What's the deployment order?

**Dependency Types**:
1. **Schema Dependencies**: Protobuf message changes
2. **API Dependencies**: gRPC service definitions, HTTP endpoints
3. **Data Dependencies**: Database schema changes
4. **Configuration Dependencies**: Environment variables, service discovery

#### 3.2 New Service Decision

**When to Create New Service**:
- New domain capability (audit, chaos testing)
- Separation of concerns
- Independent scaling requirements
- Technology diversity (Go vs Python)

**Checklist for New Service**:
- [ ] Define service responsibility (single concern)
- [ ] Choose appropriate technology (Go for simulators, Python for complex logic)
- [ ] Plan database requirements (if any)
- [ ] Design service interface (gRPC, HTTP, or both)
- [ ] Plan port allocation
- [ ] Update service registry

**Example**: Creating `test-coordinator-py`
```yaml
Service: test-coordinator-py
Port: 8088
Purpose: Orchestrate chaos testing scenarios
Tech: Python (complex orchestration logic)
Database: PostgreSQL (test results history)
APIs: HTTP REST (UI integration)
```

### Phase 4: Branch Management

**Objective**: Create proper feature branches for all affected repos

#### 4.1 Branch Naming Convention

```bash
# Format: feature/<epic-name>-<component-specific-description>
feature/sse-implementation-client
feature/sse-implementation-adapters
feature/health-checks-grpc

# Bug fixes
fix/<issue-description>

# Refactoring
refactor/<area-of-change>
```

#### 4.2 Branch Creation Process

```bash
# For each affected repository
cd /path/to/repository

# Check current state
git status
git branch

# Create feature branch from main/master
git checkout main
git pull origin main
git checkout -b feature/sse-implementation

# Verify branch
git branch --show-current
```

**Critical Rule**: **NO WORK WITHOUT BRANCH**

#### 4.3 Multi-Repo Branch Tracking

Create tracking file:
```bash
# ./project-plan/current-branches.md
## Active Feature Branches

### Epic: SSE Real-time Updates
- simulator-ui-js: `feature/sse-implementation`
- market-data-simulator-go: `feature/sse-endpoints` (future)
- risk-monitor-py: `feature/sse-endpoints` (future)
```

### Phase 5: Task Planning per Repo

**Objective**: Detailed task breakdown with acceptance criteria

#### 5.1 Update TODO.md Files

Each repository gets specific TODO.md with detailed tasks:

**Example**: `simulator-ui-js/TODO.md`
```markdown
# TODO: SSE Implementation

## Phase 1: Core Client [IN_PROGRESS]
- [x] Create SSE client utility class
  - [x] Connection management
  - [x] Automatic reconnection with exponential backoff
  - [x] Event subscription system
  - [x] Error handling
  - [x] TypeScript types
- [x] Write unit tests for SSE client
  - [x] Connection lifecycle
  - [x] Message parsing
  - [x] Reconnection logic
  - [x] Error scenarios

## Phase 2: Adapter Integration [IN_PROGRESS]
- [x] Update market data adapter
  - [x] Replace polling with SSE subscription
  - [x] Maintain fallback to polling
  - [x] Test with mock SSE server
- [x] Create risk monitor adapter
  - [x] Implement RiskPort interface
  - [x] Add SSE subscription method
  - [x] Write adapter tests
...

## Acceptance Criteria
- [ ] All tests pass (100+ tests)
- [ ] SSE connections work with real backend
- [ ] Fallback to polling works when SSE unavailable
- [ ] No memory leaks (cleanup verified)
- [ ] Documentation complete
```

#### 5.2 Mark Cross-Repo Dependencies

```markdown
## Dependencies

### Blocking
- None (UI uses fallback polling)

### Blocked By
- This work blocks: Backend SSE endpoint implementation

### Related
- protobuf-schemas: No changes needed (REST-based)
- market-data-simulator-go: Will need `/stream/prices` endpoint
- risk-monitor-py: Will need `/stream/risk` endpoint
```

### Phase 6: Interface Design First

**Objective**: Define public interfaces before implementation

**Critical Principle**: **INTERFACES BEFORE IMPLEMENTATION**

#### 6.1 Interface Changes Decision

**Ask**: Do we need to change:
- Protobuf message definitions?
- gRPC service definitions?
- HTTP API endpoints?
- JSON message formats?

**If YES**: Stop and design interfaces first

#### 6.2 Schema Updates

**Order of Operations**:
```
1. protobuf-schemas (if using gRPC)
2. Generate code from schemas
3. Update service implementations
4. Update clients
```

**Example**: Adding health check service
```protobuf
// protobuf-schemas/health/v1/health.proto
syntax = "proto3";

package health.v1;

service HealthService {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
  rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse);
}

message HealthCheckRequest {
  string service = 1;
}

message HealthCheckResponse {
  enum ServingStatus {
    UNKNOWN = 0;
    SERVING = 1;
    NOT_SERVING = 2;
    SERVICE_UNKNOWN = 3;
  }
  ServingStatus status = 1;
}
```

#### 6.3 Code Generation

```bash
# Generate from protobuf
cd protobuf-schemas
make generate-go
make generate-python

# Verify generated code
ls -la generated/go/health/v1/
ls -la generated/python/health/v1/
```

#### 6.4 HTTP API Design

**For REST APIs**: Define OpenAPI/Swagger spec first

**Example**: SSE endpoint specification
```yaml
# market-data-simulator-go/api/openapi.yaml
paths:
  /api/v1/stream/prices:
    get:
      summary: Stream real-time price updates
      description: Server-Sent Events stream for cryptocurrency prices
      produces:
        - text/event-stream
      parameters:
        - name: assets
          in: query
          description: Comma-separated list of assets (BTC,ETH,SOL)
          schema:
            type: string
      responses:
        '200':
          description: SSE stream
          content:
            text/event-stream:
              schema:
                type: string
                example: |
                  event: price
                  data: {"asset":"BTC","price":65000,"timestamp":1234567890}
```

### Phase 7: Deployment Setup (New Services)

**Objective**: Get new service deployed and integrated

#### 7.1 Invoke Deployment Skill

```bash
# Use deployment skill from ~/.claude/skills/docker-deployment/
```

**Deployment Checklist**:
- [ ] Create minimal service structure
- [ ] Configure Dockerfile
- [ ] Add to docker-compose.yml
- [ ] Allocate port
- [ ] Configure service registry integration
- [ ] Add health check endpoint
- [ ] Setup environment variables
- [ ] Configure logging
- [ ] Add Prometheus metrics
- [ ] Test deployment

**Example**: Adding test-coordinator-py
```yaml
# docker-compose.yml
services:
  test-coordinator:
    build:
      context: ./test-coordinator-py
      dockerfile: Dockerfile
    container_name: test-coordinator
    ports:
      - "8088:8088"
    environment:
      - SERVICE_NAME=test-coordinator
      - SERVICE_REGISTRY_URL=http://service-registry:8081
      - DATABASE_URL=postgresql://user:pass@postgres:5432/chaos
    depends_on:
      - postgres
      - service-registry
    networks:
      - trading-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8088/health"]
      interval: 10s
      timeout: 5s
      retries: 3
```

### Phase 8: Implementation

**Objective**: Write great code following best practices

#### 8.1 Invoke Language Skills

**Go Services**:
```bash
~/.claude/skills/go-development/
  ├── best-practices.md
  ├── testing-patterns.md
  ├── error-handling.md
  └── project-structure.md
```

**Python Services**:
```bash
~/.claude/skills/python-development/
  ├── type-hints.md
  ├── async-patterns.md
  ├── testing-pytest.md
  └── clean-architecture.md
```

**TypeScript/Next.js**:
```bash
~/.claude/skills/typescript-development/
  ├── react-patterns.md
  ├── next-js-best-practices.md
  ├── testing-jest.md
  └── clean-architecture.md
```

#### 8.2 Test-Driven Development

**TDD Protocol**:
```
1. Write failing test
2. Implement minimal code to pass
3. Refactor
4. Repeat
```

**Example from SSE Client**:
```typescript
// 1. Write test first
describe('SSEClient', () => {
  it('should establish connection with correct URL', () => {
    const client = new SSEClient('http://localhost:8080/stream')
    client.connect()

    expect(global.EventSource).toHaveBeenCalledWith(
      'http://localhost:8080/stream',
      expect.any(Object)
    )
  })
})

// 2. Implement
export class SSEClient {
  constructor(private url: string) {}

  connect(): void {
    this.eventSource = new EventSource(this.url)
  }
}

// 3. Run tests
npm test

// 4. Refactor (add error handling, options, etc.)
```

#### 8.3 Implementation Order

**By Dependency**:
```
1. Domain layer (pure business logic)
2. Application layer (ports/interfaces)
3. Infrastructure layer (adapters)
4. Presentation layer (UI/API handlers)
```

**Example**: Clean Architecture in simulator-ui-js
```
src/
  domain/
    types.ts          # First - pure types
    services/         # Second - pure functions
  application/
    ports/            # Third - interfaces
  infrastructure/
    adapters/         # Fourth - implementations
  presentation/
    components/       # Last - UI
```

### Phase 9: Testing & Quality

**Objective**: Ensure code quality and correctness

#### 9.1 Test Levels

**Unit Tests**:
- Test individual functions/classes
- Mock all dependencies
- Fast execution

**Integration Tests**:
- Test component interactions
- Use real database (test instance)
- Test API endpoints

**End-to-End Tests**:
- Test full user flows
- All services running
- Real-world scenarios

#### 9.2 Test Coverage Requirements

```bash
# Go services
go test -cover ./...
# Target: >80% coverage

# Python services
pytest --cov=src tests/
# Target: >85% coverage

# TypeScript/Next.js
npm run test:coverage
# Target: >80% coverage
```

#### 9.3 Test Execution

```bash
# Run all tests
make test-all

# Or per service
cd market-data-simulator-go && go test ./...
cd risk-monitor-py && pytest
cd simulator-ui-js && npm test
```

**Fix Cycle**: If tests fail
```
Run tests → Identify failures → Fix code → Run tests again
```

### Phase 10: Refactoring

**Objective**: Improve code quality without changing behavior

#### 10.1 Refactoring Triggers

**When to Refactor**:
- Code duplication (DRY principle)
- Long functions (>50 lines)
- Complex conditionals (cyclomatic complexity >10)
- Poor naming
- Missing abstractions
- Performance issues

**When NOT to Refactor**:
- During feature development (finish first)
- Before understanding the code
- Without tests in place

#### 10.2 Refactoring Checklist

- [ ] Verify all tests pass before refactoring
- [ ] Make one refactoring at a time
- [ ] Run tests after each change
- [ ] Commit after successful refactoring
- [ ] Document why if non-obvious

**Example Refactorings**:
```typescript
// Before: Duplicated error handling
async function fetchPrices() {
  try {
    const response = await httpClient.get('/prices')
    return response.data
  } catch (error) {
    console.error('Failed to fetch prices:', error)
    return mockPrices()
  }
}

async function fetchPositions() {
  try {
    const response = await httpClient.get('/positions')
    return response.data
  } catch (error) {
    console.error('Failed to fetch positions:', error)
    return mockPositions()
  }
}

// After: Extracted common pattern
async function fetchWithFallback<T>(
  url: string,
  fallback: () => T
): Promise<T> {
  try {
    const response = await httpClient.get(url)
    return response.data
  } catch (error) {
    console.error(`Failed to fetch ${url}:`, error)
    return fallback()
  }
}

const fetchPrices = () => fetchWithFallback('/prices', mockPrices)
const fetchPositions = () => fetchWithFallback('/positions', mockPositions)
```

### Phase 11: Security & Cross-Cutting Concerns

**Objective**: Ensure security and operational excellence

#### 11.1 Security Skill Invocation

```bash
~/.claude/skills/security-audit/
  ├── dependency-scanning.md
  ├── code-scanning.md
  ├── secret-detection.md
  └── vulnerability-assessment.md
```

#### 11.2 GitHub Actions Setup

**For Each Repository**:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run linter
        run: make lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: make test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run security scan
        uses: securego/gosec@master  # For Go
      # or
      - name: Run Bandit
        run: bandit -r src/  # For Python

  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check dependencies
        uses: snyk/actions/golang@master  # For Go
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

#### 11.3 Cross-Cutting Concerns Checklist

**Logging**:
- [ ] Structured logging (JSON format)
- [ ] Appropriate log levels
- [ ] No sensitive data in logs
- [ ] Correlation IDs for tracing

**Observability**:
- [ ] Prometheus metrics exposed
- [ ] Health check endpoint
- [ ] Readiness endpoint
- [ ] Liveness endpoint

**Error Handling**:
- [ ] Errors properly wrapped with context
- [ ] Client errors (4xx) vs server errors (5xx)
- [ ] Retry logic with exponential backoff
- [ ] Circuit breakers for external dependencies

**Configuration**:
- [ ] Environment variables for config
- [ ] No secrets in code
- [ ] Sensible defaults
- [ ] Configuration validation on startup

### Phase 12: Documentation

**Objective**: Comprehensive documentation for maintainability

#### 12.1 Repository Documentation

**Each Repository Needs**:

**README.md**:
```markdown
# Service Name

## Overview
Brief description of service purpose

## Architecture
- Technology stack
- Dependencies
- Design patterns used

## API Documentation
Link to OpenAPI spec or generated docs

## Configuration
Environment variables and their purposes

## Development
- How to build
- How to run tests
- How to run locally

## Deployment
- Docker build instructions
- Required infrastructure
- Port mappings

## Monitoring
- Prometheus metrics
- Health check endpoints
- Logging format
```

**API Documentation**:
- OpenAPI/Swagger specs for HTTP APIs
- gRPC service documentation (from protobuf comments)
- Example requests/responses

**Architecture Diagrams**:
```bash
# Update if significant changes
docs/architecture/
  ├── component-diagram.png
  ├── sequence-diagrams/
  └── data-flow.png
```

#### 12.2 Pull Request Documentation

**Create PR Files in ./docs/prs/**:

```markdown
# docs/prs/PR-001-sse-implementation.md

## Summary
Implement Server-Sent Events for real-time data streaming in UI

## Motivation
Replace 5-second polling with real-time updates for better UX and reduced server load

## Changes

### simulator-ui-js
- Added SSE client utility with reconnection
- Updated market data adapter to use SSE
- Created risk monitor adapter with SSE support
- Updated trading adapter with SSE subscriptions
- Modified pages to use SSE subscriptions
- Added 50+ unit tests

## Testing
- All unit tests pass (40+ new tests)
- Manual testing with mock SSE server
- Fallback to polling verified

## Performance Impact
- Latency: 2.5s → <100ms (96% improvement)
- Network requests: Reduced by ~95%

## Breaking Changes
None - backward compatible with polling fallback

## Dependencies
- Requires backend SSE endpoints (future work)
- Falls back gracefully if not available

## Checklist
- [x] Tests added/updated
- [x] Documentation updated
- [x] No breaking changes
- [x] Security considerations addressed
- [x] Performance impact assessed

## Related PRs
- Future: Backend SSE endpoints in market-data-simulator-go
- Future: Backend SSE endpoints in risk-monitor-py

## Screenshots
(If applicable)

## Deployment Notes
- No special deployment steps
- No database migrations
- No configuration changes required
```

### Phase 13: Final Verification

**Objective**: Ensure everything works together

#### 13.1 Integration Testing

```bash
# Start all services
docker-compose up -d

# Wait for health
./scripts/wait-for-health.sh

# Run integration tests
make integration-test

# Check logs for errors
docker-compose logs --tail=100
```

#### 13.2 Ecosystem Verification

**Checklist**:
- [ ] All services start successfully
- [ ] Service registry shows all services
- [ ] Health checks pass
- [ ] Cross-service communication works
- [ ] UI connects to all backend services
- [ ] Prometheus scraping works
- [ ] Logs are properly formatted
- [ ] No error spam in logs

#### 13.3 Ready for PR Decision

**Ready Criteria**:
- All tests pass (unit + integration)
- Documentation complete
- No known bugs
- Code reviewed (self-review at minimum)
- Performance acceptable
- Security scan clean

**If Not Ready**:
- Document remaining issues
- Prioritize fixes
- Re-test after fixes

### Phase 14: Pull Request Creation

**Objective**: Create high-quality PRs for review

#### 14.1 Conventional Commit Messages

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Adding tests
- `docs`: Documentation changes
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples**:
```bash
git commit -m "feat(sse): implement SSE client with auto-reconnection

- Create SSEClient class with event subscriptions
- Add exponential backoff for reconnection
- Include comprehensive error handling
- Add TypeScript types for type safety

Closes #123"

git commit -m "feat(adapters): add SSE support to market data adapter

- Replace polling with SSE subscription
- Maintain fallback to polling
- Add tests for SSE integration

Related to #123"
```

#### 14.2 Push Branches

```bash
# For each affected repository
cd /path/to/repository

# Ensure all changes committed
git status

# Push feature branch
git push -u origin feature/sse-implementation
```

#### 14.3 Create Pull Requests

**Using GitHub CLI** (recommended):
```bash
gh pr create \
  --title "feat: Implement SSE real-time updates" \
  --body-file docs/prs/PR-001-sse-implementation.md \
  --base main \
  --head feature/sse-implementation
```

**Or via GitHub Web UI**:
- Navigate to repository
- Click "Compare & pull request"
- Fill in title and description (from PR doc)
- Select reviewers
- Add labels
- Link related issues

#### 14.4 Link Related PRs

**In PR Description**:
```markdown
## Related PRs
- simulator-ui-js: #123 (this PR)
- market-data-simulator-go: #45 (blocked by this)
- risk-monitor-py: #67 (blocked by this)

## Dependency Graph
simulator-ui-js#123 → market-data-simulator-go#45
simulator-ui-js#123 → risk-monitor-py#67
```

### Phase 15: Session Wrap-Up

**Objective**: Update project state and summarize work

#### 15.1 Update TODO-MASTER.md

```markdown
# TODO-MASTER.md

## Epic 3: Frontend Development [IN_PROGRESS → COMPLETED]
- [x] Initialize Next.js project
- [x] Configure Clean Architecture
- [x] Implement SSE real-time updates ✅ (completed today)
  - Created SSE client utility
  - Integrated into all adapters
  - Updated all pages
  - Added comprehensive tests
  - Documented implementation
- [in_progress] Add user authentication (next session)

## Session 2025-10-10: SSE Implementation ✅
Completed SSE real-time updates for UI
- Created robust SSE client with reconnection
- Updated market data, risk monitor, trading adapters
- Modified dashboard, market, trading, risk pages
- Added 50+ tests
- Created comprehensive documentation
- PRs ready for review
```

#### 15.2 Generate Session Summary

**Session Summary Template**:
```markdown
# Session Summary: 2025-10-10

## Objective
Implement SSE (Server-Sent Events) for real-time data streaming

## Work Completed

### Repositories Modified
1. simulator-ui-js
   - Branch: feature/sse-implementation
   - PR: #123
   - Status: Ready for review

### Files Created/Modified
- Created: 4 files (~1,500 lines)
  - src/infrastructure/utils/sse-client.ts
  - src/infrastructure/adapters/rest-risk-monitor.ts
  - tests/infrastructure/sse-client.test.ts
  - tests/infrastructure/rest-market-data-sse.test.ts

- Modified: 6 files
  - src/infrastructure/adapters/rest-market-data.ts
  - src/infrastructure/adapters/rest-trading.ts
  - src/app/page.tsx
  - src/app/market/page.tsx
  - src/app/trading/page.tsx
  - src/app/risk/page.tsx

### Tests
- Added: 50+ unit tests
- Coverage: 80%+ on new code
- All tests passing ✅

### Documentation
- SSE-IMPLEMENTATION.md (400+ lines)
- IMPLEMENTATION-SUMMARY.md
- Updated README.md

## Outcomes
- ✅ Real-time price updates working
- ✅ Real-time risk metrics working
- ✅ Real-time position updates working
- ✅ Fallback to polling works
- ✅ Comprehensive test coverage
- ✅ Full documentation

## Next Steps
1. Code review of PR #123
2. Backend team: Implement SSE endpoints
3. Integration testing with real backends
4. Next epic: User authentication

## Blockers
None

## Notes
- SSE implementation is production-ready
- Graceful fallback ensures no disruption
- Performance improvements: 96% latency reduction
```

## Common Patterns & Best Practices

### Pattern 1: Interface-First Development

**Always design interfaces before implementation**:
```
1. Define protobuf/API spec
2. Generate code (if applicable)
3. Implement server
4. Implement client
```

### Pattern 2: Test-Driven Development

**Red-Green-Refactor cycle**:
```
1. Write failing test (RED)
2. Implement minimal code to pass (GREEN)
3. Improve code quality (REFACTOR)
4. Repeat
```

### Pattern 3: Parallel Work Coordination

**Dependencies allow parallel work**:
```
Independent services → Work in parallel
Shared schemas → Update schemas first, then parallel
API consumers → Update API first, then parallel consumers
```

### Pattern 4: Gradual Rollout

**For risky changes**:
```
1. Implement behind feature flag
2. Deploy to staging
3. Test thoroughly
4. Enable for small % of traffic
5. Monitor metrics
6. Gradually increase %
7. Remove feature flag when stable
```

### Pattern 5: Backward Compatibility

**Maintain compatibility during transitions**:
```
1. Add new API alongside old
2. Deprecate old API (with notice)
3. Monitor usage of old API
4. Remove old API after grace period
```

## Decision Trees

### Should I Create a New Service?

```
Is this a new domain capability? → YES → New service
Is this existing service too complex? → YES → Consider splitting
Is this for different scaling needs? → YES → New service
Is this purely UI concern? → NO → Add to UI
Is this a small utility? → NO → Add as library
```

### Should I Update Protobuf Schemas?

```
Using gRPC? → YES → Update protobuf
Breaking change? → YES → Version the API (v2)
Adding optional field? → OK → Backward compatible
Removing field? → DANGER → Coordinate with all consumers
Changing field type? → BREAKING → Version the API
```

### Should I Refactor Now?

```
Tests pass? → NO → Don't refactor yet
Feature complete? → NO → Finish feature first
Code duplication? → YES → Refactor
Performance issue? → YES → Optimize
Just don't like it? → MAYBE → Discuss with team
```

## Skill Invocations Map

```
Planning Phase:
  - No specific skills, use general problem-solving

Interface Design:
  - protobuf-skills (for gRPC)
  - api-design-skills (for REST)

Implementation:
  - go-development (for Go services)
  - python-development (for Python services)
  - typescript-development (for UI)
  - database-skills (for persistence)

Testing:
  - testing-protocols (TDD approach)
  - integration-testing (end-to-end)

Deployment:
  - docker-deployment (containerization)
  - kubernetes-deployment (orchestration)

Security:
  - security-audit (scanning & auditing)
  - secret-management (credentials)

Quality:
  - code-review (best practices)
  - performance-testing (load testing)
```

## Troubleshooting

### Problem: "Can't find the right repo to start in"
**Solution**: Check TODO-MASTER.md and look for current epic. The epic description should mention affected repos.

### Problem: "Interface changes breaking consumers"
**Solution**: Version your APIs. Never break existing versions. Add v2 alongside v1.

### Problem: "Too many repos to coordinate"
**Solution**: Use feature flags. Deploy code disabled, enable when all pieces ready.

### Problem: "Tests failing after refactoring"
**Solution**: Revert refactoring, fix tests, then refactor again. Tests are truth.

### Problem: "Don't know which skill to invoke"
**Solution**: Check ~/.claude/skills/README.md for skill descriptions and use cases.

### Problem: "Unclear cross-repo dependencies"
**Solution**: Draw a dependency diagram. Use tools like `madge` for dependency analysis.

## Metrics & Success Indicators

### Development Velocity
- Tasks completed per session
- Time to implement features
- Code review turnaround time

### Code Quality
- Test coverage (target: >80%)
- Code review feedback count
- Bug escape rate to production

### System Health
- Service uptime (target: 99.9%)
- Error rates
- Response times (p50, p95, p99)

### Team Efficiency
- PRs merged per week
- Deployment frequency
- Mean time to recovery (MTTR)

## Conclusion

This workflow ensures:
- ✅ Clear session objectives
- ✅ Proper multi-repo coordination
- ✅ Interface-first design
- ✅ High code quality
- ✅ Comprehensive testing
- ✅ Security & observability
- ✅ Great documentation
- ✅ Smooth PR process

Follow this workflow for consistent, high-quality delivery across the Trading Ecosystem multi-repo project.

---

**Version**: 1.0
**Last Updated**: 2025-10-10
**Maintained By**: Trading Ecosystem Team
