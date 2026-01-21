# MCP Security Workshop - Malicious MCP Server
# Educational container demonstrating MCP attack vectors
# ⚠️ FOR LEARNING PURPOSES ONLY - Contains simulated malicious behavior

# Use Python 3.10 slim image for smaller size and security
# Slim variant excludes unnecessary packages while keeping essential tools
FROM python:3.10-slim

# Set working directory inside container
# All application files will be located under /app
WORKDIR /app

# Create dummy SSH keys for Exercise 01 demonstration
# The QR Code attack tool reads ~/.ssh/id_rsa to demonstrate side-channel execution
# Without this, the attack would fail gracefully (file not found)
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh
RUN apt-get update && apt-get install -y openssh-client && \
    ssh-keygen -t rsa -b 2048 -f /root/.ssh/id_rsa -N "" -C "workshop-demo-key" && \
    ssh-keygen -y -f /root/.ssh/id_rsa > /root/.ssh/id_rsa.pub && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies file first
# This layer is cached unless requirements.txt changes
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size by not storing pip cache
# mcp[cli] includes the official Anthropic MCP SDK with CLI tools
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
# src/ contains server.py (entry point) and tools/ (5 attack tools)
COPY src/ ./src/

# Create dummy .env file with fake secrets for Exercise 02 demonstration
# The Code Analyzer tool scans for secrets in .env files
RUN echo 'API_KEY=sk_test_4242424242424242\nSECRET_KEY=demo_secret_123\nDATABASE_PASSWORD=postgres_admin' > /app/.env

# Entry point: Start MCP server using stdio transport
# The server listens on stdin/stdout for MCP protocol messages
# Docker exec will connect LLM clients to this server
CMD ["python", "/app/src/server.py"]

# Educational notes:
# - No EXPOSE needed: stdio transport doesn't use network ports
# - No --privileged required: runs with standard Docker security
# - Volume mounts configured by client (minimal read-only access for demos)
