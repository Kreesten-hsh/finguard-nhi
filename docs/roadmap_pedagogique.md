# Feuille de Route Pédagogique et Alignement Académique — FinGuard-NHI

**Auteur :** Kreesten-Eddy Agboton  
**Candidat :** L3 Informatique (SIL) — HECM Cotonou, Bénin  
**Référentiels :** Google Cybersecurity Professional Certificate & OWASP Top 10 for Agentic Applications (2026)  
**Dernière mise à jour :** Août 2026  

---

## 1. Objectif du Document et Principe Directeur

Ce document formalise la passerelle méthodologique entre l'acquisition académique des compétences du programme **Google Cybersecurity Professional Certificate** et l'implémentation logicielle du projet **FinGuard-NHI**.

### Règle d'Intégrité Pédagogique
> **Principe fondamental :** Aucune notion technique ou brique d'ingénierie de sécurité n'est intégrée au code source du projet sans avoir été formellement validée dans le cursus de certification correspondant ou préalablement maîtrisée et documentée.

L'objectif est de garantir une totale traçabilité entre la théorie de sécurité (fondations, réseaux, menaces, détection SIEM, automatisation) et les livrables d'ingénierie logicielle pour un futur jury académique ou technique (CISO / Bourse CSC).

---

## 2. Tableau de Correspondance : Certificat Google vs FinGuard-NHI

| Cours Google Cybersecurity | Statut | Éléments du Projet Déjà Couverts | Éléments du Projet à NE PAS Démarrer Avant ce Cours |
| :--- | :--- | :--- | :--- |
| **Cours 1 à 5** :<br>- Foundations of Cybersecurity<br>- Play It Safe: Manage Security Risks<br>- Connect & Protect: Network Security<br>- Tools of the Trade: Linux & SQL<br>- Assets, Threats, and Vulnerabilities | **Terminé**<br>(Validé Août 2026) | - Modélisation formelle des menaces (`docs/threat_model.md` — ASI01 à ASI10).<br>- Isolation réseau et conteneurisation durcie (`docker-compose.yml`, bridge isolé).<br>- Moindre privilège SQL (`agent_readonly` sur PostgreSQL).<br>- Filtrage de flux et règles RBAC/IAM déterministes (`app/policy_engine.py`). | N/A (Prérequis théoriques et systèmes entièrement validés). |
| **Cours 6** :<br>Sound the Alarm: Detection and Response | **En cours**<br>(Module 1/4) | - Analyse initiale des flux réseau et capture de paquets (`tcpdump`).<br>- Filtrage basique de journaux système via outils POSIX (`grep`, `awk`). | **Interdiction d'implémenter `app/audit_logger.py`** tant que les modules dédiés aux formats de logs (CEF / JSON structuré), à l'ingestion SIEM et aux métriques de détection d'anomalies ne sont pas achevés et validés. |
| **Cours 7** :<br>Automate Cybersecurity Tasks with Python | **Pas commencé** | - Squelette du proxy HTTP (`app/main.py`).<br>- Validation des schémas de données (`app/schemas.py`).<br>- Suite de tests automatisés (`tests/test_policy_engine.py`).<br>*(Voir section 3 pour la justification).* | - Scripts d'automatisation avancée de réponse aux incidents.<br>- Intégration de pipelines de remédiation automatisée des logs SIEM. |
| **Cours 8 & Capstone** :<br>Put It to Work: Prepare for Cybersecurity Jobs | **Pas commencé** | N/A | - Rapport final d'audit de sécurité et gouvernance.<br>- Documentation de synthèse d'architecture et soutenance finale (Jalon 4). |

---

## 3. Note de Transparence Explicite (Compétences Python)

Le développement du **Jalon 1** (squelette réseau FastAPI, validation Pydantic, moteur de règles `policy_engine.py` et suite de tests `pytest`) a été réalisé avant le démarrage du **Cours 7 (Automate Cybersecurity Tasks with Python)**.

Cette implémentation s'appuie exclusivement sur des compétences préalables en développement Python et génie logiciel (validation du cursus *Machine Learning with Python* de ~300h via freeCodeCamp, Août 2026). Ce travail est explicitement documenté comme une mobilisation de compétences préexistantes et non comme un livrable issu du Cours 7 du certificat Google.

---

## 4. Protocole Opérationnel de Progression

À compter de la validation du Jalon 1, la gouvernance de développement suit la règle suivante :

1. **Condition de Démarrage :** Aucun nouveau jalon d'ingénierie (à commencer par le Jalon 2 — journalisation CEF et télémétrie de détection) ne sera initié sans une confirmation écrite préalable de Kreesten-Eddy Agboton attestant de la finalisation des modules de cours correspondants dans la plateforme Google / Coursera.
2. **Revue de Cohérence :** Avant toute écriture de code, les concepts vus en cours (ex. champs d'en-tête CEF, sévérité normalisée, horodatage UTC, corrélation d'identifiants machines) devront être confrontés au plan d'architecture du composant cible.
3. **Traçabilité :** Tout écart ou adaptation par rapport au modèle initial devra être consigné dans ce document avant d'être fusionné dans la branche principale (`main`).
