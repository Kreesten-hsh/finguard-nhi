# GUIDE DE PARCOURS CYBERSÉCURITÉ & PORTFOLIO

**Auteur :** Kreesten-Eddy Agboton  
**Cible :** Dossier Master Cybersécurité (Bourse CSC 2027) & Trajectoire RSSI Secteur Financier (BCEAO/UEMOA)  
**Machine de travail :** Linux Mint (Dual-Boot, 12 Go RAM, 512 Go HDD)  

---

## 1. La Vision Globale : Pourquoi ce parcours ?

### Le Problème
Suivre des cours en ligne (Coursera, Hugging Face, freeCodeCamp) donne des bases théoriques et des QCM validés. Mais devant un jury académique ou un recruteur de haut niveau, les certificats génériques ne prouvent pas votre capacité opérationnelle. 

### La Solution
Transformer chaque concept théorique en **pratique réelle sur votre propre machine Linux**, puis consolider le tout dans un **projet de portfolio d'ingénierie unique et différenciant** : **FinGuard-NHI** (Sécurisation des Identités Non-Humaines / Agents IA dans le secteur financier).

### Les 4 Piliers Industriels du Projet (Zero Réinvention) :
1. **Taxonomie des Menaces Réelles** : Utilisation formelle de l'**OWASP Top 10 for Agentic Applications** (Goal Hijacking, Tool Misuse, Identity Abuse, Memory Poisoning, Rogue Agents).
2. **Architecture de Référence** : Inspirée et documentée à partir du **Microsoft Agent Governance Toolkit** (Open-Source MIT), réimplémentée de façon épurée pour un cas d'usage bancaire UEMOA.
3. **Moteur de Policy-as-Code** : Utilisation d'**Open Policy Agent (OPA)** pour l'évaluation déterministe des autorisations d'accès NHI.
4. **Justification Sectorielle Vérifiée** : Basée sur les rapports de la **Cloud Security Alliance (CSA)** documentant la lacune critique de gouvernance des identités non-humaines dans les SI bancaires.

---

## 2. Matrice d'Effort & Synchronisation avec Google Cyber

> **Principe de Réalisme Opérationnel :**  
> Les durées ci-dessous indiquent le **volume d'effort technique réel (en heures de pratique)** et non un calendrier calendaire rigide. Vous avancez par jalons validés, à votre rythme, sans dette psychologique.

| Jalon | Étape Technique | Effort Réel Estimé | Cours Google Associé | Compétences & Outils Réels | Livrable Concret |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Jalon 0** | **Temps 1 : Lab d'Acquisition** | **4 à 6 heures** | Cours 1 à 5 (Finalisation Cours 5) | Docker CLI, isolation réseau, Linux non-root, tcpdump, extraction de logs SQL. | **Banc d'essai opérationnel** sur votre Mint. |
| **Jalon 1** | **Temps 2.1 : Threat Model & OPA / Proxy** | **8 à 10 heures** | Cours 5 & Cours 7 (Python) | Modélisation **OWASP Agentic Top 10**, Proxy FastAPI, intégration **Open Policy Agent (OPA)**. | Squelette du proxy de sécurité & Matrice des risques BCEAO. |
| **Jalon 2** | **Temps 2.2 : Journalisation & Détection** | **8 à 10 heures** | Cours 6 : Détection & SIEM | Formatage CEF, règles d'alerte, audit trail inspiré du Microsoft Toolkit, Suricata / tcpdump. | Audit trail immuable et alertes de sécurité en direct. |
| **Jalon 3** | **Temps 2.3 : Réponse & Révocation** | **6 à 8 heures** | Cours 6 & Cours 7 | Script Python de remédiation : révocation instantanée de token d'agent compromis. | Mécanisme de kill-switch automatisé. |
| **Jalon 4** | **Temps 2.4 : Finalisation Portfolio** | **6 à 8 heures** | Cours 8 : Capstone | Documentation SAD (Security Architecture Doc), README GitHub pro, alignement réglementaire UEMOA. | **Dossier GitHub d'excellence (Production-Ready).** |

---

## 3. Comprendre le "Temps 1" (Le Lab d'Acquisition)

### De quoi s'agit-il exactement ?
Le **Temps 1** représente **4 à 6 heures d'effort pratique total**. Son but unique est de vous donner les **réflexes techniques sur Linux** que vous n'avez vus que sous forme de QCM ou de labs éphémères dans votre navigateur.

### Qu'est-ce que vous apprenez concrètement ?

1. **Docker sans interface graphique (CLI pure)** : Déployer et administrer des conteneurs au terminal.
2. **Le Durcissement Système (Linux Hardening)** : Bloquer l'élévation de privilège (`cap_drop: [ALL]`, `no-new-privileges`).
3. **L'Isolation Réseau (Network Segmentation)** : Isoler la base bancaire sur un réseau interne non exposé à Internet.
4. **L'Analyse de Trafic Réseau** : Capturer de vrais paquets TCP en transit avec `tcpdump`.
5. **Gestion Étanche des Secrets** : Séparer strictement le code des identifiants (`.env` vs `.env.example`).
6. **La Manipulation de Logs & SQL en CLI** : Forcer la journalisation PostgreSQL et extraire les anomalies avec `grep` et `psql`.

---

## 4. Guide Pratique Pas à Pas pour le Temps 1 (À partir de zéro)

---

### Étape 0 : Installer Docker Engine sur Linux Mint (10 minutes)

Ouvrez un terminal sur Linux Mint et copiez-collez ce bloc de commandes pour installer la version officielle de Docker :

```bash
# 1. Mise à jour des paquets et installation des prérequis
sudo apt update && sudo apt install -y ca-certificates curl gnupg lsb-release

# 2. Ajout de la clé de sécurité officielle de Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Ajout du dépôt Docker officiel pour Linux Mint (base Ubuntu)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$UBUNTU_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Installation de Docker Engine et du plugin Compose
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. Autoriser votre utilisateur à utiliser Docker sans taper 'sudo' à chaque fois
sudo usermod -aG docker $USER
```

> **IMPORTANT :** Une fois ces commandes terminées, appliquez vos nouveaux droits de groupe immédiatement en tapant :
> ```bash
> newgrp docker
> ```
> 
> **Test de validation :**
> ```bash
> docker run --rm hello-world
> ```
> *(Si vous voyez le message "Hello from Docker!", Docker est parfaitement installé).*

---

### Étape 1 : Création Automatique des Fichiers & Gestion des Secrets (5 minutes)

Copiez-collez les blocs suivants dans votre terminal pour initialiser l'espace de travail avec gestion étanche des identifiants :

#### 1. Création des dossiers
```bash
mkdir -p ~/lab-sec-socle/nginx ~/lab-sec-socle/postgres ~/lab-sec-socle/logs/nginx ~/lab-sec-socle/logs/postgres
cd ~/lab-sec-socle
```

#### 2. Création du fichier `.gitignore` (Protection contre la fuite d'identifiants)
```bash
cat << 'EOF' > ~/lab-sec-socle/.gitignore
.env
logs/
*.log
EOF
```

#### 3. Création du modèle public `.env.example` (Committed to Git)
```bash
cat << 'EOF' > ~/lab-sec-socle/.env.example
# Modèle de configuration (ne contient aucun secret réel)
POSTGRES_DB=bank_db
POSTGRES_USER=admin_sec
POSTGRES_PASSWORD=ChangeMeInYourEnvFile!
AGENT_READONLY_PASSWORD=ChangeMeInYourEnvFile!
EOF
```

#### 4. Création du fichier secret local `.env` (Ignored by Git)
```bash
cat << 'EOF' > ~/lab-sec-socle/.env
# Identifiants réels du Lab (Strictement locaux)
POSTGRES_DB=bank_db
POSTGRES_USER=admin_sec
POSTGRES_PASSWORD=AdminMasterKey2026!
AGENT_READONLY_PASSWORD=SecureReadOnly2026!
EOF
```

#### 5. Configuration Nginx (`nginx/default.conf`)
```bash
cat << 'EOF' > ~/lab-sec-socle/nginx/default.conf
server {
    listen 8080;
    server_name localhost;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log warn;

    location / {
        return 200 '{"status":"operational","service":"core-gateway"}\n';
        add_header Content-Type application/json;
    }

    location /api/v1/health {
        return 200 '{"health":"ok"}\n';
        add_header Content-Type application/json;
    }
}
EOF
```

#### 6. Script d'initialisation PostgreSQL dynamique (`postgres/init.sh`)
*Ce script utilise directement les variables d'environnement du `.env` au démarrage sans aucun mot de passe en dur.*
```bash
cat << 'EOF' > ~/lab-sec-socle/postgres/init.sh
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Table des transactions bancaires
    CREATE TABLE IF NOT EXISTS audit_transactions (
        id SERIAL PRIMARY KEY,
        sender_account VARCHAR(34) NOT NULL,
        recipient_account VARCHAR(34) NOT NULL,
        amount NUMERIC(12, 2) NOT NULL,
        currency VARCHAR(3) DEFAULT 'XOF',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Données initiales de test
    INSERT INTO audit_transactions (sender_account, recipient_account, amount) VALUES
    ('CI0340100112345678901234', 'BJ0610100198765432109876', 150000.00),
    ('BJ0610100198765432109876', 'SN0120100155555555555555', 45000.00);

    -- Compte applicatif à Moindre Privilège (Lecture Seule)
    -- Le mot de passe est injecté dynamiquement depuis la variable d'environnement
    CREATE USER agent_readonly WITH PASSWORD '$AGENT_READONLY_PASSWORD';
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO agent_readonly;
    GRANT USAGE ON SCHEMA public TO agent_readonly;
    GRANT SELECT ON audit_transactions TO agent_readonly;
EOSQL
EOF
chmod +x ~/lab-sec-socle/postgres/init.sh
```

#### 7. Orchestrateur sécurisé sans mot de passe en clair (`docker-compose.yml`)
```bash
cat << 'EOF' > ~/lab-sec-socle/docker-compose.yml
services:
  gateway:
    image: nginx:alpine
    container_name: lab_gateway
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ./logs/nginx:/var/log/nginx
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
      - CHOWN
      - SETUID
      - SETGID
    networks:
      - internal_net

  database:
    image: postgres:15-alpine
    container_name: lab_db
    restart: unless-stopped
    env_file:
      - .env
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      AGENT_READONLY_PASSWORD: ${AGENT_READONLY_PASSWORD}
    volumes:
      - ./postgres/init.sh:/docker-entrypoint-initdb.d/init.sh:ro
      - ./logs/postgres:/var/log/postgresql
    command: >
      postgres
      -c logging_collector=on
      -c log_destination=stderr
      -c log_directory=/var/log/postgresql
      -c log_filename=postgresql.log
      -c log_connections=on
      -c log_disconnections=on
      -c log_statement=all
      -c log_line_prefix='%m [%p] %u@%d '
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
      - DAC_OVERRIDE
    networks:
      - internal_net

networks:
  internal_net:
    driver: bridge
EOF
```

---

### Étape 2 : Lancement et Vérification

Toujours dans le dossier `~/lab-sec-socle`, lancez les conteneurs :

```bash
# Lancer les conteneurs en arrière-plan
docker compose up -d

# Vérifier que les 2 conteneurs ont le statut "Up"
docker compose ps
```

---

### Étape 3 : Les 3 Exercices Pratiques à Réaliser

#### Exercice 1 : Test du Moindre Privilège SQL
*Objectif : Constater qu'un compte d'agent restreint ne peut pas saboter la base de données.*

1. Ouvrez une session SQL avec le compte en lecture seule :
   ```bash
   docker exec -it lab_db psql -U agent_readonly -d bank_db
   ```
2. Testez une lecture autorisée :
   ```sql
   SELECT * FROM audit_transactions;
   ```
   *(Vous devez voir les 2 transactions s'afficher).*
3. Tentez de supprimer la table :
   ```sql
   DROP TABLE audit_transactions;
   ```
   *(PostgreSQL refuse avec l'erreur : `ERROR: must be owner of table audit_transactions`).*
4. Quittez la console SQL :
   ```sql
   \q
   ```

---

#### Exercice 2 : Capture de Trafic Réseau en Direct
*Objectif : Voir les paquets réseau circuler entre votre machine et le serveur.*

1. Dans votre terminal, lancez une capture de paquets sur le port HTTP 8080 :
   ```bash
   sudo tcpdump -i lo port 8080 -A -c 6
   ```
2. Ouvrez un **deuxième onglet de terminal** et envoyez une requête HTTP :
   ```bash
   curl http://127.0.0.1:8080/api/v1/health
   ```
3. Regardez dans le premier terminal : vous voyez en clair les en-têtes HTTP, la méthode `GET`, le code `200 OK` et la charge utile JSON.

---

#### Exercice 3 : Traque d'Attaques dans les Fichiers de Logs
*Objectif : Retrouver les traces d'une tentative d'intrusion sans interface graphique.*

1. Simulez une tentative de connexion pirate avec un faux utilisateur :
   ```bash
   docker exec -it lab_db psql -U intrus_malveillant -d bank_db
   ```
   *(La connexion échoue immédiatement).*
2. Inspectez les fichiers de logs générés en direct par PostgreSQL avec `grep` :
   ```bash
   grep "FATAL" ~/lab-sec-socle/logs/postgres/postgresql.log
   ```
3. Vous visualisez l'horodatage exact, le nom de l'utilisateur refusé (`intrus_malveillant`) et la raison du rejet.

---

## 5. Ce qui se passe après (Temps 2)

Une fois ces 3 exercices réalisés :
- Vous avez la preuve concrète que vous maîtrisez Docker, l'isolation réseau, les permissions non-root et l'analyse de logs sur votre machine.
- Nous remplacerons ensuite le serveur Nginx par votre propre **Proxy Python FastAPI (FinGuard-NHI)** développé au fil des cours 6, 7 et 8 pour filtrer les requêtes d'un vrai agent IA bancaire.

---

## 6. Ressources Ciblées & Références d'Appui (Extraites de 90DaysOfCyberSecurity)

Pour approfondir les phases techniques sans vous disperser, piochez **uniquement** dans ces 2 sections vérifiées du référentiel open-source de Farhan Ashraf :

1. **Pour l'Exercice 2 & le Jalon 2 (Analyse de Trafic Réseau)** :
   * *Section Traffic Analysis (Jours 43 à 56)* : Guides pratiques Wireshark et syntaxe de filtres BPF pour aller au-delà de `tcpdump` brut.
   * *Suricata IDS* : Documentation sur l'écriture de règles de détection d'anomalies sur les flux réseau.
2. **Pour le Jalon 2 (Journalisation & SIEM)** :
   * *Section Log Analysis & SIEM Concepts (Jours 64 à 70 / ELK)* : Principes de centralisation, formats d'événements et normalisation de logs pour structurer vos traces CEF.
