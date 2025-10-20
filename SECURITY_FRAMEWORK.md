# Security & Audit Framework

**Status**: Required for all components
**Version**: 1.0
**Last Updated**: 2025-10-03

## Core Principle

**Security is not an add-on or nice-to-have. It is a first-class architectural requirement baked into every component from day zero.**

Every repository—Python, Go, Rust, TypeScript, database—must implement the complete security framework before merging to main. This is non-negotiable.

---

## Framework Overview

This framework is derived from production security audits and implements defense-in-depth across 10 phases:

```
Phase 0: Hygiene          → Clean foundation
Phase 1: SBOM             → Know what you ship
Phase 2: SAST             → Static analysis
Phase 3: Secrets          → No leaked credentials
Phase 4: Supply Chain     → Dependency security
Phase 5: Backdoor Recon   → Obfuscation detection
Phase 6: IaC/Cloud        → Infrastructure security
Phase 7: Runtime          → Production hardening
Phase 8: Behavior Tests   → Security validation
Phase 9: CI/CD Security   → Pipeline integrity
Phase 10: Threat Model    → Risk documentation
```

---

## Universal Security Checklist

Every component **must** have:

### ✅ Phase 0: Hygiene (Foundation)
- [ ] `.gitignore` excludes secrets, env files, caches, logs, build artifacts
- [ ] `CODEOWNERS` file defines security review requirements
- [ ] Dependabot enabled (daily dependencies, weekly GitHub Actions)
- [ ] Locked dependency installation in CI (no floating versions)
- [ ] Security contact in README.md

### ✅ Phase 1: Inventory + SBOM (Know Your Dependencies)
- [ ] SBOM generation in CI (Syft/CycloneDX)
- [ ] Vulnerability scanning (Grype/Trivy)
- [ ] OSV-Scanner for known vulnerabilities
- [ ] Artifact retention (90 days minimum)
- [ ] Checksums for all build artifacts

### ✅ Phase 2: SAST (Static Analysis)
- [ ] Language-specific SAST tool (CodeQL/Semgrep/Bandit/gosec)
- [ ] Custom rules for:
  - Command injection (exec, eval, system calls)
  - SQL injection (raw queries, string concatenation)
  - Path traversal (file operations)
  - Insecure deserialization
  - Hardcoded credentials
- [ ] SARIF upload to GitHub Securit   y tab
- [ ] Zero high/critical issues policy

### ✅ Phase 3: Secrets Scanning (No Leaks)
- [ ] Gitleaks full history scan in CI
- [ ] Pre-commit hook template provided
- [ ] `.gitleaks.toml` configuration
- [ ] Secret rotation procedure documented
- [ ] AWS/GCP/Azure credential detection

### ✅ Phase 4: Supply Chain Security (Dependency Trust)
- [ ] Dependency review on PRs
- [ ] Software Bill of Materials (SBOM) published
- [ ] OSSF Scorecard for repository health
- [ ] Triage policy for vulnerabilities (24hr high, 7 day medium)
- [ ] Pinned GitHub Actions versions (no @latest)

### ✅ Phase 5: Backdoor Reconnaissance (Obfuscation Detection)
- [ ] Base64 blob detection (>80 chars)
- [ ] Unicode homoglyph scanning
- [ ] Outbound network call allowlist
- [ ] Dynamic code execution detection (eval, Function constructor)
- [ ] Obfuscation pattern detection

### ✅ Phase 6: Infrastructure as Code (Cloud Security)
- [ ] Terraform/Pulumi security scanning (Checkov/tfsec)
- [ ] No wildcard permissions
- [ ] Least privilege IAM policies
- [ ] Encryption at rest and in transit
- [ ] Network segmentation enforced

### ✅ Phase 7: Runtime Hardening (Production Security)
- [ ] Security headers (CSP, HSTS, X-Content-Type-Options, etc.)
- [ ] Input validation (Zod/Pydantic/validator)
- [ ] Output encoding (no XSS)
- [ ] Error handling (no stack traces in production)
- [ ] Rate limiting and DDoS protection

### ✅ Phase 8: Security Behavior Tests (Validation)
- [ ] Header security tests
- [ ] Authentication/authorization tests
- [ ] Input fuzzing tests
- [ ] Error handling tests
- [ ] SQL injection prevention tests

### ✅ Phase 9: CI/CD & Repository Security (Pipeline Integrity)
- [ ] Required status checks for security tools
- [ ] Branch protection (main/master)
- [ ] Code review required (CODEOWNERS)
- [ ] Signed commits encouraged
- [ ] Immutable audit logs

### ✅ Phase 10: Threat Modeling (Documentation)
- [ ] STRIDE threat model documented
- [ ] Attack surface analysis
- [ ] OWASP Top 10 mapping
- [ ] Residual risk acceptance
- [ ] Security audit report

---

## Language-Specific Implementation

Each language has specific tooling and patterns. See language-specific guides:

### TypeScript/JavaScript
- **SAST**: CodeQL (JavaScript/TypeScript), Semgrep, ESLint security plugins
- **SBOM**: Syft, npm audit
- **Secrets**: Gitleaks
- **Dependencies**: Dependabot, OSV-Scanner, npm audit
- **Runtime**: Helmet.js (Express), Next.js security headers
- **Config**: `.claude/.claude_security_typescript.md`

### Python
- **SAST**: Bandit, Semgrep, CodeQL (Python)
- **SBOM**: Syft, CycloneDX, pip-audit
- **Secrets**: Gitleaks, detect-secrets
- **Dependencies**: pip-audit, safety, OSV-Scanner
- **Runtime**: Pydantic validation, secure headers (FastAPI)
- **Config**: `.claude/.claude_security_python.md`

### Go
- **SAST**: gosec, Semgrep, CodeQL (Go)
- **SBOM**: Syft, CycloneDX
- **Secrets**: Gitleaks
- **Dependencies**: govulncheck, Nancy, OSV-Scanner
- **Runtime**: Input validation, secure defaults
- **Config**: `.claude/.claude_security_go.md`

### Rust
- **SAST**: cargo-audit, Clippy with security lints, Semgrep
- **SBOM**: cargo-sbom, Syft
- **Secrets**: Gitleaks
- **Dependencies**: cargo-deny, cargo-audit
- **Runtime**: Type safety, ownership model (memory safety by default)
- **Config**: `.claude/.claude_security_rust.md`

### PostgreSQL
- **SAST**: SQLFluff, pg_stat_statements analysis
- **Secrets**: No hardcoded passwords, environment-based auth
- **Security**: Row-level security (RLS), encrypted connections (SSL/TLS)
- **Audit**: pgAudit extension, query logging
- **Config**: `.claude/.claude_security_postgresql.md`

### Redis
- **SAST**: redis-cli --scan for key analysis
- **Secrets**: ACLs with environment-based passwords
- **Security**: TLS connections, AUTH required, protected mode
- **Audit**: MONITOR for debugging (dev only), slowlog analysis
- **Config**: `.claude/.claude_security_redis.md`

### MongoDB
- **SAST**: MongoDB security checklist
- **Secrets**: SCRAM authentication, environment-based credentials
- **Security**: TLS/SSL, network isolation, field-level encryption
- **Audit**: MongoDB auditing system, profiling
- **Config**: `.claude/.claude_security_mongodb.md`

---

## Security Workflows

### CI/CD Pipeline Integration

Every repository must have these GitHub Actions workflows:

```yaml
# Required Security Workflows
.github/workflows/
  ├── sast.yml              # Static analysis (CodeQL/Semgrep/language-specific)
  ├── sbom.yml              # SBOM generation and vulnerability scanning
  ├── secrets.yml           # Gitleaks full history scan
  ├── dependency-review.yml # PR dependency review
  ├── osv-scanner.yml       # Known vulnerability scanning
  └── security-scorecard.yml # OSSF Scorecard (optional but recommended)
```

### Branch Protection Rules

Main branch must require:
- ✅ All security checks passing
- ✅ Code review from CODEOWNERS
- ✅ Up-to-date with base branch
- ✅ Signed commits (recommended)

### PR Template Security Section

Every PR must include:

```markdown
## Security Checklist
- [ ] No secrets committed
- [ ] Dependencies reviewed (no new high/critical CVEs)
- [ ] SAST scan passing
- [ ] Input validation added for new endpoints
- [ ] Security tests added/updated
- [ ] Threat model updated (if architecture changed)
```

---

## Vulnerability Triage Policy

### SLA Response Times

| Severity | Example | Response Time | Fix Time |
|----------|---------|---------------|----------|
| **Critical** | Remote code execution, auth bypass | 4 hours | 24 hours |
| **High** | SQL injection, XSS, credential leak | 24 hours | 7 days |
| **Medium** | Outdated dependency with exploit | 7 days | 30 days |
| **Low** | Informational, minimal risk | 30 days | 90 days |

### Exception Process

If a vulnerability cannot be fixed within SLA:
1. Document in `SECURITY_EXCEPTIONS.md`
2. Explain compensating controls
3. Set review date (max 90 days)
4. Get security approval (CODEOWNERS)
5. Create tracking issue

---

## Security Documentation Requirements

Every repository must have:

### Required Files

```
docs/
  ├── SECURITY.md                 # Security policy, contact, disclosure
  ├── SECURITY_SAST.md           # SAST configuration and results
  ├── SECURITY_SBOM.md           # SBOM generation and scanning
  ├── SECURITY_SECRETS.md        # Secret scanning and rotation
  ├── SECURITY_THREAT_MODEL.md   # STRIDE analysis and risks
  └── SECURITY_AUDIT_LOG.md      # Audit trail of security reviews
```

### Security Contact

README.md must include:

```markdown
## Security

For security vulnerabilities, please email security@quantfidential.com
or report via GitHub Security Advisories.

See [SECURITY.md](docs/SECURITY.md) for our security policy.
```

---

## Testing Requirements

### Security Test Coverage

Every component must have:
- **Unit tests**: Input validation, encoding, error handling
- **Integration tests**: Authentication, authorization, session management
- **Behavior tests**: Security headers, rate limiting, CORS
- **Fuzzing tests**: Malformed inputs, edge cases
- **Penetration tests**: (Production-like environments only)

### Test Categories

```python
# Example: Python security tests
tests/
  ├── security/
  │   ├── test_authentication.py     # Auth bypass attempts
  │   ├── test_authorization.py      # Privilege escalation
  │   ├── test_injection.py          # SQL/command injection
  │   ├── test_xss.py                # Cross-site scripting
  │   ├── test_headers.py            # Security headers
  │   └── test_rate_limiting.py      # DDoS protection
```

---

## Audit & Compliance

### Regulatory Requirements

This framework satisfies:
- **SOC 2 Type II**: Security controls and monitoring
- **GDPR**: Data protection and privacy
- **PCI DSS**: Payment card data security (if applicable)
- **HIPAA**: Healthcare data security (if applicable)

### Evidence Collection

All security artifacts are:
- Stored in CI/CD artifacts (90-day retention minimum)
- Downloadable via GitHub Actions
- Indexed in `SECURITY_AUDIT_LOG.md`
- Versioned with each release

### Audit Trail

Every security decision must be documented:
- **What**: What was the finding?
- **Why**: Why is it a risk?
- **How**: How was it mitigated or accepted?
- **When**: Timestamp of decision
- **Who**: Decision maker (CODEOWNERS)

---

## Multi-Component Coordination

For the Trading Ecosystem, security spans 9 repositories:

### Shared Security Patterns

1. **Secrets Management**: Vault/AWS Secrets Manager (never in git)
2. **Authentication**: mTLS for service-to-service, JWT for external APIs
3. **Network Security**: Allowlists for outbound calls, network policies
4. **Audit Logging**: Centralized logging with correlation IDs
5. **Encryption**: TLS 1.3+ in transit, AES-256 at rest

### Cross-Component Security

- **Protobuf Schemas**: Schema validation prevents malformed messages
- **API Gateway**: Centralized auth, rate limiting, WAF
- **Service Mesh**: mTLS, traffic encryption, circuit breaking
- **Monitoring**: Security events in OpenTelemetry traces

---

## Getting Started

### New Repository Checklist

When creating a new repository:

1. **Copy Security Templates**
   ```bash
   cp -r project-plan/.github/workflows/security-* .github/workflows/
   cp project-plan/docs/SECURITY_*.md docs/
   ```

2. **Configure Language-Specific Tools**
   - See `.claude/.claude_security_<language>.md`
   - Install pre-commit hooks
   - Add CODEOWNERS

3. **Run Initial Security Scan**
   ```bash
   # SBOM
   syft dir:. -o json=sbom.json
   grype sbom:sbom.json

   # Secrets
   gitleaks detect --no-banner

   # SAST (example for Python)
   bandit -r . -f json -o bandit-report.json
   ```

4. **Document Threats**
   - Create `SECURITY_THREAT_MODEL.md`
   - Perform STRIDE analysis
   - Map to OWASP Top 10

5. **Add Security Tests**
   - Create `tests/security/` directory
   - Add authentication tests
   - Add input validation tests

6. **Update CI/CD**
   - Enable branch protection
   - Require security checks
   - Add dependency review

---

## Continuous Improvement

Security is never "done." We continuously:

1. **Monitor**: CVE feeds, security advisories, threat intelligence
2. **Update**: Dependencies, tools, configurations
3. **Test**: Regular penetration tests, chaos engineering
4. **Train**: Team security awareness, secure coding practices
5. **Review**: Quarterly security audits, threat model updates

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OSSF Best Practices](https://bestpractices.coreinfrastructure.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [STRIDE Threat Modeling](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)

---

## Ownership

- **Framework Owner**: Security Team / CISO
- **Implementation**: All Engineering Teams
- **Review Cadence**: Quarterly
- **Next Review**: 2026-01-03

**Questions?** Contact security@quantfidential.com or file an issue in `project-plan` repository.
