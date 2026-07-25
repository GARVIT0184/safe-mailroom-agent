from flask import Flask, request, jsonify
from rules import decide_action
import uuid
import json

app = Flask(__name__)


@app.route("/", methods=["POST"])
def mailroom():

    data = request.get_json(silent=True)

    print(json.dumps(data, indent=2), flush=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    operation = data.get("operation")

    # -------------------------
    # PROPOSE
    # -------------------------
    if operation == "propose":

        proposals = []

        for dossier in data.get("dossiers", []):

            decision = decide_action(dossier)

            proposals.append({
                "dossierId": dossier["dossierId"],
                "callId": str(uuid.uuid4()),
                "action": decision["action"],
                "target": decision["target"],
                "payload": decision["payload"],
                "evidence": decision["evidence"]
            })

        return jsonify({
            "profile": data.get("profile"),
            "evaluationId": data.get("evaluationId"),
            "status": "awaiting_receipts",
            "inputDigest": "",
            "proposals": proposals
        }), 200

    # -------------------------
    # COMMIT
    # -------------------------
    elif operation == "commit":

        return jsonify({
            "profile": data.get("profile"),
            "evaluationId": data.get("evaluationId"),
            "status": "completed",
            "outcomes": []
        }), 200

    return jsonify({"error": "Unknown operation"}), 400


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Safe Mailroom Agent",
        "status": "running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
