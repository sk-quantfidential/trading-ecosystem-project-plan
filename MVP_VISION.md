# Enhanced Trading Ecosystem MVP - Separated Audit Architecture

## Core Architecture Philosophy
A distributed trading ecosystem with **clean separation of concerns**: (1) **Production-Like Risk Monitor** that operates exactly like a real risk system and emits its own compliance signals, and (2) **Independent Audit Correlator** that ingests all system telemetry including risk monitor outputs to provide complete ecosystem validation and correlation analysis.

## Refined Observability Architecture

### **Clean Separation Benefits**
- **Risk Monitor purity**: Operates exactly like production with no audit contamination
- **Independent validation**: Audit Correlator can validate risk monitor effectiveness objectively
- **Signal clarity**: Risk compliance becomes another data stream to correlate
- **Production migration**: Risk Monitor transfers to production with zero changes

## Enhanced Component Architecture

### **1. Risk Monitor** (Python) - **Pure Production Design**
**Single Interface**: Only accesses production-equivalent APIs (exchanges, custodians, market data)

**Core Functions**:
- Monitors position limits, P&L drawdown, delta exposure
- Generates compliance alerts and risk signals
- **Emits own telemetry**: Risk compliance status, alert timing, threshold breaches
- Operates in complete isolation from simulation infrastructure

**Prometheus Metrics Emitted**:
```yaml
# Risk Monitor's own signals
risk_compliance_status{mandate="position_limit", asset="BTC"} 
risk_alert_generated{severity="high", type="drawdown_breach"}
risk_monitor_latency{data_source="exchange_api"}
risk_threshold_breach{limit="delta_exposure", current_value="150000"}
```

**Container**: `risk-monitor` - Single production-like container

### **2. Audit Correlator** (Go) - **Complete System Intelligence**
**Purpose**: Independent validation and correlation engine that ingests ALL system signals

**Data Ingestion Sources**:
- **Risk Monitor signals**: Compliance status, alerts, threshold breaches
- **OpenTelemetry traces**: All service interactions and timing
- **Scenario events**: Chaos injection timeline from Test Coordinator  
- **Service metrics**: Performance, health, state changes from all components
- **Market events**: Price movements, order flows, settlement activities

**Core Functions**:
- **Correlation Analysis**: Links scenario events → market changes → risk alerts
- **Validation Engine**: Proves risk monitor detected scenarios within SLA
- **Timeline Reconstruction**: Complete causal chain analysis
- **Coverage Tracking**: Ensures all risk scenarios are properly validated
- **Ground Truth Generation**: Creates validated datasets for risk system tuning

**Prometheus Metrics Generated**:
```yaml
# Audit validation metrics
scenario_risk_detection{scenario="stablecoin_depeg", detected="true", latency_ms="15000"}
risk_alert_accuracy{scenario="market_crash", alert_type="drawdown", accuracy="true_positive"}
system_causation_chain{trigger="custodian_failure", effect="risk_alert", correlation="0.95"}
audit_coverage{risk_scenario="portfolio_concentration", tested="true", validated="true"}
```

### **3. Enhanced Service Components**

#### **Exchange Simulator** (Go)
**Represents**: Real crypto exchanges (Binance, Coinbase Pro, etc.)
**Core Function**: Order matching engine with realistic latency, slippage, and liquidity constraints
**Key Behaviors**:
- Maintains order books for BTC/USD, USDT/BTC, USDT/ETH, ETH/USD, BTC/ETH
- Processes market/limit orders with realistic fills
- Manages sub-accounts and balances for trading entities
- **Chaos Backdoors**: Inject latency, reject orders, manipulate spreads, simulate downtime

**Production API**: Standard trading/custody APIs (what risk systems normally see)
**Audit API**: Internal state, chaos events, failure injection timeline
**Metrics**: Order processing latency, settlement delays, failure injection events

#### **Custodian Simulator** (Go)
**Represents**: Prime brokers and custody providers (BitGo, Coinbase Custody, etc.)
**Core Function**: Settlement and asset custody with multi-day settlement cycles
**Key Behaviors**:
- Manages master custody accounts across multiple assets
- Handles P&L settlement from exchanges (T+0 to T+2)
- Processes withdrawal/deposit instructions
- **Chaos Backdoors**: Delay settlements, reject transfers, go offline, partial settlements

**Production API**: Standard trading/custody APIs (what risk systems normally see)
**Audit API**: Internal state, chaos events, failure injection timeline
**Metrics**: Order processing latency, settlement delays, failure injection events

#### **Market Data Simulator** (Go)
**Represents**: Market data providers (CoinMetrics, CMC, exchange feeds)
**Core Function**: Real-time and historical price feeds with configurable update frequencies
**Key Behaviors**:
- Publishes tick-by-tick price updates for all trading pairs
- Maintains price history and volatility calculations
- Detects and reports price divergences across pairs
- **Connects to real data sources**: Ingests from CoinGecko, CMC, exchange websockets
- **Intelligent chaos injection**: Controlled price manipulation while maintaining realistic behavior
- **Chaos Backdoors**: Inject price shocks, create divergences, simulate stale data

**Production API**: Standard price feeds, just like real market data providers
**Audit API**: Exposes chaos injection status and price manipulation timeline
**Metrics**: Price volatility, feed latency, manipulation events

#### **Trading Strategy Engine** (Python)
**Represents**: Quantitative trading algorithms and portfolio managers
**Core Function**: Executes systematic trading strategies with position management
**Key Behaviors**:
- Runs configurable trading algorithms (arbitrage, momentum, mean reversion)
- Manages position sizing and portfolio allocation
- Responds to market signals and risk constraints
- **Chaos via Strategy Scripts**: Deliberately misbehaving strategy implementations
  - `RunawayStrategy`: Massive order spam
  - `RiskIgnorantStrategy`: Ignores risk limits
  - `VolatilityAmplifierStrategy`: Creates market impact
  - `CorrelationBreakerStrategy`: Breaks asset correlations
  - `SlowLeakStrategy`: Gradual performance degradation

**Production API**: Standard strategy management and performance APIs
**Audit API**: Strategy execution logs, chaos strategy status
**Metrics**: Strategy performance, risk breaches, chaos strategy activity

### **4. Test Coordinator** (Python)
**Purpose**: Scenario orchestration and chaos engineering platform
**Enhanced Functionality**:
- **Scenario Validation**: Automated assertions that risk monitor detected expected events
- **Timeline Reconstruction**: Correlates scenario events with risk alert timing
- **Coverage Analysis**: Tracks which risk scenarios have been properly validated
- **YAML-based Scenarios**: Declarative scenario definitions for repeatable testing

### **5. Telemetry Collector** (Go)
**Purpose**: Aggregates distributed traces and reconstructs system-wide event timelines
**Enhanced Functionality**:
- Collects OpenTelemetry traces from all services
- Reconstructs causal relationships between service interactions
- Provides real-time event stream for monitoring
- Generates system behavior analytics

## Shared Infrastructure

### **State Store** (Redis/PostgreSQL)
- Account balances across exchanges and custodians
- Current positions and order status
- Configuration and reference data

### **Configuration Service**
- Service discovery and endpoint configuration
- Trading pair definitions and contract specifications
- Risk limits and operational parameters

## Key Interaction Flows

### **Scenario Execution & Validation Flow**
1. **Test Coordinator** → Injects chaos scenario (e.g., stablecoin depeg)
2. **Audit Layer** → Records exact timing and parameters of injection  
3. **Market Data Simulator** → Gradually adjusts USDT/USD price (production-visible)
4. **Risk Monitor (Prod)** → Detects price divergence, triggers alert
5. **Audit Correlator** → Validates alert timing against injection timeline
6. **Grafana Dashboard** → Shows causation chain and validates detection SLA

### **Signal Flow Architecture**
```
┌─────────────────┐     ┌──────────────────┐    ┌─────────────────┐
│   Risk Monitor  │───▶│ Prometheus/OTEL  │◀───│ Audit Correlator│
│ (Pure Prod)     │     │  (Metrics Bus)   │    │ (Full Context)  │
└─────────────────┘     └──────────────────┘    └─────────────────┘
         │                       ▲                       ▲
         │                       │                       │
         ▼                       │                       │
┌──────────────────┐             │              ┌─────────────────┐
│Exchange/Custodian│─────────────┘              │ All Other       │
│APIs (Prod-like)  │                            │ Services        │
└──────────────────┘                            └─────────────────┘
```

### **Dual Dashboard Experience**
```
Production Risk View:          Audit/Validation View:
┌──────────────────────┐       ┌──────────────────────┐
│ ⚠️  USDT Depeg Alert│  ←──→ │ ✅ Scenario injected │
│ Time: 14:23:45       │       │ Time: 14:23:30       │  
│ Severity: HIGH       │       │ Detection: 15s SLA   │
│ Delta: +$50k exposure│       │ Status: PASS ✓      │
└──────────────────────┘       └──────────────────────┘
```

## Enhanced Grafana Dashboard Strategy

### **Dashboard Separation**

**A. Production Risk Dashboard** (Risk Monitor View)
- What a real risk manager sees in production
- Position monitoring, P&L tracking, compliance status
- **No scenario context** - pure production experience
- Data source: Risk Monitor metrics only

**B. Audit Validation Dashboard** (Audit Correlator View)  
- Complete system behavior analysis
- Scenario injection → Risk detection correlation
- Timeline analysis with causation chains
- Coverage tracking and validation results
- Data source: Audit Correlator comprehensive metrics

**C. Executive Correlation Dashboard** (Combined View)
- Side-by-side: Risk alerts vs. scenario timeline
- System health across all components
- Scenario success/failure tracking
- Risk system effectiveness scoring

## Container Architecture

### **Clean Separation in Docker Compose**
```yaml
services:
  # Pure production risk monitoring
  risk-monitor:
    image: risk-monitor:latest
    networks:
      - production-apis  # Only connects to exchange/custodian/market-data
    # NO access to audit network or scenario coordination
    
  # Complete system audit and validation  
  audit-correlator:
    image: audit-correlator:latest
    networks:
      - production-apis  # Can see what risk monitor sees
      - audit-network    # Plus complete system visibility
    volumes:
      - scenario-configs:/scenarios

  # Market data with real feeds and chaos injection
  market-data-simulator:
    image: market-data-simulator:latest
    networks:
      - production-apis
      - audit-network
    environment:
      - COINGECKO_API_KEY=${COINGECKO_API_KEY}
      - CHAOS_ENABLED=true
    
  # Trading engine with chaos strategies
  trading-strategy-engine:
    image: trading-engine:latest
    networks:
      - production-apis
      - audit-network
    volumes:
      - ./strategies:/app/strategies
      - ./strategies/chaos:/app/strategies/chaos
```

## Failure Scenarios to Model

### **1. Strategy Malfunction**
- **RunawayStrategy** sends massive orders, overwhelming exchange liquidity
- **RiskIgnorantStrategy** continues trading despite risk breaches
- **VolatilityAmplifierStrategy** amplifies market volatility through momentum chasing

### **2. Price Divergence**
- **Market Data Simulator** creates controlled spot vs futures price divergence
- **CorrelationBreakerStrategy** trades against normal asset correlations

### **3. Market Crash**
- **Market Data Simulator** orchestrates coordinated 15% price drop across all assets
- **Trading strategies** respond to volatility with increased position taking

### **4. Stablecoin Depeg**
- **Market Data Simulator** slowly depegs USDT from USD over 36-hour period
- **Risk Monitor** must detect and alert on increasing stablecoin exposure risk

### **5. Settlement Failure**
- **Custodian Simulator** fails to process exchange P&L settlements
- **Risk Monitor** must detect and alert on unsettled exposure accumulation

## Enhanced Benefits

### **Risk System Validation**
- **Proves** the risk monitor detects scenarios within acceptable timeframes
- **Validates** alert thresholds are properly calibrated  
- **Documents** risk system behavior for compliance/audit purposes
- **Tests real constraints**: API timeouts, data staleness, external dependencies

### **Scenario Testing Confidence**
- **Automated assertions** ensure scenarios run as intended
- **Timeline analysis** shows cause-and-effect relationships
- **Coverage tracking** ensures all risk scenarios are properly tested
- **Realistic chaos**: Uses real market data with controlled manipulation

### **Production Readiness**  
- **Risk monitor operates exactly like production** (limited visibility)
- **Audit layer can be removed** when moving to real trading
- **Metrics and dashboards** transfer directly to production monitoring
- **Strategy chaos testing** validates algorithmic failure handling

### **Regulatory & Compliance**
- **Complete audit trail** of risk system testing and validation
- **Documented evidence** that risk controls work under stress scenarios
- **Reproducible test results** for regulatory review
- **Independent validation** through separated audit architecture

## Prometheus + Grafana Integration

### **Multi-Data Source Dashboards**
- **Risk metrics** from Risk Monitor (position limits, P&L, alerts)
- **Scenario metrics** from Test Coordinator (chaos injection events)
- **Correlation metrics** from Audit Correlator (cause-effect relationships)
- **System metrics** from all services (performance, health, state)

### **PromQL Correlation Queries**
```promql
# Risk alert detection latency
(risk_alert_generated - on() scenario_event_injected) 
  by (scenario_type, alert_type)

# Scenario coverage tracking
sum(audit_coverage{tested="true", validated="true"}) 
  by (risk_scenario) / 
  sum(audit_coverage) by (risk_scenario)

# Risk system effectiveness
rate(risk_alert_generated[5m]) / 
  rate(scenario_event_injected[5m])
```

### **Alerting Capabilities**
- **Risk breach alerts** from Risk Monitor
- **Scenario validation failures** from Audit Correlator
- **System health alerts** from all components
- **SLA violations** for risk detection timing

This enhanced architecture provides the separation needed to validate risk monitoring systems while maintaining comprehensive auditability - exactly what you'd need to prove your risk controls work before deploying capital. The integration of real market data with controlled chaos injection creates a unique testing environment that bridges the gap between pure simulation and production systems.