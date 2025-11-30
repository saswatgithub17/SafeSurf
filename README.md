Phishing Detector — Browser Extension
Phishing Detector is a lightweight, privacy-first browser extension that analyzes URLs and webpage signals in real time to detect phishing threats. It provides clear risk ratings, actionable advice, and optional reporting—helping users browse safely and confidently.

🚀 Features
Real-time phishing detection using URL & page heuristics
Color-coded risk indicator (Safe / Suspicious / Dangerous)
Actionable safety tips for risky sites
One-click reporting to improve detection
Local-first model ensures privacy
Optional backend ML model
Lightweight and fast

🛡️ How It Works
The extension evaluates domain anomalies, URL patterns, and page-level signals.
It uses:
A local heuristic engine (runs inside browser)
An optional Flask-based backend ML model for improved accuracy
Only URLs are sent when backend mode is enabled.

📦 Installation
Browser Extension
Clone/download the repository
Open your browser’s Extension Manager
Enable Developer Mode
Click Load Unpacked
Select the project folder

🧠 Backend Setup (for ML Model Mode)
If your project has a backend API using Flask + ML, install dependencies:
pip install flask flask-cors scikit-learn pandas
(or simply run:)
pip install -r requirements.txt
Start the backend server:
python app.py

🖥️ Usage
Browse to any site
Click the extension icon
View the risk level & explanation
Follow recommended safe actions
Report suspicious pages

📊 Architecture Overview
              ┌───────────────────────────────┐
              │       Browser Extension       │
              │  (URL analysis + heuristics)  │
              └───────────────┬───────────────┘
                              │ Optional
                              ▼
              ┌────────────────────────────────┐
              │      Backend Flask Server      │
              │ ML Model (Scikit-Learn) Scores │
              └────────────────────────────────┘

Architecture Diagram
🔒 Privacy
All detection runs locally by default
No credentials or personal content collected
Optional server check sends only URLs
Fully transparent permission model
