"""
Flask app for the cloud DevOps project.

Endpoints:
  /        -> a clean HTML landing page (nice to look at / screenshot)
  /health  -> health check used by Kubernetes & monitoring (UNCHANGED)
  /api     -> the original JSON response (kept for compatibility)
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")


# A small, self-contained HTML page (no external files needed).
PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cloud DevOps Project</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, Segoe UI, Roboto, sans-serif;
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      color: #fff; min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 16px; padding: 48px 56px; text-align: center;
      backdrop-filter: blur(10px); max-width: 520px;
    }}
    h1 {{ font-size: 28px; margin-bottom: 8px; }}
    .sub {{ opacity: 0.8; margin-bottom: 28px; font-size: 15px; }}
    .badge {{
      display: inline-block; background: #FF9900; color: #111;
      font-weight: 600; padding: 6px 14px; border-radius: 20px;
      font-size: 13px; margin: 4px;
    }}
    .badge.blue {{ background: #326CE5; color: #fff; }}
    .badge.green {{ background: #2ecc71; color: #fff; }}
    .meta {{ margin-top: 24px; font-size: 13px; opacity: 0.7; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>🚀 Cloud DevOps Project</h1>
    <p class="sub">Containerized · CI/CD · GitOps · Monitored</p>
    <span class="badge">Deployed on AWS EKS</span>
    <span class="badge blue">Kubernetes</span>
    <span class="badge green">● Healthy</span>
    <p class="meta">Version {version} &nbsp;|&nbsp; Served by Kubernetes on AWS</p>
  </div>
</body>
</html>"""


@app.route("/")
def home():
    """Main page — a clean HTML landing page."""
    return PAGE.format(version=APP_VERSION)


@app.route("/health")
def health():
    """Health check endpoint (used by Kubernetes & monitoring). UNCHANGED."""
    return jsonify(status="healthy"), 200


@app.route("/api")
def api():
    """The original JSON response, kept for compatibility."""
    return jsonify(
        message="Hello from my cloud DevOps project!",
        version=APP_VERSION,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
