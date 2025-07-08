from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration Foundry
FOUNDY_API_URL = "https://projetcondor.usw-3.palantirfoundry.com/"
FUNCTION_RID = "ri.function-registry.main.function.2ca2a783-4a01-4658-8e3f-3eef704b0a39"
API_TOKEN = os.environ.get("FOUNDRY_TOKEN")  # Securisé via variable d'environnement

@app.route("/analyser", methods=["POST"])
def analyser():
    data = request.json
    demande = data.get("demande", "")
    niveau = data.get("niveauAnalyse", "Normale")

    payload = {
        "functionRid": FUNCTION_RID,
        "inputParams": {
            "demande": {"value": demande},
            "niveauAnalyse": {"value": niveau}
        }
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{FOUNDY_API_URL}/foundry-api/logic-function-execution/execute",
        json=payload,
        headers=headers
    )

    if response.ok:
        return jsonify({"resultat": response.json().get("output", "Aucune réponse reçue.")})
    else:
        return jsonify({"error": response.text}), 500

if __name__ == "__main__":
    app.run(debug=True)
