#!/usr/bin/env python3
import click
import subprocess
import os
import re
from datetime import datetime

# ------------------------
# Speed profiles
# ------------------------
SPEED_PROFILES = {
    1: {"nmap": "-T1", "gobuster": "-t 5",  "sqlmap": "--delay=3 --risk=1"},
    2: {"nmap": "-T2", "gobuster": "-t 10", "sqlmap": "--delay=2 --risk=1"},
    3: {"nmap": "-T3", "gobuster": "-t 20", "sqlmap": "--delay=1 --risk=2"},
    4: {"nmap": "-T4", "gobuster": "-t 40", "sqlmap": "--delay=0 --risk=2"},
    5: {"nmap": "-T5", "gobuster": "-t 60", "sqlmap": "--delay=0 --risk=3"},
}

# ------------------------
# Helpers
# ------------------------
def run(cmd, outfile):
    with open(outfile, "w", encoding="utf-8", errors="ignore") as f:
        subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)

def ensure_dirs(base):
    for d in ["raw", "parsed"]:
        os.makedirs(os.path.join(base, d), exist_ok=True)

# ------------------------
# Parsers
# ------------------------
def parse_nmap(raw, out):
    ports = []
    with open(raw, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "/tcp" in line and "open" in line:
                ports.append(line.strip())
    with open(out, "w") as f:
        f.write("\n".join(ports))

def parse_nikto(raw, out):
    vulns = []
    patterns = ["Vulnerability", "OSVDB", "+ "]
    with open(raw, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if any(p in line for p in patterns):
                vulns.append(line.strip())
    with open(out, "w") as f:
        f.write("\n".join(vulns))

def parse_gobuster(raw, out):
    dirs = []
    with open(raw, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if re.search(r"\(Status:\s*(200|301|302|403)\)", line):
                dirs.append(line.strip())
    with open(out, "w") as f:
        f.write("\n".join(dirs))

def parse_sqlmap(raw, out):
    findings = []
    keywords = ["is vulnerable", "identified", "parameter"]
    with open(raw, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if any(k in line.lower() for k in keywords):
                findings.append(line.strip())
    with open(out, "w") as f:
        f.write("\n".join(findings))

# ------------------------
# Notes
# ------------------------
def build_notes(base, target, domain):
    notes = []
    notes.append(f"# Lazik Recon Notes\n")
    notes.append(f"**Target:** {target}")
    if domain:
        notes.append(f"**Domain:** {domain}")
    notes.append(f"**Date:** {datetime.utcnow().isoformat()} UTC\n")

    sections = {
        "Open Ports": "open_ports.txt",
        "Directories": "directories.txt",
        "Vulnerabilities": "vulnerabilities.txt",
        "SQLi Findings": "sqlmap_findings.txt",
    }

    for title, fname in sections.items():
        path = os.path.join(base, "parsed", fname)
        notes.append(f"## {title}")
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path) as f:
                notes.append("```\n" + f.read() + "\n```")
        else:
            notes.append("_No findings._")

    with open(os.path.join(base, "recon_notes.md"), "w") as f:
        f.write("\n\n".join(notes))

# ------------------------
# CLI
# ------------------------
@click.command()
@click.option("--target", required=True, help="Target IP")
@click.option("--domain", default=None, help="Target domain")
@click.option("-s", "--speed", default=3, type=click.IntRange(1,5), help="Speed profile (1-5)")
@click.option("--output", default="out", help="Output directory")
@click.option("--nmap/--no-nmap", default=True)
@click.option("--gobuster/--no-gobuster", default=True)
@click.option("--nikto/--no-nikto", default=True)
@click.option("--sqlmap/--no-sqlmap", default=False)
def run_recon(target, domain, speed, output, nmap, gobuster, nikto, sqlmap):
    ensure_dirs(output)
    prof = SPEED_PROFILES[speed]

    if nmap:
        raw = os.path.join(output, "raw", "nmap.txt")
        cmd = f"nmap -sC -sV {prof['nmap']} {target}"
        run(cmd, raw)
        parse_nmap(raw, os.path.join(output, "parsed", "open_ports.txt"))

    if gobuster and domain:
        raw = os.path.join(output, "raw", "gobuster.txt")
        cmd = f"gobuster dir -u http://{domain} -w /usr/share/wordlists/dirb/common.txt {prof['gobuster']}"
        run(cmd, raw)
        parse_gobuster(raw, os.path.join(output, "parsed", "directories.txt"))

    if nikto:
        raw = os.path.join(output, "raw", "nikto.txt")
        cmd = f"nikto -h {target}"
        run(cmd, raw)
        parse_nikto(raw, os.path.join(output, "parsed", "vulnerabilities.txt"))

    if sqlmap:
        raw = os.path.join(output, "raw", "sqlmap.txt")
        cmd = f"sqlmap -u http://{domain}/index.php?id=1 {prof['sqlmap']} --batch"
        run(cmd, raw)
        parse_sqlmap(raw, os.path.join(output, "parsed", "sqlmap_findings.txt"))

    build_notes(output, target, domain)
    click.echo("[+] LASIK recon completed.")

if __name__ == "__main__":
    run_recon()
