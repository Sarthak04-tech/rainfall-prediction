import subprocess
import re
import sys

def stop_server(port=5000):
    try:
        out = subprocess.check_output(f'netstat -aon', shell=True).decode('utf-8', errors='ignore')
        killed = False
        for line in out.splitlines():
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.strip().split()
                pid = parts[-1]
                print(f"[*] Found process on port {port} (PID: {pid}). Terminating...")
                subprocess.call(f'taskkill /F /PID {pid}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                killed = True
        if killed:
            print("[OK] Server stopped successfully.")
        else:
            print(f"[INFO] No active server found on port {port}.")
    except Exception as e:
        print(f"[ERROR] Could not stop server: {e}")

if __name__ == "__main__":
    stop_server()
