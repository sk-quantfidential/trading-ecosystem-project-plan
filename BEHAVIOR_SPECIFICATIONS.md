# Behavior-Driven Specifications

## Scenario: Normal Trading Flow
**Given** strategy engine has $10k USD balance
**When** it places a market buy order for 0.1 BTC
**Then** exchange should fill order at current market price
**And** risk monitor should update position tracking
**And** audit correlator should record complete transaction flow

## Scenario: Custodian Settlement Failure
**Given** exchange has positive P&L to settle
**When** custodian chaos API is triggered for settlement delay
**Then** settlement should be delayed by configured duration
**And** risk monitor should detect settlement timeout
**And** audit correlator should correlate failure injection with risk alert