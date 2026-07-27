import os
import hashlib
import socket
import ipaddress

import requests
import yaml
from urllib.parse import urlparse
from flask import Flask, request, jsonify

app = Flask(__name__)

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

LEDGER = [
    {"id": "txn_1001", "pan": "4242424242424242", "amount": 4200, "currency": "USD", "status": "captured"},
    {"id": "txn_1002", "pan": "5555555555554444", "amount": 1899, "currency": "EUR", "status": "refunded"},
]


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/tokenize", methods=["POST"])
def tokenize():
    payload = request.get_json(silent=True) or {}
    pan = payload.get("pan", "")
    token = "tok_" + hashlib.sha256(pan.encode()).hexdigest()[:24]
    return jsonify(token=token, last4=pan[-4:])


@app.route("/transactions")
def transactions():
    masked_transactions = []

    for txn in LEDGER:
        masked_txn = txn.copy()

        pan = masked_txn["pan"]
        masked_txn["pan"] = "*" * (len(pan) - 4) + pan[-4:]

        masked_transactions.append(masked_txn)

    return jsonify(transactions=masked_transactions)


@app.route("/import", methods=["POST"])
def import_config():
    config = yaml.safe_load(request.data)
    return jsonify(loaded=str(config))


def is_safe_url(url):
    try:
        parsed = urlparse(url)

        # Allow only HTTPS
        if parsed.scheme != "https":
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        ip = ipaddress.ip_address(socket.gethostbyname(hostname))

        # Block private/internal IP addresses
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
        ):
            return False

        return True

    except Exception:
        return False


@app.route("/fetch")
def fetch():
    url = request.args.get("url", "")

    if not is_safe_url(url):
        return jsonify(error="Invalid or unsafe URL"), 400

    resp = requests.get(url, timeout=5)
    return jsonify(status_code=resp.status_code, body=resp.text[:2048])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
