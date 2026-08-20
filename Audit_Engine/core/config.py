import time
import random

class Config:
    def __init__(self, args):
        self.user = args.user
        self.password = args.password
        self.target_domain = args.target_domain
        self.mode = args.mode
        self.output = args.output if hasattr(args, 'output') else "audit_result.dat"
        self.sniff_enabled = args.sniff if self.mode == "labo" else False
        self.dump_live_enabled = args.dump_live if self.mode == "labo" else False
        self.min_delay = 1.5
        self.max_delay = 5.0
        self.ping_timeout = 2.0
        self.sniff_duration = 120
        self.edr_signatures = {
            "CrowdStrike": ["csfalcon", "csagent"],
            "SentinelOne": ["sentinelagent", "sentinelone"],
            "Microsoft Defender": ["msmpeng", "sense", "mssense"],
            "Carbon Black": ["cbdefense", "cb.exe"],
            "Palo Alto": ["traps", "cyvera"],
            "Trend Micro": ["tmcc", "pccntmon"],
        }
        self.sensitive_files_win = [".env", ".config", "web.config", "appsettings.json"]
        self.sensitive_files_linux = [".env", ".pem", ".key", ".bash_history"]

    def get_delay(self):
        return random.uniform(self.min_delay, self.max_delay)