# Trading Ecosystem Development Environment Setup

This document provides comprehensive instructions for setting up the development environment for the Trading Ecosystem project, which includes multiple Python services using modern frameworks and tools.

## Prerequisites

- **Python 3.13**: All services use Python 3.13 for latest language features and performance improvements
- **Conda/Miniconda**: Package and environment management
- **Docker**: For containerized services and databases
- **Git**: Version control

## Environment Setup

### 1. Conda Environment Creation

Create a unified conda environment for all Python services in the trading ecosystem:

```bash
# Create new conda environment with Python 3.13
conda create -n py313_trading_ecosystem_dev python=3.13 -y

# Activate the environment
conda activate py313_trading_ecosystem_dev

# Verify Python version
python --version  # Should show Python 3.13.x
```

### 2. Core Package Installation

Install the core packages required by all services:

```bash
# Essential web framework packages
pip install fastapi>=0.115.0 uvicorn[standard]>=0.32.0

# Data validation and settings
pip install pydantic>=2.10.0 pydantic-settings>=2.6.0

# gRPC and async support
pip install grpcio>=1.68.0 grpcio-tools>=1.68.0 grpcio-health-checking>=1.68.0

# Testing framework
pip install pytest>=8.3.0 pytest-asyncio>=0.25.0 pytest-mock>=3.14.0

# HTTP testing
pip install httpx>=0.28.0

# Database and caching
pip install redis>=5.1.0 asyncpg>=0.29.0 sqlalchemy[asyncio]>=2.0.0

# Observability and logging
pip install structlog>=24.4.0 opentelemetry-api>=1.27.0 opentelemetry-sdk>=1.27.0

# Utilities
pip install tenacity>=9.0.0 orjson>=3.10.0 msgpack>=1.1.0

# Development tools
pip install ruff>=0.8.0 mypy>=1.13.0 black>=24.10.0 pre-commit>=4.0.0
```

### 3. Service-Specific Setup

For each Python service in the ecosystem:

#### Risk Monitor Service
```bash
cd /path/to/trading-ecosystem/risk-monitor-py

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Start development server
uvicorn risk_monitor.main:app --reload --host 0.0.0.0 --port 8084
```

#### Trading Engine Service
```bash
cd /path/to/trading-ecosystem/trading-system-engine-py

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

#### Test Coordinator Service
```bash
cd /path/to/trading-ecosystem/test-coordinator-py

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Project Structure

The trading ecosystem follows a consistent structure across all Python services:

```
service-name-py/
├── src/
│   └── service_name/
│       ├── __init__.py
│       ├── main.py                    # Application entry point
│       ├── domain/                    # Business logic
│       ├── infrastructure/            # External systems integration
│       │   ├── config.py              # Configuration management
│       │   └── service_discovery.py   # Service registry
│       └── presentation/              # API layers
│           ├── http/                  # FastAPI HTTP endpoints
│           │   ├── app.py
│           │   └── routers/
│           └── grpc/                  # gRPC services
│               └── services/
├── tests/
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   └── conftest.py                   # Test configuration
├── pyproject.toml                    # Project configuration
└── README.md
```

## Development Workflow

### 1. Environment Activation
Always activate the conda environment before development:

```bash
conda activate py313_trading_ecosystem_dev
```

### 2. Running Tests
Each service uses pytest with async support:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_health_endpoints.py -v

# Run with async support
pytest -m asyncio
```

### 3. Code Quality
All services use consistent code quality tools:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/

# Run all quality checks
pre-commit run --all-files
```

### 4. Development Servers

#### HTTP Development Server
```bash
# FastAPI with auto-reload
uvicorn service_name.main:app --reload --host 0.0.0.0 --port 8084
```

#### gRPC Development Server
The gRPC server starts automatically with the main application in dual-protocol mode.

### 5. Docker Integration
Services are designed to work with Docker Compose:

```bash
# Start all infrastructure services
cd orchestrator-docker
docker compose up -d

# Check service health
docker compose ps
```

## Configuration Management

### Environment Variables
Each service uses environment-specific configuration:

```bash
# Development
export ENVIRONMENT=development
export DEBUG=true
export LOG_LEVEL=DEBUG

# Redis connection
export REDIS_URL=redis://localhost:6379/0

# Service discovery
export SERVICE_NAME=risk-monitor
export SERVICE_VERSION=0.1.0

# Ports
export HTTP_PORT=8084
export GRPC_PORT=50054
```

### Configuration Files
Services use Pydantic Settings for configuration management:

```python
# src/service_name/infrastructure/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Service configuration
    service_name: str = "service-name"
    service_version: str = "0.1.0"

    # Network configuration
    http_port: int = 8080
    grpc_port: int = 50051

    # External services
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
```

## Testing Strategy

### Test Categories
1. **Unit Tests**: Fast, isolated tests for business logic
2. **Integration Tests**: Tests for external system integration
3. **API Tests**: HTTP and gRPC endpoint testing
4. **Performance Tests**: Load and performance validation

### Test Configuration
Services use comprehensive test fixtures:

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

@pytest.fixture
def test_client(fastapi_app) -> TestClient:
    return TestClient(fastapi_app)

@pytest_asyncio.fixture
async def async_client(fastapi_app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client
```

## Troubleshooting

### Common Issues

#### 1. Conda Environment Not Activating
```bash
# Ensure conda is initialized
conda init bash
source ~/.bashrc

# Re-create environment if needed
conda env remove -n py313_trading_ecosystem_dev
conda create -n py313_trading_ecosystem_dev python=3.13 -y
```

#### 2. Package Installation Issues
```bash
# Clear pip cache
pip cache purge

# Reinstall with no cache
pip install --no-cache-dir package-name

# Check for conflicting packages
pip check
```

#### 3. Import Errors
```bash
# Install in development mode
pip install -e .

# Add current directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### 4. Test Failures
```bash
# Run tests with verbose output
pytest -v -s

# Run tests with pdb on failure
pytest --pdb

# Clear pytest cache
pytest --cache-clear
```

### Environment Verification

Run this verification script to check your setup:

```bash
#!/bin/bash
echo "=== Trading Ecosystem Development Environment Check ==="

# Check Python version
echo "Python version:"
python --version

# Check conda environment
echo "Current conda environment:"
conda info --envs | grep "*"

# Check key packages
echo "Key package versions:"
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import pydantic; print(f'Pydantic: {pydantic.__version__}')"
python -c "import pytest; print(f'Pytest: {pytest.__version__}')"

# Check if services can import
echo "Service import check:"
python -c "from risk_monitor.main import app; print('✓ Risk Monitor imports successfully')" 2>/dev/null || echo "✗ Risk Monitor import failed"

echo "=== Setup verification complete ==="
```

## Performance Optimization

### Development Performance
- Use `uvicorn --reload` for fast development iteration
- Enable hot reloading for both HTTP and gRPC services
- Use pytest-xdist for parallel test execution

### Production Considerations
- All services support OpenTelemetry tracing
- Structured logging with JSON output
- Prometheus metrics integration
- Health check endpoints for Kubernetes

## VS Code Setup

Recommended VS Code extensions and settings:

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "/path/to/miniconda3/envs/py313_trading_ecosystem_dev/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

## Git Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for development
- `feature/*`: Individual feature branches
- `hotfix/*`: Critical bug fixes

### Commit Guidelines
- Each behavior gets a new branch
- Each task gets a new commit
- Use conventional commit format:
  ```
  feat: add health check endpoints
  fix: resolve Redis connection timeout
  test: add comprehensive API tests
  docs: update development setup guide
  ```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.3
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
```

This development environment provides a robust foundation for building and maintaining the Trading Ecosystem's Python services with modern tools and best practices.