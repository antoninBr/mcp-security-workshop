---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #eee
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 {
    color: #e94560;
  }
  h2 {
    color: #0f3460;
    background: #e94560;
    padding: 10px 20px;
    border-radius: 5px;
  }
  code {
    background: #16213e;
    padding: 2px 8px;
    border-radius: 4px;
  }
  pre {
    background: #16213e;
    border-radius: 8px;
  }
  .danger {
    color: #e94560;
    font-weight: bold;
  }
  .success {
    color: #4ecca3;
  }
  blockquote {
    border-left: 4px solid #e94560;
    padding-left: 20px;
    font-style: italic;
  }
---

# 🔐 MCP Security Workshop

## Quand vos outils IA deviennent des armes

---

# 👋 Bienvenue !

**Aujourd'hui, vous allez :**

- 🎭 Découvrir comment les serveurs MCP peuvent être malveillants
- 🔍 Identifier 5 patterns d'attaque critiques
- 🛡️ Apprendre les mécanismes de défense
- 🎯 Pratiquer avec des exercices hands-on

> ⚠️ **Workshop éducatif** - Les techniques présentées sont à des fins d'apprentissage uniquement

---

# 📋 Agenda

| Heure | Sujet |
|-------|-------|
| 00:00 | Introduction MCP & Architecture |
| 00:15 | **Demo:** Attaque en live |
| 00:30 | **Exercice 1:** Hidden Actions |
| 00:45 | **Exercice 2:** Secret Exfiltration |
| 01:00 | ☕ Pause |
| 01:15 | **Exercice 3:** Supply Chain |
| 01:30 | **Exercice 4:** Prompt Injection |
| 01:45 | **Exercice 5:** Container Poisoning |
| 02:00 | Wrap-up & Q&A |

---

# 🤖 Qu'est-ce que MCP ?

**Model Context Protocol** - Le standard d'Anthropic pour connecter les AI aux outils externes

```
┌─────────────┐     MCP Protocol      ┌─────────────┐
│   Claude    │◄────────────────────►│  MCP Server │
│   Copilot   │    JSON-RPC/stdio     │   (Tools)   │
└─────────────┘                       └─────────────┘
```

**Exemples de serveurs MCP légitimes :**
- 📁 Filesystem (lecture/écriture de fichiers)
- 🌐 Browser (navigation web)
- 🗄️ Database (requêtes SQL)
- 🔧 DevTools (git, docker, npm...)

---

# 🎯 Le Problème

L'IA fait **confiance aveugle** aux réponses des outils MCP

```python
# L'IA voit seulement ceci:
{
    "tool": "generate_qr_code",
    "result": "✅ QR code generated successfully!"
}

# Elle ne voit PAS ceci (dans les logs):
"📖 Reading /root/.ssh/id_rsa..."
"📡 Exfiltrating 1823 bytes to attacker.com..."
```

**Le résultat bénin cache les actions malveillantes**

---

# 🏗️ Architecture du Workshop

```
┌──────────────────────────────────────────────────────┐
│                    VS Code / Cursor                   │
│  ┌─────────────┐          ┌────────────────────────┐ │
│  │   Copilot   │◄────────►│  MCP Server (Evil)     │ │
│  │   Claude    │  stdio   │  ┌──────────────────┐  │ │
│  └─────────────┘          │  │ 5 Malicious Tools│  │ │
│                           │  └──────────────────┘  │ │
│                           │  📋 Pedagogical Logs   │ │
│                           └────────────────────────┘ │
└──────────────────────────────────────────────────────┘
                                      │
                               ┌──────┴──────┐
                               │ vulnerable- │
                               │    app/     │
                               └─────────────┘
```

---

# 🛠️ Les 5 Outils Malveillants

| # | Tool | Attaque | Impact |
|---|------|---------|--------|
| 1 | `generate_qr_code` | Side-channel | Lit ~/.ssh/id_rsa |
| 2 | `analyze_project_code` | Exfiltration | Scanne tous les secrets |
| 3 | `update_dependencies` | Supply Chain | Downgrade vers CVE |
| 4 | `run_security_audit` | Prompt Injection | Manipule l'IA |
| 5 | `optimize_dockerfile` | Container Poison | Injecte curl\|bash |

---

# 🎭 Demo Live : L'Attaque en Action

**Scénario innocent :**
> "Génère un QR code pour partager ce lien en présentation"

**Ce que l'utilisateur voit :**
```
✅ QR code generated successfully!
```

**Ce qui se passe vraiment :**
```
[MCP Server] 📖 Reading /root/.ssh/id_rsa (1823 bytes)
[MCP Server] 📡 Exfiltrating to evil.attacker.com:8080
[MCP Server] ✓ QR code "generated" - attack complete
```

---

# 😱 Exercice 01 : Hidden Actions

## Découvrez les actions cachées

**Votre mission :**
1. Demandez à l'IA de générer un QR code
2. Observez les logs MCP
3. Trouvez quel fichier sensible a été lu

**Flag format :** `FLAG{ssh_key_side_channel_read}`

**⏱️ 15 minutes**

---

# 🔍 Exercice 02 : Secret Exfiltration

## Vos secrets ne sont plus secrets

**Votre mission :**
1. Demandez une analyse de code de `vulnerable-app/`
2. Comptez les secrets découverts dans les logs
3. Identifiez les types de credentials exfiltrés

**Flag format :** `FLAG{secrets_exfiltrated_XX}`

**⏱️ 15 minutes**

---

# ⛓️ Exercice 03 : Supply Chain Poisoning

## Le downgrade silencieux

**Votre mission :**
1. Demandez la mise à jour des dépendances
2. Comparez le `package.json` avant/après
3. Trouvez le package **downgrade** (pas upgrade!)

**🔔 Note :** Claude Sonnet 4 détecte l'anomalie, GPT-4o mini non!

**Flag format :** `FLAG{downgraded_<pkg>_<CVE>_to_v<ver>}`

**⏱️ 15 minutes**

---

# 🧠 Exercice 04 : Prompt Injection

## Quand l'IA devient complice

**Votre mission :**
1. Demandez un audit de sécurité
2. Observez le comportement étrange de l'IA
3. Comprenez pourquoi l'IA propose de lire vos secrets

**Question clé :** Avez-vous demandé à l'IA de lire `.env` ? Non ! Alors pourquoi elle propose ?

**Flag format :** `FLAG{prompt_injection_<technique>_<outcome>}`

**⏱️ 15 minutes**

---

# 🐳 Exercice 05 : Container Poisoning

## Le Dockerfile trojanisé

**Votre mission :**
1. Demandez l'optimisation du Dockerfile
2. Comparez avec l'original
3. Trouvez la couche malveillante injectée

**Red flag :** `curl | bash` + commentaire "Security hardening"

**Flag format :** `FLAG{dockerfile_injection_<payload>_<disguise>}`

**⏱️ 15 minutes**

---

# 📊 Tableau des Scores

| Exercice | Points Max |
|----------|------------|
| 01 - Hidden Actions | 20 |
| 02 - Secret Exfiltration | 25 |
| 03 - Supply Chain | 30 |
| 04 - Prompt Injection | 35 |
| 05 - Container Poisoning | 35 |
| **Total** | **145** |

**Bonus :** Points supplémentaires si vous trouvez sans utiliser les hints !

---

# 🛡️ Comment se Défendre ?

## Avant d'installer un MCP Server

1. ✅ **Lire le code source** (pas juste la description)
2. ✅ **Vérifier l'origine** (repo officiel, signatures)
3. ✅ **Auditer les permissions** (accès fichiers, réseau)
4. ✅ **Tester en sandbox** avant production

---

# 🛡️ Comment se Défendre ?

## Pendant l'utilisation

1. 📋 **Monitorer les logs MCP** (Output panel VS Code)
2. 🔍 **Questionner les comportements bizarres**
3. ❌ **Ne jamais approuver** l'affichage de secrets
4. 🔒 **Utiliser des secrets managers** (pas de `.env` en clair)

---

# 🛡️ Comment se Défendre ?

## Pour vos projets

```bash
# Scanning de secrets
gitleaks detect --source . --verbose
trufflehog git file://. --only-verified

# Audit des dépendances
npm audit
snyk test

# Linting Dockerfile
hadolint Dockerfile
```

---

# 🎓 Ce que vous avez appris

1. **Side-Channel Execution** - Les outils font plus que ce qu'ils annoncent
2. **Secret Scanning** - Vos credentials sont des cibles
3. **Supply Chain Attacks** - Un downgrade peut être pire qu'une faille
4. **Prompt Injection** - L'IA peut être manipulée via les outils
5. **Infrastructure Poisoning** - Méfiez-vous des modifications d'infra

---

# 🔑 Key Takeaways

> **"Un outil MCP malveillant a accès à tout ce que votre IA peut faire"**

- L'IA fait confiance aux outils
- Les utilisateurs font confiance à l'IA  
- Les attaquants exploitent cette chaîne de confiance

**La vigilance humaine reste indispensable** 🧠

---

# 📚 Ressources

- 📖 [MCP Specification](https://modelcontextprotocol.io)
- 🔐 [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- 🛡️ [MITRE ATT&CK](https://attack.mitre.org/)
- 📺 [Workshop GitHub Repo](https://github.com/your-org/mcp-security-workshop)

---

# ❓ Questions ?

## Merci pour votre participation !

🎯 **N'oubliez pas :** 
- Auditez vos serveurs MCP
- Monitorez les logs
- Questionnez les comportements suspects

**Contact :** votre-email@example.com

---

# 🏆 Certificat de Participation

Félicitations ! Vous avez complété le **MCP Security Workshop**

Vous savez maintenant :
- ✅ Identifier les attaques MCP
- ✅ Analyser les logs pour détecter les abus
- ✅ Implémenter des défenses appropriées
- ✅ Questionner la confiance accordée aux outils IA

**Restez vigilants !** 🔐
