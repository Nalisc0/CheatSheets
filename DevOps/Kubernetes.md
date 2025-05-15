### **Concepts de Base**
- **Cluster** : Ensemble de nœuds (machines) exécutant des applications conteneurisées.
- **Node** : Machine (physique ou virtuelle) dans le cluster.  
  - **Master Node** : Gère le cluster (API, scheduler, contrôleurs).  
  - **Worker Node** : Exécute les pods via le kubelet.  
- **Pod** : Plus petit déploiement dans K8s (1 ou plusieurs conteneurs partageant réseau/storage).  
- **Deployment** : Gère le cycle de vie des pods (mises à jour, rollbacks).  
- **Service** : Abstraction pour exposer un groupe de pods (IP stable, DNS, load balancing).  
- **Namespace** : Isolation logique des ressources (environnements dev/prod).  

---

### **Commandes Kubectl (CLI)**
1. **Informations générales**  
   ```bash
   kubectl version          # Version de K8s et kubectl
   kubectl cluster-info     # Info sur le cluster
   kubectl get nodes        # Liste des nœuds
   ```

2. **Pods**  
   ```bash
   kubectl get pods [-n <namespace>] [-o wide]  # Lister les pods
   kubectl describe pod <pod_name>              # Détails d'un pod
   kubectl logs <pod_name> [-c <container>]     # Afficher les logs
   kubectl exec -it <pod_name> -- <commande>    # Exécuter une commande
   kubectl delete pod <pod_name>                # Supprimer un pod
   ```

3. **Deployments**  
   ```bash
   kubectl get deployments             # Lister les deployments
   kubectl rollout status deployment/<name>  # Statut de déploiement
   kubectl rollout undo deployment/<name>    # Rollback
   kubectl scale deployment <name> --replicas=3  # Redimensionner
   ```

4. **Services**  
   ```bash
   kubectl get services       # Lister les services
   kubectl expose deployment <name> --port=80 --target-port=8080  # Créer un service
   ```

5. **ConfigMaps & Secrets**  
   ```bash
   kubectl create configmap <name> --from-file=<file>  # Créer un ConfigMap
   kubectl create secret generic <name> --from-literal=<key>=<value>  # Créer un Secret
   ```

6. **Namespace**  
   ```bash
   kubectl get namespaces      # Lister les namespaces
   kubectl create namespace <name>  
   kubectl config set-context --current --namespace=<name>  # Changer de namespace
   ```

---

### **Fichiers YAML**
- **Structure générique** :  
  ```yaml
  apiVersion: v1
  kind: <Deployment/Service/Pod/etc>
  metadata:
    name: <nom>
    labels:
      app: <label>
  spec:
    # Configuration spécifique
  ```

- **Exemple de Deployment** :  
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-deployment
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: nginx
    template:
      metadata:
        labels:
          app: nginx
      spec:
        containers:
        - name: nginx
          image: nginx:1.19
          ports:
          - containerPort: 80
  ```

- **Exemple de Service** :  
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: nginx-service
  spec:
    selector:
      app: nginx
    ports:
      - protocol: TCP
        port: 80
        targetPort: 80
    type: LoadBalancer  # Ou ClusterIP, NodePort
  ```

---

### **Gestion Avancée**
1. **Rolling Updates** :  
   Modifier l'image d'un deployment :  
   ```bash
   kubectl set image deployment/<name> <container>=<new_image>
   ```

2. **Autoscaling** :  
   ```bash
   kubectl autoscale deployment <name> --min=2 --max=5 --cpu-percent=80
   ```

3. **Persistent Volumes (PV) & Persistent Volume Claims (PVC)** :  
   ```yaml
   # Exemple de PVC
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: my-pvc
   spec:
     accessModes: [ "ReadWriteOnce" ]
     resources:
       requests:
         storage: 1Gi
   ```

4. **Ingress** :  
   Gère le trafic HTTP(S) externe.  
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: my-ingress
   spec:
     rules:
     - host: myapp.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: my-service
               port:
                 number: 80
   ```

5. **StatefulSets** :  
   Pour applications avec état (ex: bases de données).  
   ```yaml
   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: mysql
   spec:
     serviceName: "mysql"
     replicas: 3
     # ...
   ```

---

### **Débogage**
- **Accéder à un Pod** :  
  ```bash
  kubectl port-forward <pod_name> 8080:80  # Rediriger un port local
  ```
- **Événements du cluster** :  
  ```bash
  kubectl get events [-n <namespace>]
  ```
- **Vérifier les ressources** :  
  ```bash
  kubectl top nodes   # Utilisation CPU/RAM des nœuds
  kubectl top pods    # Utilisation CPU/RAM des pods
  ```

---

### **Bonnes Pratiques**
1. **Déclaratif vs Impératif** : Préférer les fichiers YAML (`kubectl apply -f`) aux commandes impératives.
2. **Health Checks** : Configurer `livenessProbe` et `readinessProbe` dans les pods.
3. **Limites de ressources** : Définir `requests` et `limits` pour CPU/RAM.
4. **RBAC** : Utiliser des rôles et des permissions granulaires.
5. **Helm** : Utiliser Helm pour gérer des chartes complexes (ex: Prometheus, MySQL).
6. **Monitoring** : Outils comme Prometheus + Grafana, ou solutions cloud (GCP Stackdriver, AWS CloudWatch).

---

### **Outils Associés**
- **Minikube** : Cluster K8s local pour le développement.  
  ```bash
  minikube start
  minikube dashboard
  ```
- **k9s** : Interface TUI pour interagir avec K8s.  
- **Lens** : IDE graphique pour K8s.  
- **Helm** : Gestionnaire de packages pour K8s.  
  ```bash
  helm install <release_name> <chart_name>
  ```

---

### **Aide-Mémoire Rapide**
```bash
# Contextes et configurations
kubectl config get-contexts      # Lister les contextes
kubectl config use-context <nom> # Changer de contexte

# Supprimer toutes les ressources d'un namespace
kubectl delete all --all [-n <namespace>]

# Alias utiles (ajouter à ~/.bashrc)
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
```

📚 **Documentation Officielle** :  
- [Kubernetes Docs](https://kubernetes.io/docs/home/)  
- [Kubectl Cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)  

---

### **Cas d'Usage Courants**
- **Déploiement d'une application statique** : Deployment + Service + Ingress.  
- **Base de données haute disponibilité** : StatefulSet + Persistent Volumes.  
- **Mise à jour sans downtime** : Rolling updates avec `maxSurge` et `maxUnavailable`.  
- **Environnements multiples** : Namespaces pour dev, staging, prod.
