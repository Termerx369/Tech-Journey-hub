from flask import Flask, request, render_template, jsonify
import socket
import requests
import json
from datetime import datetime

app = Flask(__name__)

def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def check_http(domain):
    urls = [f"http://{domain}", f"https://{domain}"]
    alive = []
    for url in urls:
        try:
            r = requests.get(url, timeout=5, verify=False)
            alive.append({
                "url": url,
                "status": r.status_code,
                "length": len(r.text),
                "title": r.text.split("<title>")[1].split("</title>")[0] if "<title>" in r.text else "No title"
            })
        except Exception:
            alive.append({
                "url": url,
                "status": "No response",
                "length": 0,
                "title": ""
            })
    return alive

@app.route("/", methods=["GET", "POST"])
def index():
    results_list = []
    if request.method == "POST":
        domains_input = request.form.get("domains")  # now expects comma-separated domains
        domains = [d.strip() for d in domains_input.split(",") if d.strip()]

        for domain in domains:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            ip = resolve_domain(domain)
            if ip:
                result = {
                    "timestamp": timestamp,
                    "domain": domain,
                    "ip": ip,
                    "http": check_http(domain)
                }
            else:
                result = {"domain": domain, "error": f"Could not resolve {domain}"}

            results_list.append(result)

        # Save all results to JSON
        try:
            with open("results.json", "r") as f:
                all_results = json.load(f)
        except FileNotFoundError:
            all_results = []

        all_results.extend(results_list)

        with open("results.json", "w") as f:
            json.dump(all_results, f, indent=2)

    return render_template("index.html", results=results_list)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
