# Project Configuration

## Project: Trading Ecosystem

**Project Code**: TSE
**Type**: Multi-component
**Architecture**: Clean Architecture
**Created**: 2025-09-16
**Status**: Active
**From Template**: claude-defaults v1.0

## Configuration Files

This project follows the configuration defined in these files:

### Core Philosophy & Principles

- `.claude_principles.md` - Engineering philosophy and core beliefs
- `.claude_personal.md` - Personal/team preferences and style

### Architecture & Design

- `.claude_architecture.md` - Project Architecture rules
- `.claude_solid.md` - SOLID principles and refactoring guidelines
- `.claude_code_style.md` - Architecture code conventions

### Development Process

- `.claude_workflow.md` - Git workflow, epics, and branching strategy
- `.claude_testing.md` - TDD approach and testing standards

### Repository & Structure  

- `.claude_repository.md` - Project repo structure and discovery rules
- `.claude_init.md` - Project initialization procedures

### Language-Specific

- `.claude_python.md` - Python standards (if applicable)
- `.claude_typescript.md` - TypeScript standards (if applicable)
- `.claude_go.md` - Go standards (if applicable)

## Project-Specific Configuration

### Project-Specific Overrides

<!-- Only document DEVIATIONS from standard configs here -->
<!-- Example:
- Using PostgreSQL-specific features (violates DB agnostic principle) because...
- Allowing larger functions (30 lines) in data migration scripts because...
-->

None currently.

### Project-Specific Rules

<!-- Only add rules UNIQUE to this project -->
<!-- Example:
- All monetary calculations must use Decimal type
- API responses must include rate limit headers
- Feature flags required for all new functionality
-->

None currently.

## Quick Start for Claude Code

When starting work:

1. Check current epic in TODO.md
2. **Load component-specific configuration**: If working on a specific component (not project-plan), read ALL .md files in that component's `.claude/` directory before starting work
3. Review any project-specific overrides above
4. Follow workflows defined in referenced configuration files
5. Create branches per `.claude_workflow.md`
6. Apply architecture per `.claude_architecture.md`
7. Test per `.claude_testing.md`

### Component-Specific Configuration Loading

Before working on any component, ALWAYS:

1. **Identify target component** from REPOSITORIES.md
2. **Check for component .claude/ directory**: `[component-name]/.claude/`
3. **Read ALL .md configuration files** in that directory, including:
   - Language-specific configs (`.claude_go.md`, `.claude_python.md`, etc.)
   - Component-specific architecture patterns
   - Component-specific testing requirements
   - Component-specific deployment procedures
   - Any other .md files in the component's .claude/ directory
4. **Apply component configs with higher precedence** than project-level configs

## Configuration Precedence

When rules conflict:

1. **Component-specific overrides** (component/.claude/ files) - highest priority
2. Project-specific overrides (this file)
3. Language-specific configuration (project-level)
4. Architecture/pattern configuration
5. Personal/team preferences
6. Core principles - lowest priority (but rarely overridden)

## Health Checks

Before starting work, verify:

- [ ] Can find `.claude/` directory (see `.claude_repository.md`)
- [ ] **Component-specific configs loaded** (if working on a component)
- [ ] Current epic identified in TODO.md
- [ ] On correct branch per `.claude_workflow.md`
- [ ] Tests passing on main branch
