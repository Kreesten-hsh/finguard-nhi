"""
Pourquoi ce fichier : c'est ici, et uniquement ici, que vivent les décisions
de sécurité. Aucune route FastAPI n'implémente de logique métier directement
— tout passe par cette fonction, pour qu'un futur audit (ou une migration OPA)
n'ait qu'un seul endroit à vérifier.
"""

from app.schemas import RequeteAgent, ReponseProxy, RoleNHI, TypeOperation

SEUIL_AUTO_XOF = 50_000  # Hypothèse pédagogique du lab — voir threat_model.md


def evaluer_requete(requete: RequeteAgent) -> ReponseProxy:
    # ASI03 — un agent en lecture seule ne peut jamais déclencher un paiement
    if requete.operation == TypeOperation.EXECUTION_REMBOURSEMENT and requete.role != RoleNHI.AGENT_PAYOUT:
        return ReponseProxy(
            decision="REJETE",
            reason_code="ROLE_INSUFFISANT",
            montant_xof=requete.montant_xof,
        )

    # ASI08 — le plafond n'est vérifié QUE pour les remboursements, pas les lectures
    if requete.operation == TypeOperation.EXECUTION_REMBOURSEMENT:
        if requete.montant_xof > SEUIL_AUTO_XOF:
            return ReponseProxy(
                decision="ESCALADE_HUMAINE",
                reason_code="SEUIL_DEPASSE",
                montant_xof=requete.montant_xof,
            )
        return ReponseProxy(
            decision="AUTORISE",
            reason_code="OK",
            montant_xof=requete.montant_xof,
        )

    # Lecture et vérification KYC : autorisées par défaut si le rôle correspond
    return ReponseProxy(
        decision="AUTORISE",
        reason_code="OK",
        montant_xof=requete.montant_xof,
    )
