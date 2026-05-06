"""
Crypto Protector - Programme de protection contre les scams crypto
Empêche l'envoi de fonds vers des adresses inconnues ou suspectes
"""

import os
import sys
import json
import time
import re
import hashlib
import threading
from datetime import datetime
from pathlib import Path
import pyperclip
import win32gui
import win32process
import psutil
from tkinter import Tk, messagebox

class CryptoProtector:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "config.json"
        self.whitelist_file = self.base_dir / "whitelist.json"
        self.blacklist_file = self.base_dir / "blacklist.json"
        self.log_file = self.base_dir / "protection_log.txt"

        # Charger la configuration
        self.load_config()
        self.load_lists()

        # État du presse-papiers
        self.last_clipboard = ""
        self.clipboard_blocked = False

        # Patterns pour détecter les adresses crypto
        self.crypto_patterns = {
            'BTC': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|bc1[a-zA-HJ-NP-Z0-9]{39,59}\b',
            'ETH': r'\b0x[a-fA-F0-9]{40}\b',
            'SOL': r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b',
            'USDT': r'\b0x[a-fA-F0-9]{40}\b|T[A-Za-z1-9]{33}\b',
            'BNB': r'\bbnb[0-9a-z]{39}\b|0x[a-fA-F0-9]{40}\b',
        }

        # Liste des processus crypto suspects
        self.suspicious_processes = [
            'metamask', 'phantom', 'exodus', 'electrum',
            'coinbase', 'binance', 'trust', 'ledger'
        ]

        self.running = True
        print("[✓] Crypto Protector initialisé")

    def load_config(self):
        """Charge la configuration"""
        default_config = {
            "enabled": True,
            "block_unknown": True,
            "block_new_addresses": True,
            "require_confirmation": True,
            "auto_block_clipboard": True,
            "monitor_processes": True,
            "alert_threshold": 0.01,  # BTC
            "protection_level": "high"  # low, medium, high
        }

        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """Sauvegarde la configuration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, indent=4, fp=f)

    def load_lists(self):
        """Charge les listes blanche et noire"""
        if self.whitelist_file.exists():
            with open(self.whitelist_file, 'r', encoding='utf-8') as f:
                self.whitelist = json.load(f)
        else:
            self.whitelist = {
                "addresses": [],
                "domains": [],
                "processes": []
            }
            self.save_whitelist()

        if self.blacklist_file.exists():
            with open(self.blacklist_file, 'r', encoding='utf-8') as f:
                self.blacklist = json.load(f)
        else:
            self.blacklist = {
                "addresses": [],
                "domains": [
                    "bit.ly", "tinyurl.com", "goo.gl",  # URL shorteners suspects
                ],
                "patterns": [
                    r"free.*btc", r"double.*crypto", r"airdrop.*claim",
                    r"verify.*wallet", r"connect.*wallet.*urgent"
                ]
            }
            self.save_blacklist()

    def save_whitelist(self):
        """Sauvegarde la liste blanche"""
        with open(self.whitelist_file, 'w', encoding='utf-8') as f:
            json.dump(self.whitelist, indent=4, fp=f)

    def save_blacklist(self):
        """Sauvegarde la liste noire"""
        with open(self.blacklist_file, 'w', encoding='utf-8') as f:
            json.dump(self.blacklist, indent=4, fp=f)

    def log_event(self, event_type, message, severity="INFO"):
        """Enregistre un événement dans les logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{severity}] [{event_type}] {message}\n"

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(log_entry.strip())

    def detect_crypto_address(self, text):
        """Détecte les adresses crypto dans un texte"""
        detected = []
        for crypto_type, pattern in self.crypto_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                detected.append({
                    'type': crypto_type,
                    'address': match,
                    'hash': hashlib.sha256(match.encode()).hexdigest()[:16]
                })
        return detected

    def is_address_safe(self, address):
        """Vérifie si une adresse est sûre"""
        # Vérifier la liste blanche
        if address in self.whitelist['addresses']:
            return True, "whitelist"

        # Vérifier la liste noire
        if address in self.blacklist['addresses']:
            return False, "blacklist"

        # Si le mode "block_unknown" est activé
        if self.config['block_unknown']:
            return False, "unknown"

        return True, "default"

    def check_suspicious_patterns(self, text):
        """Vérifie les patterns suspects dans le texte"""
        suspicious = []
        text_lower = text.lower()

        for pattern in self.blacklist['patterns']:
            if re.search(pattern, text_lower, re.IGNORECASE):
                suspicious.append(pattern)

        return suspicious

    def monitor_clipboard(self):
        """Monitore le presse-papiers pour détecter les adresses crypto"""
        print("[*] Monitoring du presse-papiers activé...")

        while self.running:
            try:
                clipboard_content = pyperclip.paste()

                if clipboard_content != self.last_clipboard:
                    self.last_clipboard = clipboard_content

                    # Détecter les adresses crypto
                    addresses = self.detect_crypto_address(clipboard_content)

                    if addresses:
                        for addr_info in addresses:
                            address = addr_info['address']
                            crypto_type = addr_info['type']

                            # Vérifier si l'adresse est sûre
                            is_safe, reason = self.is_address_safe(address)

                            if not is_safe:
                                self.log_event(
                                    "CLIPBOARD_BLOCKED",
                                    f"Adresse {crypto_type} bloquée: {address[:20]}... (Raison: {reason})",
                                    "WARNING"
                                )

                                if self.config['auto_block_clipboard']:
                                    # Effacer le presse-papiers
                                    pyperclip.copy("")
                                    self.show_alert(
                                        "⚠️ ADRESSE CRYPTO BLOQUÉE",
                                        f"Une adresse {crypto_type} suspecte a été détectée et effacée du presse-papiers.\n\n"
                                        f"Raison: {reason}\n"
                                        f"Hash: {addr_info['hash']}"
                                    )
                            else:
                                self.log_event(
                                    "CLIPBOARD_SAFE",
                                    f"Adresse {crypto_type} autorisée: {address[:20]}...",
                                    "INFO"
                                )

                    # Vérifier les patterns suspects
                    suspicious = self.check_suspicious_patterns(clipboard_content)
                    if suspicious:
                        self.log_event(
                            "SUSPICIOUS_CONTENT",
                            f"Contenu suspect détecté dans le presse-papiers: {suspicious}",
                            "WARNING"
                        )

                time.sleep(0.5)  # Vérifier toutes les 0.5 secondes

            except Exception as e:
                self.log_event("ERROR", f"Erreur monitoring clipboard: {str(e)}", "ERROR")
                time.sleep(1)

    def get_active_window_process(self):
        """Récupère le processus de la fenêtre active"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name().lower()
        except:
            return None

    def monitor_processes(self):
        """Monitore les processus crypto actifs"""
        print("[*] Monitoring des processus activé...")

        while self.running:
            try:
                active_process = self.get_active_window_process()

                if active_process:
                    # Vérifier si c'est un processus crypto
                    for suspect in self.suspicious_processes:
                        if suspect in active_process:
                            self.log_event(
                                "CRYPTO_PROCESS_ACTIVE",
                                f"Processus crypto détecté: {active_process}",
                                "INFO"
                            )
                            # Mode protection élevé quand un wallet est ouvert
                            break

                time.sleep(2)  # Vérifier toutes les 2 secondes

            except Exception as e:
                self.log_event("ERROR", f"Erreur monitoring process: {str(e)}", "ERROR")
                time.sleep(2)

    def show_alert(self, title, message):
        """Affiche une alerte à l'utilisateur"""
        def show():
            root = Tk()
            root.withdraw()
            messagebox.showwarning(title, message)
            root.destroy()

        # Afficher dans un thread séparé pour ne pas bloquer
        threading.Thread(target=show, daemon=True).start()

    def add_to_whitelist(self, address, note=""):
        """Ajoute une adresse à la liste blanche"""
        if address not in self.whitelist['addresses']:
            self.whitelist['addresses'].append({
                'address': address,
                'added': datetime.now().isoformat(),
                'note': note
            })
            self.save_whitelist()
            self.log_event("WHITELIST_ADD", f"Adresse ajoutée: {address[:20]}...", "INFO")
            return True
        return False

    def add_to_blacklist(self, address, reason=""):
        """Ajoute une adresse à la liste noire"""
        if address not in self.blacklist['addresses']:
            self.blacklist['addresses'].append({
                'address': address,
                'added': datetime.now().isoformat(),
                'reason': reason
            })
            self.save_blacklist()
            self.log_event("BLACKLIST_ADD", f"Adresse bloquée: {address[:20]}...", "WARNING")
            return True
        return False

    def start(self):
        """Démarre le protecteur"""
        print("\n" + "="*60)
        print("    CRYPTO PROTECTOR - Protection Anti-Scam Activée")
        print("="*60)
        print(f"[✓] Protection niveau: {self.config['protection_level'].upper()}")
        print(f"[✓] Blocage adresses inconnues: {'OUI' if self.config['block_unknown'] else 'NON'}")
        print(f"[✓] Auto-blocage clipboard: {'OUI' if self.config['auto_block_clipboard'] else 'NON'}")
        print(f"[✓] Monitoring processus: {'OUI' if self.config['monitor_processes'] else 'NON'}")
        print(f"[✓] Adresses en liste blanche: {len(self.whitelist['addresses'])}")
        print(f"[✓] Adresses en liste noire: {len(self.blacklist['addresses'])}")
        print("="*60 + "\n")

        self.log_event("SYSTEM", "Crypto Protector démarré", "INFO")

        # Démarrer les threads de monitoring
        clipboard_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        clipboard_thread.start()

        if self.config['monitor_processes']:
            process_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            process_thread.start()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Arrêt du Crypto Protector...")
            self.running = False
            self.log_event("SYSTEM", "Crypto Protector arrêté", "INFO")

def main():
    # Créer le dossier si nécessaire
    os.makedirs("D:/crypto_protector", exist_ok=True)

    protector = CryptoProtector()
    protector.start()

if __name__ == "__main__":
    main()
