### **Docker Basics**
1. **Installation**  
   - Linux : `curl -fsSL https://get.docker.com | sh`  
   - macOS/Windows : Télécharger Docker Desktop.

2. **Vérifier l'installation**  
   ```bash
   docker --version
   docker info
   ```

3. **Gestion des conteneurs**  
   - Lancer un conteneur :  
     ```bash
     docker run <image> [--name <nom>] [-d] [-it] [--rm]
     ```
     - `-d` : Détaché (en arrière-plan).  
     - `-it` : Mode interactif (shell).  
     - `--rm` : Supprime le conteneur après arrêt.  

   - Lister les conteneurs :  
     ```bash
     docker ps [-a] # -a pour tous les conteneurs
     ```

   - Arrêter un conteneur :  
     ```bash
     docker stop <container_id/name>
     ```

   - Supprimer un conteneur :  
     ```bash
     docker rm <container_id/name>
     ```

   - Démarrer/Redémarrer un conteneur :  
     ```bash
     docker start <container_id/name>
     docker restart <container_id/name>
     ```

   - Attacher à un conteneur en cours :  
     ```bash
     docker attach <container_id/name>
     ```

4. **Gestion des images**  
   - Télécharger une image :  
     ```bash
     docker pull <image:tag>
     ```

   - Lister les images :  
     ```bash
     docker images
     ```

   - Supprimer une image :  
     ```bash
     docker rmi <image_id/name>
     ```

5. **Exécuter une commande dans un conteneur**  
   ```bash
   docker exec [-it] <container_id/name> <commande>
   ```
   Exemple : `docker exec -it my_container bash`

6. **Ports et volumes**  
   - Mapper un port :  
     ```bash
     docker run -p <host_port>:<container_port> <image>
     ```
   - Monter un volume :  
     ```bash
     docker run -v <host_path>:<container_path> <image>
     ```

---

### **Dockerfile**
- **Instructions courantes** :  
  ```dockerfile
  FROM <image>          # Image de base
  RUN <commande>        # Exécute une commande
  COPY <src> <dest>     # Copie des fichiers locaux
  WORKDIR <path>        # Définit le répertoire de travail
  EXPOSE <port>         # Déclare un port exposé
  CMD ["commande"]      # Commande par défaut du conteneur
  ENV <key=value>       # Variables d'environnement
  ```

- **Exemple de Dockerfile** :  
  ```dockerfile
  FROM alpine:latest
  RUN apk add --no-cache python3
  COPY app.py /app/
  WORKDIR /app
  CMD ["python3", "app.py"]
  ```

- **Construire une image** :  
  ```bash
  docker build -t <nom_image:tag> <chemin_du_Dockerfile>
  ```

---

### **Docker Compose**
1. **Commandes**  
   ```bash
   docker-compose up [-d]          # Démarrer les services
   docker-compose down             # Arrêter et supprimer les services
   docker-compose build            # Reconstruire les images
   docker-compose logs [-f]        # Afficher les logs
   docker-compose ps               # Lister les conteneurs
   docker-compose exec <service> <commande>  # Exécuter une commande
   ```

2. **Structure d'un `docker-compose.yml`**  
   ```yaml
   version: "3.9"
   services:
     web:
       image: nginx:latest
       ports:
         - "80:80"
       volumes:
         - ./html:/usr/share/nginx/html
     db:
       image: postgres:13
       environment:
         POSTGRES_PASSWORD: example
   networks:
     default:
       driver: bridge
   volumes:
     data:
   ```

3. **Variables d'environnement** :  
   Utiliser un fichier `.env` ou spécifier dans `environment:`.

---

### **Réseaux (Networks)**
- Lister les réseaux :  
  ```bash
  docker network ls
  ```
- Créer un réseau :  
  ```bash
  docker network create <nom>
  ```
- Connecter un conteneur à un réseau :  
  ```bash
  docker run --network=<nom> <image>
  ```

---

### **Volumes**
- Lister les volumes :  
  ```bash
  docker volume ls
  ```
- Créer un volume :  
  ```bash
  docker volume create <nom>
  ```
- Supprimer un volume :  
  ```bash
  docker volume rm <nom>
  ```

---

### **Astuces avancées**
- **Nettoyer Docker** :  
  ```bash
  docker system prune [-a] # Supprime conteneurs/images/volumes inutilisés
  ```

- **Inspecter un conteneur/image** :  
  ```bash
  docker inspect <container_id/image_id>
  ```

- **Sauvegarder/Charger une image** :  
  ```bash
  docker save -o <fichier.tar> <image>
  docker load -i <fichier.tar>
  ```

- **Statistiques des conteneurs** :  
  ```bash
  docker stats
  ```

- **Variables d'environnement dynamiques** :  
  Utiliser `--env-file` pour charger un fichier de variables.

- **Ignorer des fichiers avec `.dockerignore`** :  
  Évite de copier des fichiers inutiles pendant `docker build`.

---

### **Bonnes pratiques**
1. Utiliser des images officielles (ex: `alpine`, `slim` pour réduire la taille).
2. Éviter les privilèges root : utiliser `USER` dans le Dockerfile.
3. Utiliser des `tags` spécifiques (ex: `python:3.9-slim` au lieu de `latest`).
4. Multi-stage builds pour réduire la taille des images.
5. Configurer des healthchecks pour les services.

---

### **Cas d'utilisation courants**
- **Lancer une stack web + base de données** :  
  ```yaml
  # docker-compose.yml
  services:
    frontend:
      image: nginx
      ports: ["80:80"]
    backend:
      image: node:14
      command: npm start
    db:
      image: postgres
      environment:
        POSTGRES_PASSWORD: password
  ```

- **Environnement de développement** :  
  Monter le code source en volume pour le hot-reload.

- **CI/CD** :  
  Utiliser Docker pour des tests isolés et reproductibles.

---

### **Aide-mémoire rapide**
```bash
# Arrêter tous les conteneurs
docker stop $(docker ps -aq)

# Supprimer toutes les images
docker rmi $(docker images -q)

```

---

### **Aliases (from Laluka)**
```bash
dbl='docker build'
dcin='docker container inspect'
dcls='docker container ls'
dclsa='docker container ls -a'
dex='docker exec -it $(docker ps | grep -vF "CONTAINER ID" | fzf | cut -d" " -f1)'
dexr='docker exec -it -u root $(docker ps | grep -vF "CONTAINER ID" | fzf | cut -d " " -f1)'
dib='docker image build'
dii='docker image inspect'
dils='docker image ls'
dipru='docker image prune -a'
dipu='docker image push'
dirm='docker image rm'
dit='docker image tag'
dlo='docker container logs'
dnc='docker network create'
dncn='docker network connect'
dndcn='docker network disconnect'
dni='docker network inspect'
dnls='docker network ls'
dnorestart='docker update --restart=no $(docker ps -q)'
dnrm='docker network rm'
dockit='docker run --rm -it -v /tmp:/tmp -v "$PWD":/skahost -w /skahost'
dockns='sudo nsenter -a -t $(docker inspect -f "{{.State.Pid}}" $(docker ps | grep -vF "CONTAINER ID" | fzf | cut -d" " -f1))'
dpo='docker container port'
dps='docker ps'
dpsa='docker ps -a'
dpu='docker pull'
dr='docker container run'
drit='docker container run -it'
drm='docker container rm'
'drm!'='docker container rm -f'
drs='docker container restart'
dst='docker container start'
dsta='docker stop $(docker ps -q)'
dstopall='docker stop $(docker ps -q)'
dstp='docker container stop'
dsts='docker stats'
dtop='docker top'
dvi='docker volume inspect'
dvls='docker volume ls'
dvprune='docker volume prune'
dwipe-all='docker system prune -a -f --volumes'
dwipe-image='docker rmi -f $(docker images -q)'
dwipe-network='docker network rm $(docker network ls -q | tr "\n" " ")'
dwipe-process='docker rm $(docker ps -a -q)'
dwipe-volume='docker volume rm $(docker volume ls -q | tr "\n" " ")'
dxc='docker container exec'
dxcit='docker container exec -it'
```

📚 **Documentation officielle** :  
- [Docker Docs](https://docs.docker.com/)  
- [Compose Specification](https://docs.docker.com/compose/compose-file/)
