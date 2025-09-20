#!/usr/bin/env python3
"""
Trading Ecosystem Development Environment Verification Script

This script verifies that the development environment is properly set up
for all Python services in the trading ecosystem.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python 3.13 is being used."""
    print("=== Python Version Check ===")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 13:
        print("✓ Python 3.13+ detected")
        return True
    else:
        print("✗ Python 3.13+ required")
        return False


def check_required_packages():
    """Check if required packages are installed."""
    print("\n=== Package Availability Check ===")

    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pytest",
        "httpx",
        "structlog",
        "redis",
        "tenacity"
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False

    return True


def check_package_versions():
    """Check versions of key packages."""
    print("\n=== Package Version Check ===")

    version_checks = [
        ("fastapi", "0.115.0"),
        ("pydantic", "2.10.0"),
        ("pytest", "8.3.0"),
    ]

    for package_name, min_version in version_checks:
        try:
            package = __import__(package_name)
            version = getattr(package, "__version__", "unknown")
            print(f"{package_name}: {version}")
        except ImportError:
            print(f"{package_name}: not installed")


def check_service_imports():
    """Check if trading ecosystem services can be imported."""
    print("\n=== Service Import Check ===")

    # Add src directories to path for testing
    # Go up two levels from scripts/ to get to trading-ecosystem root
    ecosystem_root = Path(__file__).parent.parent.parent
    services = [
        "risk-monitor-py",
        "trading-system-engine-py",
        "test-coordinator-py"
    ]

    for service in services:
        service_path = ecosystem_root / service / "src"
        if service_path.exists():
            sys.path.insert(0, str(service_path))

            # Try to import the main module
            service_module = service.replace("-", "_").replace("_py", "")
            try:
                __import__(service_module)
                print(f"✓ {service}")
            except ImportError as e:
                print(f"✗ {service} - {e}")
        else:
            print(f"? {service} - service directory not found")


def check_docker_services():
    """Check if Docker services are running."""
    print("\n=== Docker Services Check ===")

    try:
        result = subprocess.run(
            ["docker", "compose", "ps"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent / "orchestrator-docker"
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # Header + services
                print("✓ Docker Compose services:")
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        print(f"  {line}")
            else:
                print("? No Docker services running")
        else:
            print("✗ Docker Compose not available or not running")

    except FileNotFoundError:
        print("✗ Docker not found in PATH")


def run_sample_tests():
    """Run a simple test to verify testing infrastructure."""
    print("\n=== Testing Infrastructure Check ===")

    try:
        # Simple pytest version check
        result = subprocess.run(
            ["python", "-m", "pytest", "--version"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ Pytest available")
            print(f"  {result.stdout.strip()}")
        else:
            print("✗ Pytest not working correctly")

    except Exception as e:
        print(f"✗ Testing infrastructure error: {e}")


def main():
    """Run all verification checks."""
    print("Trading Ecosystem Development Environment Verification")
    print("=" * 55)

    checks = [
        check_python_version,
        check_required_packages,
        check_package_versions,
        check_service_imports,
        check_docker_services,
        run_sample_tests
    ]

    all_passed = True
    for check in checks:
        try:
            result = check()
            if result is False:
                all_passed = False
        except Exception as e:
            print(f"✗ Check failed with error: {e}")
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("🎉 Environment verification completed successfully!")
        print("You're ready to develop on the Trading Ecosystem.")
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print("Refer to DEVELOPMENT_SETUP.md for detailed setup instructions.")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)