## 🧩 **Principes de base**
- **Créer une nouvelle session nommée** :
  ```bash
  tmux new -s nom_session
  ```
- **Lister les sessions** :
  ```bash
  tmux ls
  ```
- **Attacher une session** :
  ```bash
  tmux attach -t nom_session
  ```
- **Détacher une session (depuis l'intérieur)** :
  ```
  Ctrl-b d
  ```

---

## 🔧 **Raccourcis clavier de base**
*(Le préfixe par défaut est `Ctrl-b`)*
- `Ctrl-b c` → Créer une nouvelle fenêtre
- `Ctrl-b n` → Aller à la **fenêtre suivante**
- `Ctrl-b p` → Aller à la **fenêtre précédente**
- `Ctrl-b w` → Choisir une fenêtre dans la liste
- `Ctrl-b ,` → Renommer la fenêtre
- `Ctrl-b &` → Fermer la fenêtre courante

---

## 📐 **Panes (volets)**
- `Ctrl-b "` → Split horizontalement
- `Ctrl-b %` → Split verticalement
- `Ctrl-b o` → Aller au **volet suivant**
- `Ctrl-b ;` → Revenir au **dernier volet utilisé**
- `Ctrl-b x` → Fermer le volet courant
- `Ctrl-b z` → Zoom / dézoom sur un volet

### 🔄 Redimensionnement :
- `Ctrl-b` suivi de :
  - `Hold Ctrl + ↑ ↓ ← →` (ou utiliser `:` avec `resize-pane`)

---

## 🗂️ **Fenêtres et sessions**
- `Ctrl-b l` → Revenir à la **dernière fenêtre**
- `Ctrl-b s` → Naviguer entre **sessions**

---

## 🛠️ **Commandes en mode commande (`:`)**
- Entrer en mode commande :
  ```
  Ctrl-b :
  ```
- Exemples :
  - `kill-session -t nom` → Tuer une session
  - `rename-session -t old new` → Renommer une session
  - `move-window -s 1 -t 2` → Déplacer fenêtre 1 à l’index 2

---

## 📋 **Copier-coller (mode copy)**
- `Ctrl-b [` → Entrer en **mode copie**
  - Naviguer avec les flèches ou `vi` (si activé)
  - `Espace` → Début de la sélection
  - `Entrée` → Copier
- `Ctrl-b ]` → Coller

---

## 🧠 **Tips**
- Ajouter ceci à `.tmux.conf` pour les raccourcis **vim-like** :
  ```bash
  setw -g mode-keys vi
  ```

  - Ajouter ceci à `.tmux.conf` pour utiliser la souris pour défiler dans le prompt :
  ```bash
  set-option -g mouse on
  ```

- Redémarrer tmux après modif :
  ```bash
  tmux source-file ~/.tmux.conf
  ```
---

## Exemple de fichier de conf .tmux.conf
```bash
set-option -g mouse on
set-option -g history-limit 10000
set-option -g status-bg white
set-option -g status-fg black
set -g base-index 1
```

---
