# 🛡️ Crypto Protector - Protection Anti-Scam

Programme de protection contre les scams et le phishing crypto. Empêche l'envoi de fonds vers des adresses inconnues ou suspectes.

## ✨ Fonctionnalités

### 🔒 Protection Multi-Niveaux
- **Monitoring du Clipboard**: Détecte automatiquement les adresses crypto copiées
- **Blocage Automatique**: Efface les adresses suspectes du presse-papiers
- **Listes Blanche/Noire**: Gestion des adresses autorisées et bloquées
- **Anti-Phishing**: Détection de patterns suspects (airdrop, verify wallet, etc.)
- **Monitoring Processus**: Surveillance des wallets actifs (MetaMask, Phantom, etc.)

### 💰 Crypto Supportées
- Bitcoin (BTC) - Addresses legacy et SegWit
- Ethereum (ETH)
- Solana (SOL)
- USDT (Tether)
- BNB (Binance)

### 🎯 Niveaux de Protection
1. **Faible**: Alertes uniquement
2. **Moyen**: Confirmation requise avant toute transaction
3. **Élevé**: Blocage automatique des adresses inconnues

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- Windows (pour le monitoring des processus)

### Installation des dépendances

```bash
cd D:\crypto_protector
pip install -r requirements.txt
```

## 🚀 Utilisation

### Mode GUI (Recommandé)
Lance l'interface graphique complète avec dashboard:

```bash
python launcher.py
```

### Mode Console
Lance uniquement le protecteur en arrière-plan:

```bash
python main.py
```

## 📊 Interface Graphique

L'interface comprend 4 onglets:

### 1. Dashboard
- État de la protection en temps réel
- Statistiques sur les adresses bloquées/autorisées
- Actions rapides (effacer clipboard, voir logs)

### 2. Configuration
- Activer/désactiver la protection
- Choisir le niveau de protection
- Configurer les options de blocage
- Activer/désactiver le monitoring des processus

### 3. Listes
- **Liste Blanche**: Adresses autorisées (exchanges, wallets personnels)
- **Liste Noire**: Adresses bloquées (scams connus, adresses suspectes)
- Ajout/suppression facile d'adresses

### 4. Logs
- Historique complet de toutes les actions
- Affichage des adresses détectées
- Alertes de sécurité

## 🛠️ Configuration

### Fichiers de configuration

```
D:\crypto_protector\
├── config.json          # Configuration principale
├── whitelist.json       # Liste blanche
├── blacklist.json       # Liste noire
├── protection_log.txt   # Logs de protection
```

### Exemple config.json

```json
{
    "enabled": true,
    "block_unknown": true,
    "block_new_addresses": true,
    "require_confirmation": true,
    "auto_block_clipboard": true,
    "monitor_processes": true,
    "protection_level": "high"
}
```

### Ajouter une adresse à la liste blanche

Via l'interface GUI ou manuellement dans `whitelist.json`:

```json
{
    "addresses": [
        {
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "added": "2025-01-15T10:30:00",
            "note": "Mon wallet MetaMask"
        }
    ]
}
```

### Ajouter une adresse à la liste noire

Via l'interface GUI ou manuellement dans `blacklist.json`:

```json
{
    "addresses": [
        {
            "address": "0xSUSPECT_ADDRESS",
            "added": "2025-01-15T11:00:00",
            "reason": "Scam détecté"
        }
    ],
    "domains": [
        "bit.ly",
        "tinyurl.com"
    ],
    "patterns": [
        "free.*btc",
        "double.*crypto",
        "airdrop.*claim"
    ]
}
```

## 🔐 Sécurité

### Ce que le programme protège:
- ✅ Copier-coller d'adresses crypto suspectes
- ✅ Sites de phishing (détection de patterns)
- ✅ Adresses inconnues non vérifiées
- ✅ Scams "airdrop" et "double your crypto"
- ✅ URLs raccourcies suspectes

### Ce que le programme NE fait PAS:
- ❌ N'intercepte pas les transactions blockchain
- ❌ N'a pas accès à vos clés privées
- ❌ Ne modifie pas les wallets installés
- ❌ Ne collecte aucune donnée personnelle

## 📝 Logs

Les logs sont enregistrés dans `protection_log.txt` avec le format:

```
[2025-01-15 14:30:15] [WARNING] [CLIPBOARD_BLOCKED] Adresse ETH bloquée: 0x742d35Cc6634C053... (Raison: unknown)
[2025-01-15 14:31:22] [INFO] [WHITELIST_ADD] Adresse ajoutée: 0x742d35Cc6634C053...
[2025-01-15 14:35:10] [WARNING] [SUSPICIOUS_CONTENT] Contenu suspect détecté: ['free.*btc']
```

## 🚨 Que faire en cas d'alerte?

### Adresse bloquée dans le clipboard
1. **NE PAS** forcer l'utilisation de cette adresse
2. Vérifier la source de l'adresse
3. Si l'adresse est légitime, l'ajouter à la liste blanche via l'interface
4. Toujours double-vérifier les adresses crypto avant envoi

### Site web suspect détecté
1. Fermer immédiatement la page
2. Ne jamais connecter votre wallet à un site inconnu
3. Vérifier l'URL officielle du service
4. Chercher des avis sur le site avant de continuer

### Processus crypto détecté
- C'est normal si vous utilisez un wallet
- La protection passe en mode "haute vigilance"
- Soyez particulièrement attentif aux adresses copiées

## 🆘 Support

### Problèmes courants

**Le programme ne démarre pas**
```bash
# Vérifier Python
python --version

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

**Les alertes ne s'affichent pas**
- Vérifier que `auto_block_clipboard` est activé dans config.json
- S'assurer que le programme tourne en arrière-plan

**Une adresse légitime est bloquée**
- Ajouter l'adresse à la liste blanche via l'interface
- Ou désactiver temporairement `block_unknown`

## ⚠️ Avertissement

Ce programme est un outil de PROTECTION DÉFENSIF uniquement. Il ne garantit pas une sécurité absolue contre tous les types d'attaques. Toujours:

- Vérifier manuellement les adresses importantes
- Utiliser des wallets hardware pour les gros montants
- Activer l'authentification 2FA partout
- Ne jamais partager vos clés privées ou seed phrases
- Vérifier les URLs des sites web crypto

## 📄 Licence

Ce logiciel est fourni "tel quel" sans garantie. Utilisez-le à vos propres risques.

## 🔄 Mises à jour

Pour mettre à jour la liste noire avec les derniers scams connus, consultez régulièrement:
- https://cryptoscamdb.org/
- https://www.scam-detector.com/crypto

---

**Restez vigilant! La meilleure protection reste votre prudence.** 🛡️
