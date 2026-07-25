from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def mailroom():
    import json

    data = request.get_json(silent=True)
    print(json.dumps(data, indent=2), flush=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    operation = data.get("operation")

    if operation == "propose":
        return jsonify({
            "status": "awaiting_receipts",
            "proposals": []
        }), 200

    elif operation == "commit":
        return jsonify({
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
