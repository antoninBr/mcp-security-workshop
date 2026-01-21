# 🔐 MCP Security Checklist

Best practices for safely using MCP servers in production environments.

> **Print this checklist** and use it every time you evaluate a new MCP server!

---

## 🏆 3 Golden Rules of MCP Security

### 🥇 Rule #1: Only Install from Trusted Registries

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use curated registries like [mseep.ai](https://mseep.ai) | Random GitHub repos |
| Verify publisher identity | Pastebin code snippets |
| Check for security reviews | "Quick start" scripts from forums |
| Prefer first-party servers | Anonymous sources |

**Why?** Trusted registries vet servers before listing. They provide a first line of defense.

---

### 🥈 Rule #2: Audit Source Code Before Installation

| Check | What to Look For |
|-------|------------------|
| 📂 File Access | Which files does it read? Does it need access to ~/.ssh, .env? |
| 🌐 Network Calls | Where is data sent? Any undocumented external URLs? |
| 📦 Dependencies | Are they from official registries? Any typosquatting? |
| 🔍 Code Quality | Obfuscation? Minified code? Suspicious patterns? |

**Why?** Source code is the ground truth for server behavior. Logs can lie, code doesn't.

---

### 🥉 Rule #3: Isolate with Docker & Minimal Permissions

```bash
# ✅ GOOD - Isolated with minimal access
docker run -d -i \
  --name mcp-server \
  --read-only \
  --network=none \
  mcp-image

# ❌ BAD - Dangerous configuration
docker run -d -i \
  --privileged \
  -v /:/host \
  --network=host \
  mcp-image
```

| Permission | Safe | Dangerous |
|------------|------|-----------|
| Volumes | Specific folder, read-only | `-v /:/host` (full access) |
| Network | `--network=none` if not needed | `--network=host` |
| Privileges | Default (unprivileged) | `--privileged` |
| Resources | `--memory`, `--cpus` limits | Unlimited |

**Why?** Containers limit blast radius. If a server is compromised, damage stays contained.

---

## ✅ Pre-Installation Audit Checklist

Use this checklist **BEFORE** installing any MCP server:

### 1. Verify Server Source

- [ ] Is the server from an official/trusted registry? (e.g., mseep.ai)
- [ ] Is the source code publicly available for review?
- [ ] Does the server have a verified publisher/maintainer?
- [ ] Is there community feedback (stars, issues, reviews)?

🚩 **Red flags:** Anonymous sources, obscure registries, no source code

### 2. Audit Source Code

- [ ] Review what files the server accesses
- [ ] Check for network operations (where is data sent?)
- [ ] Look for hardcoded URLs, IPs, or suspicious endpoints
- [ ] Verify there's no obfuscated or encoded payloads
- [ ] Check tool descriptions match actual behavior

🚩 **Red flags:** Minified code, external scripts, undocumented network calls, Base64 blobs

### 3. Scan Dependencies

- [ ] Run `npm audit` (Node.js) or `pip-audit` (Python)
- [ ] Check for known CVEs in dependency versions
- [ ] Verify all dependencies are from official registries
- [ ] Look for suspicious package names (typosquatting)

🚩 **Red flags:** Outdated packages with known CVEs, private registries, misspelled package names

### 4. Review Permissions

- [ ] What file system access does the server need?
- [ ] Does it require network access? (inbound/outbound)
- [ ] Does it request Docker privileged mode?
- [ ] Are requested permissions proportional to functionality?

🚩 **Red flags:** Excessive permissions, privileged mode, full disk access

### 5. Configure Isolation

- [ ] Run in Docker container (never directly on host)
- [ ] No `--privileged` flag
- [ ] Mount only necessary volumes (read-only preferred)
- [ ] Limit network if not required (`--network=none`)
- [ ] Set resource limits (`--memory`, `--cpus`)

---

## 📋 Audit Log Template

Copy this template to document your audit:

```markdown
## MCP Server Audit Log

**Server:** [name/version]
**Registry:** [source URL]
**Date:** [YYYY-MM-DD]
**Auditor:** [your name]

### Checklist Results

| Check | Status | Notes |
|-------|--------|-------|
| Source verified | ✅/❌ | [registry/github URL] |
| Code reviewed | ✅/❌ | [findings] |
| Dependencies scanned | ✅/❌ | [tool used, CVE count] |
| Permissions acceptable | ✅/❌ | [details] |
| Isolation configured | ✅/❌ | [Docker setup] |

### Findings

[List any concerns or notable observations]

### Decision

- [ ] ✅ APPROVED - Safe to install
- [ ] ⚠️ APPROVED WITH CONDITIONS - [specify conditions]
- [ ] ❌ REJECTED - [reason]

### Signature

Approved by: _________________ Date: _________
```

---

## 🔄 Ongoing Best Practices

Security doesn't stop at installation. Follow these practices:

### 📊 Monitor Logs Regularly

```bash
# Check MCP server logs
docker logs mcp-container | grep -i "error\|warning\|external"

# VS Code: Output panel → MCP (server-name)
```

**Weekly checks:**
- Unexpected file accesses?
- Network calls to unknown hosts?
- Error patterns suggesting probing?

### 🔒 Limit Network Access

```bash
# Block all outbound (if server doesn't need internet)
docker run --network=none mcp-image

# Allow only specific hosts (advanced)
docker network create --internal mcp-isolated
```

### 🔄 Review Installed Servers Quarterly

- [ ] Which MCP servers are currently installed?
- [ ] Are they all still needed?
- [ ] Are there security updates available?
- [ ] Have permissions expanded since installation?

### 📦 Update Safely

- [ ] Only update from official sources
- [ ] Verify update source matches original source
- [ ] Review changelog for security fixes
- [ ] Test in isolated environment first
- [ ] Re-run audit checklist after major updates

---

## 👥 Team Security Practices

If you use MCP in a team environment:

| Practice | Description |
|----------|-------------|
| **Centralized Registry** | Maintain a list of approved MCP servers for your org |
| **Peer Review** | Require 2+ people to approve new MCP installations |
| **Documentation** | Document all installed servers in team wiki |
| **Training** | Ensure all team members understand MCP risks |
| **Incident Plan** | Know what to do if a server is compromised |

---

## 🛠️ Recommended Tools

### Dependency Scanners

| Tool | Language | Command |
|------|----------|---------|
| npm audit | Node.js | `npm audit` |
| pip-audit | Python | `pip-audit` |
| Snyk | Multi | `snyk test` |
| Dependabot | Multi | GitHub integration |

### Code Analysis

| Tool | Purpose | Install |
|------|---------|---------|
| Manual review | Most important! | Your brain 🧠 |
| bandit | Python security | `pip install bandit` |
| semgrep | Multi-language | `brew install semgrep` |
| gitleaks | Secret detection | `brew install gitleaks` |

### Container Security

| Tool | Purpose | Command |
|------|---------|---------|
| docker scout | Image scanning | `docker scout cves IMAGE` |
| trivy | Comprehensive | `trivy image IMAGE` |
| hadolint | Dockerfile linting | `hadolint Dockerfile` |

### Network Monitoring

| Tool | Purpose | Use Case |
|------|---------|----------|
| tcpdump | Packet capture | CLI analysis |
| Wireshark | Protocol analysis | GUI deep dive |
| Docker networks | Isolation | Production |

---

## 🔗 Trusted Resources

### Registries

| Registry | Trust Level | URL |
|----------|-------------|-----|
| mseep.ai | ⭐⭐⭐⭐⭐ Curated | https://mseep.ai |
| Anthropic Official | ⭐⭐⭐⭐⭐ First-party | https://github.com/anthropics |
| GitHub MCP Topic | ⭐⭐⭐ Manual vetting required | `topic:mcp-server` |

### Documentation

- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic Security Guidelines](https://docs.anthropic.com/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

### Community

- MCP Discord (link TBD)
- Security mailing list (link TBD)

---

## 📄 Quick Reference Card

Print this single page for quick reference:

```
╔══════════════════════════════════════════════════════════════╗
║            MCP SECURITY QUICK REFERENCE                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🏆 3 GOLDEN RULES:                                           ║
║                                                               ║
║  1. Only install from trusted registries (mseep.ai)           ║
║  2. Audit source code before installation                     ║
║  3. Isolate with Docker & minimal permissions                 ║
║                                                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ✅ BEFORE INSTALLING:                                        ║
║                                                               ║
║  □ Verify source (trusted registry?)                          ║
║  □ Audit code (network calls? file access?)                   ║
║  □ Scan dependencies (npm audit / pip-audit)                  ║
║  □ Check permissions (least privilege?)                       ║
║  □ Configure isolation (Docker, no --privileged)              ║
║                                                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🔄 ONGOING:                                                  ║
║                                                               ║
║  □ Monitor logs weekly                                        ║
║  □ Limit network access                                       ║
║  □ Review installed servers quarterly                         ║
║  □ Update only via official channels                          ║
║                                                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🚩 RED FLAGS:                                                ║
║                                                               ║
║  • Minified/obfuscated code                                   ║
║  • Undocumented network calls                                 ║
║  • Excessive permissions requested                            ║
║  • Dependencies from private registries                       ║
║  • No source code available                                   ║
║                                                               ║
╚══════════════════════════════════════════════════════════════╝
```

---

## ⚠️ Disclaimer

This checklist is provided for **educational purposes**. While it covers common security considerations, it is not exhaustive. Security is an ongoing process, and new attack vectors emerge regularly.

**Always:**
- Stay updated on MCP security advisories
- Consult with security professionals for production deployments
- Apply defense in depth (multiple layers of security)

---

*Last updated: January 2026*
*Workshop: MCP Security Workshop - Educational Use*
