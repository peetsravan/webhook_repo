import hmac, hashlib, json, datetime as dt
from flask import Flask, request, abort, render_template, jsonify
from pymongo import MongoClient
from config import settings

app = Flask(__name__)

client = MongoClient(settings.MONGO_URI)
collection = client[settings.DB_NAME][settings.COLL_NAME]


def verify_signature(payload, signature):
    """Return True iff X-Hub-Signature-256 matches our secret."""
    if not settings.GITHUB_SECRET:
        return True   # skip when secret not set (dev mode)

    if signature is None:
        return False
    mac = hmac.new(settings.GITHUB_SECRET, payload, hashlib.sha256)

    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

def iso_now():
    return dt.datetime.now(dt.timezone.utc) \
                      .isoformat(timespec="seconds") \
                      .replace("+00:00", "Z")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/events", methods=["GET"])
def list_events():
    """Return most-recent 25 events (newest first) as JSON."""
    docs = (collection
            .find({}, {"_id": 0})       
            .sort("timestamp", -1)
            .limit(25))
    return jsonify(list(docs))

@app.route("/webhook", methods=["POST"])
def github_webhook():
    signature = request.headers.get("X-Hub-Signature-256")
    body      = request.data
    if not verify_signature(body, signature):
        abort(400, "Invalid signature")

    event  = request.headers.get("X-GitHub-Event", "ping")
    payload = request.get_json()

    if event == "push":
        branch = payload["ref"].split("/")[-1]
        if branch not in {"main", "master"}:
            return "", 204  # Skip non-main/master pushes

        doc = {
            "type": "push",
            "author": payload["pusher"]["name"],
            "to_branch": branch,
            "timestamp": iso_now()
        }
        collection.insert_one(doc)
        return "", 204

    if event == "pull_request":
        action = payload["action"]
        pr     = payload["pull_request"]

        if action == "opened":
            doc = {
                "type": "pull_request",
                "author": pr["user"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": iso_now()
            }
            collection.insert_one(doc)

        if action == "closed" and pr["merged"]:
            doc = {
                "type": "merge",
                "author": pr["merged_by"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": iso_now()
            }
            collection.insert_one(doc)

        return "", 204

    return "", 204



if __name__ == "__main__":
    app.run(debug=True, port=5000)
