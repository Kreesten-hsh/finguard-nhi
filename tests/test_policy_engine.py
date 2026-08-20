"""
Tests unitaires et d'intégration pour le proxy FinGuard-NHI.
Couvre les contrôles déterministes d'accès (policy_engine.py) et
la validation stricte des schémas Pydantic (schemas.py - Rempart ASI01/ASI03).
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ============================================================================
# TESTS DU MOTEUR DE RÈGLES (policy_engine.py) - BRANCHES DE DÉCISION
# ============================================================================

def test_readonly_ne_peut_pas_rembourser():
    """
    Cas 1 - Rempart ASI03 (Moindre Privilège / Violation de périmètre) :
    Un agent en lecture seule (agent_readonly) ne doit JAMAIS pouvoir
    déclencher une opération de remboursement, quel que soit le montant.
    """
    payload = {
        "agent_id": "AGENT-READ-01",
        "role": "agent_readonly",
        "operation": "execution_remboursement",
        "montant_xof": 10000.0,
        "reference_client": "CLI-BENIN-001",
        "motif_litige": "Demande de remboursement par agent non autorisé"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "REJETE"
    assert data["reason_code"] == "ROLE_INSUFFISANT"
    assert data["montant_xof"] == 10000.0


def test_remboursement_sous_seuil_autorise():
    """
    Cas 2 - Rôle valide sous le seuil pédagogique de 50 000 XOF :
    L'agent avec rôle agent_payout demandant 49 999 XOF doit être autorisé
    en autonomie complète.
    """
    payload = {
        "agent_id": "AGENT-PAYOUT-01",
        "role": "agent_payout",
        "operation": "execution_remboursement",
        "montant_xof": 49999.0,
        "reference_client": "CLI-BENIN-002",
        "motif_litige": "Remboursement transaction échouée TPE"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "AUTORISE"
    assert data["reason_code"] == "OK"
    assert data["montant_xof"] == 49999.0


def test_remboursement_seuil_exact_50000_autorise():
    """
    Cas 3 - Test aux limites (Boundary test) à 50 000 XOF exact :
    La condition étant montant > 50 000, le seuil exact de 50 000 XOF doit
    rester autorisé de manière déterministe.
    """
    payload = {
        "agent_id": "AGENT-PAYOUT-01",
        "role": "agent_payout",
        "operation": "execution_remboursement",
        "montant_xof": 50000.0,
        "reference_client": "CLI-BENIN-003",
        "motif_litige": "Remboursement seuil exact limite"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "AUTORISE"
    assert data["reason_code"] == "OK"
    assert data["montant_xof"] == 50000.0


def test_remboursement_au_dessus_seuil_escalade_humaine():
    """
    Cas 4 - Test aux limites (Boundary test) à 50 001 XOF :
    Dès 1 XOF au-delà du seuil de 50 000 XOF, le proxy déclenche
    obligatoirement le garde-fou d'escalade vers un opérateur humain.
    """
    payload = {
        "agent_id": "AGENT-PAYOUT-01",
        "role": "agent_payout",
        "operation": "execution_remboursement",
        "montant_xof": 50001.0,
        "reference_client": "CLI-BENIN-004",
        "motif_litige": "Dépassement de seuil pour validation humaine"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "ESCALADE_HUMAINE"
    assert data["reason_code"] == "SEUIL_DEPASSE"
    assert data["montant_xof"] == 50001.0


def test_lecture_transaction_readonly_autorise():
    """
    Cas 5 - Opération de lecture pour rôle agent_readonly :
    Vérifie que le rôle readonly fonctionne normalement pour son périmètre
    dédié (lecture) et n'est pas bloqué globalement.
    """
    payload = {
        "agent_id": "AGENT-READ-01",
        "role": "agent_readonly",
        "operation": "lecture_transaction",
        "montant_xof": 0.0,
        "reference_client": "CLI-BENIN-005",
        "motif_litige": "Consultation historique transaction"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "AUTORISE"
    assert data["reason_code"] == "OK"


def test_verification_kyc_payout_autorise():
    """
    Cas 6 - Opération de vérification KYC pour rôle agent_payout :
    Vérifie qu'un rôle payout conserve ses droits de consultation et
    de vérification KYC nécessaires aux vérifications pré-paiement.
    """
    payload = {
        "agent_id": "AGENT-PAYOUT-01",
        "role": "agent_payout",
        "operation": "verification_kyc",
        "montant_xof": 0.0,
        "reference_client": "CLI-BENIN-006",
        "motif_litige": "Contrôle KYC préalable"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "AUTORISE"
    assert data["reason_code"] == "OK"


# ============================================================================
# TESTS DE VALIDATION DE SCHÉMA (schemas.py) - REJET AMONT 422
# ============================================================================

def test_rejet_role_invalide_schema_422():
    """
    Cas 7 - Défense contre l'usurpation / injection de rôles :
    L'injection d'un rôle arbitraire ('super_admin') non déclaré dans l'Enum
    RoleNHI est interceptée par Pydantic et rejetée avec HTTP 422.
    """
    payload = {
        "agent_id": "AGENT-ATTACK-01",
        "role": "super_admin",
        "operation": "execution_remboursement",
        "montant_xof": 1000.0,
        "reference_client": "CLI-BENIN-007",
        "motif_litige": "Tentative d'élévation de privilège"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 422


def test_rejet_montant_negatif_schema_422():
    """
    Cas 8 - Intégrité des données financières (Plafond ge=0) :
    Un montant négatif (-100 XOF) susceptible de corrompre la logique
    comptable est rejeté par validation Pydantic avec HTTP 422.
    """
    payload = {
        "agent_id": "AGENT-PAYOUT-01",
        "role": "agent_payout",
        "operation": "execution_remboursement",
        "montant_xof": -100.0,
        "reference_client": "CLI-BENIN-008",
        "motif_litige": "Montant erroné ou manipulé"
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 422


def test_rejet_motif_trop_long_asi01_schema_422():
    """
    Cas 9 - Rempart ASI01 (Prompt / Payload Injection) :
    Une charge utile dépassant la limite structurelle de 500 caractères sur
    motif_litige est bloquée net par Pydantic (HTTP 422) avant traitement.
    """
    payload_long = "A" * 501
    payload = {
        "agent_id": "AGENT-PAYOUT-01",
        "role": "agent_payout",
        "operation": "execution_remboursement",
        "montant_xof": 1000.0,
        "reference_client": "CLI-BENIN-009",
        "motif_litige": payload_long
    }
    response = client.post("/agent/requete", json=payload)
    assert response.status_code == 422
