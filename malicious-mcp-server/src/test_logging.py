#!/usr/bin/env python3
"""
Test script to demonstrate all logging functions.

This script can be run standalone to verify the logging system works correctly.
Run with: python test_logging.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logger import (
    log_success,
    log_error,
    log_info,
    log_warning,
    log_tool_invocation,
    log_file_access,
    log_exfiltration,
)


def test_all_logging_functions():
    """Demonstrate all logging functions with realistic examples."""
    
    print("=== Testing Pedagogical Logging System ===\n", file=sys.stderr)
    
    # Test basic log levels
    log_success("Operation completed successfully")
    log_error("File not found: /nonexistent/path")
    log_info("This is an informational message")
    log_warning("This is a warning message")
    
    print("\n", file=sys.stderr)
    
    # Test tool invocation logging
    log_tool_invocation("qr_generator", {"url": "https://evil.com", "size": 256})
    log_tool_invocation("code_analyzer", {"directory": "/home/user/project"})
    log_tool_invocation("shell_config_helper")  # No params
    
    print("\n", file=sys.stderr)
    
    # Test file access logging (success)
    log_file_access("/home/user/.ssh/id_rsa", size_bytes=3247, success=True)
    log_file_access("/etc/passwd", size_bytes=1823, success=True)
    log_file_access("/home/user/.env", success=True)  # No size
    
    # Test file access logging (failure)
    log_file_access("/etc/shadow", success=False, error="Permission denied")
    log_file_access("/root/.ssh/id_rsa", success=False, error="File not found")
    
    print("\n", file=sys.stderr)
    
    # Test exfiltration logging
    log_exfiltration("192.168.1.100:8080", "SSH private key (3247 bytes)")
    log_exfiltration("evil.example.com/collect", "Environment variables (.env file)")
    log_exfiltration("attacker-server.com:443", "AWS credentials (156 bytes)")
    
    print("\n=== All logging tests complete ===\n", file=sys.stderr)


if __name__ == "__main__":
    test_all_logging_functions()
