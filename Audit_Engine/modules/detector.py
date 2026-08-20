import os
import sys
import platform
import psutil
import socket

class EnvironmentDetector:
    def __init__(self, config):
        self.config = config

    def scan(self):
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "hostname": socket.gethostname(),
            "edr_detected": [],
            "is_admin": self._check_admin(),
            "network_info": self._check_network()
        }
        info["edr_detected"] = self._detect_edr()
        info["hooks_detected"] = self._detect_hooks()
        return info

    def _check_admin(self):
        try:
            if sys.platform == "win32":
                return os.system("net session >nul 2>&1") == 0
            else:
                return os.getuid() == 0
        except:
            return False

    def _detect_edr(self):
        detected = []
        try:
            for proc in psutil.process_iter(['name']):
                name = proc.info['name'].lower() if proc.info['name'] else ""
                for edr, sigs in self.config.edr_signatures.items():
                    for sig in sigs:
                        if sig in name:
                            detected.append(edr)
            return list(set(detected))
        except Exception as e:
            return [f"Erreur: {e}"]

    def _detect_hooks(self):
        return {"ntdll_hooked": False}

    def _check_network(self):
        try:
            socket.gethostbyname(self.config.target_domain)
            return {"dns_resolution": True}
        except:
            return {"dns_resolution": False}