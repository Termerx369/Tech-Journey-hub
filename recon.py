import socket
import sys
from datetime import datetime

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recon.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    ip = resolve_domain(domain)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if ip:
        print(f"[{timestamp}] {domain} → {ip}")
        with open("results.txt", "a") as f:
            f.write(f"{timestamp} {domain} {ip}\n")
    else:
        print(f"[{timestamp}] Could not resolve {domain}")

