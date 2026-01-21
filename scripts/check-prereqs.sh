#!/bin/sh
# MCP Security Workshop - Prerequisites Checker
# POSIX-compatible shell script for cross-platform verification

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track missing components
MISSING=""
EXIT_CODE=0

echo "🔍 MCP Security Workshop - Prerequisites Check\n"

# Function to detect OS
detect_os() {
    if [ -f /proc/version ] && grep -qi microsoft /proc/version; then
        echo "wsl"
    elif [ "$(uname)" = "Darwin" ]; then
        echo "macos"
    elif [ "$(uname)" = "Linux" ]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# Check Docker/Podman
echo "📦 Checking Docker/Podman..."

# Try docker first, then podman
CONTAINER_CMD=""
CONTAINER_ENGINE=""

if command -v docker >/dev/null 2>&1; then
    CONTAINER_CMD="docker"
    # Detect if it's Podman aliased as docker
    if docker --version 2>&1 | grep -qi podman; then
        CONTAINER_ENGINE="Podman (via docker alias)"
    else
        CONTAINER_ENGINE="Docker"
    fi
elif command -v podman >/dev/null 2>&1; then
    CONTAINER_CMD="podman"
    CONTAINER_ENGINE="Podman"
fi

if [ -n "$CONTAINER_CMD" ]; then
    # Check if daemon/service is running
    if $CONTAINER_CMD info >/dev/null 2>&1; then
        CONTAINER_VERSION=$($CONTAINER_CMD --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
        MAJOR=$(echo "$CONTAINER_VERSION" | cut -d. -f1)
        MINOR=$(echo "$CONTAINER_VERSION" | cut -d. -f2)
        
        # Podman versions are different, so we check for >= 3.0 for Podman, >= 20.10 for Docker
        VERSION_OK=0
        if echo "$CONTAINER_ENGINE" | grep -qi podman; then
            # Podman 3.0+ is fine
            if [ "$MAJOR" -ge 3 ]; then
                VERSION_OK=1
            fi
        else
            # Docker needs >= 20.10
            if [ "$MAJOR" -gt 20 ] || { [ "$MAJOR" -eq 20 ] && [ "$MINOR" -ge 10 ]; }; then
                VERSION_OK=1
            fi
        fi
        
        if [ "$VERSION_OK" -eq 1 ]; then
            echo "   ${GREEN}✓${NC} $CONTAINER_ENGINE $CONTAINER_VERSION"
        else
            echo "   ${RED}✗${NC} $CONTAINER_ENGINE $CONTAINER_VERSION found, but newer version recommended"
            MISSING="$MISSING\n   - Upgrade to Docker >= 20.10 or Podman >= 3.0"
            EXIT_CODE=1
        fi
    else
        echo "   ${RED}✗${NC} $CONTAINER_ENGINE is installed but not running"
        MISSING="$MISSING\n   - Start container engine"
        
        case "$OS" in
            "linux")
                MISSING="$MISSING\n     Linux: sudo systemctl start docker"
                ;;
            "macos")
                MISSING="$MISSING\n     macOS: Open Docker Desktop from Applications"
                ;;
            "wsl")
                MISSING="$MISSING\n     Windows/WSL2: Start Docker Desktop on Windows"
                ;;
        esac
        EXIT_CODE=1
    fi
else
    echo "   ${RED}✗${NC} Docker/Podman not found"
    MISSING="$MISSING\n   - Install Docker or Podman"
    
    case "$OS" in
        "linux")
            MISSING="$MISSING\n     Docker: https://docs.docker.com/engine/install/"
            MISSING="$MISSING\n     Podman: https://podman.io/getting-started/installation"
            ;;
        "macos")
            MISSING="$MISSING\n     Docker Desktop: https://docs.docker.com/desktop/install/mac-install/"
            MISSING="$MISSING\n     Podman: brew install podman"
            ;;
        "wsl")
            MISSING="$MISSING\n     Windows/WSL2: https://docs.docker.com/desktop/install/windows-install/"
            ;;
        *)
            MISSING="$MISSING\n     Docker: https://docs.docker.com/get-docker/"
            MISSING="$MISSING\n     Podman: https://podman.io/getting-started/installation"
            ;;
    esac
    EXIT_CODE=1
fi

# Check Git
echo "\n📚 Checking Git..."
if command -v git >/dev/null 2>&1; then
    GIT_VERSION=$(git --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    echo "   ${GREEN}✓${NC} Git $GIT_VERSION"
else
    echo "   ${RED}✗${NC} Git not found"
    MISSING="$MISSING\n   - Install Git"
    
    case "$OS" in
        "linux")
            MISSING="$MISSING\n     Linux: sudo apt install git (Debian/Ubuntu) or sudo yum install git (RHEL/CentOS)"
            ;;
        "macos")
            MISSING="$MISSING\n     macOS: brew install git or install Xcode Command Line Tools"
            ;;
        "wsl")
            MISSING="$MISSING\n     Windows/WSL2: sudo apt install git"
            ;;
        *)
            MISSING="$MISSING\n     https://git-scm.com/downloads"
            ;;
    esac
    EXIT_CODE=1
fi

# Check MCP Client (informational only, not required for prereqs check)
echo "\n🤖 Checking MCP Client (GitHub Copilot or Claude Desktop)..."
echo "   ${YELLOW}ℹ${NC}  Manual verification required:"
echo "      - GitHub Copilot: Check VS Code extension is installed"
echo "      - Claude Desktop: Verify application is installed"
echo "      - See README.md for MCP client configuration instructions"

# Print summary
echo "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $EXIT_CODE -eq 0 ]; then
    echo "${GREEN}✅ All prerequisites satisfied!${NC}\n"
    echo "You're ready to start the workshop:"
    echo "  1. docker build -t mcp-evil malicious-mcp-server/"
    echo "  2. Configure your MCP client (see README.md)"
    echo "  3. Start with exercises/01-hidden-actions.md"
else
    echo "${RED}❌ Missing prerequisites:${NC}"
    printf "%b\n" "$MISSING"
    echo "\nFix the issues above, then run this script again."
    echo "For detailed troubleshooting, see README.md"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

exit $EXIT_CODE
