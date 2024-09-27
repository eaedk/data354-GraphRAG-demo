# Hiring Challenge: Construction d'un Agent Conversationnel Spécialisé

Ce dépôt GitHub contient le challenge organisé par **data354** pour évaluer vos compétences en développement d'agents conversationnels spécialisés.

## Table des Matières

- [À propos de data354](#à-propos-de-data354)
- [Présentation du Challenge](#présentation-du-challenge)

- [Structure du Repository](#structure-du-repository)
- [Comment Démarrer](#comment-démarrer)

- [Ressources](#ressources)

## À propos de data354

data354 est spécialisé dans les services liés à la donnée, offrant des solutions de stratégie, architecture, data engineering, et data science. Nous accompagnons nos clients dans la valorisation de leurs données à travers nos centres de ressources à Abidjan et Paris.

## Présentation du Challenge

OpenAI a révolutionné l'IA avec des agents conversationnels basés sur les Large Language Models (LLM). Toutefois, ces modèles ont des limites en termes de données privées et spécifiques. Pour y remédier, nous proposons d'explorer la **Génération Augmentée par Graphe de Connaissances (GraphRAG)**. Le but est de créer un agent conversationnel capable de répondre aux questions basées sur des documents OHADA.

### Votre Tâche

- **Pré-traiter les données** : Nettoyage et préparation des documents.
- **Créer une chaîne GraphRAG** : Intégration de graphes de connaissances.
- **Développer une interface web** : Pour interagir avec l'agent.

**Documents OHADA à utiliser** : 
- [Acte uniforme sur les contrats de transport de marchandises](/).
- [Acte uniforme sur le droit de l'arbitrage](/).


## Structure du Repository

```plaintext
├── data/
├── src/
├── docs/
├── requirements.txt
└── LICENSE
```

## Comment Démarrer

1. Cloner le dépôt:

```sh
git clone https://github.com/votre-utilisateur/hiring-challenge.git
cd hiring-challenge
```

1. Installer les dépendances:

```sh
pip install -r requirements.txt

```

1. Lancer l'application:

```sh
streamlit run

```

## Ressources

- [LangChain Documentation](https://python.langchain.com/docs/get-started/introduction)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Chainlit Documentation](https://docs.chainlit.io/get-started/overview)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/)