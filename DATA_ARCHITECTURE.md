# Trading Ecosystem Data Architecture

**Document Version**: 1.0
**Created**: 2025-09-17
**Epic**: TSE-0001 Foundation Services & Infrastructure
**Purpose**: Define data persistence requirements and adapter repositories for MVP

## Executive Summary

This document defines the data persistence architecture for the Trading Ecosystem MVP. Following Clean Architecture principles, each component will have its own dedicated data adapter with domain-specific APIs, while sharing a single Redis instance and single PostgreSQL instance for all data persistence needs.

## Architecture Principles

### Clean Architecture Compliance
- **Domain-Specific Adapters**: Each component has a tailored data adapter API
- **No Shared Tables**: Components never directly access each other's data
- **Domain Concepts**: APIs expose business concepts, not database implementation details
- **Persistence Abstraction**: Business logic is isolated from persistence concerns

### Shared Infrastructure (MVP Simplification)
- **Single Redis Instance**: Shared for caching, session data, and real-time operations
- **Single PostgreSQL Instance**: Shared for persistent data storage
- **Logical Separation**: Schema namespacing and access patterns maintain component isolation

## Data Persistence Requirements Analysis

### TSE-0001.4: Market Data Foundation (market-data-simulator-go)

**Data Requirements**:
- Real-time price feeds (BTC/USD, ETH/USD, USDT pairs)
- Historical OHLCV data with time-series optimization
- Market microstructure (bid/ask spreads, volumes)
- Scenario definitions and chaos injection configurations
- Price manipulation state and correlation tracking

**Storage Patterns**:
- **Redis**: Real-time prices (ring buffers), active scenario state
- **PostgreSQL**: Historical OHLCV, scenario definitions, market metadata

**Required Adapter**: `market-data-adapter-go`

### TSE-0001.5a/5b: Exchange Services (exchange-simulator-go)

**Data Requirements**:
- Account management with sub-account isolation
- Multi-asset balance tracking (BTC, ETH, USD, USDT)
- Order lifecycle management and matching
- Trade history and transaction audit trails
- Order books with high-frequency updates

**Storage Patterns**:
- **Redis**: Active order books, real-time balances, session data
- **PostgreSQL**: Account records, trade history, audit trails, order archives

**Required Adapter**: `exchange-data-adapter-go`

### TSE-0001.6: Custodian Foundation (custodian-simulator-go)

**Data Requirements**:
- Master account management with segregated client assets
- Multi-day settlement cycles (T+0 to T+3)
- Transfer instructions and approval workflows
- Multi-signature security simulation state
- Cross-venue reconciliation data

**Storage Patterns**:
- **Redis**: Pending settlements, approval workflow state
- **PostgreSQL**: Master accounts, settlement history, audit trails, compliance records

**Required Adapter**: `custodian-data-adapter-go`

### TSE-0001.7a/7b: Risk Monitor (risk-monitor-py)

**Data Requirements**:
- Position aggregation across multiple venues
- Real-time P&L calculations and mark-to-market
- Risk limit definitions and breach tracking
- Alert history and escalation workflows
- Performance metrics and compliance reporting

**Storage Patterns**:
- **Redis**: Real-time positions, active alerts, calculation cache
- **PostgreSQL**: Risk limits configuration, alert history, compliance reports

**Required Adapter**: `risk-data-adapter-py`

### TSE-0001.8: Trading Engine (trading-system-engine-py)

**Data Requirements**:
- Strategy definitions and configuration
- Portfolio positions and P&L tracking
- Order management and execution history
- Performance attribution and analytics
- Backtesting data and results

**Storage Patterns**:
- **Redis**: Active strategy state, real-time portfolio data
- **PostgreSQL**: Strategy definitions, execution history, performance analytics

**Required Adapter**: `trading-data-adapter-py`

### TSE-0001.9: Test Coordinator (test-coordinator-py)

**Data Requirements**:
- Scenario definitions and templates
- Execution logs and validation results
- System state snapshots during chaos testing
- Test reports and analytics
- Scenario scheduling and dependencies

**Storage Patterns**:
- **Redis**: Active scenario state, execution locks
- **PostgreSQL**: Scenario definitions, execution logs, test reports

**Required Adapter**: `test-coordinator-data-adapter-py`

### TSE-0001.10: Audit Correlator (audit-correlator-go)

**Data Requirements**:
- Event ingestion from all services (telemetry, traces, logs)
- Causal chain reconstruction and correlation data
- Timeline analytics and performance metrics
- Audit trail generation for regulatory compliance
- Event storage with high-volume time-series optimization

**Storage Patterns**:
- **Redis**: Real-time event processing, correlation cache
- **PostgreSQL**: Event archives, audit trails, correlation results, analytics

**Required Adapter**: `audit-data-adapter-go`

## Required Data Adapter Repositories

Based on the analysis, the following new repositories are required:

### Go Data Adapters
1. **`market-data-adapter-go`**
   - Component: market-data-simulator-go
   - Domain: Market data, pricing, scenarios
   - Key APIs: Price feeds, historical data, scenario management

2. **`exchange-data-adapter-go`**
   - Component: exchange-simulator-go
   - Domain: Trading, accounts, orders
   - Key APIs: Account management, order lifecycle, trade execution

3. **`custodian-data-adapter-go`**
   - Component: custodian-simulator-go
   - Domain: Custody, settlements, transfers
   - Key APIs: Account custody, settlement processing, reconciliation

4. **`audit-data-adapter-go`**
   - Component: audit-correlator-go
   - Domain: Events, correlation, audit trails
   - Key APIs: Event ingestion, correlation analysis, audit reporting

### Python Data Adapters
5. **`risk-data-adapter-py`**
   - Component: risk-monitor-py
   - Domain: Risk management, compliance, alerting
   - Key APIs: Position aggregation, risk monitoring, alert management

6. **`trading-data-adapter-py`**
   - Component: trading-system-engine-py
   - Domain: Strategy execution, portfolio management
   - Key APIs: Strategy management, portfolio tracking, performance analytics

7. **`test-coordinator-data-adapter-py`**
   - Component: test-coordinator-py
   - Domain: Chaos testing, scenario orchestration
   - Key APIs: Scenario management, execution tracking, validation

## Database Schema Organization

### PostgreSQL Schema Namespacing
Each adapter will have its own schema namespace to maintain logical separation:

```sql
-- Market data domain
CREATE SCHEMA market_data;

-- Exchange domain
CREATE SCHEMA exchange;

-- Custodian domain
CREATE SCHEMA custodian;

-- Risk management domain
CREATE SCHEMA risk;

-- Trading domain
CREATE SCHEMA trading;

-- Test coordination domain
CREATE SCHEMA test_coordination;

-- Audit domain
CREATE SCHEMA audit;
```

### Redis Key Namespacing
Each adapter will use consistent key prefixes to avoid collisions:

```
market:*      # Market data adapter keys
exchange:*    # Exchange adapter keys
custodian:*   # Custodian adapter keys
risk:*        # Risk adapter keys
trading:*     # Trading adapter keys
test:*        # Test coordination adapter keys
audit:*       # Audit adapter keys
```

## API Design Principles

### Domain-Driven APIs
Each adapter exposes business domain concepts, not database artifacts:

**Good Examples**:
- `GetAccountPortfolio(accountID) -> Portfolio`
- `ProcessSettlement(settlement) -> SettlementResult`
- `CalculateRiskMetrics(positions) -> RiskSummary`

**Avoid**:
- `GetAccountTable() -> []AccountRow`
- `UpdatePositionRecord(id, fields) -> bool`
- `QueryTradeHistory(sql) -> ResultSet`

### Consistency Patterns
- **Read-Heavy Operations**: Redis caching with PostgreSQL fallback
- **Write-Heavy Operations**: Write-through to PostgreSQL with Redis invalidation
- **Real-Time Data**: Redis primary with PostgreSQL archival
- **Audit Data**: PostgreSQL primary with Redis for active queries

## Technology Standards

### Database Naming Conventions
- **PostgreSQL**: snake_case for tables, columns, functions
- **Redis**: kebab-case with namespace prefixes
- **Go adapters**: PascalCase for public APIs, camelCase for internal
- **Python adapters**: snake_case for all functions and variables

### Connection Management
- **Connection Pooling**: Each adapter manages its own connection pools
- **Health Checks**: All adapters expose health check endpoints
- **Circuit Breakers**: Automatic failure handling and degradation
- **Observability**: Prometheus metrics and OpenTelemetry tracing

## Migration and Deployment Strategy

### Repository Creation Order
1. Create all adapter repositories with basic structure
2. Implement basic health checks and connection management
3. Develop domain-specific APIs iteratively
4. Add comprehensive testing and observability

### Database Initialization
1. Single PostgreSQL instance with all schemas
2. Single Redis instance with namespace separation
3. Automated schema migration scripts per adapter
4. Development seed data for testing

### Integration Testing
1. Adapter-level unit tests with test containers
2. Cross-adapter integration tests with shared infrastructure
3. End-to-end scenario tests using test-coordinator
4. Performance testing under realistic load

## Next Steps

1. **Repository Creation**: Create the 7 identified data adapter repositories
2. **Component Configuration**: Add `.claude/` configuration for each adapter
3. **Schema Design**: Detailed schema design per adapter (post-repo creation)
4. **API Definition**: Define domain-specific APIs per adapter
5. **Implementation**: Implement adapters with comprehensive testing

## Appendix: Component Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Shared Infrastructure                       │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │     Redis Cache     │    │        PostgreSQL DB            │ │
│  │                     │    │ ┌─────────────────────────────┐ │ │
│  │ • Real-time data    │    │ │     Schema Namespaces       │ │ │
│  │ • Session state     │    │ │ • market_data               │ │ │
│  │ • Cache layers      │    │ │ • exchange                  │ │ │
│  │ • Event queues      │    │ │ • custodian                 │ │ │
│  └─────────────────────┘    │ │ • risk                      │ │ │
│                             │ │ • trading                   │ │ │
│                             │ │ • test_coordination         │ │ │
│                             │ │ • audit                     │ │ │
│                             │ └─────────────────────────────┘ │ │
│                             └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                      │
    ┌─────────────────────────────────┼─────────────────────────────────┐
    │                                 │                                 │
    ▼                                 ▼                                 ▼
┌─────────────┐               ┌─────────────┐                   ┌─────────────┐
│Go Adapters  │               │Go Adapters  │                   │Py Adapters  │
│             │               │             │                   │             │
│market-data  │               │exchange-data│                   │risk-data    │
│custodian    │               │audit-data   │                   │trading-data │
│             │               │             │                   │test-coord   │
└─────────────┘               └─────────────┘                   └─────────────┘
    │                                 │                                 │
    ▼                                 ▼                                 ▼
┌─────────────┐               ┌─────────────┐                   ┌─────────────┐
│Market Data  │               │Exchange     │                   │Risk Monitor │
│Simulator    │               │Simulator    │                   │Trading Eng  │
│Custodian    │               │Audit        │                   │Test Coord   │
│Simulator    │               │Correlator   │                   │             │
└─────────────┘               └─────────────┘                   └─────────────┘
```

---

**Document Approval**: Ready for repository creation and detailed implementation planning.