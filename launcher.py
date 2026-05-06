"""
Lanceur pour Crypto Protector avec GUI
Démarre le protecteur en arrière-plan et lance l'interface graphique
"""

import sys
import threading
from pathlib import Path

# Ajouter le dossier courant au path
sys.path.insert(0, str(Path(__file__).parent))

from main import CryptoProtector
from gui import launch_gui

def main():
    """Lance l'application avec GUI"""
    print("Démarrage de Crypto Protector...")

    # Créer le protecteur
    protector = CryptoProtector()

    # Démarrer le monitoring en arrière-plan
    def run_protector():
        protector.start()

    protector_thread = threading.Thread(target=run_protector, daemon=True)
    protector_thread.start()

    # Lancer l'interface graphique
    try:
        launch_gui(protector)
    except KeyboardInterrupt:
        print("\nArrêt de l'application...")
        protector.running = False

if __name__ == "__main__":
    main()
