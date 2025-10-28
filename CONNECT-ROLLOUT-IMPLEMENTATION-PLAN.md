# Connect Protocol Rollout: Implementation Plan

## Summary

This document provides a step-by-step plan to add Connect protocol support to the three simulator services, following the pattern successfully implemented in `audit-correlator-go`.

## Implementation Checklist Template

Use this checklist for each service:

### Pre-Implementation

- [ ] Identify all gRPC services the simulator exposes
- [ ] Locate proto files (protobuf-schemas vs local)
- [ ] Check current HTTP server implementation (Gin, standard, or none)
- [ ] Verify current port mappings in docker-compose.yml
- [ ] Review existing gRPC server initialization

### Implementation Steps

#### Step 1: Create Feature Branch
```bash
cd <service-directory>
git checkout main
git pull origin main
git checkout -b feature/epic-TSE-0002-connect-protocol
```

#### Step 2: Add Dependencies
```bash
go get connectrpc.com/connect@latest
go get connectrpc.com/grpcreflect@latest  # For reflection support
go get connectrpc.com/cors@latest         # For CORS
go get golang.org/x/net/http2@latest      # For HTTP/2
go mod tidy
```

**Files Modified**: `go.mod`, `go.sum`

#### Step 3: Generate Connect Handlers

**If proto files are in protobuf-schemas**:
```bash
cd ../protobuf-schemas
export PATH="$PATH:$(go env GOPATH)/bin"

# Generate Connect handlers
protoc \
  --connect-go_out=. \
  --connect-go_opt=paths=source_relative \
  --proto_path=. \
  <service>/v1/<service>_service.proto

# Copy to service repo with fixed imports
# (Follow audit-correlator pattern)
```

**Result**: `gen/go/<service>/v1/<service>connect/*.connect.go`

#### Step 4: Create Connect Adapter

Create `internal/presentation/connect/<service>_connect_adapter.go`:

```go
package connectpresentation

import (
	"context"
	"connectrpc.com/connect"
	"google.golang.org/grpc/metadata"

	<service>v1 "path/to/generated/proto"
	"path/to/generated/connect"
	grpcservices "path/to/grpc/services"
)

// <Service>ConnectAdapter adapts gRPC service to Connect protocol
type <Service>ConnectAdapter struct {
	grpcServer *grpcservices.<Service>Server
}

// Ensure adapter implements Connect handler interface
var _ <service>connect.<Service>Handler = (*<Service>ConnectAdapter)(nil)

// New<Service>ConnectAdapter creates adapter
func New<Service>ConnectAdapter(grpcServer *grpcservices.<Service>Server) *<Service>ConnectAdapter {
	return &<Service>ConnectAdapter{
		grpcServer: grpcServer,
	}
}

// Implement each RPC method (unary example):
func (h *<Service>ConnectAdapter) MethodName(
	ctx context.Context,
	req *connect.Request[<service>v1.RequestType],
) (*connect.Response[<service>v1.ResponseType], error) {
	resp, err := h.grpcServer.MethodName(ctx, req.Msg)
	if err != nil {
		return nil, err
	}
	return connect.NewResponse(resp), nil
}

// For streaming RPCs, create stream adapters (see audit-correlator example)
```

**Files Created**: `internal/presentation/connect/<service>_connect_adapter.go`

#### Step 5: Update HTTP Server

In `cmd/server/main.go`:

**Add Imports**:
```go
import (
	"golang.org/x/net/http2"
	"golang.org/x/net/http2/h2c"

	<service>connect "path/to/generated/connect"
	connectpresentation "path/to/internal/presentation/connect"
	grpcservices "path/to/internal/presentation/grpc/services"
)
```

**Add CORS Middleware** (if using Gin):
```go
// Add CORS middleware for Connect protocol (browser requests)
router.Use(func(c *gin.Context) {
	c.Header("Access-Control-Allow-Origin", "*")
	c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
	c.Header("Access-Control-Allow-Headers", "Content-Type, Connect-Protocol-Version, Connect-Timeout-Ms, X-Client, X-Client-Version")
	c.Header("Access-Control-Expose-Headers", "Connect-Protocol-Version")

	if c.Request.Method == "OPTIONS" {
		c.AbortWithStatus(http.StatusNoContent)
		return
	}

	c.Next()
})
```

**Register Connect Handlers**:
```go
// Register Connect protocol handlers
func registerConnectHandlers(router *gin.Engine, <service>Server *grpcservices.<Service>Server, logger *logrus.Logger) {
	// Create Connect adapter
	connectAdapter := connectpresentation.New<Service>ConnectAdapter(<service>Server)

	// Generate Connect HTTP handler
	path, handler := <service>connect.New<Service>Handler(connectAdapter)

	// Register with Gin router
	router.Any(path+"*method", gin.WrapH(handler))

	logger.WithField("path", path).Info("Registered Connect protocol handlers for <Service>")
}
```

**Enable HTTP/2**:
```go
return &http.Server{
	Addr:    fmt.Sprintf(":%d", cfg.HTTPPort),
	Handler: h2c.NewHandler(router, &http2.Server{}), // Enable HTTP/2
}
```

**Files Modified**: `cmd/server/main.go`

#### Step 6: Verify Docker Configuration

Check `docker-compose.yml` in orchestrator-docker:

```yaml
<service>-simulator:
  ports:
    - "127.0.0.1:8084:8080"   # HTTP port (should exist)
    - "127.0.0.1:50054:50051" # gRPC port
```

**Verify**: HTTP port is mapped (if not, add it)

#### Step 7: Build and Test

```bash
# Build
go build ./...

# Run tests
go test ./... -short -count=1

# Check for issues
echo $?  # Should be 0
```

#### Step 8: Create PR Documentation

Create `docs/prs/feat-epic-TSE-0002-connect-protocol.md`:

```markdown
# feat(epic-TSE-0002): Add Connect protocol support for browser clients

## Summary
Adds Connect protocol support to enable browser-based gRPC communication...

## What Changed
- Added Connect dependencies
- Generated Connect handlers
- Created Connect adapter
- Registered Connect routes
- Added CORS middleware
- Enabled HTTP/2 support

## Testing
- Build succeeds
- All tests pass
- Connect endpoint responds

## Related Work
- Follows pattern from audit-correlator-go
- Part of Epic TSE-0002 simulator rollout
```

#### Step 9: Commit Changes

```bash
git add -A
git status  # Verify changes

git commit -m "$(cat <<'EOF'
feat(epic-TSE-0002): Add Connect protocol support for browser clients

Enables browser-based gRPC communication by adding Connect protocol support
alongside existing native gRPC server. Follows pattern from audit-correlator-go.

Changes:
- Add Connect framework dependencies
- Generate Connect protocol handlers
- Create Connect adapter for <Service>Service
- Register Connect routes on HTTP server
- Add CORS middleware for browser requests
- Enable HTTP/2 support (h2c)

Testing:
- All tests pass (no regression)
- Build succeeds
- Ready for Docker deployment

Integration:
- HTTP port (<port>) serves Connect protocol
- gRPC port (<grpc-port>) serves native gRPC
- Browser clients use Connect via HTTP port

Part of Epic TSE-0002 simulator Connect rollout.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### Step 10: Test Deployment

```bash
# Rebuild Docker container
cd ../orchestrator-docker
docker-compose build --no-cache <service>-simulator

# Restart service
docker-compose up -d <service>-simulator

# Check logs
docker logs trading-ecosystem-<service>-simulator | grep -i connect

# Test Connect endpoint
curl -X POST http://localhost:<http-port>/<service>.v1.<Service>Service/<Method> \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Post-Implementation

- [ ] All tests pass
- [ ] Docker container runs successfully
- [ ] Connect endpoint responds
- [ ] CORS headers present
- [ ] HTTP/2 enabled
- [ ] Documentation updated
- [ ] PR ready for review

## Service-Specific Customizations

### Exchange Simulator

**Proto Service**: `exchange.v1.ExchangeService`
**Port**: HTTP 8084, gRPC 50054
**Specific Needs**:
- Order management RPCs (likely unary)
- Position streaming (may need stream adapter)

### Market Data Simulator

**Proto Service**: `marketdata.v1.MarketDataService`
**Port**: HTTP 8085, gRPC 50055
**Specific Needs**:
- Market data streaming (definitely needs stream adapter)
- Tick data streaming (server streaming)
- High-frequency updates

### Custodian Simulator

**Proto Service**: `custodian.v1.CustodianService`
**Port**: HTTP 8083, gRPC 50053
**Specific Needs**:
- Asset management RPCs (likely unary)
- Balance inquiries

## Common Issues and Solutions

### Issue 1: Proto Files Not Found

**Problem**: Can't find proto files to generate Connect handlers

**Solution**:
```bash
# Check protobuf-schemas
cd ../protobuf-schemas
find . -name "*<service>*.proto"

# If not found, check service's own directory
cd ../<service>-simulator-go
find . -name "*.proto"
```

### Issue 2: Import Path Mismatches

**Problem**: Generated Connect files reference wrong module paths

**Solution**: Use sed to fix imports (see audit-correlator example):
```bash
sed 's|old/module/path|new/module/path|g' input.go > output.go
```

### Issue 3: No HTTP Server Exists

**Problem**: Service only has gRPC server, no HTTP server

**Solution**: Add HTTP server setup (copy from audit-correlator pattern)

### Issue 4: Stream Adapter Compilation Errors

**Problem**: Stream adapters don't implement required interfaces

**Solution**: Check gRPC stream interface and implement all methods:
- `Send(msg) error`
- `Context() context.Context`
- `SetHeader(md metadata.MD) error`
- `SendHeader(md metadata.MD) error`
- `SetTrailer(md metadata.MD)`

### Issue 5: CORS Not Working

**Problem**: Browser shows CORS errors

**Solution**: Verify middleware order and headers:
```go
// CORS must be registered BEFORE other middleware
router.Use(corsMiddleware)
router.Use(otherMiddleware)
```

## Testing Checklist

### Unit Tests
- [ ] `go test ./... -short` passes
- [ ] No new test failures
- [ ] Connect adapter compiles

### Integration Tests
- [ ] Docker container builds
- [ ] Service starts successfully
- [ ] Connect endpoint reachable
- [ ] CORS headers present

### Manual Tests
```bash
# Test 1: List services (if reflection enabled)
grpcurl -plaintext localhost:<http-port> list

# Test 2: Call unary RPC via curl
curl -X POST http://localhost:<http-port>/<service>.v1.<Service>/<Method> \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'

# Test 3: Check CORS headers
curl -X OPTIONS http://localhost:<http-port>/<service>.v1.<Service>/<Method> \
  -H "Origin: http://localhost:3002" \
  -v 2>&1 | grep -i "access-control"
```

## Timeline

Per service (assuming no major complications):
- Analysis: 30 minutes
- Implementation: 1-2 hours
- Testing: 30 minutes
- Documentation: 30 minutes
- **Total**: 2.5-3.5 hours per service

Total for three simulators: **7.5-10.5 hours**

## Success Criteria

### Per Service:
✅ Build succeeds with Connect dependencies
✅ All tests pass (no regression)
✅ Connect handlers generated
✅ Connect adapter created
✅ Routes registered on HTTP server
✅ CORS middleware configured
✅ HTTP/2 enabled
✅ Docker container runs
✅ Connect endpoint responds
✅ Browser can communicate

### Overall:
✅ Consistent pattern across all simulators
✅ Git quality standards followed
✅ Documentation complete
✅ All services support Connect protocol

## Recommended Order

1. **exchange-simulator-go** (Start here - likely simplest)
2. **custodian-simulator-go** (Similar to exchange)
3. **market-data-simulator-go** (Most complex - streaming)

**Rationale**: Learn from simpler services, apply lessons to more complex ones.

## Next Actions

1. Start with `exchange-simulator-go`
2. Follow checklist step-by-step
3. Document any issues encountered
4. Apply learnings to next service
5. Repeat until all three complete

---

**Ready to Start**: Yes - proceed with exchange-simulator-go analysis and implementation
