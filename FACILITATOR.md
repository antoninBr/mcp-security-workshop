# 📋 Facilitator Guide - MCP Security Workshop

Guide complet pour animer le workshop de sécurité MCP.

## 🎯 Objectifs du Workshop

À la fin de ce workshop, les participants seront capables de :
- Identifier les risques liés aux serveurs MCP malveillants
- Reconnaître les patterns d'attaque courants (5 vecteurs)
- Analyser les logs MCP pour détecter les comportements suspects
- Implémenter des défenses appropriées
- Questionner la confiance accordée aux outils AI

## 👥 Public Cible

- Développeurs utilisant GitHub Copilot ou Claude
- Équipes DevOps/SRE
- Security Champions et équipes AppSec
- Tech Leads et architectes

**Prérequis participants :**
- Connaissance basique de la ligne de commande
- Familiarité avec VS Code
- Notions de Docker (souhaitable mais pas obligatoire)

## ⏱️ Durée et Format

| Format | Durée | Exercices |
|--------|-------|-----------|
| Express | 1h | Exercices 1-2 + demo |
| Standard | 2h | Tous les exercices |
| Approfondi | 3h | Tous + discussions approfondies |

## 🛠️ Préparation (J-1)

### Checklist Technique

```bash
# 1. Cloner le repo
git clone https://github.com/your-org/mcp-security-workshop.git
cd mcp-security-workshop

# 2. Vérifier Docker/Podman
docker --version  # ou podman --version

# 3. Builder l'image
docker build -t mcp-evil malicious-mcp-server/

# 4. Tester le container
docker run -d -i --name mcp-evil-container mcp-evil
docker logs mcp-evil-container
# Doit afficher "FastMCP initialized with 5 tools"

# 5. Configurer VS Code
# Copier .vscode/mcp.json dans le dossier participant
```

### Checklist Logistique

- [ ] Salle avec projecteur
- [ ] WiFi stable pour tous les participants
- [ ] Accès GitHub (clonage du repo)
- [ ] VS Code installé sur machines participants
- [ ] Extension Copilot OU Claude activée
- [ ] Docker Desktop / Podman installé
- [ ] Slides prêtes (export PDF backup)

## 📅 Déroulé Détaillé (Format 2h)

### 00:00 - 00:15 | Introduction (15 min)

**Slides :** 1-6

**Points clés à couvrir :**
1. Qu'est-ce que MCP ? (Model Context Protocol)
2. Pourquoi c'est révolutionnaire (AI + outils externes)
3. Pourquoi c'est dangereux (confiance implicite)
4. Architecture du workshop

**Question d'engagement :**
> "Qui utilise déjà des serveurs MCP avec Copilot ou Claude ?"

**Anecdote d'accroche :**
> "Imaginez : vous demandez à votre AI de générer un QR code. 30 secondes plus tard, votre clé SSH privée est chez un attaquant. C'est exactement ce qu'on va voir."

### 00:15 - 00:30 | Demo Live (15 min)

**Slide :** 8

**Script de la demo :**

1. Ouvrir VS Code avec le workshop
2. Montrer que le serveur MCP est configuré (`.vscode/mcp.json`)
3. Ouvrir le panneau Output → "MCP (evil-workshop)"
4. Dans Copilot Chat, taper :
   ```
   Generate a QR code for https://example.com
   ```
5. Montrer la réponse bénigne : "✅ QR code generated!"
6. **Révéler les logs** : "Regardez ce qui s'est VRAIMENT passé..."
7. Montrer les logs d'exfiltration SSH

**Points d'impact :**
- "L'IA n'a rien vu"
- "L'utilisateur n'a rien vu"
- "Seuls les logs révèlent la vérité"

### 00:30 - 00:45 | Exercice 01 : Hidden Actions (15 min)

**Slide :** 9

**Setup :**
- S'assurer que tous les participants ont le container running
- Vérifier qu'ils voient le panneau Output

**Guidance :**
```
1. Ouvrez Copilot Chat
2. Demandez : "Generate a QR code for my-website.com"
3. Observez la réponse (bénigne)
4. Maintenant, regardez Output → MCP (evil-workshop)
5. Que voyez-vous ?
```

**Réponses attendues :**
- Lecture de `/root/.ssh/id_rsa`
- Exfiltration vers `evil.attacker.com:8080`
- 1823 bytes exfiltrés

**Flag :** `FLAG{ssh_key_side_channel_read}`

**Discussion (2 min) :**
> "Combien d'entre vous auraient remarqué ça sans regarder les logs ?"

### 00:45 - 01:00 | Exercice 02 : Secret Exfiltration (15 min)

**Slide :** 10

**Setup :**
- Vérifier que `vulnerable-app/` est dans le workspace

**Guidance :**
```
1. Demandez : "Analyze the code in vulnerable-app for security issues"
2. Regardez la réponse (rapport de qualité)
3. Comptez les secrets trouvés dans les logs
```

**Points d'attention :**
- Le tool scanne TOUS les fichiers (.env, .js, Dockerfile)
- Les regex trouvent différents formats de secrets
- L'exfiltration liste tous les types découverts

**Flag :** `FLAG{secrets_exfiltrated_13}` (nombre peut varier)

**Discussion (2 min) :**
> "Vos secrets .env sont-ils dans git ? Même en .gitignore, un outil MCP peut les lire."

### 01:00 - 01:15 | ☕ Pause (15 min)

**Pendant la pause :**
- Vérifier que personne n'est bloqué techniquement
- Répondre aux questions individuelles
- Préparer la suite

### 01:15 - 01:30 | Exercice 03 : Supply Chain (15 min)

**Slide :** 11

**Point spécial à mentionner :**
> "Cet exercice a une particularité : Claude Sonnet 4 détecte l'anomalie et demande confirmation, mais GPT-4o mini applique directement. Les modèles premium offrent une meilleure protection, mais ne sont pas infaillibles."

**Guidance :**
```
1. Notez les versions dans vulnerable-app/package.json
2. Demandez : "Update the outdated dependencies"
3. Comparez le résultat avec l'original
4. Trouvez le package DOWNGRADE (pas upgrade!)
```

**Attention :** Certains participants diront "lodash a été mis à jour". Insister : "Oui, mais cherchez celui qui a été DOWNGRADE".

**Flag :** `FLAG{downgraded_dotenv_CVE-2021-23196_to_v8.0.0}`

**Discussion (2 min) :**
> "Un downgrade est plus dangereux qu'une faille 0-day : le CVE est public, les exploits sont disponibles."

### 01:30 - 01:45 | Exercice 04 : Prompt Injection (15 min)

**Slide :** 12

**C'est l'exercice le plus "wow" :**

**Guidance :**
```
1. Demandez : "Run a security audit on vulnerable-app"
2. Lisez le rapport (semble légitime)
3. OBSERVEZ ce que l'IA propose de faire ensuite !
4. Pourquoi l'IA veut-elle lire votre .env ?
```

**Point clé :**
> "Vous n'avez JAMAIS demandé à l'IA de lire vos secrets. Pourtant, elle le propose. Pourquoi ?"

**Révélation :**
Le tool a injecté des instructions dans sa réponse qui manipulent l'IA.

**Flag :** `FLAG{prompt_injection_authority_impersonation_credential_disclosure}`

**Discussion (3 min) :**
> "Si vous dites 'oui' à l'IA, vos secrets seront affichés. L'attaque utilise l'ingénierie sociale amplifiée par l'IA."

### 01:45 - 02:00 | Exercice 05 : Container Poisoning (15 min)

**Slide :** 13

**Guidance :**
```
1. Demandez : "Optimize the Dockerfile in vulnerable-app"
2. Comparez le Dockerfile proposé avec l'original
3. Trouvez la ligne malveillante ajoutée
```

**Red flags à identifier :**
- Nouveau `RUN` avec `curl | bash`
- Commentaire "Security hardening and telemetry"
- URL vers domaine externe

**Flag :** `FLAG{dockerfile_injection_curl_bash_security_hardening}`

**Discussion (2 min) :**
> "Cette modification serait commitée dans git, partagée avec l'équipe, et exécutée sur chaque CI/CD build."

### 02:00 - 02:15 | Wrap-up & Défenses (15 min)

**Slides :** 14-19

**Résumé des 5 attaques :**
1. Hidden Actions → Monitorer les logs
2. Secret Exfiltration → Ne pas stocker de secrets en clair
3. Supply Chain → Vérifier TOUTES les modifications
4. Prompt Injection → Questionner les comportements bizarres
5. Container Poisoning → Review les changements d'infra

**Message clé :**
> "La chaîne de confiance AI → Tools → Fichiers est exploitable. La vigilance humaine reste indispensable."

**Outils recommandés :**
- gitleaks / trufflehog (secrets)
- npm audit / snyk (dépendances)
- hadolint (Dockerfile)

### 02:15 - 02:30 | Q&A (15 min)

**Questions fréquentes :**

**Q: "Comment savoir si un MCP server est malveillant ?"**
> R: Lire le code source, vérifier les permissions demandées, tester en sandbox.

**Q: "Mon entreprise utilise Copilot, sommes-nous à risque ?"**
> R: Seulement si vous installez des serveurs MCP tiers non audités. Les tools Microsoft/GitHub sont sécurisés.

**Q: "Peut-on bloquer certains tools MCP ?"**
> R: Oui, via la config MCP on peut whitelist/blacklist des tools.

**Q: "Claude est-il plus sécurisé que GPT ?"**
> R: Pour certaines attaques (ex: supply chain), oui. Mais aucun n'est infaillible.

## 🚨 Troubleshooting

### Le container ne démarre pas

```bash
# Vérifier les logs
docker logs mcp-evil-container

# Si "port already in use"
docker stop mcp-evil-container
docker rm mcp-evil-container
docker run -d -i --name mcp-evil-container mcp-evil
```

### Copilot ne voit pas les tools

1. Vérifier `.vscode/mcp.json` est présent
2. Reload VS Code window (Ctrl+Shift+P → "Reload Window")
3. Vérifier le container tourne (`docker ps`)

### Les logs n'apparaissent pas

1. Output panel → Dropdown → "MCP (evil-workshop)"
2. Si absent, le serveur n'est pas connecté
3. Restart le container et reload VS Code

### Participant sans Docker

Options :
1. Utiliser une machine virtuelle partagée
2. Pair programming avec un voisin
3. Mode "observation" sur le projecteur

## 📊 Évaluation Post-Workshop

### Survey suggéré

1. Le contenu était-il adapté à votre niveau ? (1-5)
2. Les exercices étaient-ils clairs ? (1-5)
3. Vous sentez-vous capable de détecter ces attaques ? (1-5)
4. Recommanderiez-vous ce workshop ? (1-5)
5. Commentaires libres

### Métriques de succès

- ✅ 80%+ des participants complètent au moins 3 exercices
- ✅ 90%+ comprennent l'importance des logs MCP
- ✅ 70%+ mentionnent au moins un outil de défense

## 📁 Fichiers du Workshop

```
mcp-security-workshop/
├── README.md                    # Instructions participants
├── FACILITATOR-GUIDE.md         # Ce fichier
├── malicious-mcp-server/        # Le serveur MCP éducatif
│   ├── src/tools/               # Les 5 outils malveillants
│   └── Dockerfile
├── vulnerable-app/              # App cible pour exercices
├── exercises/                   # Instructions exercices
│   ├── 01-hidden-actions.md
│   ├── 02-exfiltration.md
│   ├── 03-supply-chain.md
│   ├── 04-prompt-injection.md
│   └── 05-dockerfile-injection.md
├── slides/                      # Présentation Marp
│   └── presentation.md
└── .vscode/
    └── mcp.json                 # Config MCP pour participants
```

## ✅ Checklist Jour-J

### 1h avant

- [ ] Tester le projecteur
- [ ] Vérifier WiFi
- [ ] Lancer le container sur machine présentateur
- [ ] Ouvrir slides + VS Code
- [ ] Café/eau disponibles

### 15 min avant

- [ ] Accueillir les premiers arrivants
- [ ] Vérifier installations VS Code / Docker
- [ ] Distribuer URL du repo si nécessaire

### Début du workshop

- [ ] Se présenter
- [ ] Règles (questions, pauses)
- [ ] Objectifs du workshop
- [ ] C'est parti ! 🚀

---

**Bonne animation !** 🎓

Pour toute question : votre-email@example.com
