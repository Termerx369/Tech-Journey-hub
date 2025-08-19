import socket
import sys
import requests
import json
from datetime import datetime

def resolve_domain(domain):
    """Resolve domain to IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def check_http(domain):
    """Check if HTTP/HTTPS services are alive."""
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recon.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    ip = resolve_domain(domain)
    if not ip:
        print(f"[{timestamp}] Could not resolve {domain}")
        sys.exit(0)

    results = {
        "timestamp": timestamp,
        "domain": domain,
        "ip": ip,
        "http": check_http(domain)
    }

    # Print nicely in console
    print(json.dumps(results, indent=2))

    # Save to results.json
    try:
        with open("results.json", "r") as f:
            all_results = json.load(f)
    except FileNotFoundError:
        all_results = []

    all_results.append(results)

    with open("results.json", "w") as f:
        json.dump(all_results, f, indent=2)

