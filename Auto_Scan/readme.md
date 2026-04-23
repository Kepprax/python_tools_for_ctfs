this tool python-based "All-in-One" reconnaissance tool designed to automate the initial phases of a penetration test of CTF machines It orchestrates industry-standard security tools like Nmap, Gobuster, Nikto, and Sqlmap 
into a single, streamlined workflow.

Multi-Speed Profiles: Choose between 5 levels of intensity (from T1 for stealth to T5 for aggressive scanning).

Automated Parsing: Automatically extracts critical data from noisy tool outputs into clean, readable summaries.

Consolidated Reporting: Generates a centralized recon_notes.md report for easy documentation.

Modular Execution: Enable or disable specific tools (Nmap, Gobuster, Nikto, SQLmap) based on the target scope.

Ensure you have Python 3 installed along with the following system tools (standard on Kali Linux):

-nmap

-gobuster

-nikto

-sqlmap

Installation

Install the required Python dependency:

pip install click

Usage :

python3 lasik.py --target <TARGET_IP> --domain <TARGET_DOMAIN>

Options:

--target :Required. Target IP address.

--domain :Target domain name (Required for Gobuster/SQLmap)

-s, --speed :Speed profile (1-5). Default is 3.

--output :Name of the output directory. Default is out.

--no-nmap :Skips the Nmap scan.

--sqlmap :Enables SQLmap scan (Disabled by default).

Examples:

1. Aggressive Stealth-Breaker (T5):

python3 lasik.py --target 10.10.10.10 --domain example.com -s 5

2. Quick Vulnerability Assessment (No Directory Brute-forcing):

python3 lasik.py --target 10.10.10.10 --no-gobuster

Output Structure:
The tool organizes findings into a structured directory:

/raw: Original, untouched output files from each tool.

/parsed: Cleaned-up text files containing only actionable data (e.g., open ports, discovered directories).

recon_notes.md: A comprehensive summary of the entire recon session in Markdown.
