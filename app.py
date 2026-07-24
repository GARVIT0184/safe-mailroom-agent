
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/")
def mailroom():

    body = request.get_json()

    if not body:
        return jsonify({
            "error":"Invalid JSON"
        }),400

    operation = body.get("operation")

    if operation=="propose":
        return jsonify({
            "status":"awaiting_receipts",
            "proposals":[]
        })

    elif operation=="commit":
        return jsonify({
            "status":"completed",
            "outcomes":[]
        })

    return jsonify({
        "error":"Unknown operation"
    }),400


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
