#!/bin/bash

# Initialize workspace
mkdir -p ~/BugBounty
cd ~/BugBounty

# Create new dated directory
TODAY=$(date +%Y%m%d)
mkdir "centralbank_$TODAY"
cd "centralbank_$TODAY"

# Run recon
echo "[+] Starting recon: $(date)"
assetfinder --subs-only centralbank.go.ke > subs_raw.txt
subfinder -d centralbank.go.ke -silent >> subs_raw.txt
sort -u subs_raw.txt | grep '\.go\.ke$' > subdomains.txt
cat subdomains.txt | httprobe -c 50 > live_targets.txt

# Find high-value targets
grep -E 'dev|test|staging|portal' live_targets.txt > high_value.txt

# Encrypt findings
openssl enc -aes-256-cbc -salt -in high_value.txt -out high_value.enc -pass pass:"${1:-default_password}"

# Cleanup plaintext
rm -f subs_raw.txt subdomains.txt live_targets.txt high_value.txt

# Report
echo "[+] Recon completed: $(date)"
echo "High-value targets saved (encrypted): high_value.enc"
echo "Use: openssl enc -d -aes-256-cbc -in high_value.enc -out decrypted.txt"
