import re
import time
import paramiko

UNIT = """\
[Unit]
Description=Logging
After=network.target

[Service]
ExecStart=/bin/python /bin/zggrep/zggrep.py
WorkingDirectory=/bin/zggrep
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect("host", username="root", key_filename="/path/to/key")

# 1. Write the unit file directly
sftp = client.open_sftp()
with sftp.open("/etc/systemd/system/myjob.service", "w") as f:
    f.write(UNIT)
sftp.close()

# 2. Drive systemctl through the interactive shell
shell = client.invoke_shell()

def run(cmd, timeout=30):
    """Send a command, wait for the sentinel, return (output, exit_code)."""
    shell.send(f"{cmd}; echo __DONE__$?\n")
    buf, deadline = "", time.time() + timeout
    while time.time() < deadline:
        if shell.recv_ready():
            buf += shell.recv(65536).decode(errors="replace")
            m = re.search(r"__DONE__(\d+)", buf)
            if m:
                return buf[:m.start()], int(m.group(1))
        else:
            time.sleep(0.05)
    raise TimeoutError(f"no sentinel for: {cmd}\n{buf}")

for cmd in (
    "systemctl daemon-reload",
    "systemctl enable --now myjob.service",
    "systemctl is-active myjob.service",
):
    out, rc = run(cmd)
    print(f"$ {cmd}\n{out.strip()}\n[exit {rc}]")

shell.close()
client.close()