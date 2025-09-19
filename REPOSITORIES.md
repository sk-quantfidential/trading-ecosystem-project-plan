# Solution Components

## Overview
**Solution Name**: Trading Ecosystem
**Architecture Style**: Clean Architecture with Microservices
**Component Count**: 16
**Project Type**: Multi-component
**Epic Management**: Centralized in project-plan repository

## Core Services

### audit-correlator-go
- **Repository**: ./audit-correlator-go
- **Purpose**: Event correlation and system behavior analysis for regulatory compliance
- **Tech Stack**: Go
- **Epic Participation**: TSE-0001.10 (Audit Infrastructure), TSE-0001.12c (Audit Integration)
- **Status**: Active
- **Data Persistence**: audit-data-adapter-go

### custodian-simulator-go
- **Repository**: ./custodian-simulator-go
- **Purpose**: Asset custody and settlement simulation with multi-asset support
- **Tech Stack**: Go
- **Epic Participation**: TSE-0001.6 (Custodian Foundation)
- **Status**: Active
- **Data Persistence**: custodian-data-adapter-go

### exchange-simulator-go
- **Repository**: ./exchange-simulator-go
- **Purpose**: Exchange connectivity simulation with order matching and account management
- **Tech Stack**: Go
- **Epic Participation**: TSE-0001.5a (Exchange Account Management), TSE-0001.5b (Exchange Order Processing)
- **Status**: Active
- **Data Persistence**: exchange-data-adapter-go

### market-data-simulator-go
- **Repository**: ./market-data-simulator-go
- **Purpose**: Market data generation and distribution with chaos injection capabilities
- **Tech Stack**: Go
- **Epic Participation**: TSE-0001.4 (Market Data Foundation)
- **Status**: Active
- **Data Persistence**: market-data-adapter-go

### orchestrator-docker
- **Repository**: ./orchestrator-docker
- **Purpose**: Docker orchestration for building, starting, stopping and monitoring component health
- **Tech Stack**: Docker Compose, Shell Scripts
- **Epic Participation**: TSE-0001.3a (Core Infrastructure Setup)
- **Status**: Active

### project-plan
- **Repository**: ./project-plan
- **Purpose**: Central documentation, configuration, and multi-component project coordination
- **Tech Stack**: Markdown Documentation, Claude Configuration
- **Epic Participation**: All epics (coordination hub)
- **Status**: Active

### protobuf-schemas
- **Repository**: ./protobuf-schemas
- **Purpose**: Shared protocol buffer schemas and client library generation
- **Tech Stack**: Protocol Buffers, Go, Python
- **Epic Participation**: TSE-0001.2 (Protocol Buffer Integration), all service integration milestones
- **Status**: Active ✅ Completed TSE-0001.2

### risk-monitor-py
- **Repository**: ./risk-monitor-py
- **Purpose**: Real-time risk monitoring and alert system with production API integration
- **Tech Stack**: Python
- **Epic Participation**: TSE-0001.7a (Risk Monitor Data Collection), TSE-0001.7b (Risk Monitor Alert Generation)
- **Status**: Active
- **Data Persistence**: risk-data-adapter-py

### test-coordinator-py
- **Repository**: ./test-coordinator-py
- **Purpose**: Scenario orchestration and chaos testing framework coordination
- **Tech Stack**: Python
- **Epic Participation**: TSE-0001.9 (Test Coordination Framework), TSE-0001.12d (Chaos Testing Integration)
- **Status**: Active
- **Data Persistence**: test-coordination-adapter-py

### trading-system-engine-py
- **Repository**: ./trading-system-engine-py
- **Purpose**: Core trading engine with systematic trading strategies and portfolio management
- **Tech Stack**: Python
- **Epic Participation**: TSE-0001.8 (Trading Engine Foundation)
- **Status**: Active
- **Data Persistence**: trading-data-adapter-py

## Data Adapter Services

### audit-data-adapter-go
- **Repository**: ./audit-data-adapter-go
- **Purpose**: Data persistence adapter for audit correlator with event ingestion and correlation analysis
- **Tech Stack**: Go, PostgreSQL, Redis
- **Epic Participation**: TSE-0001.10 (Audit Infrastructure)
- **Status**: Active (Repository Created)
- **Serves**: audit-correlator-go
- **Schema Namespace**: audit

### custodian-data-adapter-go
- **Repository**: ./custodian-data-adapter-go
- **Purpose**: Data persistence adapter for custodian simulator with asset custody and settlement processing
- **Tech Stack**: Go, PostgreSQL, Redis
- **Epic Participation**: TSE-0001.6 (Custodian Foundation)
- **Status**: Active (Repository Created)
- **Serves**: custodian-simulator-go
- **Schema Namespace**: custodian

### exchange-data-adapter-go
- **Repository**: ./exchange-data-adapter-go
- **Purpose**: Data persistence adapter for exchange simulator with account management and order lifecycle
- **Tech Stack**: Go, PostgreSQL, Redis
- **Epic Participation**: TSE-0001.5a (Exchange Account Management), TSE-0001.5b (Exchange Order Processing)
- **Status**: Active (Repository Created)
- **Serves**: exchange-simulator-go
- **Schema Namespace**: exchange

### market-data-adapter-go
- **Repository**: ./market-data-adapter-go
- **Purpose**: Data persistence adapter for market data simulator with price feeds and scenario management
- **Tech Stack**: Go, PostgreSQL, Redis
- **Epic Participation**: TSE-0001.4 (Market Data Foundation)
- **Status**: Active (Repository Created)
- **Serves**: market-data-simulator-go
- **Schema Namespace**: market_data

### risk-data-adapter-py
- **Repository**: ./risk-data-adapter-py
- **Purpose**: Data persistence adapter for risk monitor with position aggregation and risk monitoring
- **Tech Stack**: Python, PostgreSQL, Redis
- **Epic Participation**: TSE-0001.7a (Risk Monitor Data Collection), TSE-0001.7b (Risk Monitor Alert Generation)
- **Status**: Active (Repository Created)
- **Serves**: risk-monitor-py
- **Schema Namespace**: risk

### test-coordination-adapter-py
- **Repository**: ./test-coordination-adapter-py
- **Purpose**: Data persistence adapter for test coordinator with scenario management and execution tracking
- **Tech Stack**: Python, PostgreSQL, Redis
- **Epic Participation**: TSE-0001.9 (Test Coordination Framework)
- **Status**: Active (Repository Created)
- **Serves**: test-coordinator-py
- **Schema Namespace**: test_coordination

### trading-data-adapter-py
- **Repository**: ./trading-data-adapter-py
- **Purpose**: Data persistence adapter for trading engine with strategy management and portfolio tracking
- **Tech Stack**: Python, PostgreSQL, Redis
- **Epic Participation**: TSE-0001.8 (Trading Engine Foundation)
- **Status**: Active (Repository Created)
- **Serves**: trading-system-engine-py
- **Schema Namespace**: trading

## Architecture Overview

### Clean Architecture Compliance
- **Domain-Specific Adapters**: Each component has a dedicated data adapter with tailored APIs
- **No Shared Tables**: Components never directly access each other's data
- **Domain Concepts**: APIs expose business concepts, not database implementation details
- **Persistence Abstraction**: Business logic isolated from persistence concerns

### Shared Infrastructure (MVP)
- **Single Redis Instance**: Shared for caching, session data, and real-time operations
- **Single PostgreSQL Instance**: Shared for persistent data storage
- **Logical Separation**: Schema namespacing and access patterns maintain component isolation

## Integration Map

### Service Communication Flow
```
Market Data Simulator → Market Data Adapter → Redis/PostgreSQL
                      ↓
                   gRPC/REST APIs
                      ↓
Trading Engine ← Trading Data Adapter ← Redis/PostgreSQL
     ↓
Exchange Simulator ← Exchange Data Adapter ← Redis/PostgreSQL
     ↓
Custodian Simulator ← Custodian Data Adapter ← Redis/PostgreSQL
     ↓
Risk Monitor ← Risk Data Adapter ← Redis/PostgreSQL
     ↓
Audit Correlator ← Audit Data Adapter ← Redis/PostgreSQL
     ↑
Test Coordinator ← Test Coordination Adapter ← Redis/PostgreSQL
```

### Data Architecture
- **Redis Key Namespacing**: `market:*`, `exchange:*`, `custodian:*`, `risk:*`, `trading:*`, `test:*`, `audit:*`
- **PostgreSQL Schema Separation**: `market_data`, `exchange`, `custodian`, `risk`, `trading`, `test_coordination`, `audit`
- **Consistency Patterns**: Redis caching with PostgreSQL persistence, write-through with invalidation

### API Contracts
- **Protocol Definitions**: protobuf-schemas repository
- **Inter-Service Communication**: gRPC with Protocol Buffers
- **Production APIs**: REST endpoints for external integration
- **Real-time Data**: gRPC streaming for market data and events

## Development Workflow

### Repository Structure
- **Multi-Component Project**: Each service is a separate git repository
- **Centralized Planning**: project-plan repository for epic coordination
- **Clean Separation**: No shared code between services (except protobuf schemas)

### Configuration Management
- **Shared Configuration**: project-plan/.claude/ directory for global settings
- **Component Configuration**: Individual .claude/ directories for service-specific settings
- **Epic Coordination**: TODO-MASTER.md tracks cross-component milestone progress
- **Data Architecture**: DATA_ARCHITECTURE.md defines persistence requirements and patterns

### Current Epic Progress
- **TSE-0001 Foundation Services & Infrastructure**: In Progress
- **Infrastructure Foundation Phase**: 4/4 milestones completed ✅
- **Core Services Phase**: 0/10 milestones completed
- **Next Milestone**: TSE-0001.3a (Core Infrastructure Setup)

## Technology Stack Summary

### Core Services
- **Go Services**: audit-correlator-go, custodian-simulator-go, exchange-simulator-go, market-data-simulator-go
- **Python Services**: risk-monitor-py, test-coordinator-py, trading-system-engine-py

### Data Adapters
- **Go Data Adapters**: audit-data-adapter-go, custodian-data-adapter-go, exchange-data-adapter-go, market-data-adapter-go
- **Python Data Adapters**: risk-data-adapter-py, test-coordination-adapter-py, trading-data-adapter-py

### Infrastructure
- **Communication**: protobuf-schemas for all inter-service contracts
- **Orchestration**: orchestrator-docker for deployment and health monitoring
- **Data Storage**: Single Redis + Single PostgreSQL with logical separation
- **Coordination**: project-plan for documentation, planning, and configuration

## Component Dependencies

### Infrastructure Foundation (Sequential)
TSE-0001.1a,1b,1c ✅ → TSE-0001.2 ✅ → TSE-0001.3a → TSE-0001.3b,3c

### Core Services (Parallel after 3b,3c)
- Market Data: TSE-0001.3b → TSE-0001.4
- Exchange: TSE-0001.3b → TSE-0001.5a → TSE-0001.5b
- Custodian: TSE-0001.3b + TSE-0001.5b → TSE-0001.6
- Risk Monitor: TSE-0001.3c + (TSE-0001.4,5b,6) → TSE-0001.7a → TSE-0001.7b
- Trading Engine: TSE-0001.3c + TSE-0001.4 + TSE-0001.5b → TSE-0001.8
- Test Coordination: TSE-0001.3c → TSE-0001.9
- Audit: TSE-0001.3b + TSE-0001.9 → TSE-0001.10

---

**Last Updated**: 2025-09-18
**Document Version**: 2.0 (Updated with data adapter repositories)
**Epic Context**: TSE-0001 Foundation Services & Infrastructure