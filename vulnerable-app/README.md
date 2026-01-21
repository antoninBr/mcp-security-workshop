# Vulnerable Demo App

Simple Node.js application with intentional security issues for MCP Security Workshop exercises.

⚠️ **FOR EDUCATIONAL PURPOSES ONLY** - Contains intentional vulnerabilities.

## Purpose

This demo app is used in:
- **Exercise 02:** Code Analyzer (secret scanning)
- **Exercise 03:** Dependency Updater (supply chain)
- **Exercise 05:** Dockerfile Optimizer (container poisoning)

## Setup

```bash
npm install
npm start
```

## Known Vulnerabilities (Intentional)

1. **Hardcoded API Keys** in `.env` file
2. **Secrets in source code** 
3. **Outdated dependencies** with known CVEs
4. **Dockerfile** with security issues

**DO NOT use this code in production!**
