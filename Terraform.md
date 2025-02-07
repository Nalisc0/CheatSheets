### **Concepts Clés**
- **Infrastructure as Code (IaC)** : Définir l’infrastructure via des fichiers de configuration.
- **Provider** : Plugin pour interagir avec une plateforme (AWS, Azure, GCP, etc.).
- **Resource** : Composant d’infrastructure (ex: VM, réseau, bucket S3).
- **State** : Fichier (`terraform.tfstate`) stockant l’état actuel de l’infrastructure.
- **Variables/Outputs** : Variables d’entrée et sorties du module.
- **Module** : Ensemble réutilisable de configurations Terraform.
- **Workspace** : Environnements isolés (ex: dev, prod).

---

### **Installation**
- **Linux** :
  ```bash
  curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
  sudo apt update && sudo apt install terraform
  ```
- **macOS** :
  ```bash
  brew tap hashicorp/tap
  brew install hashicorp/tap/terraform
  ```
- **Vérification** :
  ```bash
  terraform -version
  ```

---

### **Commandes de Base**
| **Commande** | **Description** |
|--------------|------------------|
| `terraform init` | Initialise le répertoire (télécharge providers/modules). |
| `terraform plan` | Affiche les modifications prévues (dry-run). |
| `terraform apply` | Applique les changements. |
| `terraform destroy` | Détruit toutes les ressources gérées. |
| `terraform fmt` | Formate les fichiers `.tf`. |
| `terraform validate` | Vérifie la syntaxe des configurations. |
| `terraform refresh` | Met à jour le state avec l’état réel de l’infrastructure. |
| `terraform output` | Affiche les outputs définis. |
| `terraform state list` | Liste les ressources dans le state. |

---

### **Structure des Fichiers**
- **`main.tf`** : Définit les providers et ressources principales.
- **`variables.tf`** : Déclare les variables d’entrée.
- **`outputs.tf`** : Définit les données exposées après `apply`.
- **`terraform.tfvars`** : Valeurs des variables (optionnel).

---

### **Exemple de Configuration**
```hcl
# Configure le provider AWS
provider "aws" {
  region = "eu-west-1"
}

# Crée une instance EC2
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = var.instance_type
  tags = {
    Name = "Terraform-Example"
  }
}

# Variable d'entrée
variable "instance_type" {
  description = "Type d'instance EC2"
  default     = "t2.micro"
}

# Output
output "public_ip" {
  value = aws_instance.web.public_ip
}
```

---

### **Gestion du State**
- **Backend** : Stockage distant du state (S3, Azure Storage, etc.).
  ```hcl
  terraform {
    backend "s3" {
      bucket = "my-terraform-state"
      key    = "prod/terraform.tfstate"
      region = "eu-west-1"
    }
  }
  ```
- **Commandes** :
  ```bash
  terraform state mv <source> <destination>  # Renomme une ressource dans le state
  terraform taint <resource>                 # Force le recréation d'une ressource
  ```

---

### **Variables**
- **Types** : `string`, `number`, `bool`, `list`, `map`, `object`.
- **Définition** :
  ```hcl
  variable "env" {
    type        = string
    description = "Environnement (dev/prod)"
    sensitive   = true  # Masque la valeur dans les logs
  }
  ```
- **Utilisation** :
  ```hcl
  resource "aws_instance" "web" {
    tags = {
      Environment = var.env
    }
  }
  ```

---

### **Modules**
- **Module local** :
  ```hcl
  module "vpc" {
    source = "./modules/vpc"
    cidr   = "10.0.0.0/16"
  }
  ```
- **Module public** (Terraform Registry) :
  ```hcl
  module "ec2" {
    source  = "terraform-aws-modules/ec2-instance/aws"
    version = "3.0.0"
    # ... paramètres
  }
  ```

---

### **Workspaces**
- **Créer/Changer de workspace** :
  ```bash
  terraform workspace new dev
  terraform workspace select dev
  ```
- **Lister les workspaces** :
  ```bash
  terraform workspace list
  ```

---

### **Bonnes Pratiques**
1. **Version Control** : Versionnez les fichiers `.tf` (pas le `terraform.tfstate`).
2. **Remote State** : Stockez le state dans un backend sécurisé (S3 + DynamoDB pour le verrouillage).
3. **Modules** : Réutilisez les configurations via des modules.
4. **Variables Sensibles** : Utilisez `sensitive = true` ou des outils comme Vault.
5. **`.gitignore`** :
  ```
  .terraform/
  *.tfstate
  *.tfstate.backup
  .terraform.lock.hcl
  ```

---

### **Fonctions et Expressions**
- **Interpolation** :
  ```hcl
  resource "aws_eip" "lb" {
    instance = aws_instance.web.id
  }
  ```
- **Fonctions** :
  ```hcl
  output "upper_name" {
    value = upper(var.name)
  }
  ```
  - **String** : `join`, `split`, `replace`.
  - **List/Map** : `concat`, `merge`, `lookup`.
  - **Fichiers** : `file`, `templatefile`.

---

### **Astuces Avancées**
- **Data Sources** : Récupérez des infos existantes :
  ```hcl
  data "aws_ami" "ubuntu" {
    most_recent = true
    owners      = ["099720109477"]  # Canonical
  }
  ```
- **Dynamic Blocks** : Générez des blocs dynamiques :
  ```hcl
  dynamic "security_group_rule" {
    for_each = var.rules
    content {
      type        = security_group_rule.value.type
      cidr_blocks = security_group_rule.value.cidr_blocks
      # ...
    }
  }
  ```
- **Provisioners** (à éviter si possible) :
  ```hcl
  resource "aws_instance" "web" {
    provisioner "remote-exec" {
      inline = ["sudo apt update"]
    }
  }
  ```

---

### **Exemple de Workflow**
```bash
# Initialiser
terraform init

# Planifier les changements
terraform plan -out=tfplan

# Appliquer
terraform apply tfplan

# Détruire
terraform destroy
```

---

### **Aide-Mémoire Rapide**
```bash
# Afficher les outputs
terraform output public_ip

# Importer une ressource existante
terraform import aws_instance.web i-1234567890abcdef0

# Rafraîchir le state
terraform refresh

# Débuguer
TF_LOG=DEBUG terraform apply
```

📚 **Documentation** :
- [Terraform Docs](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform)
