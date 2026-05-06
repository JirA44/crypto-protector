"""
Interface graphique pour Crypto Protector
Permet de configurer et monitorer la protection
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from pathlib import Path
from datetime import datetime
import threading

class CryptoProtectorGUI:
    def __init__(self, protector):
        self.protector = protector
        self.root = tk.Tk()
        self.root.title("Crypto Protector - Protection Anti-Scam")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        """Crée l'interface graphique"""

        # Notebook (onglets)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Onglet 1: Dashboard
        self.dashboard_frame = ttk.Frame(notebook)
        notebook.add(self.dashboard_frame, text="📊 Dashboard")
        self.create_dashboard()

        # Onglet 2: Configuration
        self.config_frame = ttk.Frame(notebook)
        notebook.add(self.config_frame, text="⚙️ Configuration")
        self.create_config()

        # Onglet 3: Listes
        self.lists_frame = ttk.Frame(notebook)
        notebook.add(self.lists_frame, text="📋 Listes")
        self.create_lists()

        # Onglet 4: Logs
        self.logs_frame = ttk.Frame(notebook)
        notebook.add(self.logs_frame, text="📜 Logs")
        self.create_logs()

    def create_dashboard(self):
        """Crée le dashboard principal"""

        # Status frame
        status_frame = ttk.LabelFrame(self.dashboard_frame, text="État de la Protection", padding=10)
        status_frame.pack(fill='x', padx=10, pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="🛡️ PROTECTION ACTIVE",
            font=("Arial", 16, "bold"),
            fg="green"
        )
        self.status_label.pack()

        # Statistiques
        stats_frame = ttk.LabelFrame(self.dashboard_frame, text="Statistiques", padding=10)
        stats_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.stats_text = tk.Text(stats_frame, height=15, font=("Consolas", 10))
        self.stats_text.pack(fill='both', expand=True)

        # Boutons d'action
        actions_frame = ttk.Frame(self.dashboard_frame)
        actions_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(
            actions_frame,
            text="🔄 Actualiser",
            command=self.update_status
        ).pack(side='left', padx=5)

        ttk.Button(
            actions_frame,
            text="🗑️ Effacer Clipboard",
            command=self.clear_clipboard
        ).pack(side='left', padx=5)

        ttk.Button(
            actions_frame,
            text="📊 Voir Logs",
            command=self.view_logs
        ).pack(side='left', padx=5)

    def create_config(self):
        """Crée l'interface de configuration"""

        config_inner = ttk.Frame(self.config_frame, padding=10)
        config_inner.pack(fill='both', expand=True)

        # Protection générale
        general_frame = ttk.LabelFrame(config_inner, text="Protection Générale", padding=10)
        general_frame.pack(fill='x', pady=5)

        self.enabled_var = tk.BooleanVar(value=self.protector.config.get('enabled', True))
        ttk.Checkbutton(
            general_frame,
            text="Activer la protection",
            variable=self.enabled_var
        ).pack(anchor='w', pady=2)

        self.block_unknown_var = tk.BooleanVar(value=self.protector.config.get('block_unknown', True))
        ttk.Checkbutton(
            general_frame,
            text="Bloquer les adresses inconnues",
            variable=self.block_unknown_var
        ).pack(anchor='w', pady=2)

        self.auto_block_var = tk.BooleanVar(value=self.protector.config.get('auto_block_clipboard', True))
        ttk.Checkbutton(
            general_frame,
            text="Effacer automatiquement le clipboard si adresse suspecte",
            variable=self.auto_block_var
        ).pack(anchor='w', pady=2)

        self.monitor_proc_var = tk.BooleanVar(value=self.protector.config.get('monitor_processes', True))
        ttk.Checkbutton(
            general_frame,
            text="Monitorer les processus crypto",
            variable=self.monitor_proc_var
        ).pack(anchor='w', pady=2)

        # Niveau de protection
        level_frame = ttk.LabelFrame(config_inner, text="Niveau de Protection", padding=10)
        level_frame.pack(fill='x', pady=5)

        self.level_var = tk.StringVar(value=self.protector.config.get('protection_level', 'high'))

        ttk.Radiobutton(
            level_frame,
            text="🟢 Faible - Alertes uniquement",
            variable=self.level_var,
            value="low"
        ).pack(anchor='w', pady=2)

        ttk.Radiobutton(
            level_frame,
            text="🟡 Moyen - Confirmation requise",
            variable=self.level_var,
            value="medium"
        ).pack(anchor='w', pady=2)

        ttk.Radiobutton(
            level_frame,
            text="🔴 Élevé - Blocage automatique",
            variable=self.level_var,
            value="high"
        ).pack(anchor='w', pady=2)

        # Bouton sauvegarder
        ttk.Button(
            config_inner,
            text="💾 Sauvegarder la Configuration",
            command=self.save_config
        ).pack(pady=20)

    def create_lists(self):
        """Crée l'interface des listes"""

        lists_inner = ttk.Frame(self.lists_frame, padding=10)
        lists_inner.pack(fill='both', expand=True)

        # Liste blanche
        white_frame = ttk.LabelFrame(lists_inner, text="✅ Liste Blanche (Adresses Autorisées)", padding=10)
        white_frame.pack(fill='both', expand=True, pady=5)

        white_top = ttk.Frame(white_frame)
        white_top.pack(fill='x', pady=5)

        ttk.Label(white_top, text="Ajouter adresse:").pack(side='left', padx=5)
        self.white_entry = ttk.Entry(white_top, width=50)
        self.white_entry.pack(side='left', padx=5)
        ttk.Button(white_top, text="➕ Ajouter", command=self.add_whitelist).pack(side='left', padx=5)

        self.white_listbox = tk.Listbox(white_frame, height=8)
        self.white_listbox.pack(fill='both', expand=True, pady=5)

        ttk.Button(white_frame, text="🗑️ Supprimer", command=self.remove_whitelist).pack()

        # Liste noire
        black_frame = ttk.LabelFrame(lists_inner, text="❌ Liste Noire (Adresses Bloquées)", padding=10)
        black_frame.pack(fill='both', expand=True, pady=5)

        black_top = ttk.Frame(black_frame)
        black_top.pack(fill='x', pady=5)

        ttk.Label(black_top, text="Ajouter adresse:").pack(side='left', padx=5)
        self.black_entry = ttk.Entry(black_top, width=50)
        self.black_entry.pack(side='left', padx=5)
        ttk.Button(black_top, text="➕ Ajouter", command=self.add_blacklist).pack(side='left', padx=5)

        self.black_listbox = tk.Listbox(black_frame, height=8)
        self.black_listbox.pack(fill='both', expand=True, pady=5)

        ttk.Button(black_frame, text="🗑️ Supprimer", command=self.remove_blacklist).pack()

        self.refresh_lists()

    def create_logs(self):
        """Crée l'interface des logs"""

        logs_inner = ttk.Frame(self.logs_frame, padding=10)
        logs_inner.pack(fill='both', expand=True)

        # Boutons
        buttons_frame = ttk.Frame(logs_inner)
        buttons_frame.pack(fill='x', pady=5)

        ttk.Button(
            buttons_frame,
            text="🔄 Actualiser",
            command=self.refresh_logs
        ).pack(side='left', padx=5)

        ttk.Button(
            buttons_frame,
            text="🗑️ Effacer les logs",
            command=self.clear_logs
        ).pack(side='left', padx=5)

        # Zone de texte pour les logs
        self.logs_text = scrolledtext.ScrolledText(
            logs_inner,
            height=25,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.logs_text.pack(fill='both', expand=True)

        self.refresh_logs()

    def update_status(self):
        """Met à jour le dashboard"""
        stats = f"""
╔══════════════════════════════════════════════════════════╗
║           CRYPTO PROTECTOR - STATISTIQUES                ║
╚══════════════════════════════════════════════════════════╝

📊 État: {'🟢 ACTIF' if self.protector.config.get('enabled') else '🔴 INACTIF'}
🛡️ Niveau: {self.protector.config.get('protection_level', 'high').upper()}

📋 LISTES
  ✅ Adresses autorisées: {len(self.protector.whitelist['addresses'])}
  ❌ Adresses bloquées:   {len(self.protector.blacklist['addresses'])}
  🚫 Domaines bloqués:    {len(self.protector.blacklist['domains'])}

⚙️ CONFIGURATION
  🔒 Bloquer adresses inconnues:     {'OUI' if self.protector.config.get('block_unknown') else 'NON'}
  📋 Auto-effacer clipboard:         {'OUI' if self.protector.config.get('auto_block_clipboard') else 'NON'}
  👁️ Monitorer processus:            {'OUI' if self.protector.config.get('monitor_processes') else 'NON'}

📁 FICHIERS
  • Configuration: {self.protector.config_file}
  • Liste blanche: {self.protector.whitelist_file}
  • Liste noire:   {self.protector.blacklist_file}
  • Logs:          {self.protector.log_file}

⏰ Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', stats)

    def clear_clipboard(self):
        """Efface le clipboard"""
        import pyperclip
        pyperclip.copy("")
        messagebox.showinfo("Clipboard", "Le presse-papiers a été effacé!")

    def view_logs(self):
        """Affiche les logs"""
        self.refresh_logs()

    def save_config(self):
        """Sauvegarde la configuration"""
        self.protector.config['enabled'] = self.enabled_var.get()
        self.protector.config['block_unknown'] = self.block_unknown_var.get()
        self.protector.config['auto_block_clipboard'] = self.auto_block_var.get()
        self.protector.config['monitor_processes'] = self.monitor_proc_var.get()
        self.protector.config['protection_level'] = self.level_var.get()

        self.protector.save_config()
        messagebox.showinfo("Configuration", "Configuration sauvegardée avec succès!")
        self.update_status()

    def add_whitelist(self):
        """Ajoute une adresse à la liste blanche"""
        address = self.white_entry.get().strip()
        if address:
            self.protector.add_to_whitelist(address, note="Ajouté manuellement via GUI")
            self.white_entry.delete(0, tk.END)
            self.refresh_lists()
            self.update_status()

    def remove_whitelist(self):
        """Supprime une adresse de la liste blanche"""
        selection = self.white_listbox.curselection()
        if selection:
            idx = selection[0]
            if idx < len(self.protector.whitelist['addresses']):
                addr = self.protector.whitelist['addresses'][idx]
                self.protector.whitelist['addresses'].pop(idx)
                self.protector.save_whitelist()
                self.refresh_lists()
                self.update_status()

    def add_blacklist(self):
        """Ajoute une adresse à la liste noire"""
        address = self.black_entry.get().strip()
        if address:
            self.protector.add_to_blacklist(address, reason="Ajouté manuellement via GUI")
            self.black_entry.delete(0, tk.END)
            self.refresh_lists()
            self.update_status()

    def remove_blacklist(self):
        """Supprime une adresse de la liste noire"""
        selection = self.black_listbox.curselection()
        if selection:
            idx = selection[0]
            if idx < len(self.protector.blacklist['addresses']):
                self.protector.blacklist['addresses'].pop(idx)
                self.protector.save_blacklist()
                self.refresh_lists()
                self.update_status()

    def refresh_lists(self):
        """Actualise les listes"""
        # Liste blanche
        self.white_listbox.delete(0, tk.END)
        for item in self.protector.whitelist['addresses']:
            if isinstance(item, dict):
                addr = item.get('address', str(item))
            else:
                addr = str(item)
            self.white_listbox.insert(tk.END, addr[:60])

        # Liste noire
        self.black_listbox.delete(0, tk.END)
        for item in self.protector.blacklist['addresses']:
            if isinstance(item, dict):
                addr = item.get('address', str(item))
            else:
                addr = str(item)
            self.black_listbox.insert(tk.END, addr[:60])

    def refresh_logs(self):
        """Actualise les logs"""
        try:
            if self.protector.log_file.exists():
                with open(self.protector.log_file, 'r', encoding='utf-8') as f:
                    logs = f.readlines()
                    # Afficher les 100 dernières lignes
                    recent_logs = ''.join(logs[-100:])
                    self.logs_text.delete('1.0', tk.END)
                    self.logs_text.insert('1.0', recent_logs)
                    self.logs_text.see(tk.END)
        except Exception as e:
            self.logs_text.delete('1.0', tk.END)
            self.logs_text.insert('1.0', f"Erreur lors du chargement des logs: {str(e)}")

    def clear_logs(self):
        """Efface les logs"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment effacer tous les logs?"):
            with open(self.protector.log_file, 'w', encoding='utf-8') as f:
                f.write("")
            self.refresh_logs()

    def run(self):
        """Lance l'interface"""
        self.root.mainloop()

def launch_gui(protector):
    """Lance l'interface graphique"""
    gui = CryptoProtectorGUI(protector)
    gui.run()
