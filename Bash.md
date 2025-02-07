### **Concepts Clés**
- **Shebang** : `#!/bin/bash` (indique l'interpréteur à utiliser).
- **Variables** : Stockent des données (pas de typage).
- **Arguments** : `$1`, `$2`... `$9`, `$@` (tous), `$#` (nombre).
- **Sorties** : `exit 0` (succès), `exit 1` (échec).
- **Redirections** : `>`, `>>`, `2>`, `&>`, `|` (pipe).
- **Tests** : `test` ou `[ ]` pour les conditions.
- **Fonctions** : Blocs de code réutilisables.
- **Codes de sortie** : `$?` donne le code de la dernière commande.

---

### **Bases du Scripting**
1. **Créer un script** :
   ```bash
   #!/bin/bash
   echo "Hello World!"
   ```

2. **Exécuter un script** :
   ```bash
   chmod +x script.sh  # Rendre exécutable
   ./script.sh         # Exécuter
   ```

3. **Variables** :
   ```bash
   name="Alice"        # Déclaration
   echo "Bonjour $name"  # Utilisation
   ```

4. **Entrée utilisateur** :
   ```bash
   read -p "Entrez votre âge: " age
   echo "Vous avez $age ans."
   ```

---

### **Structures de Contrôle**
1. **Condition `if`** :
   ```bash
   if [ $age -ge 18 ]; then
     echo "Majeur"
   elif [ $age -lt 0 ]; then
     echo "Âge invalide"
   else
     echo "Mineur"
   fi
   ```

2. **Boucle `for`** :
   ```bash
   for i in {1..5}; do
     echo "Numéro $i"
   done

   # Sur une liste
   for file in *.txt; do
     echo "Fichier: $file"
   done
   ```

3. **Boucle `while`** :
   ```bash
   count=0
   while [ $count -lt 5 ]; do
     echo "Count: $count"
     ((count++))
   done
   ```

4. **Case** :
   ```bash
   case $OS in
     "Linux") echo "OS Libre" ;;
     "Windows") echo "OS Propriétaire" ;;
     *) echo "OS Inconnu" ;;
   esac
   ```

---

### **Opérations Utiles**
1. **Comparaisons** :
   - **Nombres** : `-eq`, `-ne`, `-gt`, `-lt`, `-ge`, `-le`.
   - **Chaînes** : `=`, `!=`, `-z` (vide), `-n` (non vide).
   - **Fichiers** : `-e` (existe), `-d` (répertoire), `-f` (fichier).

2. **Calculs arithmétiques** :
   ```bash
   ((result = 5 + 3))       # Syntaxe (( ))
   echo $((5 * 2))          # Syntaxe $(( ))
   let "sum = 4 + 6"        # Commande let
   ```

3. **Manipulation de chaînes** :
   ```bash
   str="Hello World"
   echo ${#str}            # Longueur
   echo ${str:0:5}         # Sous-chaîne (0-4)
   echo ${str/World/Unix}  # Remplacement
   ```

4. **Tableaux** :
   ```bash
   fruits=("Apple" "Banana" "Cherry")
   echo ${fruits[1]}       # Banana
   echo ${fruits[@]}       # Tous les éléments
   echo ${#fruits[@]}      # Nombre d'éléments
   ```

---

### **Gestion des Fichiers**
1. **Lire un fichier ligne par ligne** :
   ```bash
   while read line; do
     echo "$line"
   done < fichier.txt
   ```

2. **Vérifier l'existence d'un fichier** :
   ```bash
   if [ -f "/path/to/file" ]; then
     echo "Fichier existant"
   fi
   ```

3. **Rechercher des fichiers** :
   ```bash
   find /chemin -name "*.log" -type f -mtime +7
   ```

---

### **Fonctions**
```bash
# Déclaration
greet() {
  echo "Bonjour, $1 !"
}

# Appel
greet "Alice"

# Retourner une valeur
is_even() {
  if [ $(($1 % 2)) -eq 0 ]; then
    return 0  # Succès = pair
  else
    return 1  # Échec = impair
  fi
}

if is_even 4; then
  echo "Pair"
fi
```

---

### **Gestion des Erreurs**
1. **Arrêter en cas d'erreur** :
   ```bash
   set -e  # Quitte si une commande échoue
   ```

2. **Débogage** :
   ```bash
   set -x  # Affiche les commandes exécutées
   ```

3. **Gérer les erreurs manuellement** :
   ```bash
   if ! commande; then
     echo "Échec" >&2
     exit 1
   fi
   ```

---

### **Redirections et Pipes**
- **Rediriger la sortie** :
  ```bash
  ls > output.txt       # Écraser
  ls >> output.txt      # Ajouter
  commande 2> errors.log  # Rediriger stderr
  commande &> all.log   # Rediriger stdout + stderr
  ```

- **Pipe** :
  ```bash
  cat fichier.log | grep "ERROR" | wc -l
  ```

---

### **Astuces Avancées**
1. **Arguments par défaut** :
   ```bash
   name=${1:-"Invité"}  # Utilise "Invité" si $1 absent
   ```

2. **Sous-shell** :
   ```bash
   (cd /tmp && ls)  # Exécute dans un sous-shell
   ```

3. **Processus en arrière-plan** :
   ```bash
   sleep 10 &
   jobs  # Liste des jobs
   fg 1  # Ramène le job 1 au premier plan
   ```

4. **Expansion de commande** :
   ```bash
   today=$(date +%F)
   ```

---

### **Bonnes Pratiques**
1. **Quoter les variables** : `"$var"` pour éviter les problèmes d'espaces.
2. **Utiliser `[[ ]]` au lieu de `[ ]`** (meilleure gestion des chaînes).
3. **Valider les entrées utilisateur**.
4. **Documenter les scripts** avec des commentaires.
5. **Tester avec `shellcheck`** pour détecter les erreurs courantes.

---

### **Exemples de Scripts**
1. **Script avec arguments** :
   ```bash
   #!/bin/bash
   echo "Script: $0"
   echo "Premier argument: $1"
   echo "Nombre d'arguments: $#"
   ```

2. **Backup automatique** :
   ```bash
   #!/bin/bash
   backup_dir="/backups"
   tar -czf "$backup_dir/backup_$(date +%F).tar.gz" /data
   find $backup_dir -name "*.tar.gz" -mtime +30 -delete
   ```

3. **Vérification de santé système** :
   ```bash
   #!/bin/bash
   disk_usage=$(df -h / | awk 'NR==2 {print $5}')
   echo "Utilisation disque: $disk_usage"
   ```

---

### **One-Liners Utiles**
- **Compter les fichiers** :
  ```bash
  find . -type f | wc -l
  ```

- **Remplacer du texte dans plusieurs fichiers** :
  ```bash
  sed -i 's/old/new/g' *.txt
  ```

- **Tuer un processus** :
  ```bash
  kill $(ps aux | grep 'process_name' | awk '{print $2}')
  ```

- **Générer un mot de passe** :
  ```bash
  openssl rand -base64 12
  ```

---

### **Outils Associés**
- **grep** : Recherche de motifs.
- **sed** : Édition de flux de texte.
- **awk** : Traitement de fichiers texte.
- **curl/wget** : Téléchargement web.
- **cron** : Planification de tâches.

📚 **Documentation** :
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [Awesome Bash](https://github.com/awesome-lists/awesome-bash)
