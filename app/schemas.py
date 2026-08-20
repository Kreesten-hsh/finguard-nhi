"""
Pourquoi ce fichier : Pydantic force la FORME des données avant qu'elles
n'atteignent le moteur de règles. Une requête malformée est rejetée par
FastAPI automatiquement (erreur 422), sans jamais toucher policy_engine.py.
C'est la première ligne de défense contre ASI01 (injection via champs texte).
"""

from enum import Enum
from pydantic import BaseModel, Field


class RoleNHI(str, Enum):
    """Rôles possibles pour une identité non-humaine. Un agent ne peut agir
    qu'avec un rôle explicitement défini ici — pas de rôle libre en texte."""
    AGENT_READONLY = "agent_readonly"
    AGENT_PAYOUT = "agent_payout"


class TypeOperation(str, Enum):
    """Opérations autorisées. DDL/DML destructifs (DROP, DELETE) ne sont
    volontairement PAS dans cette liste — ASI03."""
    LECTURE_TRANSACTION = "lecture_transaction"
    VERIFICATION_KYC = "verification_kyc"
    EXECUTION_REMBOURSEMENT = "execution_remboursement"


class RequeteAgent(BaseModel):
    """Ce que AgentPay doit envoyer à chaque appel."""
    agent_id: str
    role: RoleNHI
    operation: TypeOperation
    montant_xof: float = Field(ge=0, description="Montant en XOF, doit être positif ou nul")
    reference_client: str = Field(max_length=100, description="Limité pour éviter l'injection de payloads longs")
    motif_litige: str = Field(max_length=500, description="Limité pour la même raison — ASI01")


class ReponseProxy(BaseModel):
    """Ce que FinGuard renvoie après décision."""
    decision: str          # "AUTORISE" | "REJETE" | "ESCALADE_HUMAINE"
    reason_code: str       # ex: "SEUIL_DEPASSE", "ROLE_INSUFFISANT", "OK"
    montant_xof: float
