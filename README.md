
# 🧬 Necrosis – Malware Caméléon Autonome pour Audit de Sécurité Active Directory

**Version** : 1.0 (Proof of Concept – Laboratoire)  
**Statut** : Projet de recherche – Master 2 Sécurité des Réseaux et Systèmes Avancés  
**Auteur** : Victor Sylvano


---

## 📌 Description

**Necrosis** est un moteur offensif de type **Red Team** / **APT simulée**, conçu pour évaluer la résistance des environnements Active Directory face à la compromission des identifiants. Il articule six couches d’extraction (mémoire, disque, applicatif, réseau, annuaire, bases de données) avec un **Moteur Caméléon** capable de détecter dynamiquement son environnement (OS, privilèges, EDR) et de muter son comportement (obfuscation, délais aléatoires, modification du flux de contrôle) afin de minimiser sa surface de détection.

Ce projet est un **exercice académique** réalisé dans un environnement de laboratoire contrôlé. Il n’est **pas** destiné à un usage en production réelle sans autorisation explicite.

---

## 🎯 Objectifs pédagogiques

- Modéliser une menace persistante avancée (APT) autonome.
- Implémenter des techniques d’évasion face aux EDR/SIEM modernes.
- Extraire des identifiants à tous les niveaux (mémoire, disque, réseau, navigateurs, bases de données).
- Pivoter de manière autonome à travers les VLANs sans infrastructure C2.
- Exfiltrer les données de manière furtive (compression, dissimulation).

---

## 🧩 Architecture

Necrosis/
│
├── main.py                         # Point d'entrée (argparse)
├── requirements.txt                # Dépendances
├── README.md                       # Documentation
│
├── core/
│   ├── __init__.py
│   ├── config.py                   # Configuration (seuils, signatures EDR)
│   └── orchestrator.py             # Boucle principale (Détection → Siphon → Export)
│
├── modules/
│   ├── __init__.py
│   ├── detector.py                 # Fingerprinting OS, EDR, hooks API
│   ├── mutation.py                 # Obfuscation XOR/Base64, délais aléatoires
│   └── siphon.py                   # Collecteur global (Windows/Linux/DB/Network)
│
├── collectors/
│   ├── __init__.py
│   ├── ad_collector.py             # LDAP : users, groups, computers
│   ├── win_collector.py            # Windows : SAM (VSS), LSASS (comsvcs), DPAPI, CredManager
│   ├── linux_collector.py          # Linux : /etc/shadow, clés SSH, .env
│   └── db_collector.py             # PostgreSQL / MySQL : users, privilèges, PII
│
├── utils/
│   ├── __init__.py
│   ├── network.py                  # ARP Spoofing (Scapy), restauration 120s
│   ├── crypto.py                   # Chiffrement AES / XOR
│   └── export.py                   # JSON → ZLIB (-70%) → Base64
│
└── payloads/
    ├── __init__.py
    └── agent_stub.py               # Stub fileless pour injection mémoire (WinRM/SSH)



---

## ⚙️ Prérequis

- **Système** : Windows 10/11 ou Linux (Ubuntu/Debian) pour le développement.
- **Python** : 3.10 ou supérieur.
- **Environnement** : Réseau Active Directory de laboratoire (VM isolées).
- **Droits** : Compte avec privilèges **Administrateur / SYSTEM** sur les cibles (pour les snapshots VSS et le dump LSASS).

---

## 📦 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-repo/necrosis.git
