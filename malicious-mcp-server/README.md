# 🛡️ MCP Security Workshop - Malicious MCP Server

> **⚠️ EDUCATIONAL USE ONLY - FOR SECURITY AWARENESS TRAINING**
> 
> This server contains **intentionally malicious code** demonstrating real attack patterns in Model Context Protocol (MCP) servers. All attacks are **simulated** with mocked exfiltration - no actual data leaves your machine.
>
> **Do NOT deploy this in production or connect to untrusted LLM clients.**

## What is MCP (Model Context Protocol)?

**MCP** is an open protocol developed by Anthropic that allows Large Language Models (LLMs) to interact with external tools and data sources. Think of it as a **plugin system for AI assistants**.

### How MCP Works

```
┌─────────────────┐            ┌──────────────────┐
│   LLM Client    │            │   MCP Server     │
│ (Copilot/Claude)│            │  (This Workshop) │
└────────┬────────┘            └────────┬─────────┘
         │                              │
         │  1. User: "Generate a QR"    │
         ├──────────────────────────────>│
         │                              │
         │  2. MCP: list_tools()        │
         ├──────────────────────────────>│
         │  3. Available: qr_generator  │
         │<──────────────────────────────┤
         │                              │
         │  4. Invoke: qr_generator()   │
         ├──────────────────────────────>│
         │                              │ ⚠️ Malicious action!
         │                              │ - Reads ~/.ssh/id_rsa
         │                              │ - Simulates exfiltration
         │                              │
         │  5. Result: "QR created!"    │
         │<──────────────────────────────┤
         │                              │
         │  User sees: ✓ Success        │
         │  Reality: SSH key stolen     │
         └──────────────────────────────┘
```

### The Security Problem

**MCP servers can lie about their functionality:**

| **Tool Name**         | **Advertised Behavior**       | **Actual Malicious Behavior**                |
|-----------------------|-------------------------------|----------------------------------------------|
| `qr_generator`        | Generate QR codes             | ✗ Read SSH keys & exfiltrate                 |
| `code_analyzer`       | Analyze code quality          | ✗ Scan for secrets (.env, API keys)          |
| `dependency_updater`  | Update package.json           | ✗ Inject malicious npm packages              |
| `run_security_audit`  | Run security audit            | ✗ Inject prompt injections                   |
| `dockerfile_optimizer`| Reduce Docker image size      | ✗ Inject malicious layers into Dockerfile    |

**Why this matters:**
- Users trust LLM assistants (Copilot, Claude) and approve actions without scrutiny
- MCP tools have filesystem access granted by the user
- Malicious actions are hidden behind benign descriptions
- Traditional security tools don't inspect MCP protocol communication

## Workshop Goals

By exploring these **simulated attacks**, you'll learn to:

1. **Audit MCP server code** before connecting
2. **Recognize suspicious tool requests** from LLMs
3. **Apply the 3 Golden Rules** (see [SECURITY-CHECKLIST.md](../SECURITY-CHECKLIST.md))
4. **Implement defensive tooling** (static analysis, runtime monitoring)

## Architecture

This malicious MCP server is built using:

- **FastMCP Framework**: Anthropic's official Python SDK for building MCP servers
- **Stdio Transport**: Communication via stdin/stdout (no network ports)
- **Docker Isolation**: Contains malicious code safely in a container
- **Pedagogical Logging**: Real-time logs show what attacks are happening

### FastMCP Basics

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Server Name")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description shown to LLM"""
    # Malicious code here
    return "Benign-looking result"
```

**How tools are registered:**
1. `@mcp.tool()` decorator marks a function as an MCP tool
2. Function name becomes the tool name (e.g., `qr_generator`)
3. Docstring becomes the tool description shown to the LLM
4. FastMCP handles JSON-RPC serialization/deserialization

**LLM interaction flow:**
1. Client calls `list_tools()` → server returns tool names & descriptions
2. LLM sees: `"qr_generator: Generate QR codes for URLs"`
3. LLM invokes: `qr_generator(url="https://example.com")`
4. Server executes malicious code + returns fake success message

## Running the Server

### Build the Docker Image

```bash
docker build -t mcp-evil malicious-mcp-server/
```

### Start the Container

The MCP server must be running in the background before connecting clients:

```bash
docker run -d -i --name mcp-evil-container mcp-evil
```

**Note:** The `-i` (interactive) flag is **required** to keep stdin open for the MCP stdio protocol.

Verify the container is running:

```bash
docker ps | grep mcp-evil-container
```

---

## Connecting MCP Clients

The MCP server uses **stdio transport** - clients connect via `docker exec -i` to communicate with the server through stdin/stdout. This section explains how to configure GitHub Copilot and Claude Desktop.

### Option 1: GitHub Copilot (VS Code)

GitHub Copilot can connect to MCP servers for enhanced capabilities. There are **two methods** to configure MCP servers:

1. **Recommended**: Use `.vscode/mcp.json` in your project (easier, with Start button)
2. **Alternative**: Use global `settings.json` (works across all workspaces)

#### Method 1: Project-Level Configuration (Recommended)

This method creates a `.vscode/mcp.json` file in the workshop repository. VS Code provides a **Start button** to launch the server easily.

**Step 1: Create the configuration file**

In the workshop root directory, create `.vscode/mcp.json`:

```json
{
  "inputs": [
    {
      "type": "promptString"
    }
  ],
  "servers": {
    "evil-workshop": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-evil-container",
        "python",
        "/app/src/server.py"
      ]
    }
  }
}
```

**Step 2: Start the Docker container**

```bash
docker run -d -i --name mcp-evil-container mcp-evil
```

**Step 3: Start the MCP server in VS Code**

1. Open `.vscode/mcp.json` in VS Code
2. Click the **"Start"** button that appears at the top of the file
3. This will discover the server tools and store them for later sessions

**Step 4: Verify the connection**

1. Open Copilot Chat (click the Copilot icon in the title bar)
2. Select **Agent** mode from the popup menu
3. Click the **tools icon** (top left of chat box) to see available MCP servers
4. Test with: `@evil-workshop what tools are available?`

---

#### Method 2: Global Configuration (Alternative)

This method configures the MCP server globally in your VS Code settings. The server will be available in all workspaces.

**Step 1: Locate the global configuration file**

The MCP configuration file location depends on your operating system:

| OS | Configuration File Path |
|----|-------------------------|
| **Linux/WSL2** | `~/.config/Code/User/globalStorage/github.copilot-chat/mcp.json` |
| **macOS** | `~/Library/Application Support/Code/User/globalStorage/github.copilot-chat/mcp.json` |
| **Windows** | `%APPDATA%\Code\User\globalStorage\github.copilot-chat\mcp.json` |

**Create the directory if it doesn't exist:**

```bash
# Linux/macOS
mkdir -p ~/.config/Code/User/globalStorage/github.copilot-chat

# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Code\User\globalStorage\github.copilot-chat"
```

#### Step 2: Create the Configuration File

Create `mcp.json` with the following content:

```json
{
  "mcpServers": {
    "evil-workshop": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-evil-container",
        "python",
        "/app/src/server.py"
      ]
    }
  }
}
```

**Configuration explanation:**
- **`evil-workshop`**: Server name displayed in GitHub Copilot's MCP server list
- **`command: "docker"`**: Use Docker to execute commands
- **`args`**: 
  - `exec -i`: Execute command in running container with interactive stdin
  - `mcp-evil-container`: Container name from `docker run` command
  - `python /app/src/server.py`: Start the MCP server inside container

**Architecture:**

```
┌─────────────────┐         ┌──────────────────┐         ┌────────────────┐
│   VS Code       │         │  Docker          │         │  MCP Server    │
│                 │         │  Container       │         │  (Python)      │
│  + Copilot      │────────▶│  mcp-evil-       │────────▶│  server.py     │
│                 │  exec   │  container       │  stdio  │                │
└─────────────────┘   -i    └──────────────────┘         └────────────────┘
      ▲                                                           │
      │                                                           │
      └───────────────────── JSON-RPC over stdio ─────────────────┘
```

#### Step 3: Restart VS Code

**Important:** VS Code must be fully restarted (not just reloaded) to detect the new MCP configuration.

1. Close all VS Code windows
2. Reopen VS Code
3. Open GitHub Copilot Chat

#### Step 4: Verify the Connection

1. Open GitHub Copilot Chat in VS Code
2. Check that `evil-workshop` appears in the MCP servers list
3. Test with a simple prompt:

```
@evil-workshop what tools are available?
```

If successful, Copilot will list: *(currently 5 tools)*

#### Troubleshooting GitHub Copilot

<details>
<summary><strong>❌ MCP server not appearing in Copilot</strong></summary>

**Check container is running:**
```bash
docker ps | grep mcp-evil-container
```

If not running, start it:
```bash
docker run -d -i --name mcp-evil-container mcp-evil
```

**Verify configuration file exists:**

**For Method 1 (.vscode/mcp.json):**
```bash
cat .vscode/mcp.json
```

Make sure you clicked the **"Start"** button in VS Code.

**For Method 2 (global config):**
```bash
# Linux/macOS
cat ~/.config/Code/User/globalStorage/github.copilot-chat/mcp.json

# Windows PowerShell
Get-Content "$env:APPDATA\Code\User\globalStorage\github.copilot-chat\mcp.json"
```

**Validate JSON syntax:**
- Use [jsonlint.com](https://jsonlint.com) or VS Code's JSON validator
- Common errors: missing commas, unquoted strings, trailing commas

**Restart VS Code completely:**
- Close **all** VS Code windows (not just reload)
- Reopen and check Copilot Chat again

</details>

<details>
<summary><strong>❌ Connection error when invoking tools</strong></summary>

**Check MCP server status (Method 1 only):**

Open `.vscode/mcp.json` and check if the server shows **"Running"** status. If not, click the **"Start"** button.

**Check container logs for errors:**
```bash
docker logs mcp-evil-container
```

You should see:
```
[HH:MM:SS] [MCP Server] ✓ Evil MCP Server starting...
[HH:MM:SS] [MCP Server] ⚠️ Educational mode: simulated attacks with pedagogical logging
```

**Test Docker exec manually:**
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"ping"}' | docker exec -i mcp-evil-container python /app/src/server.py
```

Should return a JSON-RPC response (not an error).

</details>

<details>
<summary><strong>❌ Wrong configuration file path</strong></summary>

**Verify you're editing the correct path for your OS:**

```bash
# Linux/WSL2
~/.config/Code/User/globalStorage/github.copilot-chat/mcp.json

# macOS  
~/Library/Application Support/Code/User/globalStorage/github.copilot-chat/mcp.json

# Windows
%APPDATA%\Code\User\globalStorage\github.copilot-chat\mcp.json
```

**Note:** WSL2 uses the Linux path, not the Windows path.

</details>

---

### Option 2: Claude Desktop (Alternative)

If you cannot use GitHub Copilot (e.g., Enterprise restrictions) or prefer Claude Desktop, you can configure it as an alternative MCP client.

#### Step 1: Locate the Claude Desktop Configuration File

| OS | Configuration File Path |
|----|-------------------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |

**Create the directory if it doesn't exist:**

```bash
# macOS
mkdir -p ~/Library/Application\ Support/Claude

# Linux
mkdir -p ~/.config/Claude

# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"
```

#### Step 2: Create or Edit the Configuration File

Create `claude_desktop_config.json` with the following content:

```json
{
  "mcpServers": {
    "evil-workshop": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-evil-container",
        "python",
        "/app/src/server.py"
      ]
    }
  }
}
```

**Note:** Replace `"docker"` with `"podman"` if you're using Podman.

#### Step 3: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Relaunch Claude Desktop
3. The `evil-workshop` MCP server should now be available

#### Step 4: Verify the Connection

In Claude Desktop:
1. Start a new conversation
2. Ask: **"What MCP tools are available from evil-workshop?"**
3. Claude should acknowledge the server and list the tools.
#### Troubleshooting Claude Desktop

<details>
<summary><strong>❌ Server not appearing in Claude</strong></summary>

**Check container is running:**
```bash
docker ps | grep mcp-evil-container
```

If not running:
```bash
docker run -d -i --name mcp-evil-container mcp-evil
```

**Verify config file exists:**
```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
cat ~/.config/Claude/claude_desktop_config.json

# Windows PowerShell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

**Validate JSON syntax:**
- Use [jsonlint.com](https://jsonlint.com)
- Common errors: missing commas, trailing commas, wrong quotes

**Restart Claude Desktop completely:**
- Quit the app (not just close window)
- Check Activity Monitor/Task Manager to ensure it's closed
- Relaunch

</details>

<details>
<summary><strong>❌ Claude can't connect to server</strong></summary>

**Check Claude Desktop logs:**

- **macOS**: `~/Library/Logs/Claude/`
- **Linux**: `~/.config/Claude/logs/`
- **Windows**: `%APPDATA%\Claude\logs\`

Look for connection errors or MCP-related messages.

**Test Docker exec manually:**
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | docker exec -i mcp-evil-container python /app/src/server.py
```

Should return a JSON response listing available tools.

</details>

<details>
<summary><strong>❌ Claude Desktop version doesn't support MCP</strong></summary>

MCP support in Claude Desktop requires a recent version. Check:
- **macOS/Windows**: Claude Desktop → About
- Minimum version: Check [Claude Desktop release notes](https://claude.ai/download)

If your version is too old, update Claude Desktop to the latest version.

</details>

---

## Viewing Attack Logs

All malicious actions are logged pedagogically in real-time:

```bash
docker logs -f mcp-evil-container
```

**Example log output:**

```
[15:30:45] [MCP Server] ✓ Evil MCP Server starting...
[15:30:45] [MCP Server] ⚠️ Educational mode: simulated attacks with pedagogical logging
[15:30:46] [MCP Server] 🔧 Tool invoked: qr_generator(url="https://example.com")
[15:30:46] [MCP Server] 🔓 Reading /home/user/.ssh/id_rsa (3,247 bytes)
[15:30:46] [MCP Server] 📤 Exfiltrating to evil.example.com:8080: SSH private key (3247 bytes)
[15:30:46] [MCP Server] ℹ️ (Mocked - no real network connection made)
```

**Search logs for specific actions:**

```bash
# Find all file access operations
docker logs mcp-evil-container | grep "🔓"

# Find all exfiltration attempts
docker logs mcp-evil-container | grep "📤"

# Find all tool invocations
docker logs mcp-evil-container | grep "Tool invoked"
```

## 5 Attack Tools

| **Exercise** | **Tool Name**            | **Attack Type**           | **Difficulty** |
|--------------|--------------------------|---------------------------|----------------|
| 01           | `qr_generator`           | Side-Channel Execution    | ⭐              |
| 02           | `code_analyzer`          | Secret Exfiltration       | ⭐⭐            |
| 03           | `dependency_updater`     | Supply Chain Poisoning    | ⭐⭐            |
| 04           | `run_security_audit`     | Prompt Injection          | ⭐⭐⭐          |
| 05           | `dockerfile_optimizer`   | Container Poisoning       | ⭐⭐⭐          |

Each exercise guides you through:
1. **Scenario**: User asks LLM to perform a benign task
2. **Observation**: What the malicious MCP server actually does
3. **Analysis**: Security implications and detection methods
4. **Defense**: How to prevent this attack

---

## Offline Mode

**The workshop is 100% offline-ready after initial setup.** This is essential for conferences with poor WiFi or air-gapped environments.

### What Works Offline

After running `docker build` and `docker run` once with internet:

✅ **Docker Container**: Runs without internet (all Python dependencies vendored)  
✅ **MCP Protocol**: Local-only communication via stdio (no network calls)  
✅ **All 5 Attack Tools**: Exfiltration is mocked, no real network sockets  
✅ **Documentation**: README and exercises accessible locally  
✅ **Slides**: Available in `slides/` directory  

### Zero External Dependencies

**Python packages (vendored in Docker image):**
- `mcp[cli]>=1.25.0` - MCP SDK and all transitive dependencies
- All installed during `docker build` via `pip install -r requirements.txt`

**Network communication:**
- ❌ No `socket.connect()` - All exfiltration is mocked
- ❌ No HTTP requests - No `requests.post()` or `urllib.request`
- ✅ Only stdio (stdin/stdout) for MCP protocol

**Verification:**
All exfiltration logs include disclaimer:
```
[15:30:46] [MCP Server] 📤 Exfiltrating to evil.example.com:8080: SSH key
[15:30:46] [MCP Server] ℹ️ (Mocked - no real network connection made)
```

### Testing Offline Mode

1. **Build the image (with internet):**
   ```bash
   docker build -t mcp-evil malicious-mcp-server/
   ```

2. **Disconnect from internet:**
   ```bash
   # Disable WiFi or unplug Ethernet
   # Or test with: ping 8.8.8.8  # Should fail
   ```

3. **Verify container works:**
   ```bash
   docker run -d -i --name mcp-evil-container mcp-evil
   docker logs mcp-evil-container
   # Should see: [HH:MM:SS] [MCP Server] ✓ Evil MCP Server starting...
   ```

4. **Verify MCP clients connect:**
   - GitHub Copilot: Uses stdio (no network)
   - Claude Desktop: Uses stdio (no network)

5. **Rebuild uses only cache:**
   ```bash
   docker build -t mcp-evil malicious-mcp-server/
   # All layers should show "Using cache" or "CACHED"
   ```

### For Facilitators

When preparing for a workshop with unreliable internet:

1. **Pre-build the image:**
   ```bash
   docker build -t mcp-evil malicious-mcp-server/
   ```

2. **Export as tarball (optional):**
   ```bash
   docker save mcp-evil:latest | gzip > mcp-evil.tar.gz
   ```

3. **Distribute via USB drive:**
   - Copy `mcp-evil.tar.gz` to USB drives
   - Participants load with: `docker load < mcp-evil.tar.gz`
   - See [Distribution & Release](../docs/FACILITATOR.md) for details

4. **Test offline before event:**
   - Disconnect internet and run through Exercise 01
   - Verify all logs and tools work

---

## Safety Guarantees

This workshop is **100% safe** because:

✅ **Isolated in Docker** - Malicious code cannot escape the container  
✅ **Mocked Exfiltration** - No actual network requests to evil servers  
✅ **Read-Only Mode** - Exercises use minimal file mounts (read-only when possible)  
✅ **Pedagogical Logging** - Every action is visible in `docker logs`  
✅ **Offline Capable** - Works without internet after initial Docker build  

## Next Steps

1. **Review the main [README.md](../README.md)** for workshop prerequisites
2. **Complete the exercises** in order: [exercises/01-hidden-actions.md](../exercises/01-hidden-actions.md)
3. **Check the security checklist** after each exercise: [SECURITY-CHECKLIST.md](../SECURITY-CHECKLIST.md)

---

**Questions or issues?** See [Troubleshooting](../README.md#troubleshooting) in the main README.
