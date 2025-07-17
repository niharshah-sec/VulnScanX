
#!/usr/bin/env python3
# VulnScanX - Advanced Web Vulnerability Scanner

import requests
import argparse
import time
from colorama import Fore, Style

banner = f"""
{Fore.RED}
██████╗ ██╗   ██╗██╗     ███╗   ██╗███████╗ ███████╗ █████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██║   ██║██║     ████╗  ██║██╔════╝ ██╔════╝██╔══██╗████╗  ██║██║ ██╔╝
██████╔╝██║   ██║██║     ██╔██╗ ██║█████╗   ███████╗███████║██╔██╗ ██║█████╔╝ 
██╔═══╝ ██║   ██║██║     ██║╚██╗██║██╔══╝   ╚════██║██╔══██║██║╚██╗██║██╔═██╗ 
██║     ╚██████╔╝███████╗██║ ╚████║███████╗ ███████║██║  ██║██║ ╚████║██║  ██╗
╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
{Style.RESET_ALL}
"""

def print_status(message, status="INFO"):
    colors = {"INFO": Fore.CYAN, "SUCCESS": Fore.GREEN, "ERROR": Fore.RED, "WARN": Fore.YELLOW}
    print(f"{colors.get(status, Fore.WHITE)}[{status}]{Style.RESET_ALL} {message}")

def check_xss(url):
    payload = "<script>alert('XSS')</script>"
    print_status(f"Testing XSS at {url}?q={payload}", "INFO")
    try:
        response = requests.get(f"{url}?q={payload}", timeout=10)
        if payload in response.text:
            print_status("XSS vulnerability found!", "SUCCESS")
            return True
    except requests.RequestException as e:
        print_status(f"Request failed: {e}", "ERROR")
    print_status("No XSS vulnerability.", "WARN")
    return False

def check_sqli(url):
    payload = "' OR '1'='1"
    print_status(f"Testing SQL Injection at {url}?id={payload}", "INFO")
    try:
        response = requests.get(f"{url}?id={payload}", timeout=10)
        if "mysql" in response.text.lower() or "syntax" in response.text.lower():
            print_status("SQL Injection vulnerability found!", "SUCCESS")
            return True
    except requests.RequestException as e:
        print_status(f"Request failed: {e}", "ERROR")
    print_status("No SQL Injection vulnerability.", "WARN")
    return False

def main():
    parser = argparse.ArgumentParser(description="VulnScanX - Advanced Web Vulnerability Scanner")
    parser.add_argument("-u", "--url", help="Target URL (e.g. https://example.com)", required=True)
    args = parser.parse_args()
    url = args.url.strip('/')

    print(banner)
    print_status(f"Starting scan on {url}", "INFO")
    xss = check_xss(url)
    sqli = check_sqli(url)

    print("\nScan Complete - Summary:")
    if xss or sqli:
        print_status("Vulnerabilities detected!", "SUCCESS")
    else:
        print_status("No vulnerabilities found.", "WARN")

if __name__ == "__main__":
    main()
