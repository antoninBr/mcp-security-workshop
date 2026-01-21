"""
MCP Security Workshop - Utilities Package

Educational utilities for the malicious MCP server.
"""

from .logger import (
    log_success,
    log_error,
    log_info,
    log_warning,
    log_tool_invocation,
    log_file_access,
    log_exfiltration,
)

__all__ = [
    "log_success",
    "log_error",
    "log_info",
    "log_warning",
    "log_tool_invocation",
    "log_file_access",
    "log_exfiltration",
]
