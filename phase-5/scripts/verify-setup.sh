#!/bin/bash
# Quick verification script to check Phase 5 setup

echo "=========================================="
echo "  Phase 5 Setup Verification"
echo "=========================================="
echo ""

# Check required tools
echo "Checking required tools..."
MISSING_TOOLS=0

if ! command -v doctl &> /dev/null; then
    echo "❌ doctl not found"
    MISSING_TOOLS=1
else
    echo "✅ doctl installed"
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found"
    MISSING_TOOLS=1
else
    echo "✅ kubectl installed"
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm not found"
    MISSING_TOOLS=1
else
    echo "✅ helm installed"
fi

if ! command -v docker &> /dev/null; then
    echo "❌ docker not found"
    MISSING_TOOLS=1
else
    echo "✅ docker installed"
fi

echo ""

if [ $MISSING_TOOLS -eq 1 ]; then
    echo "⚠️  Some required tools are missing. Please install them before proceeding."
    exit 1
fi

# Check DigitalOcean authentication
echo "Checking DigitalOcean authentication..."
if doctl account get &> /dev/null; then
    echo "✅ Authenticated with DigitalOcean"
    doctl account get
else
    echo "❌ Not authenticated with DigitalOcean"
    echo "Run: doctl auth init"
    exit 1
fi

echo ""
echo "=========================================="
echo "  ✅ All prerequisites met!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review constitution.md and specifications"
echo "  2. Run: ./scripts/setup-doks.sh"
echo "  3. Run: ./scripts/install-kafka.sh"
echo "  4. Run: ./scripts/install-dapr.sh"
echo "  5. Run: ./scripts/setup-monitoring.sh"
echo "  6. Build and push Docker images"
echo "  7. Run: ./scripts/deploy-production.sh"
echo ""
