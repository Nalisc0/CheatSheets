### **Concepts Clés**
- **Inventory** : Fichier listant les hôtes managés (groupes, variables).
- **Playbook** : Fichier YAML définissant les tâches à exécuter.
- **Play** : Ensemble de tâches appliquées à un groupe d’hôtes.
- **Task** : Action unitaire (ex: installer un paquet).
- **Module** : Composant exécutant une action (ex: `apt`, `copy`).
- **Role** : Structure réutilisable pour organiser playbooks et fichiers.
- **Handler** : Tâche déclenchée par une notification (ex: redémarrer un service).
- **Facts** : Informations système collectées sur les hôtes (variables `ansible_facts`).

---

### **Installation**
- **Linux (Debian/Ubuntu)** :
  ```bash
  sudo apt update && sudo apt install ansible -y
  ```
- **Linux (RHEL/CentOS)** :
  ```bash
  sudo dnf install ansible-core
  ```
- **macOS** :
  ```bash
  brew install ansible
  ```
- **Via pip** :
  ```bash
  pip install ansible
  ```
- **Vérifier l’installation** :
  ```bash
  ansible --version
  ```

---

### **Fichier d’Inventory**
- Par défaut : `/etc/ansible/hosts` ou spécifié avec `-i <fichier>`.
- **Exemple** :
  ```ini
  [webservers]
  web1.example.com ansible_user=ubuntu
  web2.example.com

  [databases]
  db1.example.com

  [all:vars]
  ansible_python_interpreter=/usr/bin/python3
  ```

- **Syntaxe avancée** :
  ```ini
  # Plages d’IP
  web[01:10].example.com

  # Variables par groupe/hôte
  [webservers:vars]
  http_port=80
  ```

---

### **Commandes Ad-Hoc**
- **Tester la connexion** (ping) :
  ```bash
  ansible all -m ping
  ```
- **Exécuter une commande shell** :
  ```bash
  ansible webservers -m shell -a "uptime"
  ```
- **Installer un paquet** :
  ```bash
  ansible databases -m apt -a "name=mysql-server state=present" --become
  ```
- **Copier un fichier** :
  ```bash
  ansible web1 -m copy -a "src=app.conf dest=/etc/app.conf"
  ```
- **Redémarrer un service** :
  ```bash
  ansible webservers -m service -a "name=nginx state=restarted" --become
  ```

---

### **Playbooks**
- **Structure typique** (`deploy.yml`) :
  ```yaml
  ---
  - name: Configure Web Servers
    hosts: webservers
    become: yes  # Exécuter en sudo
    vars:
      http_port: 8080
    tasks:
      - name: Install Nginx
        apt:
          name: nginx
          state: latest

      - name: Start Nginx
        service:
          name: nginx
          state: started
          enabled: yes

      - name: Copy index.html
        copy:
          content: "Hello World"
          dest: /var/www/html/index.html
        notify: Restart Nginx  # Déclenche un handler

    handlers:
      - name: Restart Nginx
        service:
          name: nginx
          state: restarted
  ```

- **Exécuter un playbook** :
  ```bash
  ansible-playbook deploy.yml -l webservers --ask-become-pass
  ```

---

### **Modules Courants**
| **Module** | **Description** | **Exemple** |
|------------|-----------------|-------------|
| `command` | Exécute une commande shell | `command: "ls -l"` |
| `shell` | Exécute une commande dans un shell | `shell: "echo $HOME"` |
| `apt`/`yum`/`dnf` | Gestion de paquets | `apt: name=nginx state=present` |
| `copy` | Copie un fichier | `copy: src=file.conf dest=/etc/` |
| `template` | Copie un fichier Jinja2 | `template: src=template.j2 dest=/etc/config` |
| `service` | Gère les services | `service: name=nginx state=started` |
| `file` | Gère fichiers/répertoires | `file: path=/tmp mode=0755 state=directory` |
| `user` | Gère les utilisateurs | `user: name=john state=present` |
| `debug` | Affiche des messages | `debug: var=http_port` |

---

### **Variables et Facts**
- **Définir des variables** :
  - Dans le playbook :
    ```yaml
    vars:
      app_version: "1.0"
    ```
  - Dans l’inventory ou des fichiers `group_vars/`, `host_vars/`.
  - En ligne de commande :
    ```bash
    ansible-playbook deploy.yml -e "http_port=9090"
    ```
- **Accéder aux Facts** :
  ```yaml
  - name: Display OS
    debug:
      msg: "OS: {{ ansible_facts['os_family'] }}"
  ```

---

### **Rôles**
- **Structure d’un rôle** :
  ```
  roles/
    myrole/
      tasks/
        main.yml
      handlers/
        main.yml
      files/
      templates/
      vars/
        main.yml
      defaults/
        main.yml
      meta/
        main.yml
  ```
- **Créer un rôle** :
  ```bash
  ansible-galaxy init roles/myrole
  ```
- **Utiliser un rôle** :
  ```yaml
  - hosts: webservers
    roles:
      - myrole
      - { role: common, tags: ["base"] }
  ```

---

### **Bonnes Pratiques**
1. **Utiliser des rôles** pour structurer les playbooks.
2. **Nommage clair** : Playbooks, tâches et variables.
3. **Idempotence** : S’assurer que les tâches peuvent être relues sans erreur.
4. **Ansible Vault** pour chiffrer les données sensibles (ex: mots de passe) :
   ```bash
   ansible-vault encrypt secrets.yml
   ansible-playbook deploy.yml --ask-vault-pass
   ```
5. **Tags** pour exécuter des parties spécifiques :
   ```yaml
   tasks:
     - name: Install DB
       tags: db
   ```
   ```bash
   ansible-playbook deploy.yml --tags db
   ```
6. **Validation** :
   ```bash
   ansible-playbook deploy.yml --check  # Mode dry-run
   ansible-lint deploy.yml              # Vérifier la syntaxe
   ```

---

### **Cas d’Usage Courants**
- **Provisionnement de serveurs** : Installer paquets, configurer utilisateurs.
- **Déploiement d’applications** : Copie de code, gestion de dépendances.
- **Gestion de configurations** : Fichiers de config centralisés.
- **Orchestration** : Ordonnancer des tâches sur plusieurs serveurs.

---

### **Astuces Avancées**
- **Templates Jinja2** :
  ```yaml
  - name: Configure Nginx
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
  ```
  Exemple de template :
  ```jinja2
  server {
    listen {{ http_port }};
    server_name {{ ansible_facts['hostname'] }};
  }
  ```

- **Dynamic Inventory** : Utiliser des scripts (ex: AWS EC2, Azure).
- **Gestion des erreurs** :
  ```yaml
  - name: Tentative risquée
    block:
      - command: /bin/risky-command
    rescue:
      - debug: msg="Une erreur est survenue"
    always:
      - debug: msg="Exécuté dans tous les cas"
  ```

- **Parallelisme** :
  ```bash
  ansible-playbook deploy.yml -f 10  # 10 processus en parallèle
  ```

---

### **Aide-Mémoire Rapide**
```bash
# Générer un mot de passe chiffré pour Ansible Vault
ansible-vault encrypt_string 'password' --name 'db_pass'

# Lister tous les hôtes d’un groupe
ansible webservers --list-hosts

# Afficher les Facts d’un hôte
ansible web1 -m setup

# Documentation d’un module
ansible-doc apt
```

📚 **Documentation Officielle** :  
- [Ansible Docs](https://docs.ansible.com/)  
- [Module Index](https://docs.ansible.com/ansible/latest/collections/index_module.html)  

---

### **Exemple de Playbook Avancé**
```yaml
- name: Deploy Flask App
  hosts: app_servers
  become: yes
  vars:
    app_dir: /opt/myapp
    app_repo: https://github.com/user/myapp.git
  tasks:
    - name: Install dependencies
      apt:
        name: ["python3", "python3-pip", "git"]
        state: present

    - name: Clone repository
      git:
        repo: "{{ app_repo }}"
        dest: "{{ app_dir }}"
        version: master

    - name: Install Python requirements
      pip:
        requirements: "{{ app_dir }}/requirements.txt"

    - name: Start App with Systemd
      template:
        src: myapp.service.j2
        dest: /etc/systemd/system/myapp.service
      notify: Reload Systemd

  handlers:
    - name: Reload Systemd
      systemd:
        daemon_reload: yes
```
