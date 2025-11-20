# 🔍 1) Informations générales

### Afficher toutes les interfaces

```bash
ip a
ip addr
```

### Afficher une interface spécifique

```bash
ip a show eth0
```

### Afficher l’état des interfaces

```bash
ip link
```

### Afficher le routage

```bash
ip route
```

### Afficher les règles de policy routing (RPDB)

```bash
ip rule
```

### Afficher les voisins (ARP/NDP)

```bash
ip neigh
```

---

# 🧱 2) Gestion des interfaces réseau (link)

### Monter / Descendre une interface

```bash
ip link set eth0 up
ip link set eth0 down
```

### Modifier le nom d’une interface

```bash
ip link set eth0 name lan0
```

### Changer l’adresse MAC

```bash
ip link set eth0 address 00:11:22:33:44:55
```

### Créer une interface virtuelle (dummy)

```bash
ip link add dummy0 type dummy
ip link set dummy0 up
```

### Supprimer l’interface

```bash
ip link delete dummy0
```

---

# 🌐 3) Gestion des adresses (addr)

### Ajouter une adresse IP

```bash
ip addr add 192.168.1.10/24 dev eth0
```

### Supprimer une adresse IP

```bash
ip addr del 192.168.1.10/24 dev eth0
```

### Ajouter une IPv6

```bash
ip addr add 2001:db8::1/64 dev eth0
```

---

# 🛣️ 4) Routage (route)

### Afficher la table de routage

```bash
ip route
```

### Ajouter une route

```bash
ip route add 192.168.2.0/24 via 192.168.1.1
```

### Ajouter une route via une interface

```bash
ip route add 10.0.0.0/24 dev tun0
```

### Ajouter une route par défaut

```bash
ip route add default via 192.168.1.1
```

### Supprimer une route

```bash
ip route del 192.168.2.0/24
```

---

# 🧭 5) Policy Routing (ip rule)

### Lister les règles

```bash
ip rule show
```

### Ajouter une règle basée sur une source

```bash
ip rule add from 10.0.0.0/24 table 100
```

### Ajouter une règle basée sur le fwmark (iptables)

```bash
ip rule add fwmark 10 table 200
```

### Supprimer une règle

```bash
ip rule del from 10.0.0.0/24 table 100
```

---

# 💠 6) ARP / NDP (neigh)

### Voir les entrées ARP

```bash
ip neigh
```

### Ajouter une entrée ARP statique

```bash
ip neigh add 192.168.1.20 lladdr aa:bb:cc:dd:ee:ff dev eth0
```

### Supprimer une entrée ARP

```bash
ip neigh del 192.168.1.20 dev eth0
```

---

# 🕳️ 7) Tunnels (ip tunnel)

### Lister les tunnels

```bash
ip tunnel
```

### Créer un tunnel IPIP

```bash
ip tunnel add tun0 mode ipip remote 1.2.3.4 local 5.6.7.8
ip link set tun0 up
```

### Créer un tunnel GRE

```bash
ip tunnel add gre1 mode gre remote 1.2.3.4 local 5.6.7.8
ip link set gre1 up
```

### Supprimer un tunnel

```bash
ip tunnel del gre1
```

---

# 🎛️ 8) TUN/TAP (ip tuntap)

### Créer une interface TUN

```bash
ip tuntap add dev tun0 mode tun
ip link set tun0 up
```

### Créer une interface TAP

```bash
ip tuntap add dev tap0 mode tap
ip link set tap0 up
```

### Supprimer une interface TUN/TAP

```bash
ip tuntap del dev tun0 mode tun
```

---

# 🏷️ 9) VLAN (ip link add type vlan)

### Créer un VLAN 10 sur eth0

```bash
ip link add link eth0 name eth0.10 type vlan id 10
ip link set eth0.10 up
```

### Supprimer le VLAN

```bash
ip link delete eth0.10
```

---

# 🎚️ 10) VRF (Virtual Routing & Forwarding)

### Créer un VRF

```bash
ip link add vrf-blue type vrf table 100
ip link set vrf-blue up
```

### Associer une interface au VRF

```bash
ip link set eth1 master vrf-blue
```

---

# 📡 11) Monitoring & Debug

### Suivre les changements de lien

```bash
ip monitor link
```

### Suivre les adresses

```bash
ip monitor addr
```

### Suivre les routes

```bash
ip monitor route
```

---

# 🧨 12) Adresses multiples (IP alias)

### Ajouter plusieurs IP sur la même interface

```bash
ip addr add 10.0.0.2/24 dev eth0
ip addr add 10.0.0.3/24 dev eth0
```

---

# 🔧 13) Raccourcis utiles

### Remplacer un ifconfig

```bash
ip a
```

### Remplacer un route -n

```bash
ip route
```

### Relancer une interface

```bash
ip link set eth0 down && ip link set eth0 up
```

---

# 📜 14) Bonus : Syntaxe complète

### ip [OBJECT] [COMMAND] [OPTIONS]

Les objets courants :

| Objet     | Signification                |
| --------- | ---------------------------- |
| `link`    | interface physique/virtuelle |
| `addr`    | adresses IP                  |
| `route`   | routes                       |
| `neigh`   | ARP/NDP                      |
| `rule`    | policy routing               |
| `tunnel`  | tunnels GRE/IPIP             |
| `tuntap`  | interfaces TUN/TAP           |
| `vrf`     | routing instances            |
| `monitor` | monitoring dynamique         |

---

