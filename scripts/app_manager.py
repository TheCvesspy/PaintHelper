import os
import subprocess
import sys
import time
import re

PID_FILE = ".reflex.pid"
FRONTEND_PORT = "3000"
BACKEND_PORT = "8001"

def get_pids_by_ports(ports):
    pids = set()
    try:
        output = subprocess.check_output(["netstat", "-ano"], text=True)
        for line in output.splitlines():
            for port in ports:
                # Matches listening port and captures PID at the end
                if f":{port}" in line and "LISTENING" in line:
                    match = re.search(r"(\d+)\s*$", line)
                    if match:
                        pids.add(match.group(1))
    except Exception as e:
        print(f"Error finding PIDs by ports: {e}")
    return list(pids)

def start():
    print("Starting Quill's Hub...")
    
    # We run 'reflex run' in a new process group so it doesn't die with this script
    cmd = ["py", "-m", "reflex", "run", "--frontend-port", FRONTEND_PORT, "--backend-port", BACKEND_PORT]
    
    try:
        # Start the process group
        subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        )
        
        print("Waiting for both Frontend and Backend to initialize ports...")
        attempts = 0
        found_pids = []
        while attempts < 45: # Increased to 45 seconds for robustness
            time.sleep(1)
            # Find PIDs for each port separately to ensure we have both
            fe_pids = get_pids_by_ports([FRONTEND_PORT])
            be_pids = get_pids_by_ports([BACKEND_PORT])
            
            combined = list(set(fe_pids + be_pids))
            if len(fe_pids) >= 1 and len(be_pids) >= 1:
                found_pids = combined
                break
            
            # Update status message occasionally
            if attempts % 5 == 0 and attempts > 0:
                print(f"Still waiting... detected FE: {fe_pids}, BE: {be_pids}")
                
            attempts += 1
            
        if found_pids:
            with open(PID_FILE, "w") as f:
                f.write(",".join(found_pids))
            print(f"App started successfully.")
            print(f"Tracked Frontend PID(s): {', '.join(get_pids_by_ports([FRONTEND_PORT]))}")
            print(f"Tracked Backend PID(s): {', '.join(get_pids_by_ports([BACKEND_PORT]))}")
        else:
            print("Warning: Could not detect both ports listening after 45s. Startup might be slow or failed.")
            # Still save whatever we found
            current = get_pids_by_ports([FRONTEND_PORT, BACKEND_PORT])
            if current:
                with open(PID_FILE, "w") as f:
                    f.write(",".join(current))
            
    except Exception as e:
        print(f"Failed to start app: {e}")

def stop():
    print("Initiating shutdown sequence...")
    
    file_pids = []
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            content = f.read().strip()
            file_pids = content.split(",") if content else []
    
    # Always check current ports too
    port_pids = get_pids_by_ports([FRONTEND_PORT, BACKEND_PORT])
    
    # Combine and unique
    all_pids = list(set(file_pids + port_pids))

    if all_pids:
        print(f"Detected processes to terminate: {', '.join(all_pids)}")
        for pid in all_pids:
            if not pid: continue
            print(f"Terminating process tree for PID {pid}...")
            # /F = Force, /T = Tree (kills children), /PID = specific PID
            res = subprocess.run(["taskkill", "/F", "/T", "/PID", pid], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"PID {pid} and its children terminated.")
            else:
                # Often it might already be dead if it was a child of another PID we just killed
                if "not found" not in res.stderr.lower():
                    print(f"Note for PID {pid}: {res.stderr.strip()}")
        
        print("Shutdown complete.")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    else:
        print("No running Frontend or Backend processes detected.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py app_manager.py [start|stop]")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    if command == "start":
        start()
    elif command == "stop":
        stop()
    else:
        print(f"Unknown command: {command}")
