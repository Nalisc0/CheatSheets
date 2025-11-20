# 🔥 1) Bases essentielles

### Voir les règles

```bash
sudo iptables -L -v -n
```

### Voir les règles avec les numéros de ligne

```bash
sudo iptables -L -v -n --line-numbers
```

### Vider toutes les règles

```bash
sudo iptables -F
```

### Supprimer une règle selon son numéro

```bash
sudo iptables -D INPUT 3
```

### Définir les politiques par défaut

```bash
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
```

---

# 🎯 2) Tables & chaînes principales

### Tables

| Table      | Fonction                            |
| ---------- | ----------------------------------- |
| **filter** | firewall (INPUT / OUTPUT / FORWARD) |
| **nat**    | NAT, masquerading, DNAT, SNAT       |
| **mangle** | marquage de paquets, QoS            |
| **raw**    | exemptions de tracking (conntrack)  |

### Chaînes

| Chaîne          | Fonction                            |
| --------------- | ----------------------------------- |
| **INPUT**       | trafic entrant destiné à la machine |
| **OUTPUT**      | trafic émis par la machine          |
| **FORWARD**     | trafic routé à travers la machine   |
| **PREROUTING**  | modification avant routage          |
| **POSTROUTING** | modification après routage          |

---

# 🌐 3) Règles simples INPUT / OUTPUT

### Autoriser SSH

```bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

### Autoriser HTTP/HTTPS

```bash
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT
```

### Autoriser ICMP (ping)

```bash
iptables -A INPUT -p icmp -j ACCEPT
```

### Bloquer une IP

```bash
iptables -A INPUT -s 1.2.3.4 -j DROP
```

### Bloquer un port

```bash
iptables -A INPUT -p tcp --dport 23 -j DROP
```

---

# 🔐 4) Stateful firewall (conntrack)

### Autoriser les connexions établies et relatives

```bash
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

### Bloquer les paquets invalides

```bash
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
```

---

# 🔄 5) NAT — Masquerading (VPN, partage de connexion)

### Activer le NAT (postrouting)

```bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### Exemple complet pour routeur/VPN :

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

---

# ↪️ 6) DNAT — Redirection de port (port-forwarding)

### Rediriger le port externe 80 vers une machine interne

```bash
iptables -t nat -A PREROUTING -p tcp --dport 80 \
  -j DNAT --to-destination 192.168.1.10:8080
```

### Avec FORWARD autorisé :

```bash
iptables -A FORWARD -p tcp -d 192.168.1.10 --dport 8080 -j ACCEPT
```

---

# 🔁 7) SNAT — Changer l’IP source

### Fixer l’IP source à 1.2.3.4

```bash
iptables -t nat -A POSTROUTING -o eth0 \
  -j SNAT --to-source 1.2.3.4
```

---

# 📜 8) Logging

### Loguer un packet INPUT

```bash
iptables -A INPUT -j LOG --log-prefix "iptables-input: "
```

### Log + DROP

```bash
iptables -A INPUT -j LOG --log-prefix "iptables-dropped: "
iptables -A INPUT -j DROP
```

---

# 🛡️ 9) Anti-DDoS & protection

### Limiter les connexions SSH (3 connexions/min)

```bash
iptables -A INPUT -p tcp --dport 22 \
  -m limit --limit 3/min -j ACCEPT
```

### Bloquer le scan SYN flood

```bash
iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP
```

### Limiter ICMP (ping)

```bash
iptables -A INPUT -p icmp -m limit --limit 1/s -j ACCEPT
```

---

# 🚫 10) Bloquer par ports / protocoles

### Bloquer tout UDP

```bash
iptables -A INPUT -p udp -j DROP
```

### Bloquer une plage de ports

```bash
iptables -A INPUT -p tcp --dport 1:1024 -j DROP
```

---

# 🧪 11) Mangle table — marquage de paquets (QoS, routing policy)

### Marquer les paquets

```bash
iptables -t mangle -A PREROUTING -p tcp --dport 443 -j MARK --set-mark 10
```

### Utilisé ensuite par `ip rule` :

```bash
ip rule add fwmark 10 table 200
```

---

# 👥 12) Filtrage par utilisateur ou groupe

### Autoriser seulement un user à sortir

```bash
iptables -A OUTPUT -p tcp --dport 80 -m owner --uid-owner alice -j ACCEPT
```

### Bloquer un user

```bash
iptables -A OUTPUT -m owner --uid-owner bob -j DROP
```

---

# 🔍 13) Filtrage avancé (modules)

### multiport (plusieurs ports)

```bash
iptables -A INPUT -p tcp -m multiport --dports 22,80,443 -j ACCEPT
```

### udp + plage

```bash
iptables -A INPUT -p udp --dport 4000:5000 -j ACCEPT
```

### IP ranges

```bash
iptables -A INPUT -m iprange --src-range 10.0.0.1-10.0.0.200 -j ACCEPT
```

---

# ♻️ 14) Sauvegarde et restauration

### Sauvegarder les règles

```bash
iptables-save > /etc/iptables.rules
```

### Restaurer

```bash
iptables-restore < /etc/iptables.rules
```

---

# 🔒 15) Exemple de firewall complet minimaliste

```bash
iptables -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
```
