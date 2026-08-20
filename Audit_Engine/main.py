#!/usr/bin/env python3
import argparse
import json
import os
from core.orchestrator import Orchestrator
from core.config import Config

def main():
    parser = argparse.ArgumentParser(
        description="Audit Engine - Red Team & IAM Collector",
        epilog="Exemple: main.py --user DOMAINE\\user --password pass --target-domain labo.local --mode labo --sniff"
    )
    parser.add_argument("--mode", choices=["prod", "labo"], default="labo")
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--target-domain", required=True)
    
    # Flags pour les modules risqués
    parser.add_argument("--sniff", action="store_true", help="Active le sniffing ARP (labo uniquement)")
    parser.add_argument("--dump-live", action="store_true", help="Active le dump LSASS en mémoire (labo uniquement)")
    
    # Fichier de sortie
    parser.add_argument("--output", default="audit_result.dat", help="Fichier de sortie (compressé)")
    
    # 🟢 NOUVEAUX ARGUMENTS POUR LINUX ET BASES
    parser.add_argument("--linux-hosts", help="Chemin vers un fichier texte contenant les IPs Linux (une par ligne)")
    parser.add_argument("--db-config", help="Chemin vers un fichier JSON de config des bases de données")

    args = parser.parse_args()
    
    # Charge les fichiers si présents
    linux_hosts = []
    if args.linux_hosts and os.path.exists(args.linux_hosts):
        with open(args.linux_hosts, 'r') as f:
            linux_hosts = [line.strip() for line in f if line.strip()]
    
    db_configs = []
    if args.db_config and os.path.exists(args.db_config):
        with open(args.db_config, 'r') as f:
            db_configs = json.load(f)  # Format: [{"type":"postgres","host":"ip","user":"root","password":"pass","dbname":"db"}]
    
    # On injecte les listes dans config
    config = Config(args)
    config.linux_hosts = linux_hosts
    config.db_configs = db_configs
    
    orch = Orchestrator(config)
    orch.run()

if __name__ == "__main__":
    main()