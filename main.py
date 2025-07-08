from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# --- Configuration Foundry (à personnaliser) -----------------
FOUNDY_API_URL = "https://projetcondor.usw-3.palantirfoundry.com/"     # ← remplace ton-tenant
FUNCTION_RID   = "ri.function-registry.main.function.2ca2a783-4a01-4658-8e3f-3eef704b0a39"   # ← remplace par ton RID
API_TOKEN      = os.environ.get("FOUNDRY_TOKEN")               # injecté sur Render
# -------------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    """Page d’accueil simple pour vérifier que le service tourne."""
    return (
        "<h2>✅ Serveur actif — utilisez POST /analyser pour lancer une analyse.</h2>",
        200,
        {"Content-Type": "text/html"},
    )

@app.route("/analyser", methods=["POST"])
def analyser():
    """Endpoint qui relaye la demande à la logique AIP sur Foundry."""
    data = request.get_json(silent=True) or {}
    demande = data.get("demande", "")
    niveau  = data.get("niveauAnalyse", "Normale")

    payload = {
        "functionRid": FUNCTION_RID,
        "inputParams": {
            "demande":        {"value": demande},
            "niveauAnalyse":  {"value": niveau}
        }
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type":  "application/json"
    }

    try:
        resp = requests.post(
            f"{FOUNDY_API_URL}/foundry-api/logic-function-execution/execute",
            json=payload,
            headers=headers,
            timeout=90
        )
        if resp.ok:
            return jsonify({"resultat": resp.json().get("output", "Aucune sortie reçue.")}), 200
        return jsonify({"error": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Lancement local ----------------------------------------
if __name__ == "__main__":
    # Pour un test local : python main.py
    app.run(host="0.0.0.0", port=8050, debug=True)
