# Crypto Protector — aide de vigilance contre les arnaques

Crypto Protector surveille certains contenus liés aux cryptomonnaies, notamment les adresses copiées dans le presse-papiers. Il peut afficher une alerte et appliquer des règles locales de liste blanche ou noire.

> Cet outil ne bloque pas une transaction dans le wallet et ne garantit pas qu’une adresse ou un site est sûr. Il ne remplace pas la vérification de l’adresse complète sur l’écran du wallet avant chaque envoi.

## À quoi sert-il ?

Il ajoute un contrôle local entre le copier-coller d’une adresse et son utilisation. Il peut aider à remarquer une adresse inconnue, une entrée correspondant à une règle suspecte ou une différence entre une adresse copiée et celles que l’on a explicitement autorisées.

## Pourquoi l’utiliser ?

Les attaques par remplacement du presse-papiers et les faux liens de distribution crypto reposent souvent sur une vérification trop rapide. Un outil de surveillance peut fournir un rappel au moment où l’adresse est copiée et conserver un journal des alertes. Une alerte reste un signal à examiner : une adresse inconnue n’est pas automatiquement frauduleuse, et une adresse autorisée n’est pas automatiquement sans risque.

## Exemple d’utilisation

1. Démarrer l’application graphique avec `python launcher.py`.
2. Choisir le niveau de protection dans la configuration.
3. Ajouter manuellement les adresses de confiance que l’on a vérifiées, en indiquant à qui elles appartiennent.
4. Copier une adresse de destination et lire l’alerte avant de poursuivre dans le wallet.
5. Si l’alerte semble incorrecte, vérifier l’adresse par une source indépendante au lieu de désactiver immédiatement la protection.

Pour lancer uniquement le programme en console :

```bash
python main.py
```

## English

### What is Crypto Protector for?

Crypto Protector is a local alert tool that watches selected crypto-related content, especially addresses copied to the clipboard, and applies user-configured allow/block lists and detection rules.

### Why use it?

A clipboard check can remind you to inspect a destination address before using it in a wallet and can log alerts for later review. An alert is only a signal: an unknown address is not automatically malicious, and an allow-listed address is not automatically safe.

### Example

Run `python launcher.py`, choose a protection level, add only addresses you have independently verified, then review the alert when you copy a destination. Always compare the complete address and network in your wallet before sending.

This tool does not intercept blockchain transactions or guarantee that an address or website is safe. Heuristic detection can produce false positives and miss new threats.


## Fonctions indiquées par le projet

- surveillance du presse-papiers et détection de motifs configurés ;
- listes blanche et noire ;
- journal des événements ;
- surveillance de certains processus de wallet sous Windows ;
- interface graphique avec tableau de bord et réglages.

La détection de motifs est heuristique : elle peut produire des faux positifs et manquer des menaces nouvelles. L’outil ne lit pas les clés privées et n’intercepte pas les transactions blockchain.

## Installation

Prérequis : Python 3.8 ou supérieur. La surveillance de processus est destinée à Windows.

```powershell
python -m pip install -r requirements.txt
python launcher.py
```

Pour démarrer en console, utiliser `python main.py`.

## Utilisation prudente

Toujours comparer l’adresse de destination complète dans le wallet, vérifier le réseau et effectuer un petit transfert de vérification lorsque c’est approprié. Ne jamais saisir une phrase de récupération dans cet outil ni dans un site tiers.
