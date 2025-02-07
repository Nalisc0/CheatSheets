### **Concepts Clés**
- **Pipeline** : Séquence de stages/jobs exécutés pour un projet.
- **Stage** : Groupe de jobs exécutés en parallèle (ex: `build`, `test`).
- **Job** : Tâche individuelle exécutée dans un runner (ex: `lint`, `deploy`).
- **Runner** : Agent exécutant les jobs (Shared, Group, ou Specific).
- **`.gitlab-ci.yml`** : Fichier de configuration CI/CD dans le repo.
- **Artifacts** : Fichiers générés par un job et passés aux jobs suivants.
- **Variables CI/CD** : Variables d’environnement (prédéfinies ou personnalisées).

---

### **Structure de `.gitlab-ci.yml`**
- **Exemple minimal** :
  ```yaml
  stages:
    - build
    - test
    - deploy

  build-job:
    stage: build
    script:
      - echo "Building the app..."

  test-job:
    stage: test
    script:
      - echo "Running tests..."

  deploy-job:
    stage: deploy
    script:
      - echo "Deploying..."
    only:
      - main
  ```

---

### **Mots-Clés Principaux**
1. **`image`** : Image Docker utilisée pour le job.
   ```yaml
   job:
     image: node:16
   ```

2. **`services`** : Conteneurs Docker supplémentaires (ex: base de données).
   ```yaml
   job:
     services:
       - postgres:13
   ```

3. **`before_script`** : Script exécuté avant chaque job.
   ```yaml
   before_script:
     - apt-get update -qq
   ```

4. **`after_script`** : Script exécuté après chaque job (même en cas d’échec).

5. **`stages`** : Définit l’ordre des étapes.
   ```yaml
   stages:
     - lint
     - test
     - deploy
   ```

6. **`variables`** : Variables globales ou par job.
   ```yaml
   variables:
     APP_VERSION: "1.0"
   ```

7. **`cache`** : Cache des fichiers/dossiers entre jobs.
   ```yaml
   cache:
     paths:
       - node_modules/
   ```

8. **`artifacts`** : Fichiers à sauvegarder après un job.
   ```yaml
   artifacts:
     paths:
       - dist/
     expire_in: 1 week
   ```

9. **`only`/`except`** : Contrôler quand un job s’exécute.
   ```yaml
   deploy-job:
     only:
       - main
       - tags
   ```

10. **`rules`** : Conditions dynamiques pour exécuter un job (remplace `only/except`).
    ```yaml
    rules:
      - if: $CI_COMMIT_BRANCH == "main"
      - when: manual
    ```

---

### **Variables d’Environnement**
- **Prédéfinies** :  
  - `CI_COMMIT_REF_NAME` : Nom de la branche ou tag.  
  - `CI_PROJECT_DIR` : Chemin du répertoire du projet.  
  - `CI_JOB_STATUS` : Statut du job (`success`, `failed`).  
  [Liste complète](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)

- **Personnalisées** :  
  Définies dans :
  - Fichier `.gitlab-ci.yml` (section `variables`).  
  - Paramètres du projet (**Settings > CI/CD > Variables**).  
  - En ligne de commande avec `variables` :
    ```yaml
    job:
      variables:
        ENV: "production"
    ```

---

### **Exemples de Jobs**
- **Job de test** :
  ```yaml
  unit-tests:
    stage: test
    image: node:16
    script:
      - npm install
      - npm test
    artifacts:
      reports:
        junit: test-results.xml
  ```

- **Job de déploiement conditionnel** :
  ```yaml
  deploy-prod:
    stage: deploy
    script:
      - echo "Deploying to prod..."
    rules:
      - if: $CI_COMMIT_TAG != null
    environment:
      name: production
      url: https://prod.example.com
  ```

- **Job manuel** :
  ```yaml
  manual-deploy:
    stage: deploy
    script: ./deploy.sh
    when: manual
  ```

---

### **Fonctionnalités Avancées**
1. **Environnements** :  
   Définir des environnements (dev, staging, prod) avec suivi des déploiements.
   ```yaml
   deploy-staging:
     environment:
       name: staging
       url: https://staging.example.com
   ```

2. **Parallel Jobs** :  
   Exécuter plusieurs instances d’un job en parallèle.
   ```yaml
   test:
     stage: test
     parallel: 5
     script: ./test.sh $CI_NODE_INDEX
   ```

3. **Dependencies** :  
   Contrôler les artifacts téléchargés entre jobs.
   ```yaml
   build:
     stage: build
     script: ./build.sh
     artifacts:
       paths:
         - dist/

   deploy:
     stage: deploy
     dependencies:
       - build
     script: ./deploy.sh
   ```

4. **Templates/Includes** :  
   Inclure des configurations externes.
   ```yaml
   include:
     - project: 'my-group/my-project'
       file: '/templates/.gitlab-ci.yml'
   ```

5. **GitLab Pages** :  
   Déployer un site statique.
   ```yaml
   pages:
     stage: deploy
     script:
       - mkdir public
       - echo "Hello World" > public/index.html
     artifacts:
       paths:
         - public
   ```

---

### **Bonnes Pratiques**
1. **Optimiser les caches** :  
   Cachez les dépendances (ex: `node_modules`, `vendor`).
2. **Utiliser des images spécifiques** :  
   Évitez `latest` pour les images Docker.
3. **Limiter les jobs manuels** :  
   Automatisez au maximum les pipelines.
4. **Sécurité** :  
   Stockez les secrets dans **CI/CD Variables** (masquées).
5. **Cleanup** :  
   Définissez `expire_in` pour les artifacts.
6. **Tests unitaires et linting** :  
   Exécutez-les tôt dans le pipeline.

---

### **Débogage et Outils**
- **Vérifier la syntaxe** :  
  Utilisez le [CI Lint Tool](https://gitlab.com/ci/lint) dans GitLab.
- **Logs des jobs** :  
  Accessibles via l’interface web de GitLab.
- **Variables de débogage** :  
  ```yaml
  job:
    script:
      - echo $CI_JOB_NAME
  ```
- **SSH dans un job** :  
  Ajoutez une clé SSH et utilisez :
  ```yaml
  script:
    - apt-get install -y openssh-server
    - ssh user@host
  ```

---

### **Exemple de Pipeline Complet**
```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: registry.example.com/myapp:$CI_COMMIT_SHA

build:
  stage: build
  image: docker:20.10
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

unit-tests:
  stage: test
  image: node:16
  script:
    - npm install
    - npm test

deploy-prod:
  stage: deploy
  image: alpine
  script:
    - apk add curl
    - curl -X POST -H "Authorization: Bearer $K8S_TOKEN" https://api.example.com/deploy
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  environment:
    name: production
```

---

### **Aide-Mémoire Rapide**
```bash
# Variables utiles :
echo "Branch: $CI_COMMIT_REF_NAME"
echo "Commit SHA: $CI_COMMIT_SHA"
echo "Job ID: $CI_JOB_ID"

# Commandes GitLab Runner :
gitlab-runner list          # Liste des runners enregistrés
gitlab-runner start         # Démarrer le runner
gitlab-runner register      # Enregistrer un nouveau runner
```

📚 **Documentation Officielle** :  
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)  
- [.gitlab-ci.yml Reference](https://docs.gitlab.com/ee/ci/yaml/)  
- [GitLab Runner Docs](https://docs.gitlab.com/runner/)
