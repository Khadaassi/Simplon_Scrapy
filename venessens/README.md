
<p align="center">Scraping Project</p>

# <p align="center">BricoSimplon - Veille Concurrentielle</p>
<p align="center">
    <img src="images/banner.png" alt="Banner">
</p>

Ce projet est un système de scraping conçu pour collecter des données tarifaires sur une large gamme de produits pour BricoSimplon, un site de e-commerce spécialisé dans le bricolage et l'aménagement de la maison. L'objectif est de surveiller en temps réel les prix pratiqués par Venessens, un concurrent, afin de fournir des insights précieux pour optimiser la stratégie commerciale de BricoSimplon.

---

## ➤ Menu

* [➤ Project Context](#-project-context)
* [➤ Project Structure](#-project-structure)
* [➤ How to Run](#-how-to-run)
* [➤ Outputs](#-outputs)
* [➤ Evaluation Criteria](#-evaluation-criteria)
* [➤ License](#-license)
* [➤ Authors](#-authors)

---

## Project Context

En tant que Data Engineer dans une start-up spécialisée dans la veille concurrentielle, votre mission est de :
- Concevoir un système de scraping respectant les contraintes légales et éthiques.
- Collecter des données tarifaires pour analyser la compétitivité du marché.
- Nettoyer, structurer, et rendre les données exploitables pour BricoSimplon.

---

## Project Structure

- **venessens/**
    - `__init__.py`: Initialisation du module.
    - `items.py`: Définition des items à scraper.
    - `middleware.py`: Configuration des middlewares pour Scrapy.
    - `settings.py`: Paramètres de configuration pour Scrapy.
    - `pipelines.py`: Traitement des données collectées.
    - `runner.py`: Script pour exécuter les spiders.
    - **spiders/**
        - `__init__.py`: Initialisation du module des spiders.
        - `categorie.py`: Spider pour extraire les catégories de produits.
        - `page_produit.py`: Spider pour extraire les détails des produits.
- `scrapy.cfg`: Configuration principale de Scrapy.
- `requirements.txt`: Liste des dépendances Python nécessaires.
- `categories.csv`: Données des catégories exportées.
- `page_produit.csv`: Données des produits exportées.
- `images/`: Contient des images utiles pour le README.

---

## How to Run

1. **Installer les dépendances nécessaires :**
    ```bash
    pip install -r requirements.txt
    ```

2. **Lancer les spiders :**
    - Pour les catégories :
        ```bash
        scrapy crawl categorie -o categories.csv
        ```
    - Pour les produits :
        ```bash
        scrapy crawl page_produit -o page_produit.csv
        ```

---

## Outputs

- Deux fichiers CSV :
    - `categories.csv` : Liste des catégories extraites.
    - `page_produit.csv` : Détails des produits extraits.
- Une base de données contenant des données nettoyées et structurées.

---

## Evaluation Criteria

### Respect des Fonctionnalités Obligatoires :
- Deux items Scrapy correctement créés pour les catégories et les produits.
- Deux spiders fonctionnels.
- Pipeline de traitement des données efficace.
- Exportation des données en fichiers CSV sans erreurs.

### Qualité du Code :
- Code modulaire et structuré.
- Respect des standards PEP 8.
- Docstrings et commentaires explicatifs présents.

### Respect des Bonnes Pratiques de Scraping :
- Limitation des requêtes via `DOWNLOAD_DELAY`.
- Respect des conditions d'utilisation du site cible.
- Identification via `USER_AGENT`.

### Gestion des Données :
- Suppression des doublons grâce à des identifiants uniques.
- Données nettoyées et formatées de manière cohérente.

---

## License

MIT License

Copyright (c) 2024 Sami Kabdani & Khadija Aassi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Authors

- Sami Kabdani  
  [![GitHub Logo](images/github-mark.png)](https://github.com/Sami-Kbdn)

- Khadija Aassi  
  [![GitHub Logo](images/github-mark.png)](https://github.com/Khadaassi)
