# Epic TSE-0002: Connect Protocol Rollout Plan for Simulators

## Executive Summary

Apply the Connect protocol implementation pattern from `audit-correlator-go` to the three simulator services (`exchange-simulator-go`, `market-data-simulator-go`, `custodian-simulator-go`) to enable browser-based gRPC communication.

## Current Status

✅ **Completed**: `audit-correlator-go`
- Connect protocol support implemented
- Browser connectivity working (port 8082)
- TopologyService accessible via Connect protocol

⏳ **Pending**: Three simulator services
- `exchange-simulator-go`
- `market-data-simulator-go`
- `custodian-simulator-go`

## Why This Is Needed

**Problem**: Simulators likely only expose native gRPC, which browsers cannot use directly.

**Solution**: Add Connect protocol handlers alongside existing gRPC servers (same pattern as audit-correlator).

**Benefit**: Browser-based UI can communicate with all services via Connect protocol.

## Implementation Pattern (from audit-correlator-go)

### What Was Added to audit-correlator-go:

1. **Dependencies** (`go.mod`):
   ```go
   connectrpc.com/connect v1.19.1
   connectrpc.com/grpcreflect v1.3.0
   connectrpc.com/cors v0.1.0
   golang.org/x/net/http2
   ```

2. **Generated Connect Handlers** (`gen/go/.../connect/`):
   - Generated from proto files via `protoc-gen-connect-go`
   - Provides `ServiceNameHandler` interface
   - Supports Connect, gRPC, and gRPC-Web protocols

3. **Connect Adapter** (`internal/presentation/connect/`):
   - Wraps existing gRPC service implementation
   - Implements Connect handler interface
   - Stream adapters for server streaming RPCs

4. **HTTP Server Integration** (`cmd/server/main.go`):
   - CORS middleware for browser requests
   - HTTP/2 support via `h2c`
   - Connect routes registered on HTTP server
   - Example: `/audit.v1.TopologyService/*`

5. **Docker Configuration** (`docker-compose.yml`):
   - HTTP port exposed (8082) for Connect protocol
   - gRPC port exposed (50052) for native gRPC

## Rollout Plan

### Phase 1: Analysis & Preparation

**Tasks**:
1. ✅ Identify all three simulator services
2. 🔄 Discover proto services each simulator exposes
3. 🔄 Check current HTTP/gRPC port configuration
4. 🔄 Identify existing gRPC service implementations
5. 🔄 Document service-specific differences

**Deliverables**:
- Service analysis document for each simulator
- Proto service inventory
- Port mapping documentation

### Phase 2: Pattern Extraction

**Tasks**:
1. Extract reusable Connect integration pattern
2. Create template/checklist for applying pattern
3. Document required code changes per layer
4. Identify service-specific customizations needed

**Deliverables**:
- Connect integration template
- Step-by-step implementation checklist
- Code snippets for each layer

### Phase 3: Implementation (Per Service)

**Order**:
1. **exchange-simulator-go** (likely simplest)
2. **market-data-simulator-go** (streaming likely)
3. **custodian-simulator-go** (similar to exchange)

**Per-Service Tasks**:
1. Create feature branch (`feature/epic-TSE-0002-connect-protocol-<service>`)
2. Add Connect dependencies to `go.mod`
3. Generate Connect handlers from proto files
4. Create Connect adapter for each gRPC service
5. Register Connect routes on HTTP server
6. Add CORS middleware
7. Enable HTTP/2 support
8. Update docker-compose.yml (if needed)
9. Build and test
10. Create PR documentation
11. Commit changes

**Estimated Time**: ~2-3 hours per service

### Phase 4: Testing & Verification

**Per-Service Tests**:
1. Build verification (`go build ./...`)
2. Unit tests pass (`go test ./...`)
3. Docker container rebuilds successfully
4. Connect endpoint responds to curl
5. gRPC reflection working (if applicable)

**Integration Tests**:
1. All services running in docker-compose
2. Browser can reach all Connect endpoints
3. Port mappings verified
4. CORS headers present

**Deliverables**:
- Test results for each service
- Integration test documentation

### Phase 5: Documentation & Deployment

**Tasks**:
1. Update main topology visualization docs
2. Document all service Connect endpoints
3. Create unified deployment guide
4. Update UI configuration if needed

**Deliverables**:
- Complete Connect endpoint reference
- Deployment guide for all services
- Troubleshooting guide

## Service-Specific Analysis Needed

### For Each Simulator Service:

1. **Proto Services Exposed**:
   - What gRPC services does it implement?
   - What RPC methods (unary vs streaming)?
   - Are proto files in protobuf-schemas or local?

2. **Current Architecture**:
   - How is gRPC server initialized?
   - Where is HTTP server (if any)?
   - What ports are currently exposed?

3. **Customizations Needed**:
   - Service-specific Connect adapters
   - Multiple service handlers per container?
   - Special streaming implementations?

## Expected Changes Per Service

### Minimal Changes (If Pattern Matches)

**Files to Add** (~3-5 files):
1. `gen/go/<service>/v1/<service>connect/*.connect.go` (generated)
2. `internal/presentation/connect/<service>_connect_adapter.go`
3. `docs/prs/feat-epic-TSE-0002-connect-protocol-<service>.md`

**Files to Modify** (~2-3 files):
1. `go.mod` (add Connect dependencies)
2. `go.sum` (auto-updated)
3. `cmd/server/main.go` (register Connect handlers, add CORS, HTTP/2)

**Optional Changes**:
1. `docker-compose.yml` (if port mappings need adjustment)
2. `.env` files (if base URLs need updating)

### Potential Complications

1. **No HTTP Server**: If service only has gRPC, need to add HTTP server
2. **Multiple gRPC Services**: Need Connect adapter for each
3. **Custom Streaming**: May need specialized stream adapters
4. **Authentication**: If auth middleware exists, may need Connect-compatible version

## Port Assignments (Current)

From docker-compose.yml:
- **audit-correlator**: HTTP 8082, gRPC 50052 ✅ (Has Connect)
- **exchange-simulator**: HTTP 8084?, gRPC 50054?
- **market-data-simulator**: HTTP 8085?, gRPC 50055?
- **custodian-simulator**: HTTP 8083?, gRPC 50053?

**Verify**: Check actual docker-compose.yml for current port mappings

## Success Criteria

### Per Service:
- ✅ Build succeeds with Connect dependencies
- ✅ All tests pass
- ✅ Connect handlers generated and registered
- ✅ CORS middleware configured
- ✅ HTTP/2 enabled
- ✅ Docker container runs successfully
- ✅ Connect endpoint responds to curl
- ✅ Browser can communicate via Connect protocol

### Overall:
- ✅ All four services (audit + 3 simulators) support Connect protocol
- ✅ UI can communicate with all services
- ✅ Consistent pattern applied across services
- ✅ Documentation complete
- ✅ Git quality standards followed (feature branches, PRs)

## Risk Mitigation

### Low Risk:
- Pattern already proven in audit-correlator-go
- Connect library well-documented
- No breaking changes to existing gRPC

### Medium Risk:
- Service-specific architectural differences
- May need HTTP server if none exists
- Streaming RPCs may need custom adapters

### Mitigation Strategies:
1. Start with simplest service (exchange-simulator)
2. Document issues and solutions for reuse
3. Test thoroughly at each step
4. Maintain parallel gRPC support (no breaking changes)

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Analysis | 1-2 hours | None |
| Phase 2: Pattern Extraction | 1 hour | Phase 1 complete |
| Phase 3: Implementation | 6-9 hours | Phase 2 complete |
| - Exchange Simulator | 2-3 hours | - |
| - Market Data Simulator | 2-3 hours | Exchange done |
| - Custodian Simulator | 2-3 hours | Market Data done |
| Phase 4: Testing | 2-3 hours | Phase 3 complete |
| Phase 5: Documentation | 1-2 hours | Phase 4 complete |
| **Total** | **11-17 hours** | Sequential |

## Next Steps

### Immediate Actions:

1. **Analyze Services** (Start with exchange-simulator-go):
   ```bash
   cd exchange-simulator-go
   # Find proto services
   grep -r "Register.*Server" cmd/server/main.go
   # Check current HTTP server
   grep -r "http.Server\|gin.Engine" cmd/server/main.go
   # Verify port configuration
   grep -A 5 "exchange-simulator:" ../orchestrator-docker/docker-compose.yml
   ```

2. **Create Analysis Document**: Document findings for each service

3. **Extract Pattern**: Create reusable implementation guide

4. **Start Implementation**: Begin with exchange-simulator-go

## Questions to Answer

Before starting implementation:

1. **Architecture**:
   - Do all simulators have HTTP servers already?
   - Are they using Gin or standard http.Server?
   - Where are gRPC servers initialized?

2. **Proto Files**:
   - Are proto files in protobuf-schemas repo?
   - Are Connect handlers already generated?
   - Do we need to generate them?

3. **Deployment**:
   - Are HTTP ports already exposed in docker-compose?
   - Do we need to update any port mappings?
   - Is UI already configured for these ports?

4. **Testing**:
   - Do services have existing tests?
   - How can we verify Connect functionality?
   - Integration test setup?

## Reference Documents

- `audit-correlator-go/docs/prs/feat-epic-TSE-0002-connect-protocol-support.md`
- `audit-correlator-go/docs/CONNECT_PROTOCOL_SETUP.md`
- `audit-correlator-go/internal/presentation/connect/topology_connect_adapter.go`
- `audit-correlator-go/cmd/server/main.go` (registerConnectHandlers function)

## Decision Points

**Decision 1**: Sequential vs Parallel Implementation?
- **Recommendation**: Sequential (learn from each, reuse solutions)

**Decision 2**: Generate Connect handlers or manual adapters?
- **Recommendation**: Generate where possible (type-safe, maintainable)

**Decision 3**: Add HTTP server if missing vs Connect-only?
- **Recommendation**: Add full HTTP server (enables future REST endpoints)

**Decision 4**: Feature branch per service vs single branch?
- **Recommendation**: Per service (easier review, independent deployment)

## Success Metrics

After rollout:
- **Code Reuse**: ~80% of Connect implementation reusable across services
- **Test Coverage**: All existing tests continue passing
- **Performance**: No degradation in native gRPC performance
- **Compatibility**: Browser clients can communicate with all services
- **Documentation**: Complete setup guide for adding Connect to new services

---

**Status**: Planning phase - ready to begin analysis
**Owner**: Development team
**Epic**: TSE-0002 Network Topology Visualization
**Priority**: High (unblocks full UI integration)
