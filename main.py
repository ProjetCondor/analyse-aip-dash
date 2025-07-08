from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# --- Configuration Foundry (à personnaliser) -----------------
FOUNDY_API_URL = "https://projetcondor.usw-3.palantirfoundry.com"
FUNCTION_RID   = "ri.function-registry.main.function.2ca2a783-4a01-4658-8e3f-3eef704b0a39"
API_TOKEN      = os.environ.get("FOUNDRY_TOKEN")  # injecté via Render
# -------------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    """Affiche l'interface HTML simple."""
    return render_template("index.html")

@app.route("/analyser", methods=["POST"])
def analyser():
    """Relaye la demande à la logique AIP sur Foundry."""
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
    app.run(host="0.0.0.0", port=8050, debug=True)
