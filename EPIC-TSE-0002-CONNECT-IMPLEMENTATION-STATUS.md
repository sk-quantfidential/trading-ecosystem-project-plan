# Epic TSE-0002: Connect Protocol Rollout - Implementation Status

## Executive Summary

**Original Plan**: Roll out Connect protocol to all three simulator services (exchange, market-data, custodian)

**Revised Scope**: Implement Connect protocol only for services with working gRPC implementations

**Status**: ✅ **Phase 1 Complete** - market-data-simulator-go has Connect protocol support

## Discovery Findings

During analysis of the three simulator services, we discovered:

### market-data-simulator-go ✅
- **Has working gRPC service**: MarketDataService with 5 RPCs
- **Streaming support**: 2 server streaming RPCs functional
- **HTTP server**: Gin-based HTTP server on port 8085
- **Ready for Connect**: ✅ Implementation completed

### exchange-simulator-go ⚠️
- **No gRPC services**: Only health checks registered
- **Proto definitions exist**: But not generated or implemented
- **HTTP server exists**: Gin-based on port 8084
- **Needs**: gRPC service implementation first

### custodian-simulator-go ⚠️
- **No gRPC services**: Only health checks registered
- **HTTP server exists**: Gin-based on port 8083
- **Needs**: gRPC service implementation first

## Implemented: market-data-simulator-go

### Changes Summary
- ✅ Added Connect dependencies (connect, grpcreflect, cors, http2)
- ✅ Generated Connect handlers from proto files
- ✅ Created Connect adapter with streaming support
- ✅ Registered Connect handlers on HTTP server
- ✅ Added CORS middleware for browser requests
- ✅ Enabled HTTP/2 (h2c) support
- ✅ All tests passing (no regression)
- ✅ Documentation complete

### Service Coverage
All 5 MarketDataService RPCs now support Connect protocol:
1. **GetPrice** (unary) - Get current price
2. **StreamPrices** (server streaming) - Real-time price updates
3. **GenerateSimulation** (unary) - Generate simulated data
4. **StreamScenario** (server streaming) - Scenario testing
5. **HealthCheck** (unary) - Service health

### Browser Capabilities
- ✅ Real-time market data streaming
- ✅ Market simulation generation
- ✅ Scenario testing (rally, crash, divergence)
- ✅ CORS-compliant requests
- ✅ WebSocket-style streaming via HTTP/2

### Deployment
- **Branch**: `feature/epic-TSE-0002-connect-protocol`
- **Commit**: `fd562c2`
- **Port**: 8085 (HTTP with Connect protocol)
- **Status**: Ready for Docker deployment

## Not Implemented: exchange-simulator-go

### Why Not Ready
Exchange simulator has proto service definitions but they are **not implemented**:

```protobuf
// proto/api/v1/instrument_service.proto
service InstrumentService {
    rpc GetSecurity(GetSecurityRequest) returns (GetSecurityResponse);
    rpc SearchSecurities(SearchSecuritiesRequest) returns (SearchSecuritiesResponse);
    rpc GetCorporateActions(GetCorporateActionsRequest) returns (GetCorporateActionsResponse);
    rpc GetSecurityFundamentals(GetSecurityFundamentalsRequest) returns (GetSecurityFundamentalsResponse);
    rpc GetSecurities(GetSecuritiesRequest) returns (GetSecuritiesResponse);
}

// proto/api/v1/market_data_service.proto
service MarketDataService {
    rpc GetL1MarketData(GetL1MarketDataRequest) returns (GetL1MarketDataResponse);
    rpc GetL2MarketData(GetL2MarketDataRequest) returns (GetL2MarketDataResponse);
    rpc GetCandleData(GetCandleDataRequest) returns (GetCandleDataResponse);
    rpc GetTradePrints(GetTradePrintsRequest) returns (GetTradePrintsResponse);
    rpc GetMarketStatistics(GetMarketStatisticsRequest) returns (GetMarketStatisticsResponse);
    rpc StreamL1Data(StreamL1DataRequest) returns (stream L1MarketData);
    rpc StreamL2Data(StreamL2DataRequest) returns (stream L2MarketData);
    rpc StreamTrades(StreamTradesRequest) returns (stream TradePrint);
}
```

**Current state**: These services are not registered in the gRPC server.

### Required Before Connect
1. **Implement gRPC services**: Create handlers for all RPCs
2. **Register with gRPC server**: Add service registration in main.go
3. **Test gRPC functionality**: Verify all RPCs work with grpcurl
4. **Then apply Connect pattern**: Follow market-data-simulator pattern

### Recommended Approach
Create a separate epic for exchange simulator behaviors:
- **Epic**: Exchange Simulator Business Logic Implementation
- **Behaviors**: Instrument data, market data, security fundamentals
- **Deliverables**: Working gRPC services for all defined RPCs
- **Then**: Apply Connect protocol pattern (2-3 hours)

## Not Implemented: custodian-simulator-go

### Why Not Ready
Custodian simulator has **no proto service definitions** and no gRPC services.

### Required Before Connect
1. **Define proto services**: Create .proto files for custodian operations
2. **Generate proto code**: Run protoc to generate Go code
3. **Implement gRPC services**: Create handlers for all RPCs
4. **Register with gRPC server**: Add service registration
5. **Test gRPC functionality**: Verify with grpcurl
6. **Then apply Connect pattern**: Follow market-data-simulator pattern

### Recommended Approach
Create a separate epic for custodian simulator behaviors:
- **Epic**: Custodian Simulator Business Logic Implementation
- **Behaviors**: Asset custody, settlements, balance inquiries
- **Deliverables**: Proto definitions and working gRPC services
- **Then**: Apply Connect protocol pattern (2-3 hours)

## Revised Epic Scope

### Phase 1: Services with Working gRPC ✅
- ✅ audit-correlator-go (completed previously)
- ✅ market-data-simulator-go (completed this implementation)

### Phase 2: Implement Exchange gRPC Services (Future Epic)
**Epic**: TSE-XXXX Exchange Simulator Business Logic
- Implement InstrumentService (5 RPCs)
- Implement MarketDataService (8 RPCs)
- Integration testing
- **Then**: Add Connect protocol support

### Phase 3: Implement Custodian gRPC Services (Future Epic)
**Epic**: TSE-YYYY Custodian Simulator Business Logic
- Define proto services for custodian operations
- Implement custodian gRPC services
- Integration testing
- **Then**: Add Connect protocol support

## Success Metrics

### Completed (Phase 1)
- ✅ 2 services with Connect protocol support
- ✅ Consistent pattern across implementations
- ✅ Browser connectivity to topology visualization (audit-correlator)
- ✅ Browser connectivity to market data streams (market-data-simulator)
- ✅ All tests passing
- ✅ Documentation complete

### Future (Phases 2-3)
- ⏸️ Exchange simulator gRPC services implemented
- ⏸️ Exchange simulator Connect protocol added
- ⏸️ Custodian simulator gRPC services implemented
- ⏸️ Custodian simulator Connect protocol added
- ⏸️ All 4 services support browser connectivity

## Time Investment

### Actual (Phase 1 - market-data-simulator)
- Analysis: 30 minutes
- Implementation: 90 minutes
- Testing: 15 minutes
- Documentation: 30 minutes
- **Total**: 2.5 hours

### Estimated (Future Phases)
- **Exchange gRPC implementation**: 12-15 hours (13 RPCs, streaming)
- **Exchange Connect addition**: 2-3 hours
- **Custodian gRPC implementation**: 8-10 hours (TBD RPCs)
- **Custodian Connect addition**: 2-3 hours
- **Total remaining**: 24-31 hours

## Lessons Learned

1. **Verify gRPC services exist before planning Connect rollout**
   - Assumption: All simulators had working gRPC services
   - Reality: Only market-data-simulator had implemented services

2. **Connect protocol is the easy part**
   - Connect implementation: 2-3 hours per service
   - gRPC service implementation: 10-15 hours per service
   - Don't underestimate gRPC implementation complexity

3. **Proto definitions ≠ Working services**
   - Exchange had proto files but no implementations
   - Need to verify RegisterServer calls in code

4. **Pattern reusability is high**
   - audit-correlator → market-data-simulator pattern worked perfectly
   - Same pattern will work for exchange/custodian once gRPC is ready

5. **Scope flexibility is valuable**
   - Original plan: All three simulators
   - Revised: Focus on what's ready
   - Delivered value immediately rather than blocked

## Recommendations

### For Exchange and Custodian Simulators

1. **Create separate behavior-focused epics**
   - Don't bundle Connect protocol with gRPC implementation
   - Focus epics on business logic and behaviors
   - Add Connect protocol as final step in each epic

2. **Follow TDD approach**
   - Write tests for each RPC method
   - Implement gRPC handlers to pass tests
   - Verify with grpcurl before Connect

3. **Use market-data-simulator as reference**
   - Study `internal/handlers/grpc_marketdata.go` for patterns
   - Reference `internal/proto/marketdata.proto` for proto style
   - Follow same directory structure

4. **Reuse Connect pattern**
   - Copy `marketdata_connect_adapter.go` as template
   - Adjust for service-specific RPCs
   - Test with browser client

### For Project Planning

1. **Verify implementation status before planning**
   - Check RegisterServer calls in code
   - Don't assume proto files mean working services
   - Test with grpcurl early

2. **Separate business logic from protocol support**
   - gRPC service implementation: Behavior-focused epic
   - Connect protocol addition: Quick follow-on task

3. **Deliver incrementally**
   - market-data-simulator Connect support delivers value now
   - Exchange/custodian can follow when ready
   - No blocked dependencies

## Current Status

### Completed
- ✅ market-data-simulator-go Connect protocol support
- ✅ Browser can stream real-time market data
- ✅ Documentation and testing complete
- ✅ Ready for Docker deployment

### Pending (Future Work)
- 📋 Exchange simulator gRPC service implementation
- 📋 Custodian simulator gRPC service implementation
- 📋 Connect protocol for exchange (after gRPC complete)
- 📋 Connect protocol for custodian (after gRPC complete)

---

**Status Date**: 2025-10-26
**Epic**: TSE-0002 Network Topology Visualization
**Phase 1**: ✅ Complete (2/2 ready services have Connect support)
**Next**: Create epics for exchange/custodian gRPC implementations
