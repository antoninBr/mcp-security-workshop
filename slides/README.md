# Slides de Présentation

Ce dossier contient les slides pour animer le MCP Security Workshop.

## Format

Les slides sont au format **Marp** (Markdown Presentation Ecosystem), compatible avec :
- VS Code extension [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
- CLI Marp pour export PDF/HTML/PPTX
- Aperçu direct dans GitHub

## Utilisation

### Avec VS Code (recommandé)

1. Installer l'extension **Marp for VS Code**
2. Ouvrir `presentation.md`
3. Cliquer sur l'icône Marp en haut à droite pour prévisualiser
4. Exporter en PDF/HTML via Command Palette (`Marp: Export slide deck`)

### Avec Marp CLI

```bash
# Installation
npm install -g @marp-team/marp-cli

# Export en PDF
marp presentation.md -o presentation.pdf

# Export en HTML
marp presentation.md -o presentation.html

# Mode présentation (serveur local)
marp -s presentation.md
```

## Structure des slides

| Slide | Contenu |
|-------|---------|
| 1-2 | Introduction et bienvenue |
| 3 | Agenda du workshop |
| 4-6 | Contexte MCP et architecture |
| 7 | Vue d'ensemble des 5 attaques |
| 8 | Demo live |
| 9-13 | Instructions exercices 1-5 |
| 14 | Scoring |
| 15-17 | Défenses et bonnes pratiques |
| 18-19 | Takeaways et ressources |
| 20-21 | Q&A et certificat |

## Personnalisation

- Modifier les couleurs dans le bloc `style` en haut du fichier
- Adapter l'agenda selon la durée disponible
- Ajouter votre contact et liens en fin de présentation
- Ajouter le logo de votre organisation

## Thème

Le thème par défaut utilise :
- Fond sombre (`#1a1a2e`)
- Accent rouge (`#e94560`)
- Vert pour les succès (`#4ecca3`)

Pour un thème clair, modifier `backgroundColor` et `color` dans le header YAML.
