# Trading Ecosystem Workflow Quick Checklist

Use this checklist at the start of each development session.

## 🚀 Session Start

### 1. Load Context (5 min)
- [ ] Read TODO-MASTER.md
- [ ] Check current epic status
- [ ] Review ./project-plan/.claude/ configs
- [ ] Understand available skills (~/.claude/skills)

### 2. Define Session Outcome (10 min)
- [ ] What will we complete today?
- [ ] Which repos are affected?
- [ ] Any cross-repo dependencies?
- [ ] Clear definition of done?

**Outcome**: _________________________________

**Affected Repos**: _________________________________

## 📋 Planning Phase

### 3. Multi-Repo Analysis (10 min)
- [ ] List all affected repositories
- [ ] Identify cross-dependencies
- [ ] Check for interface changes needed
- [ ] Determine if new service required

**Repositories**:
```
[ ] audit-correlator-go
[ ] custodian-simulator-go
[ ] exchange-simulator-go
[ ] market-data-simulator-go
[ ] risk-monitor-py
[ ] trading-system-engine-py
[ ] test-coordinator-py
[ ] protobuf-schemas
[ ] simulator-ui-js
```

### 4. Branch Management (5 min)
For each affected repo:
- [ ] Create feature branch: `feature/<epic>-<description>`
- [ ] Verify branch is checked out
- [ ] Document in current-branches.md

**Branch Names**:
- Repo: _____________ Branch: _____________
- Repo: _____________ Branch: _____________
- Repo: _____________ Branch: _____________

### 5. Task Planning (15 min)
- [ ] Update TODO.md for each affected repo
- [ ] Add detailed tasks with acceptance criteria
- [ ] Mark cross-repo dependencies
- [ ] Identify blocking/blocked work

## 🎨 Interface Design (if needed)

### 6. Interface Changes (30 min if needed)
- [ ] **STOP**: Do NOT code yet if interfaces need changes
- [ ] Update protobuf schemas (if using gRPC)
- [ ] Update OpenAPI specs (if using HTTP)
- [ ] Define message formats (JSON schemas)
- [ ] Generate code from schemas
- [ ] Review with team if breaking changes

**Interface Changes**:
```
[ ] Protobuf: _________________
[ ] gRPC service: _________________
[ ] HTTP endpoint: _________________
[ ] Message format: _________________
```

## 🏗️ New Service Setup (if needed)

### 7. New Service Deployment (1 hour if needed)
- [ ] Invoke deployment skill
- [ ] Create minimal service structure
- [ ] Choose tech stack (Go/Python/TypeScript)
- [ ] Configure Docker & docker-compose
- [ ] Allocate port
- [ ] Add to service registry
- [ ] Setup health check endpoint
- [ ] Configure environment variables
- [ ] Add Prometheus metrics
- [ ] Test deployment in ecosystem

**New Service**:
- Name: _________________
- Tech: _________________
- Port: _________________

## 💻 Implementation Phase

### 8. Invoke Skills (start)
Check which skills to load:
```
[ ] go-development
[ ] python-development
[ ] typescript-development
[ ] database-skills
[ ] testing-protocols
```

### 9. Test-Driven Development (main work)
For each task:
- [ ] Write failing test first (RED)
- [ ] Implement minimal code (GREEN)
- [ ] Refactor for quality (REFACTOR)
- [ ] Commit with conventional message

**TDD Cycle Count**: _____ cycles completed

### 10. Implementation Order
- [ ] Domain layer (pure business logic)
- [ ] Application layer (ports/interfaces)
- [ ] Infrastructure layer (adapters)
- [ ] Presentation layer (UI/handlers)

## ✅ Quality Assurance

### 11. Testing (continuous)
- [ ] All unit tests pass
- [ ] Test coverage > 80%
- [ ] Integration tests pass
- [ ] Manual testing complete

**Test Results**:
- Unit: _____ / _____ passing
- Integration: _____ / _____ passing
- Coverage: _____%

### 12. Refactoring (30 min)
- [ ] All tests pass before refactoring
- [ ] Remove code duplication
- [ ] Simplify complex logic
- [ ] Improve naming
- [ ] All tests still pass after refactoring

**Refactorings Done**:
- _________________________________
- _________________________________

### 13. Security & Cross-Cutting (20 min)
- [ ] Invoke security-audit skill
- [ ] Run security scanner
- [ ] Check for secrets in code
- [ ] Verify logging (structured, no sensitive data)
- [ ] Add/verify Prometheus metrics
- [ ] Health check endpoint working
- [ ] Error handling comprehensive
- [ ] Configuration via env vars

**Security Scan**: [ ] PASS [ ] FAIL

### 14. GitHub Actions (10 min)
For each repo:
- [ ] Linting workflow exists
- [ ] Test workflow exists
- [ ] Security scan workflow exists
- [ ] Dependency check workflow exists

## 📚 Documentation

### 15. Repository Documentation (30 min)
For each affected repo:
- [ ] Update README.md (overview, setup, API)
- [ ] Update API documentation (OpenAPI/gRPC docs)
- [ ] Update architecture diagrams (if changed)
- [ ] Add inline code comments (complex logic only)

### 16. PR Documentation (20 min)
- [ ] Create PR file in ./docs/prs/PR-XXX-<description>.md
- [ ] Include: Summary, Motivation, Changes, Testing
- [ ] Document breaking changes (if any)
- [ ] List dependencies and related PRs
- [ ] Add performance impact
- [ ] Include deployment notes

## 🚢 Final Verification

### 17. Integration Testing (20 min)
- [ ] Start all services (docker-compose up)
- [ ] Wait for health checks
- [ ] Run integration test suite
- [ ] Verify service-to-service communication
- [ ] Check UI connects to backends
- [ ] Review logs for errors

**Integration Status**: [ ] PASS [ ] FAIL

### 18. Ecosystem Health (10 min)
- [ ] All services showing in service registry
- [ ] Prometheus scraping all services
- [ ] Grafana dashboards showing data
- [ ] Jaeger tracing working
- [ ] No error spam in logs

## 📤 Pull Request Creation

### 19. Commit & Push (10 min)
For each repo:
- [ ] Review all changes (git diff)
- [ ] Stage relevant files
- [ ] Create conventional commit(s)
- [ ] Push feature branch to origin

**Commit Messages**:
```
feat(<scope>): <description>
fix(<scope>): <description>
refactor(<scope>): <description>
```

### 20. Create PRs (15 min)
For each repo:
- [ ] Create PR via GitHub CLI or web
- [ ] Use PR doc as description
- [ ] Link related PRs
- [ ] Add reviewers
- [ ] Add labels (feature/fix/refactor)
- [ ] Link to issues

**Pull Requests**:
- Repo: _____________ PR: #_____
- Repo: _____________ PR: #_____
- Repo: _____________ PR: #_____

## 📝 Session Wrap-Up

### 21. Update Project Status (10 min)
- [ ] Update TODO-MASTER.md (mark completed)
- [ ] Update repo TODO.md files
- [ ] Document current-branches.md

### 22. Session Summary (10 min)
- [ ] Create session summary document
- [ ] List completed work
- [ ] Document next steps
- [ ] Note any blockers
- [ ] Record important decisions

**Session Summary**: ./docs/sessions/SESSION-YYYY-MM-DD.md

## ✨ Session Complete!

### Final Checklist
- [ ] All planned work completed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] PRs created and linked
- [ ] No uncommitted changes
- [ ] TODO-MASTER.md reflects current state

### Key Metrics
- **Time Spent**: _____ hours
- **Tasks Completed**: _____ / _____
- **Tests Added**: _____
- **Code Coverage**: _____%
- **PRs Created**: _____
- **Lines Added**: ~_____
- **Lines Removed**: ~_____

### Satisfaction Check
- [ ] Clear objectives achieved
- [ ] High-quality code delivered
- [ ] Good documentation written
- [ ] Ready for code review
- [ ] No known critical issues

---

## 🎯 Quick Reference

### Command Cheat Sheet

```bash
# Start session
cat project-plan/TODO-MASTER.md

# Create branch
git checkout -b feature/<epic>-<description>

# Run tests
make test            # All tests
go test ./...        # Go
pytest               # Python
npm test             # Node

# Generate diagrams
dot -Tsvg WORKFLOW.dot -o WORKFLOW.svg

# Create PR
gh pr create --title "feat: ..." --body-file docs/prs/PR-XXX.md

# Start services
docker-compose up -d

# Check health
docker-compose ps
curl http://localhost:8081/health

# View logs
docker-compose logs -f <service>
```

### Port Assignments
- 8081: service-registry
- 8082: audit-correlator
- 8083: custodian-simulator
- 8084: exchange-simulator
- 8085: market-data-simulator
- 8086: risk-monitor
- 8087: trading-system-engine
- 8088: test-coordinator
- 3002: simulator-ui

### Useful Links
- TODO-MASTER: `./project-plan/TODO-MASTER.md`
- Workflow Guide: `./project-plan/WORKFLOW-GUIDE.md`
- Skills: `~/.claude/skills/`
- Local Config: `./project-plan/.claude/`

---

**Print this checklist** and keep it handy during development sessions!

**Version**: 1.0 | **Date**: 2025-10-10
