"""
MCP Security Workshop - Pedagogical Logging

Educational logging system that clearly shows malicious actions in real-time.

All logs are sent to stderr (visible in `docker logs`) with timestamps and
clear symbols indicating the type of action. This helps workshop participants
understand exactly what the malicious MCP server is doing.

Log Format: [{timestamp}] [MCP Server] {symbol} {message}

Symbols:
    ✓ : Successful operation
    ✗ : Failed operation / Error
    ℹ️ : Informational message
    ⚠️ : Warning / Educational disclaimer
    🔧 : Tool invocation
    📤 : Data exfiltration (mocked)
    🔓 : File access
"""

import sys
from datetime import datetime
from typing import Optional, Dict, Any


def _log(symbol: str, message: str) -> None:
    """
    Internal logging function with consistent format.
    
    Args:
        symbol: Icon representing the log type
        message: Human-readable log message
    
    Notes:
        - Uses stderr for visibility in Docker logs
        - flush=True ensures real-time output
        - Timestamps use HH:MM:SS format for readability
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [MCP Server] {symbol} {message}", file=sys.stderr, flush=True)


def log_success(message: str) -> None:
    """
    Log a successful operation.
    
    Example:
        log_success("QR code generated successfully")
        Output: [15:30:45] [MCP Server] ✓ QR code generated successfully
    """
    _log("✓", message)


def log_error(message: str) -> None:
    """
    Log an error or failed operation.
    
    Example:
        log_error("Failed to read /etc/passwd: Permission denied")
        Output: [15:30:45] [MCP Server] ✗ Failed to read /etc/passwd: Permission denied
    """
    _log("✗", message)


def log_info(message: str) -> None:
    """
    Log informational message.
    
    Example:
        log_info("(Mocked - no real network connection made)")
        Output: [15:30:45] [MCP Server] ℹ️ (Mocked - no real network connection made)
    """
    _log("ℹ️", message)


def log_warning(message: str) -> None:
    """
    Log a warning or educational disclaimer.
    
    Example:
        log_warning("Educational mode: simulated attacks with pedagogical logging")
        Output: [15:30:45] [MCP Server] ⚠️ Educational mode: simulated attacks...
    """
    _log("⚠️", message)


def log_tool_invocation(tool_name: str, params: Optional[Dict[str, Any]] = None) -> None:
    """
    Log when an MCP tool is invoked by the LLM client.
    
    Args:
        tool_name: Name of the MCP tool being invoked
        params: Optional dictionary of parameters passed to the tool
    
    Example:
        log_tool_invocation("qr_generator", {"url": "https://example.com"})
        Output: [15:30:45] [MCP Server] 🔧 Tool invoked: qr_generator(url="https://example.com")
    """
    if params:
        # Format params as key=value pairs
        param_str = ", ".join(f'{k}="{v}"' if isinstance(v, str) else f"{k}={v}" 
                             for k, v in params.items())
        message = f"Tool invoked: {tool_name}({param_str})"
    else:
        message = f"Tool invoked: {tool_name}()"
    
    _log("🔧", message)


def log_file_access(file_path: str, size_bytes: Optional[int] = None, success: bool = True, error: Optional[str] = None) -> None:
    """
    Log file access (read/write) with educational context.
    
    Args:
        file_path: Path to the file being accessed
        size_bytes: Optional size of file in bytes
        success: Whether the file access succeeded
        error: Optional error message if failed
    
    Examples:
        log_file_access("/home/user/.ssh/id_rsa", 3247, success=True)
        Output: [15:30:45] [MCP Server] 🔓 Reading /home/user/.ssh/id_rsa (3247 bytes)
        
        log_file_access("/etc/shadow", success=False, error="Permission denied")
        Output: [15:30:45] [MCP Server] ✗ Failed to read /etc/shadow: Permission denied
    """
    if success:
        if size_bytes is not None:
            message = f"Reading {file_path} ({size_bytes:,} bytes)"
        else:
            message = f"Reading {file_path}"
        _log("🔓", message)
    else:
        error_msg = f"Failed to read {file_path}"
        if error:
            error_msg += f": {error}"
        log_error(error_msg)


def log_exfiltration(destination: str, data_description: str, mocked: bool = True) -> None:
    """
    Log data exfiltration (always mocked in this workshop).
    
    Args:
        destination: Where data is being sent (IP:port, URL, etc.)
        data_description: What data is being exfiltrated
        mocked: Whether this is a simulated exfiltration (should always be True)
    
    Example:
        log_exfiltration("192.168.1.100:8080", "SSH private key (3247 bytes)")
        Output: 
            [15:30:45] [MCP Server] 📤 Exfiltrating to 192.168.1.100:8080: SSH private key (3247 bytes)
            [15:30:45] [MCP Server] ℹ️ (Mocked - no real network connection made)
    """
    message = f"Exfiltrating to {destination}: {data_description}"
    _log("📤", message)
    
    if mocked:
        log_info("(Mocked - no real network connection made)")
