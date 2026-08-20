import json
import zlib
import base64
import os

class DataExporter:
    def __init__(self, config):
        self.config = config

    def export(self, data):
        json_str = json.dumps(data, indent=2, default=str)
        compressed = zlib.compress(json_str.encode('utf-8'))
        payload = base64.b64encode(compressed).decode('ascii')
        with open(self.config.output, 'w') as f:
            f.write(payload)
        return payload