# Trading Ecosystem Epics

```yaml
epics:
  - id: epic-TSE-0001
    title: Foundation Services & Infrastructure
    goal: Establish minimal viable services with clean architecture, Docker deployment, and BDD testing to enable rapid future development
    status: In Progress (Infrastructure Foundation Phase: 4/4 completed)
    repos:
      # Core Services
      - protobuf-schemas
      - market-data-simulator-go
      - exchange-simulator-go
      - custodian-simulator-go
      - audit-correlator-go
      - risk-monitor-py
      - trading-system-engine-py
      - test-coordinator-py
      - orchestrator-docker
      - project-plan
      # Data Adapters (Clean Architecture)
      - market-data-adapter-go
      - exchange-data-adapter-go
      - custodian-data-adapter-go
      - audit-data-adapter-go
      - risk-data-adapter-py
      - trading-data-adapter-py
      - test-coordination-adapter-py
    labels:
      - foundation
      - infrastructure
      - microservices
      - docker
      - grpc
      - bdd
      - clean-architecture
      - observability
      - chaos-engineering
      - risk-monitoring
      - trading-simulation
      - data-adapters
      - domain-driven-design

  - id: epic-TSE-0003
    title: Data Adapter Foundation
    goal: Create domain-driven data persistence adapters following Clean Architecture principles
    status: Completed (TSE-0003.0)
    repos:
      - market-data-adapter-go
      - exchange-data-adapter-go
      - custodian-data-adapter-go
      - audit-data-adapter-go
      - risk-data-adapter-py
      - trading-data-adapter-py
      - test-coordination-adapter-py
      - project-plan
    labels:
      - data-architecture
      - clean-architecture
      - domain-driven-design
      - postgresql
      - redis
      - data-adapters
```