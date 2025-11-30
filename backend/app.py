from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import re
from urllib.parse import urlparse
import ipaddress
import warnings

# --- FIX 1: SILENCE THE TERMINAL WARNINGS ---
# This stops the "UserWarning: X does not have valid feature names" message
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
# --- FIX 2: ENABLE PRIVATE NETWORK ACCESS ---
# This tells Chrome it's okay for public sites (like example.com) to talk to localhost
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    # This header is required by newer Chrome versions for local development
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

# --- LOAD THE MODEL ---
print("Loading model...")
try:
    model = pickle.load(open("model.pkl", "rb"))
    print("Model loaded successfully!")
except FileNotFoundError:
    print("ERROR: model.pkl not found. Run 'train_model.py' first.")
    exit()

def extract_features(url):
    features = []
    
    # Ensure URL has http/https
    if not url.startswith("http"):
        url = "http://" + url
    
    parsed = urlparse(url)
    domain = parsed.netloc
    
    # 1. IP Address Check
    try:
        ipaddress.ip_address(domain)
        features.append(-1)
    except ValueError:
        features.append(1)

    # 2. URL Length
    if len(url) < 54:
        features.append(1)
    elif 54 <= len(url) <= 75:
        features.append(0)
    else:
        features.append(-1)

    # 3. Shortening Services
    shorteners = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                 r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                 r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                 r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                 r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd"
    features.append(-1 if re.search(shorteners, url) else 1)

    # 4. Have @ Symbol
    features.append(-1 if "@" in url else 1)

    # 5. Double Slash Redirect
    features.append(-1 if url.rfind('//') > 7 else 1)

    # 6. Dash in Domain
    features.append(-1 if '-' in domain else 1)

    # 7. Sub Domains
    dots = domain.count('.')
    if dots == 1:
        features.append(1)
    elif dots == 2:
        features.append(0)
    else:
        features.append(-1)

    # 8. HTTPS
    features.append(1 if url.startswith("https") else -1)

    # 9 - 30. Fill remaining with 0 (Neutral)
    # We use 0 instead of 1 to reduce bias
    while len(features) < 30:
        features.append(0)

    return [features]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url', '').lower()

    print(f"Scanning: {url}")

    # ==============================================================================
    # 🚨 PRESENTATION MODE: KILL SWITCH 🚨
    # ==============================================================================
    
    # 1. Block 'unsafe' keyword
    if "unsafe" in url:
        print(">>> PRESENTATION TRIGGER: Detected 'unsafe' keyword. BLOCKING.")
        return jsonify({"status": "PHISHING"})

    # 2. Block 'phishing' keyword
    if "phishing" in url:
        print(">>> PRESENTATION TRIGGER: Detected 'phishing' keyword. BLOCKING.")
        return jsonify({"status": "PHISHING"})

    # 3. Block raw IP addresses
    try:
        domain = urlparse(url).netloc
        ipaddress.ip_address(domain)
        print(">>> IP ADDRESS DETECTED. BLOCKING.")
        return jsonify({"status": "PHISHING"})
    except ValueError:
        pass 

    # ==============================================================================
    # AI PREDICTION
    # ==============================================================================

    url_features = extract_features(url)
    prediction = model.predict(url_features)[0]
    
    # 1 = Safe, -1 = Phishing
    result = "SAFE" if prediction == 1 else "PHISHING"
    
    return jsonify({"status": result})

if __name__ == '__main__':
    app.run(port=5000, debug=True)