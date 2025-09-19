# Observability Specifications

## Metrics Taxonomy
### Risk Monitor Metrics
- `risk_position_size{asset, venue}`: Current position sizes
- `risk_pnl_drawdown{strategy}`: Portfolio drawdown tracking
- `risk_alert_generated{severity, type}`: Risk alert events

### Audit Correlator Metrics  
- `scenario_validation{scenario, result}`: Test scenario outcomes
- `causation_analysis{trigger, effect, correlation}`: Event correlation scores