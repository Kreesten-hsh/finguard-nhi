# Modélisation des Menaces : AgentPay (FinGuard-NHI)

**Auteur :** Kreesten-Eddy Agboton  
**Référentiel :** OWASP Top 10 for Agentic Applications (2026)  
**Contexte Métier :** Agent IA Autonome de Réconciliation Mobile Money (Fintech UEMOA)  
**Date d'actualisation :** Août 2026  

---

## 1. Contexte Opérationnel et Périmètre du Système

### 1.1 Profil de l'Agent (`AgentPay`)
`AgentPay` est une Identité Non-Humaine (NHI) disposant de droits d'accès machine propres. Sa mission est d'automatiser le traitement des réclamations et litiges sur des flux Mobile Money :
1. **Lecture** des transactions en attente dans la base de données interne (`bank_db`).
2. **Interrogation** d'une API tierce pour la vérification KYC / statut du compte client.
3. **Exécution** de remboursements financiers via une passerelle de paiement Mobile Money.

### 1.2 Règle Métier de Simulation (Hypothèse Pédagogique du Lab)
* **Montant $\le 50\,000\text{ XOF}$** : Traitement et remboursement automatisés si validation technique.
* **Montant $> 50\,000\text{ XOF}$** : Escalade obligatoire avec blocage préventif et soumission à validation humaine (*Human-in-the-Loop*).
*(Note : Ce plafond est une règle arbitraire définie pour la démonstration technique du lab).*

---

## 2. Matrice Formelle des Menaces (OWASP ASI01 à ASI10)

| Réf. OWASP | Catégorie de Risque | Vecteur d'Attaque sur `AgentPay` | Impact Métier | Contrôle Défensif Cible (FinGuard-NHI) |
| :--- | :--- | :--- | :--- | :--- |
| **ASI01** | **Agent Goal Hijack** | Injection de prompt indirecte dans le champ `motif_litige` ou `reference_client` de la transaction lue en base. | L'agent abandonne sa tâche de vérification et émet un remboursement indu. | Assainissement déterministe des entrées avant inclusion dans le contexte de prompt. |
| **ASI02** | **Tool Misuse & Exploitation** | Détournement des arguments d'appel d'outil (ex: rediriger le paiement vers un wallet non lié au dossier). | Fuite de liquidités / vol direct de fonds Mobile Money. | Validation stricte du schéma d'appel d'outil (*Tool Call Schema Validation*) par le proxy. |
| **ASI03** | **Identity & Privilege Abuse (NHI)** | Tentative d'utilisation des credentials pour exécuter des requêtes DDL/DML arbitraires ou accéder à d'autres services. | Élévation de privilèges machine / compromission de la base bancaire. | Jetons éphémères restreints (*scoped tokens*), principe du moindre privilège, RBAC/ABAC via moteur de règles Python (app/policy_engine.py). |
| **ASI04** | **Agentic Supply Chain Vulnerabilities** | Dépendance externe compromise (librairie d'orchestration d'agent, modèle ou outil tiers empoisonné). | Exécution de code malveillant au cœur de l'agent. | Verrouillage strict des dépendances (`requirements.lock`), conteneurs minimaux sans droits root. |
| **ASI05** | **Unexpected Code Execution (RCE)** | L'agent génère ou exécute du code interprété dynamiquement pour traiter une structure de données atypique. | Prise de contrôle total du conteneur de l'agent. | Interdiction totale d'interpréteur de code dynamique (`eval`, `exec`) dans l'environnement d'exécution. |
| **ASI06** | **Memory & Context Poisoning** | Injection persistante d'instructions malveillantes dans la mémoire de travail ou l'historique des litiges traités. | Déviation durable des décisions futures sur les transactions suivantes. | Sessions d'exécution *stateless* par transaction sans persistance de mémoire non validée. |
| **ASI07** | **Insecure Inter-Agent / API Comm** | Réponse de l'API KYC falsifiée (usurpation, absence d'authentification mutuelle ou interception). | Validation de remboursements pour des comptes frauduleux. | Chiffrement mTLS et vérification cryptographique des signatures d'API tierces. |
| **ASI08** | **Cascading Failures & Agent Drift** | Boucle autonome d'approbation massive de micro-remboursements sous le seuil de 50 000 XOF. | Vidage de la trésorerie par fractionnement d'attaques (*smurfing*). | *Rate-limiting* global et plafonds cumulatifs glissants par fenêtre de temps sur le proxy. |
| **ASI09** | **Human-Agent Trust Exploitation** | L'agent génère une justification hautement plausible mais falsifiée pour faire valider un litige $> 50\,000\text{ XOF}$ par l'opérateur humain. | L'opérateur humain valide aveuglément la fraude (*rubber-stamping*). | Présentation brute des preuves techniques vérifiées (données sources) sans se fier au résumé narratif de l'agent. |
| **ASI10** | **Rogue Agents** | Dérive autonome progressive de l'agent due à l'accumulation de contexte ou à un biais statistique, sans attaquant externe. | Décisions financières erratiques ou systématiquement favorables au remboursement. | Mécanisme de surveillance comportementale et coupe-circuit automatique (*Kill-Switch*). |

---

## 3. Contrôle Transversal : Observabilité & Traçabilité Médico-légale

Pour garantir la non-répudiation et permettre les audits de conformité :
* **Format Standardisé** : Journalisation de tous les événements au format CEF (*Common Event Format*) / JSON structuré.
* **Corrélation Stricte** : Chaque ligne d'audit lie de façon indélébile :
  `Timestamp_UTC | Agent_ID | Token_Fingerprint | Input_Hash | Tool_Called | Proxy_Decision | Reason_Code`
* **Intégrité des Journaux** : Les journaux sont écrits dans un volume en lecture seule pour l'agent, empêchant toute suppression de traces après exécution.
