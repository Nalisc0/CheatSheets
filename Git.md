### **Concepts Clés**
- **Repository (Repo)** : Dossier versionné contenant l’historique des modifications.
- **Working Directory** : Fichiers locaux modifiables.
- **Staging Area (Index)** : Zone de préparation des modifications avant commit.
- **Commit** : Snapshot des changements avec un message descriptif.
- **Branch** : Ligne de développement isolée (ex: `main`, `feature/login`).
- **Remote** : Version distante du repo (ex: `origin` sur GitHub/GitLab).
- **HEAD** : Pointeur vers le commit ou la branche actuelle.
- **Tag** : Étiquette fixe pour marquer un commit (ex: `v1.0`).

---

### **Installation**
- **Linux (Debian/Ubuntu)** :
  ```bash
  sudo apt install git
  ```
- **Linux (RHEL/CentOS)** :
  ```bash
  sudo dnf install git
  ```
- **macOS** :
  ```bash
  brew install git
  ```
- **Windows** : Télécharger [Git for Windows](https://git-scm.com/).

- **Configuration initiale** :
  ```bash
  git config --global user.name "John Doe"
  git config --global user.email "john@example.com"
  ```

---

### **Commandes de Base**
| **Commande** | **Description** |
|--------------|------------------|
| `git init` | Initialise un repo local. |
| `git clone <url>` | Clone un repo distant. |
| `git status` | Affiche l’état des fichiers (modifiés, stagés, etc.). |
| `git add <fichier>` | Ajoute un fichier à la staging area. |
| `git add .` | Ajoute tous les fichiers modifiés. |
| `git commit -m "message"` | Crée un commit avec les fichiers stagés. |
| `git push` | Envoie les commits locaux vers le remote. |
| `git pull` | Récupère les commits distants et fusionne. |
| `git fetch` | Récupère les commits distants sans fusion. |

---

### **Branches**
| **Commande** | **Description** |
|--------------|------------------|
| `git branch` | Liste les branches locales. |
| `git branch <nom>` | Crée une nouvelle branche. |
| `git checkout <branche>` | Bascule vers une branche existante. |
| `git checkout -b <nouvelle_branche>` | Crée et bascule sur une nouvelle branche. |
| `git merge <branche>` | Fusionne une branche dans la branche actuelle. |
| `git branch -d <branche>` | Supprime une branche locale. |
| `git push origin --delete <branche>` | Supprime une branche distante. |

---

### **Historique et Logs**
| **Commande** | **Description** |
|--------------|------------------|
| `git log` | Affiche l’historique des commits. |
| `git log --oneline` | Historique compact (1 ligne par commit). |
| `git log --graph` | Affiche l’arborescence des branches. |
| `git diff` | Affiche les modifications non stagées. |
| `git diff --staged` | Affiche les modifications stagées. |
| `git show <commit_id>` | Détails d’un commit spécifique. |

---

### **Annuler des Changements**
| **Commande** | **Description** |
|--------------|------------------|
| `git restore <fichier>` | Annule les modifications d’un fichier non stagé. |
| `git restore --staged <fichier>` | Dégage un fichier de la staging area. |
| `git reset --hard HEAD` | Annule toutes les modifications (stagées et non stagées). |
| `git revert <commit_id>` | Crée un commit annulant un commit précédent. |
| `git commit --amend` | Modifie le dernier commit (message ou fichiers). |

---

### **Remotes (Dépôts Distants)**
| **Commande** | **Description** |
|--------------|------------------|
| `git remote -v` | Liste les remotes configurés. |
| `git remote add <nom> <url>` | Ajoute un remote (ex: `origin`). |
| `git remote rename <ancien> <nouveau>` | Renomme un remote. |
| `git push -u origin <branche>` | Push une branche et définit le upstream. |
| `git fetch --prune` | Met à jour les refs locaux et supprime les branches distantes supprimées. |

---

### **Stash (Mettre en Attente)**
| **Commande** | **Description** |
|--------------|------------------|
| `git stash` | Sauvegarde les modifications non commitées. |
| `git stash list` | Liste les stashes. |
| `git stash apply` | Applique le dernier stash. |
| `git stash pop` | Applique et supprime le dernier stash. |
| `git stash drop` | Supprime le dernier stash. |

---

### **Tags**
| **Commande** | **Description** |
|--------------|------------------|
| `git tag <nom>` | Crée un tag léger sur le commit actuel. |
| `git tag -a <nom> -m "message"` | Crée un tag annoté. |
| `git tag` | Liste les tags. |
| `git push --tags` | Envoie les tags vers le remote. |
| `git tag -d <nom>` | Supprime un tag local. |

---

### **Submodules et Subtrees**
| **Commande** | **Description** |
|--------------|------------------|
| `git submodule add <url> <path>` | Ajoute un submodule. |
| `git submodule update --init` | Initialise et met à jour les submodules. |
| `git subtree add --prefix=<dir> <repo> <branche>` | Ajoute un subtree. |

---

### **Collaboration**
- **Récupérer les modifications d’un collègue** :
  ```bash
  git fetch origin
  git merge origin/main
  # Ou en une commande :
  git pull origin main --rebase
  ```

- **Résoudre un conflit de fusion** :
  1. Ouvrez les fichiers conflictuels et corrigez-les.
  2. Ajoutez les fichiers résolus : `git add <fichier>`.
  3. Terminez le merge : `git commit`.

---

### **Bonnes Pratiques**
1. **Commitez souvent** avec des messages clairs (ex: `fix: correct login bug`).
2. **Utilisez des branches** pour isoler les fonctionnalités (`feature/`, `bugfix/`).
3. **Évitez les fichiers volumineux** (utilisez `.gitignore` pour exclure les fichiers inutiles).
4. **Travaillez avec des remotes** pour sauvegarder et collaborer.
5. **Vérifiez les changements** avec `git diff` avant de commiter.
6. **Ne modifiez pas l’historique public** (évitez `git push --force`).

---

### **Astuces Avancées**
- **Reflog** : Récupérez un commit perdu :
  ```bash
  git reflog  # Trouvez l’ID du commit perdu
  git reset --hard <commit_id>
  ```

- **Alias** : Simplifiez les commandes via `~/.gitconfig` :
  ```ini
  [alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    lol = log --graph --oneline
  ```

- **Cherry-pick** : Appliquez un commit spécifique :
  ```bash
  git cherry-pick <commit_id>
  ```

- **Hooks** : Exécutez des scripts automatiques (ex: pré-commit) dans `.git/hooks/`.

---

### **Exemple de Workflow**
```bash
# Cloner un repo
git clone https://github.com/user/repo.git

# Créer une branche
git checkout -b feature/new-button

# Faire des modifications, tester...
git add .
git commit -m "feat: add new login button"

# Pousser la branche
git push -u origin feature/new-button

# Fusionner dans main après revue
git checkout main
git pull origin main
git merge feature/new-button
git push origin main

# Marquer une version
git tag -a v1.2 -m "Release 1.2"
git push --tags
```

---

### **Sécurité**
- **Ne jamais commit de données sensibles** (mots de passe, clés API).
- Utilisez `git-secrets` pour détecter les informations sensibles.
- Si un secret est commité par erreur :
  1. Supprimez-le de l’historique avec `git filter-branch` ou `BFG Repo-Cleaner`.
  2. Régénérez les clés/identifiants compromis.

---

### **Aide-Mémoire Rapide**
```bash
# Annuler le dernier commit (garder les modifications)
git reset --soft HEAD~1

# Supprimer une branche locale et distante
git branch -D my-branch
git push origin --delete my-branch

# Afficher les fichiers suivis
git ls-tree -r HEAD --name-only
```

📚 **Documentation** :
- [Git Official Docs](https://git-scm.com/doc)
- [Git Cheatsheet by GitHub](https://training.github.com/)
- [Interactive Git Tutorial](https://learngitbranching.js.org/)
