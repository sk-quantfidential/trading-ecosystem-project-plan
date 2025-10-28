# Solution Components

## Overview
**Solution Name**: Trading Ecosystem
**Architecture Style**: Microservices
**Component Count**: 10

## Core Services

### audit-correlator-go
- **Repository**: ./audit-correlator-go
- **Purpose**: Correlates and processes audit trails across the trading ecosystem
- **Tech Stack**: Go
- **Epic Participation**: TBD
- **Status**: Active

### custodian-simulator-go
- **Repository**: ./custodian-simulator-go
- **Purpose**: Simulates custodian services for testing and development
- **Tech Stack**: Go
- **Epic Participation**: TBD
- **Status**: Active

### exchange-simulator-go
- **Repository**: ./exchange-simulator-go
- **Purpose**: Simulates exchange connectivity and order execution
- **Tech Stack**: Go
- **Epic Participation**: TBD
- **Status**: Active

### market-data-simulator-go
- **Repository**: ./market-data-simulator-go
- **Purpose**: Generates and distributes simulated market data feeds
- **Tech Stack**: Go
- **Epic Participation**: TBD
- **Status**: Active

### project-plan
- **Repository**: ./project-plan
- **Purpose**: Central documentation, configuration, and project coordination
- **Tech Stack**: Documentation
- **Epic Participation**: All epics
- **Status**: Active

### protobuf-schemas
- **Repository**: ./protobuf-schemas
- **Purpose**: Shared protocol buffer schemas for inter-service communication
- **Tech Stack**: Protocol Buffers
- **Epic Participation**: All epics requiring API contracts
- **Status**: Active

### risk-monitor-py
- **Repository**: ./risk-monitor-py
- **Purpose**: Real-time risk monitoring and alert system
- **Tech Stack**: Python
- **Epic Participation**: TBD
- **Status**: Active

### test-coordinator-go
- **Repository**: ./test-coordinator-go
- **Purpose**: Coordinates integration testing across multiple services
- **Tech Stack**: Go
- **Epic Participation**: Testing and QA epics
- **Status**: Active

### trading-system-engine-py
- **Repository**: ./trading-system-engine-py
- **Purpose**: Core trading engine handling order management and execution
- **Tech Stack**: Python
- **Epic Participation**: TBD
- **Status**: Active

### simulator-ui-js
- **Repository**: ./simulator-ui-js
- **Purpose**: Web-based UI for visualizing network topology and controlling chaos scenarios
- **Tech Stack**: TypeScript, React, Next.js, D3.js, gRPC-Web
- **Epic Participation**: TSE-0002 (Network Topology Visualization)
- **Status**: Active

## Integration Map

### Service Communication
```
Market Data Simulator → Trading System Engine
                    ↓
Exchange Simulator ← Trading System Engine → Risk Monitor
                    ↓                           ↓
Custodian Simulator ← Trading System Engine    Audit Correlator
                    ↓
Test Coordinator (orchestrates all services)
```

### API Contracts
- **Protocol Definitions**: See protobuf-schemas repository
- **Internal APIs**: Protocol buffer based communication
- **Events**: Real-time messaging between services

## Development Workflow

### Git Repositories
All components are separate git repositories within the trading-ecosystem directory structure.

### Configuration Management
- **Shared Configuration**: project-plan/.claude/ directory
- **Component Configuration**: Individual .claude/ directories (if needed)
- **Central Planning**: project-plan/TODO-MASTER.md for cross-component coordination

## Technology Stack Summary

- **Go Services**: audit-correlator, custodian-simulator, exchange-simulator, market-data-simulator, test-coordinator
- **Python Services**: risk-monitor, trading-system-engine
- **Shared Schemas**: protobuf-schemas for all inter-service communication
- **Coordination**: project-plan for documentation and planning