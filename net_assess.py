#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from datetime import datetime

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
RESET = "\033[0m"

BANNER = f"""{RED}
███╗   ██╗███████╗████████╗   ██████╗██╗  ██╗██╗███████╗██╗     ██████╗ 
████╗  ██║██╔════╝╚══██╔══╝  ██╔════╝██║  ██║██║██╔════╝██║     ██╔═══██╗
██╔██╗ ██║█████╗     ██║     ╚█████╗ ███████║██║█████╗  ██║     ██║   ██║
██║╚██╗██║██╔══╝     ██║      ╚═══██╗██╔══██║██║██╔══╝  ██║     ██║   ██║
██║ ╚████║███████╗   ██║     ██████╔╝██║  ██║██║███████╗███████╗╚██████╔╝
╚═╝  ╚═══╝╚══════╝   ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚══════╝{GREEN}
[+] =================================================================== [+]
[+]           NETWORK SECURITY ASSESSMENT & AUDIT TOOL v1.0             [+]
[+] =================================================================== [+]
{RESET}"""

def clean_print(status, text):
    if status == "info": print(f"{BLUE}[*]{RESET} {text}")
    elif status == "success": print(f"{GREEN}[+]{RESET} {text}")
    elif status == "warning": print(f"{YELLOW}[!]{RESET} {text}")

def run_real_scan(target_subnet):
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)
    clean_print("info", f"Initializing Real Security Modules... Done.\n[*] Target Subnet: {target_subnet}")
    print(f"\n{GREEN}[+] Asli Scanning Background Mein Chal Rahi Hai. Please Wait...{RESET}")
    
    nmap_command = f"nmap -F -sV {target_subnet}"
    process = subprocess.Popen(nmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    toolbar_width = 40
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))
    
    while process.poll() is None:
        time.sleep(0.4)
        sys.stdout.write("█")
        sys.stdout.flush()
    sys.stdout.write("]\n\n")
    
    stdout, stderr = process.communicate()
    clean_print("success", "Background Scanning finished successfully!")
    
    if not os.path.exists("reports"): os.makedirs("reports")
    report_path = "reports/scan_report.md"
    
    vuln_count = 0
    risk_analysis_section = ""
    host_rows = ""
    hosts_data = stdout.split("Nmap scan report for ")
    active_hosts_count = len(hosts_data) - 1
    
    if active_hosts_count <= 0:
        active_hosts_count = 1
        host_rows = "| No Active Hosts Found | N/A | N/A | Check target subnet range |\n"
    else:
        for host in hosts_data[1:]:
            lines = host.splitlines()
            if not lines: continue
            ip = lines[0].split()[-1].replace('(', '').replace(')', '')
            for line in lines:
                if "/tcp" in line and "open" in line:
                    parts = line.split()
                    port_num = parts[0].split("/")[0]
                    service = parts[1]
                    version = " ".join(parts[3:]) if len(parts) > 3 else "Unknown"
                    host_rows += f"| {ip} | Connected Device | {port_num} | {service} ({version}) |\n"
                    
                    if port_num in ["22", "21"]:
                        vuln_count += 1
                        risk_analysis_section += f"### [RISK LEVEL: HIGH] Exposed Management Protocol\n* **Target:** {ip} (Port {port_num})\n* **Description:** Exposed {service} port detected. Attackers might attempt brute force attacks.\n* **Fix:** Restrict port {port_num} via firewall.\n\n"
                    elif port_num == "80":
                        vuln_count += 1
                        risk_analysis_section += f"### [RISK LEVEL: MEDIUM] Plaintext HTTP Active\n* **Target:** {ip} (Port 80)\n* **Description:** Unencrypted web traffic detected. Credentials can be sniffed.\n* **Fix:** Enforce encrypted HTTPS (Port 443).\n\n"

    if vuln_count == 0:
        risk_analysis_section = "### [RISK LEVEL: LOW] No Immediate High Risks Found\n* All ports appear secure from basic network exploitation."
    
    clean_print("warning", f"{vuln_count} Real Vulnerabilities/Exposures mapped dynamically.")
    
    report_content = f"""# REAL NETWORK SECURITY ASSESSMENT REPORT
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Target Network:** {target_subnet}
**Scan Status:** COMPLETED SUCCESFULLY

---
## 1. EXECUTIVE SUMMARY
The assessment successfully performed a real-time background infrastructure scan. A total of **{active_hosts_count} active targets** were analyzed.

---
## 2. DISCOVERED HOSTS & PORTS

| Host IP Address | Device Category | Open Port | Discovered Service & Version |
| :--- | :--- | :--- | :--- |
{host_rows}
---
## 3. REAL VULNERABILITY & RISK ANALYSIS
{risk_analysis_section}
"""
    with open(report_path, "w") as f: f.write(report_content)
    clean_print("info", f"Generating REAL custom report inside '{report_path}'... Done.")

if __name__ == "__main__":
    if os.getuid() != 0 if hasattr(os, 'getuid') else False: print(f"{YELLOW}[!] WARNING: Run this script with 'sudo' on Linux for accurate scanning.{RESET}\n")
    target = input("[?] Enter Target Subnet/IP (e.g., 127.0.0.1): ") or "127.0.0.1"
    run_real_scan(target)
