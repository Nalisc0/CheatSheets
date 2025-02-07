### **Concepts Clés**
- **Régions/Zones de disponibilité (AZ)** : AWS divise le monde en régions (ex: `us-east-1`), chacune avec plusieurs AZ.
- **Services principaux** : EC2 (machines virtuelles), S3 (stockage objet), RDS (bases de données), Lambda (serverless), IAM (gestion des accès).
- **Modèle de tarification** : Pay-as-you-go (facturation à l’usage).
- **ARN (Amazon Resource Name)** : Identifiant unique des ressources AWS (ex: `arn:aws:s3:::my-bucket`).

---

### **AWS CLI (Command Line Interface)**
1. **Installation** :
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```
2. **Configuration** :
   ```bash
   aws configure  # Configure les clés d’accès, région par défaut, etc.
   ```

---

### **Services Essentiels**

#### **EC2 (Elastic Compute Cloud)**
- **Lancer une instance** :
  ```bash
  aws ec2 run-instances \
    --image-id ami-12345678 \
    --instance-type t2.micro \
    --key-name my-key-pair
  ```
- **Liste des instances** :
  ```bash
  aws ec2 describe-instances
  ```
- **Arrêter/Supprimer** :
  ```bash
  aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
  ```

#### **S3 (Simple Storage Service)**
- **Créer un bucket** :
  ```bash
  aws s3 mb s3://mon-bucket --region eu-west-1
  ```
- **Copier un fichier** :
  ```bash
  aws s3 cp fichier.txt s3://mon-bucket/
  ```
- **Synchroniser un dossier** :
  ```bash
  aws s3 sync ./dossier s3://mon-bucket/dossier
  ```
- **Activer le versioning** :
  ```bash
  aws s3api put-bucket-versioning --bucket mon-bucket --versioning-configuration Status=Enabled
  ```

#### **IAM (Identity and Access Management)**
- **Créer un utilisateur** :
  ```bash
  aws iam create-user --user-name alice
  ```
- **Attacher une politique** :
  ```bash
  aws iam attach-user-policy --user-name alice --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
  ```
- **Créer un rôle** :
  ```json
  # trust-policy.json
  {
    "Version": "2012-10-17",
    "Statement": [{ "Effect": "Allow", "Principal": { "Service": "lambda.amazonaws.com" }, "Action": "sts:AssumeRole" }]
  }
  ```
  ```bash
  aws iam create-role --role-name LambdaRole --assume-role-policy-document file://trust-policy.json
  ```

#### **Lambda (Serverless)**
- **Créer une fonction** :
  ```bash
  aws lambda create-function \
    --function-name ma-fonction \
    --runtime python3.9 \
    --role arn:aws:iam::123456789012:role/LambdaRole \
    --handler lambda_function.handler \
    --zip-file fileb://function.zip
  ```
- **Invoquer une fonction** :
  ```bash
  aws lambda invoke --function-name ma-fonction output.txt
  ```

#### **RDS (Relational Database Service)**
- **Créer une instance MySQL** :
  ```bash
  aws rds create-db-instance \
    --db-instance-identifier mydb \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username admin \
    --master-user-password password \
    --allocated-storage 20
  ```

---

### **Réseau et Sécurité**

#### **VPC (Virtual Private Cloud)**
- **Créer un VPC** :
  ```bash
  aws ec2 create-vpc --cidr-block 10.0.0.0/16
  ```
- **Créer un sous-réseau** :
  ```bash
  aws ec2 create-subnet --vpc-id vpc-123456 --cidr-block 10.0.1.0/24
  ```

#### **Security Groups (Groupes de sécurité)**
- **Autoriser le port SSH** :
  ```bash
  aws ec2 authorize-security-group-ingress \
    --group-id sg-123456 \
    --protocol tcp --port 22 --cidr 0.0.0.0/0
  ```

#### **Route 53 (DNS)**
- **Créer un enregistrement DNS** :
  ```bash
  aws route53 change-resource-record-sets \
    --hosted-zone-id Z123456789 \
    --change-batch '{"Changes": [{ "Action": "CREATE", "ResourceRecordSet": { "Name": "example.com", "Type": "A", "TTL": 300, "ResourceRecords": [{ "Value": "192.0.2.1" }] } }]}'
  ```

---

### **Gestion et Surveillance**

#### **CloudWatch (Monitoring)**
- **Voir les logs** :
  ```bash
  aws logs tail /aws/lambda/ma-fonction --follow
  ```
- **Créer une alarme** :
  ```bash
  aws cloudwatch put-metric-alarm \
    --alarm-name CPU-Alarm \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
  ```

#### **CloudFormation (Infrastructure as Code)**
- **Exemple de template** (`template.yml`) :
  ```yaml
  AWSTemplateFormatVersion: '2010-09-09'
  Resources:
    MyEC2Instance:
      Type: AWS::EC2::Instance
      Properties:
        ImageId: ami-12345678
        InstanceType: t2.micro
  ```
- **Déployer** :
  ```bash
  aws cloudformation deploy --template-file template.yml --stack-name my-stack
  ```

---

### **Bonnes Pratiques**
1. **IAM** :
   - Utilisez des rôles plutôt que des clés d’accès pour les ressources.
   - Appliquez le principe du moindre privilège.
   - Activez la MFA (Authentification multi-facteurs).
2. **Coûts** :
   - Surveillez les coûts avec **AWS Cost Explorer**.
   - Supprimez les ressources inutilisées (instances EC2 arrêtées, buckets S3 vides).
3. **Haute disponibilité** :
   - Répartissez les instances sur plusieurs AZ.
   - Utilisez des groupes Auto Scaling.
4. **Sécurité** :
   - Chiffrez les données au repos (S3, EBS, RDS).
   - Utilisez des Security Groups restrictifs.

---

### **Astuces CLI**
- **Filtrage avec `--query`** :
  ```bash
  aws ec2 describe-instances --query "Reservations[*].Instances[*].{ID:InstanceId, IP:PublicIpAddress}"
  ```
- **Sortie formatée** :
  ```bash
  aws s3 ls --human-readable  # Taille lisible
  aws ec2 describe-vpcs --output table  # Format tableau
  ```
- **Profils multiples** :
  ```bash
  aws s3 ls --profile production  # Utilise le profil "production"
  ```

---

### **Commandes Utiles en One-Liner**
- **Liste des buckets S3** :
  ```bash
  aws s3 ls
  ```
- **Télécharger un fichier depuis S3** :
  ```bash
  aws s3 cp s3://mon-bucket/fichier.txt .
  ```
- **Redémarrer une instance EC2** :
  ```bash
  aws ec2 reboot-instances --instance-ids i-1234567890abcdef0
  ```
- **Obtenir l’adresse IP publique d’une instance** :
  ```bash
  aws ec2 describe-instances --instance-ids i-1234567890abcdef0 --query "Reservations[0].Instances[0].PublicIpAddress" --output text
  ```

---

### **Outils Associés**
- **AWS SAM** : Framework serverless pour déployer des fonctions Lambda.
- **AWS CDK** : Définir l’infrastructure en code (TypeScript, Python, etc.).
- **AWS SDKs** : Intégration avec des langages comme Python, JavaScript, Java.
- **AWS Copilot** : CLI pour déployer des applications conteneurisées.

📚 **Documentation** :
- [AWS CLI Reference](https://awscli.amazonaws.com/v2/documentation/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Cheat Sheets](https://tutorialsdojo.com/aws-cheat-sheets/)
