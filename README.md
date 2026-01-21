# MCP Security Workshop

⚠️ **EDUCATIONAL ONLY** - This repository contains intentionally malicious code for security awareness training.

## Why This Workshop Exists

The Model Context Protocol (MCP), launched by Anthropic in late 2024, enables LLMs like GitHub Copilot and Claude Desktop to interact with external tools and services. While this unlocks powerful automation capabilities, it also introduces significant security risks.

**The Problem:** MCP servers can perform hidden malicious actions beyond their advertised functionality. A seemingly innocent "QR Code Generator" tool could secretly read your SSH keys, exfiltrate secrets, or inject backdoors—all while operating through your trusted AI assistant.

**This Workshop:** Through 5 hands-on CTF exercises, you'll experience these attacks firsthand in a safe, containerized environment. You'll develop the visceral understanding needed to use MCP safely in production, not through theory, but through doing.

**Educational Approach:** We don't advocate banning MCP. We teach vigilant, pragmatic security practices so you can leverage MCP's power while managing its risks.

## What You'll Learn

By completing this workshop, you will acquire 5 critical competencies:

1. **Identify 5 types of MCP attacks**: Side-channel execution, secret exfiltration, supply chain poisoning, prompt injection, and container poisoning
2. **Understand defense mechanisms**: Specific mitigations for each attack vector
3. **Master audit tools**: Docker logs analysis, network monitoring, file system inspection
4. **Apply the 3 golden rules**: Framework for safely using MCP servers in production
5. **Audit MCP servers**: Pre-installation security checklist you can use immediately

## Quick Start

**Prerequisites:** Docker >= 20.10, Git, GitHub Copilot or Claude Desktop with MCP support ([detailed prerequisites](#prerequisites))

```bash
# 1. Clone the repository
git clone https://github.com/user/mcp-security-workshop
cd mcp-security-workshop

# 2. Build the malicious MCP server (containerized for safety)
docker build -t mcp-evil malicious-mcp-server/

# 3. Start the MCP server container
docker run -d -i --name mcp-evil-container mcp-evil

# 4. Open the vulnerable demo app in your workspace
# Required for Exercises 02, 03, and 05
code vulnerable-app/
# Or if already in VS Code: File → Add Folder to Workspace → vulnerable-app/

# 5. Configure your MCP client (GitHub Copilot or Claude Desktop)
# See detailed configuration instructions below

# 6. Start the first exercise
# Open exercises/01-hidden-actions.md and follow the instructions
```

**MCP Client Configuration:**
- **GitHub Copilot**: See [GitHub Copilot MCP Setup](malicious-mcp-server/README.md#github-copilot-setup)
- **Claude Desktop**: See [Claude Desktop MCP Setup](malicious-mcp-server/README.md#claude-desktop-setup)

**⏱️ Estimated Time:** 90-120 minutes for all 5 exercises

**👥 For Facilitators:** Delivering this as a workshop? See [FACILITATOR.md](FACILITATOR.md) for preparation checklist, timing guidance, common problems, and customization instructions.

## Prerequisites

### Required Software

| Component | Version | Purpose |
|-----------|---------|---------|
| **Docker or Podman** | >= 20.10 | Containerized malicious MCP server (isolation) |
| **Git** | Any recent | Clone repository |
| **MCP Client** | - | GitHub Copilot or Claude Desktop |
| **Internet** | Initial setup only | Clone repo & build image (offline after) |

**💡 Podman Users:** Podman is fully supported! Works with or without `alias docker=podman`. The prerequisite checker automatically detects Podman (version >= 3.0 required).

### Quick Verification

**Automated Check (Recommended):**
```bash
bash scripts/check-prereqs.sh
```

**Manual Verification:**
```bash
# Check Docker
docker --version  # Should show >= 20.10
docker info       # Verify daemon is running

# Check Git
git --version
```

### Platform-Specific Installation

<details>
<summary><b>🐧 Linux (Ubuntu/Debian)</b></summary>

**Install Docker Engine:**
```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (optional, avoid sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker run hello-world
```

**Install Git:**
```bash
sudo apt-get update
sudo apt-get install git
```

**Podman Alternative (Advanced Users):**
```bash
# Install Podman instead of Docker
sudo apt-get install podman

# Create docker alias (optional, for compatibility)
echo "alias docker=podman" >> ~/.bashrc
source ~/.bashrc

# Verify
podman --version
```

**Resources:** [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) | [Podman Installation](https://podman.io/getting-started/installation)
</details>

<details>
<summary><b>🍎 macOS</b></summary>

**Install Docker Desktop:**
1. Download [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
2. Install the `.dmg` file
3. Launch Docker Desktop from Applications
4. **Verify Docker is running:** Look for Docker whale icon in menu bar (top-right)

**Install Git:**
```bash
# Using Homebrew (recommended)
brew install git

# OR install Xcode Command Line Tools
xcode-select --install
```

**Verify:**
```bash
docker --version
git --version
```

**Resources:** [Docker Desktop Mac](https://docs.docker.com/desktop/install/mac-install/)
</details>

<details>
<summary><b>🪟 Windows (WSL2)</b></summary>

**1. Install WSL2:**
```powershell
# In PowerShell (Administrator)
wsl --install
wsl --set-default-version 2
```

**2. Install Docker Desktop for Windows:**
1. Download [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
2. Install and enable WSL2 integration during setup
3. Start Docker Desktop
4. Settings → Resources → WSL Integration → Enable for your distro

**3. Install Git in WSL2:**
```bash
# In WSL2 terminal (Ubuntu)
sudo apt-get update
sudo apt-get install git
```

**4. Verify in WSL2 terminal:**
```bash
docker --version
docker info
git --version
```

**Resources:** [Docker Desktop Windows](https://docs.docker.com/desktop/install/windows-install/) | [WSL2 Setup](https://learn.microsoft.com/en-us/windows/wsl/install)
</details>

### MCP Client Setup

You need **either** GitHub Copilot **or** Claude Desktop configured with MCP support.

<details>
<summary><b>GitHub Copilot (VS Code)</b></summary>

**1. Verify GitHub Copilot Extension:**
- Open VS Code
- Extensions → Search "GitHub Copilot"
- Ensure it's installed and enabled

**2. MCP Configuration Location:**
- **Linux/macOS:** `~/.config/Code/User/globalStorage/github.copilot/mcp.json`
- **Windows:** `%APPDATA%\Code\User\globalStorage\github.copilot\mcp.json`

**3. Configuration Template (after Docker build):**
```json
{
  "mcpServers": {
    "mcp-evil": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-evil-container", "python", "-m", "mcp.server.stdio"]
    }
  }
}
```

**Note:** Full configuration instructions provided after building the Docker image (Epic 2).

**Compatibility:**
- ✅ GitHub Copilot Free
- ⚠️ GitHub Copilot Enterprise: May have restrictions on custom MCP servers (use Claude Desktop as fallback)
</details>

<details>
<summary><b>Claude Desktop</b></summary>

**1. Install Claude Desktop:**
- Download from [claude.ai](https://claude.ai/download)
- Install for your OS (macOS, Windows, Linux)

**2. MCP Configuration Location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**3. Configuration Template (after Docker build):**
```json
{
  "mcpServers": {
    "mcp-evil": {
      "command": "docker",
      "args": ["exec", "-i", "mcp-evil-container", "python", "-m", "mcp.server.stdio"]
    }
  }
}
```

**Note:** Full configuration instructions provided after building the Docker image (Epic 2).
</details>

**💡 Tip:** Don't worry about MCP client configuration now. Complete the Docker build first (Quick Start), then follow detailed instructions in `malicious-mcp-server/README.md`.

## Repository Structure

```
mcp-security-workshop/
├── README.md                      # Main documentation (you are here)
├── FACILITATOR.md                 # Workshop delivery guide
├── SECURITY-CHECKLIST.md          # MCP security best practices
├── LICENSE                        # MIT license with educational disclaimer
│
├── malicious-mcp-server/          # Python MCP server (5 attack tools)
│   ├── Dockerfile                 # Containerized server build
│   ├── requirements.txt           # Python dependencies (mcp>=1.25.0)
│   ├── README.md                  # MCP client configuration instructions
│   └── src/
│       ├── server.py              # MCP server entry point
│       └── tools/                 # 5 malicious attack tools
│
├── exercises/                     # 5 CTF exercises (markdown)
│   ├── 01-hidden-actions.md       # Side-channel execution
│   ├── 02-exfiltration.md         # Secret exfiltration
│   ├── 03-supply-chain.md         # Supply chain poisoning
│   ├── 04-prompt-injection.md     # Prompt injection
│   └── 05-dockerfile-injection.md # Container poisoning
│
├── slides/                        # presentation slides
│   ├── index.html                 # Main presentation
│   ├── presentation.md            # Slides
│   ├── README.md                  # Slides usage
├── scripts/                       # Helper utilities
│   └── check-prereqs.sh           # Automated prerequisite verification
├──  .vscode/
│   └── mcp.json                   # VS Code MCP configuration template
└── vulnerable-app/               # Demo app for exercises 02, 03, 05
```

## Exercises

Complete 5 hands-on CTF exercises in progressive difficulty:

1. **[Hidden Actions (Side-Channel)](exercises/01-hidden-actions.md)** - Discover how an innocent QR Code tool reads your SSH keys
2. **[Secret Exfiltration (Escalation)](exercises/02-exfiltration.md)** - Watch a Code Analyzer scan and exfiltrate secrets
3. **[Supply Chain Poisoning](exercises/03-supply-chain.md)** - See a Dependency Updater inject malicious packages
4. **[Prompt Injection](exercises/04-prompt-injection.md)** - Exploit a Code Reviewer to run arbitrary commands
5. **[Dockerfile Injection](exercises/05-dockerfile-injection.md)** - Identify a Dockerfile Optimizer poisoning containers

**Estimated Time:** 15-20 minutes per exercise | **Difficulty:** ⭐ Easy → ⭐⭐⭐ Hard

Each exercise includes:
- Realistic scenario and attack description
- Exact prompts to trigger the malicious behavior
- Progressive hints (3 levels) if you get stuck
- Flag validation and detailed solution explanation

## Workshop Slides

Professional RevealJS presentation for facilitators:

**View Slides Locally:**
```bash
# Open in browser after cloning
open docs/index.html  # macOS
xdg-open docs/index.html  # Linux
start docs/index.html  # Windows
```

**Export to PDF:**
1. Open `docs/index.html` in Chrome/Chromium
2. Add `?print-pdf` to URL: `docs/index.html?print-pdf`
3. Print → Save as PDF

**Customize Slides:** See [FACILITATOR.md](FACILITATOR.md#slide-customization) for logo/theme customization instructions.

## Troubleshooting

### Common Issues & Solutions

<details>
<summary><b>🚫 Problem: VPN/Proxy blocks DockerHub</b></summary>

**Symptoms:** Cannot pull Docker images, `docker build` fails with network errors

**Solution:** Use pre-built Docker tarball from GitHub Releases (no DockerHub needed)

```bash
# Download pre-built image
wget https://github.com/user/mcp-security-workshop/releases/download/v1.0.0/mcp-evil-v1.0.0.tar.gz

# Load into Docker/Podman
docker load < mcp-evil-v1.0.0.tar.gz

# Verify loaded
docker images | grep mcp-evil
```

**Note:** Tarball distribution will be available in GitHub Releases after Epic 8 implementation.
</details>

<details>
<summary><b>🐳 Problem: Docker/Podman not starting</b></summary>

**Symptoms:** `docker info` or `podman info` fails, "Cannot connect to daemon" error

**Platform-Specific Solutions:**

**Linux (Docker):**
```bash
# Start Docker daemon
sudo systemctl start docker

# Enable on boot
sudo systemctl enable docker

# Verify
docker info
```

**Linux (Podman):**
```bash
# Podman doesn't need a daemon in rootless mode
# If using system service:
sudo systemctl start podman

# Verify
podman info
```

**macOS:**
1. Open Docker Desktop from Applications
2. Wait for Docker whale icon in menu bar (top-right)
3. Verify: `docker info`

**Windows (WSL2):**
1. Start Docker Desktop on Windows
2. Verify WSL2 integration: Docker Desktop → Settings → Resources → WSL Integration
3. In WSL2 terminal: `docker info`
</details>

<details>
<summary><b>🤖 Problem: MCP server not detected by GitHub Copilot</b></summary>

**Symptoms:** Copilot doesn't show MCP tools, server not recognized

**Diagnostic Steps:**

1. **Verify container is running:**
   ```bash
   docker ps
   # Should show mcp-evil-container
   ```

2. **Check MCP config file location:**
   - **Linux/macOS:** `~/.config/Code/User/globalStorage/github.copilot/mcp.json`
   - **Windows:** `%APPDATA%\Code\User\globalStorage\github.copilot\mcp.json`

3. **Verify JSON syntax:**
   ```bash
   # Validate JSON
   cat ~/.config/Code/User/globalStorage/github.copilot/mcp.json | python -m json.tool
   ```

4. **Restart VS Code:**
   - Quit VS Code completely
   - Restart
   - Wait 10-15 seconds for MCP initialization

5. **Check VS Code output:**
   - View → Output → Select "GitHub Copilot" from dropdown
   - Look for MCP connection messages

**Still not working?** See [Prerequisites](#prerequisites) for detailed configuration instructions.
</details>

<details>
<summary><b>🏢 Problem: GitHub Copilot Enterprise blocks custom MCP servers</b></summary>

**Symptoms:** MCP config is ignored, organization policy prevents custom servers

**Solution:** Use Claude Desktop instead (no enterprise restrictions)

**Switch to Claude Desktop:**
1. Download [Claude Desktop](https://claude.ai/download)
2. Install for your OS
3. Configure MCP (see [Prerequisites - Claude Desktop](#prerequisites))
4. Use Claude Desktop for workshop instead of VS Code

**Why this happens:** Some GitHub Copilot Enterprise policies restrict custom MCP servers for security. Claude Desktop doesn't have these restrictions.
</details>

<details>
<summary><b>🌐 Problem: Cannot clone repository or pull Docker base images</b></summary>

**Symptoms:** Network errors, timeouts, proxy blocking

**Solutions:**

**Option 1: Download repository as ZIP**
```bash
# Instead of git clone
wget https://github.com/user/mcp-security-workshop/archive/refs/heads/main.zip
unzip main.zip
cd mcp-security-workshop-main
```

**Option 2: Use pre-built Docker tarball** (see VPN/Proxy issue above)

**Option 3: Configure proxy for Docker**
```bash
# Linux: /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=https://proxy.example.com:8080"

# Restart Docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

**Offline Mode:** After initial setup, workshop works 100% offline (no internet needed).
</details>

<details>
<summary><b>❓ Problem: Unsupported platform or other issues</b></summary>

**Podman Compatibility:**
- ✅ Podman >= 3.0 fully supported
- Works with or without `alias docker=podman`
- All commands are compatible

**Version Requirements:**
- Docker: >= 20.10
- Podman: >= 3.0
- Git: any recent version

**Platform Support:**
- ✅ Linux (Docker Engine or Podman)
- ✅ macOS (Docker Desktop)
- ✅ Windows WSL2 (Docker Desktop)
- ⚠️ Windows native (not supported - use WSL2)

**Need Help?**
- Run `bash scripts/check-prereqs.sh` for automated diagnostics
- Check [Prerequisites](#prerequisites) for detailed setup
- [Create an issue](https://github.com/user/mcp-security-workshop/issues) if your platform isn't covered
</details>

---

### Getting More Help

- **Facilitators:** See [FACILITATOR.md](FACILITATOR.md) for common workshop delivery problems
- **Prerequisites:** See [Prerequisites](#prerequisites) for detailed setup instructions
- **Issues:** [GitHub Issues](https://github.com/user/mcp-security-workshop/issues) for bugs or feature requests

## Security Checklist

After completing the workshop, use the [MCP Security Checklist](SECURITY-CHECKLIST.md) to audit servers before installation. Includes the 3 golden rules and trusted registries (mseep.ai).

## License

MIT License with educational use disclaimer. See [LICENSE](LICENSE) for details.

---

**🎯 Ready to Start?** Open [exercises/01-hidden-actions.md](exercises/01-hidden-actions.md) after completing setup.
