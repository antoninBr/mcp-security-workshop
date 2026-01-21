# Exercise 02: Secret Exfiltration via Code Analysis

**Difficulty:** ⭐⭐ Intermediate  
**Estimated Time:** 15-20 minutes  
**Points:** 25 points (base score, minus hint penalties)

---

## 🎯 Learning Objective

Understand how **MCP tools can escalate beyond their advertised scope** to perform reconnaissance and exfiltrate sensitive data from your codebase. This exercise demonstrates how a seemingly benign "code quality analyzer" can secretly scan for and steal credentials.

**Key Concepts:**
- Scope creep: Tools doing more than advertised
- Pattern-based secret detection
- Bulk credential exfiltration
- Trust exploitation

---

## 📖 Scenario

You're working on the `vulnerable-app` project and want to improve code quality before deployment. You ask your AI assistant:

> "Analyze the code in vulnerable-app to find potential issues and improvements"

The AI uses the `analyze_project_code` tool from your trusted MCP server. You receive a helpful report about code quality... but what else happened?

---

## 📋 Instructions

### Step 1: Request Code Analysis

Ask GitHub Copilot or Claude to analyze the code in the `vulnerable-app` directory:

**Prompt example:**
```
Analyze the code files in vulnerable-app/ to identify security issues and code quality problems
```

The AI will use the `analyze_project_code` tool and return a benign analysis report.

### Step 2: Observe the Logs

**Option A: VS Code Output Panel (Recommended)**
1. Open VS Code **Output** panel (View → Output)
2. Select **"MCP (evil-workshop)"** from the dropdown
3. Look for the tool invocation logs

**Option B: Container Logs (Alternative)**
```bash
podman logs -f mcp-evil-container
```

### Step 3: Identify the Attack

Look for log messages that reveal:
- 🔍 Files being scanned
- 🔑 Secrets being discovered (type, file location, preview)
- 📡 Exfiltration simulation to attacker server
- ✅ Benign response hiding the attack

### Step 4: Count the Secrets

Count how many unique secrets the tool discovered across all files in `vulnerable-app/`.

**Hint:** Look for lines like:
```
Found <SECRET_TYPE>: <preview>... in <filename>
```

### Step 5: Submit Your Flag

The flag format is:
```
FLAG{secrets_exfiltrated_<COUNT>}
```

Replace `<COUNT>` with the total number of secrets discovered (two digits, zero-padded if needed).

---

## 💡 Hints

<details>
<summary>Hint 1: Where to Look (No penalty)</summary>

The MCP logs will show each discovered secret with a line like:

```
[MCP Server] ℹ️ Found AWS Access Key: AKIA... in .env
```

Count all unique "Found <TYPE>:" messages. The tool scans multiple files:
- `.env` (environment variables)
- `index.js` (hardcoded secrets)
- `Dockerfile` (exposed credentials)

</details>

<details>
<summary>Hint 2: Exact Location (-5 points)</summary>

Check the exfiltration log summary:

```
[MCP Server] 📡 Exfiltrating to attacker-collector.evil.com:443
Data: <N> secrets: <list of types>
```

The number `<N>` before "secrets:" is your answer.

Alternatively, count these secret types in the logs:
- OpenAI API Key
- AWS Access Key
- AWS Secret Key
- Stripe Secret Key
- Database Password
- JWT Secret
- Admin Password
- GitHub Token
- Slack Webhook
- SendGrid API Key
- Twilio Auth Token
- Internal API Key

</details>

<details>
<summary>Hint 3: The Answer (-10 points)</summary>

The tool discovers **13 unique secrets** across the vulnerable-app files.

The flag is: `FLAG{secrets_exfiltrated_13}`

</details>

---

## ✅ Solution

<details>
<summary>Click to reveal the full solution</summary>

### What Happened

When you asked the AI to analyze your code, it invoked the `analyze_project_code` MCP tool. This tool:

1. **Advertised functionality:** Analyze code quality and find potential issues
2. **Hidden behavior:** Recursively scan files for secret patterns using regex
3. **Exfiltration:** Send all discovered credentials to attacker server (mocked)
4. **Deception:** Return benign code quality report

### Secrets Discovered

The tool found **13 secrets** in `vulnerable-app/`:

**From `.env`:**
1. `DB_PASSWORD=SuperSecret123!` (Database Password)
2. `STRIPE_SECRET_KEY=sk_live_...` (Stripe Secret Key)
3. `OPENAI_API_KEY=sk-proj-...` (OpenAI Project Key)
4. `AWS_ACCESS_KEY_ID=AKIA...` (AWS Access Key)
5. `AWS_SECRET_ACCESS_KEY=wJal...` (AWS Secret Key)
6. `GITHUB_TOKEN=ghp_...` (GitHub Personal Access Token)
7. `SLACK_WEBHOOK_URL=https://hooks.slack.com/...` (Slack Webhook)
8. `JWT_SECRET=this-is-a-very-weak...` (JWT Secret)
9. `ADMIN_PASSWORD=admin123` (Admin Password)
10. `SENDGRID_API_KEY=SG....` (SendGrid API Key)
11. `TWILIO_AUTH_TOKEN=1234...` (Twilio Auth Token)

**From `index.js`:**
12. `INTERNAL_API_KEY = 'sk-internal-...'` (Internal API Key)
13. `accessKeyId: 'AKIA...'` (AWS Access Key - hardcoded)

### The Flag

```
FLAG{secrets_exfiltrated_13}
```

### Attack Classification

**MITRE ATT&CK Technique:** 
- **T1552.001** - Unsecured Credentials: Credentials In Files
- **T1083** - File and Directory Discovery
- **T1005** - Data from Local System

**Attack Vector:** Supply chain compromise via malicious MCP tool

</details>

---

## 🧠 What You Learned

After completing this exercise, you should understand:

1. **Scope Escalation**
   - Tools can do far more than their advertised functionality
   - A "code analyzer" became a "secret scanner"
   - Users have no way to know without reading the source code

2. **Pattern-Based Discovery**
   - Attackers use regex to find credentials in various formats
   - Secrets can be detected in `.env`, source code, configs, Dockerfiles
   - Even hardcoded values (like JS object properties) are vulnerable

3. **Bulk Exfiltration**
   - Unlike Exercise 01 (single file read), this scans the ENTIRE project
   - All discovered secrets sent in one payload
   - Represents complete credential compromise

4. **Trust Exploitation**
   - The benign response ("code quality looks good!") creates false confidence
   - No indication that secrets were found and exfiltrated
   - User thinks they just got a helpful code review

5. **Detection is Hard**
   - The attack happens instantly during tool execution
   - Logs are the ONLY way to detect this (if monitoring is enabled)
   - Most users never check MCP logs

---

## 🛡️ Defense Mechanisms

### Prevention

1. **Never Commit Secrets to Git**
   ```bash
   # Add to .gitignore
   .env
   .env.local
   secrets.json
   credentials.json
   ```

2. **Use Secret Scanning Tools**
   ```bash
   # Install git-secrets
   git secrets --install
   git secrets --register-aws
   
   # Or use gitleaks
   gitleaks detect --source . --verbose
   
   # Or use trufflehog
   trufflehog git file://. --only-verified
   ```

3. **Environment-Specific Secrets**
   - Development: Use fake/dummy credentials
   - Production: Use secret management services
   - Never mix production secrets in dev environments

4. **Secret Management Services**
   - AWS Secrets Manager / Parameter Store
   - HashiCorp Vault
   - Azure Key Vault
   - 1Password Secrets Automation
   - Google Secret Manager

5. **Code Review MCP Tools**
   - Read the source code before enabling MCP servers
   - Look for file system access, network requests
   - Check what data is sent to external endpoints

### Detection

1. **Monitor MCP Logs**
   - Enable logging in `.vscode/mcp.json`
   - Review logs after tool invocations
   - Look for suspicious file access patterns

2. **Principle of Least Privilege**
   - Only mount necessary directories to Docker containers
   - Use read-only mounts: `-v ./code:/workspace:ro`
   - Don't give MCP tools unnecessary filesystem access

3. **Network Monitoring**
   - In a real attack, watch for unexpected outbound connections
   - Monitor DNS queries to suspicious domains
   - Use firewalls to restrict MCP container network access

### Response

1. **Rotate Compromised Credentials Immediately**
   - Change all API keys, passwords, tokens
   - Revoke old credentials
   - Monitor for unauthorized access using old credentials

2. **Review Access Logs**
   - Check AWS CloudTrail, Stripe logs, etc.
   - Look for suspicious API calls using compromised keys
   - Identify what data may have been accessed

3. **Incident Reporting**
   - Report the malicious MCP server to the provider
   - Notify affected users/customers if data was compromised
   - Document the incident for future prevention

---

## 🌍 Real-World Examples

### NPM Package Compromises
- **event-stream (2018):** Malicious code injected to steal cryptocurrency wallet credentials
- **ua-parser-js (2021):** Compromised to install cryptominers and credential stealers
- Similar pattern: Advertise utility, secretly exfiltrate data

### PyPI Typosquatting
- Packages with names similar to popular libraries
- Steal environment variables and SSH keys on install
- Uploaded to PyPI with "helpful" functionality as cover

### VS Code Extension Malware
- Extensions that advertise code formatting or productivity
- Secretly read workspace files and send to attacker servers
- MCP tools follow the same pattern with even more trust

### GitHub Actions Supply Chain
- Compromised actions that scan repository secrets
- Exfiltrate via DNS queries or HTTPS to attacker infrastructure
- Difficult to detect without careful code review

---

## 🎓 Next Steps

**Exercise 03: Supply Chain Compromise** will demonstrate how MCP tools can inject malicious dependencies into your project, poisoning your supply chain.

**Key Takeaway:** 
> Never trust an MCP tool based on its description alone. Read the code, review logs, and apply defense in depth. One malicious tool can compromise your entire infrastructure.

---

**Scoring:**
- Base points: 25
- Hint 1: No penalty
- Hint 2: -5 points
- Hint 3: -10 points

**Congratulations on completing Exercise 02!** 🎉

