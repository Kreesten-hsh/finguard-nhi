"""
Pourquoi ce fichier : couche réseau uniquement. Il reçoit, valide (via
schemas.py), délègue la décision (via policy_engine.py), répond.
Zéro logique de sécurité ici — si tu te retrouves à écrire un `if montant >`
dans ce fichier, c'est que quelque chose est mal rangé.
"""

from fastapi import FastAPI
from app.schemas import RequeteAgent, ReponseProxy
from app.policy_engine import evaluer_requete

app = FastAPI(
    title="FinGuard-NHI Proxy",
    description="Passerelle de sécurité et contrôle d'accès déterministe pour Agents IA bancaires",
    version="0.1.0"
)


@app.post("/agent/requete", response_model=ReponseProxy)
def traiter_requete(requete: RequeteAgent) -> ReponseProxy:
    return evaluer_requete(requete)
