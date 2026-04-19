import socket
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

# Constants for the scan
TARGET_PORTS = range(1, 1025)
TIMEOUT = 0.5
MAX_THREADS = 100


def scan_port(target, port, open_ports):
    """
    Attempts to connect to a specific port on the target IP.
    Uses a context manager to ensure the socket is closed.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            if s.connect_ex((target, port)) == 0:
                print(f"[+] Port {port} is open")
                open_ports.append(port)
    except (socket.timeout, ConnectionRefusedError):
        pass
    except Exception as e:
        print(f"[!] Error scanning port {port}: {e}")


def run_scanner():
    """
    Main execution logic for the threaded port scanner.
    """
    target = input("Enter target IP address: ").strip()

    # Simple validation for IP/Hostname
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("[!] Invalid hostname or IP address.")
        return

    print(f"\n{'=' * 40}")
    print(f"Scanning Target: {target_ip}")
    print(f"Port Range: 1 - 1024")
    print(f"{'=' * 40}\n")

    open_ports = []

    # Using ThreadPoolExecutor for efficient resource management
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for port in TARGET_PORTS:
            executor.submit(scan_port, target_ip, port, open_ports)

    print(f"\n{'=' * 40}")
    print(f"Scan Complete.")
    print(f"Total Open Ports Found: {len(open_ports)}")
    print(f"{'=' * 40}")


if __name__ == "__main__":
    run_scanner()