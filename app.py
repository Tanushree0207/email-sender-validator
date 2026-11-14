
from flask import Flask, jsonify, request
import re
from datetime import datetime
import os

app = Flask(__name__)

# Store recent validation results
history = []


def validate_email(email):
    # Check email format
    pattern = r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        return {
            "email": email,
            "risk_score": 0,
            "risk_level": "Invalid",
            "reasons": ["Invalid email format"]
        }

    score = 0
    reasons = []

    domain = email.split("@")[1].lower()
        # Check for disposable email domains
    disposable_domains = [
        "mailinator.com",
        "tempmail.com",
        "10minutemail.com"
    ]

    if domain in disposable_domains:
        score += 30
        reasons.append("Disposable email domain detected")

    # Check for suspicious domain indicators
    if any(part.startswith("xn--") for part in domain.split(".")):
        score += 40
        reasons.append("Internationalized domain detected")

    suspicious_words = ["verify", "account", "secure", "login"]

    if any(word in domain for word in suspicious_words):
        score += 25
        reasons.append("Suspicious keyword found in domain")

    if any(char.isdigit() for char in domain):
        score += 20
        reasons.append("Domain contains numbers")

    score = min(score, 100)

    if score >= 50:
        risk_level = "High"
    elif score >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    if not reasons:
        reasons.append("No suspicious indicators detected")

    return {
        "email": email,
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons
    }


# Endpoint 1: Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "message": "Email Sender Validator API is running"
    })


# Endpoint 2: Email validation
@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    result = validate_email(email)
    result["timestamp"] = datetime.now().isoformat()

    history.insert(0, result)
    del history[50:]

    return jsonify(result), 200


# Endpoint 3: Validation history
@app.route("/history", methods=["GET"])
def get_history():
    return jsonify({
        "total": len(history),
        "history": history
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

# Ansible handler restart test
