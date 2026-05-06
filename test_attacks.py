"""
Simulateur d'attaques crypto pour tester Crypto Protector
ATTENTION: Ceci est un outil de TEST uniquement
"""

import pyperclip
import time
import random

class AttackSimulator:
    def __init__(self):
        self.fake_addresses = {
            'BTC': [
                '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Genesis address
                 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
                '3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy',
            ],
            'ETH': [
                '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
                '0xdAC17F958D2ee523a2206206994597C13D831ec7',  # USDT contract
                '0x0000000000000000000000000000000000000000',
            ],
            'SOL': [
                'DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK',
                '11111111111111111111111111111111',
                'SysvarC1ock11111111111111111111111111111111',
            ]
        }

        self.phishing_messages = [
            "🎁 FREE AIRDROP! Click here to claim your 1 BTC: bit.ly/free-btc-now",
            "⚠️ URGENT: Verify your wallet immediately or lose access! Connect now: metamask-verify.com",
            "💰 DOUBLE YOUR CRYPTO! Send 0.1 BTC, receive 0.2 BTC back! Limited time!",
            "🚨 Security Alert: Suspicious activity detected. Confirm your wallet: trust-wallet-secure.net",
            "🎉 You won 5 ETH! Claim your prize now before it expires: eth-claim.io",
            "⭐ Exclusive offer: Get free USDT tokens! Just connect your wallet: usdt-free.com",
        ]

        self.scam_patterns = [
            "Click here for FREE Bitcoin rewards!",
            "Connect your wallet to verify ownership",
            "Send 1 ETH get 2 ETH back guaranteed",
            "Congratulations! You've been selected for our airdrop program",
            "URGENT: Your crypto wallet needs immediate verification",
        ]

    def simulate_clipboard_attack(self, crypto_type='ETH', count=3):
        """Simule une attaque par clipboard (copie d'adresses suspectes)"""
        print(f"\n{'='*60}")
        print(f"🎭 SIMULATION: Attaque par Clipboard ({crypto_type})")
        print(f"{'='*60}")

        addresses = self.fake_addresses.get(crypto_type, self.fake_addresses['ETH'])

        for i in range(count):
            addr = random.choice(addresses)
            print(f"\n[{i+1}/{count}] Copie d'une adresse {crypto_type} suspecte dans le clipboard...")
            print(f"  Adresse: {addr}")

            pyperclip.copy(addr)
            print(f"  ✓ Adresse copiée! Le protecteur devrait la détecter et la bloquer...")
            time.sleep(3)  # Attendre que le protecteur détecte

    def simulate_phishing_attack(self, count=3):
        """Simule une attaque de phishing (messages suspects)"""
        print(f"\n{'='*60}")
        print(f"🎣 SIMULATION: Attaque de Phishing")
        print(f"{'='*60}")

        for i in range(count):
            msg = random.choice(self.phishing_messages)
            print(f"\n[{i+1}/{count}] Message de phishing détecté...")
            print(f"  Message: {msg}")

            pyperclip.copy(msg)
            print(f"  ✓ Message copié! Le protecteur devrait détecter les patterns suspects...")
            time.sleep(3)

    def simulate_address_swap_attack(self):
        """Simule une attaque de swap d'adresse (malware qui change l'adresse)"""
        print(f"\n{'='*60}")
        print(f"🔄 SIMULATION: Attaque Address Swap")
        print(f"{'='*60}")

        print("\n[1/3] Vous copiez votre adresse légitime...")
        legit_addr = "0xYOUR_LEGIT_WALLET_ADDRESS_HERE_123456789"
        pyperclip.copy(legit_addr)
        print(f"  Adresse légitime: {legit_addr}")
        time.sleep(2)

        print("\n[2/3] ⚠️ Malware détecté! Remplacement de l'adresse par une adresse de scammer...")
        scam_addr = self.fake_addresses['ETH'][0]
        pyperclip.copy(scam_addr)
        print(f"  Adresse du scammer: {scam_addr}")
        print(f"  ✓ Le protecteur devrait bloquer cette adresse inconnue!")
        time.sleep(3)

    def simulate_typosquatting_attack(self):
        """Simule une attaque typosquatting (faux sites web)"""
        print(f"\n{'='*60}")
        print(f"⌨️ SIMULATION: Attaque Typosquatting")
        print(f"{'='*60}")

        fake_sites = [
            "metamask-verify.com - FAUX site MetaMask",
            "binance-support.net - FAUX site Binance",
            "coinbase-wallet.org - FAUX site Coinbase",
            "trust-wallet-secure.io - FAUX site Trust Wallet",
        ]

        for i, site in enumerate(fake_sites, 1):
            print(f"\n[{i}/{len(fake_sites)}] Site suspect: {site}")
            # Copier un message avec le site et une adresse
            msg = f"Visit {site.split(' - ')[0]} to claim rewards! Send to: {random.choice(self.fake_addresses['ETH'])}"
            pyperclip.copy(msg)
            print(f"  ✓ Message copié avec adresse suspecte...")
            time.sleep(3)

    def simulate_social_engineering(self):
        """Simule une attaque d'ingénierie sociale"""
        print(f"\n{'='*60}")
        print(f"🗣️ SIMULATION: Attaque d'Ingénierie Sociale")
        print(f"{'='*60}")

        scenarios = [
            {
                'title': 'Support technique fake',
                'message': f"Hello, I'm from MetaMask support. Please send test transaction to verify: {self.fake_addresses['ETH'][0]}"
            },
            {
                'title': 'Faux giveaway',
                'message': f"Elon Musk is giving away BTC! Send 0.1 BTC to {self.fake_addresses['BTC'][0]} and get 1 BTC back!"
            },
            {
                'title': 'Urgence créée',
                'message': f"URGENT: Your wallet will be locked in 1 hour! Migrate funds immediately to: {self.fake_addresses['SOL'][0]}"
            }
        ]

        for i, scenario in enumerate(scenarios, 1):
            print(f"\n[{i}/{len(scenarios)}] Scénario: {scenario['title']}")
            print(f"  Message: {scenario['message']}")
            pyperclip.copy(scenario['message'])
            print(f"  ✓ Le protecteur devrait détecter les patterns suspects et l'adresse...")
            time.sleep(4)

    def run_full_test_suite(self):
        """Lance une suite complète de tests d'attaques"""
        print("\n" + "="*60)
        print("  🎭 CRYPTO PROTECTOR - SUITE DE TESTS D'ATTAQUES")
        print("="*60)
        print("\nCe script va simuler différentes attaques crypto pour tester")
        print("la protection. Le Crypto Protector devrait bloquer toutes ces")
        print("tentatives!\n")
        input("Appuyez sur Entrée pour commencer les tests...")

        # Test 1: Clipboard attacks
        self.simulate_clipboard_attack('ETH', 3)
        time.sleep(2)

        self.simulate_clipboard_attack('BTC', 2)
        time.sleep(2)

        # Test 2: Phishing
        self.simulate_phishing_attack(3)
        time.sleep(2)

        # Test 3: Address swap
        self.simulate_address_swap_attack()
        time.sleep(2)

        # Test 4: Typosquatting
        self.simulate_typosquatting_attack()
        time.sleep(2)

        # Test 5: Social engineering
        self.simulate_social_engineering()

        print(f"\n{'='*60}")
        print("  ✅ SUITE DE TESTS TERMINÉE")
        print("="*60)
        print("\nVérifiez les logs du Crypto Protector pour voir toutes")
        print("les attaques qui ont été bloquées!")
        print("\nConsultez l'onglet 'Logs' dans l'interface graphique.")

def main():
    simulator = AttackSimulator()

    print("\n🎭 SIMULATEUR D'ATTAQUES CRYPTO - MENU")
    print("="*60)
    print("1. Test complet (toutes les attaques)")
    print("2. Attaque Clipboard (ETH)")
    print("3. Attaque Clipboard (BTC)")
    print("4. Attaque Phishing")
    print("5. Attaque Address Swap")
    print("6. Attaque Typosquatting")
    print("7. Attaque Ingénierie Sociale")
    print("0. Quitter")
    print("="*60)

    choice = input("\nChoisissez un test (0-7): ").strip()

    if choice == '1':
        simulator.run_full_test_suite()
    elif choice == '2':
        simulator.simulate_clipboard_attack('ETH', 5)
    elif choice == '3':
        simulator.simulate_clipboard_attack('BTC', 5)
    elif choice == '4':
        simulator.simulate_phishing_attack(5)
    elif choice == '5':
        simulator.simulate_address_swap_attack()
    elif choice == '6':
        simulator.simulate_typosquatting_attack()
    elif choice == '7':
        simulator.simulate_social_engineering()
    elif choice == '0':
        print("Au revoir!")
        return
    else:
        print("Choix invalide!")
        return

    print("\n" + "="*60)
    print("Test terminé! Vérifiez les alertes du Crypto Protector.")
    print("="*60)

if __name__ == "__main__":
    main()
