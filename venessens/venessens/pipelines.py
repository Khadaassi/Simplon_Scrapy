import sqlite3

class VenessensPipeline:
    """
    Pipeline pour sauvegarder les données extraites dans une base de données SQLite.
    Gère deux types de données : catégories et produits, selon le spider utilisé.
    """

    def open_spider(self, spider):
        """
        Méthode appelée lorsque le spider est ouvert.
        Initialise la connexion à la base de données et crée les tables si elles n'existent pas.

        Args:
            spider (scrapy.Spider): Le spider en cours d'exécution.
        """
        # Connexion à la base de données SQLite
        self.connection = sqlite3.connect("venessens.db")
        self.cursor = self.connection.cursor()

        # Création de la table pour les catégories si elle n'existe pas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID auto-incrémenté
                nom_categorie TEXT NOT NULL,           -- Nom de la catégorie
                url_categorie TEXT NOT NULL UNIQUE,    -- URL de la catégorie (unique)
                is_page_list BOOLEAN NOT NULL          -- Indique si c'est une page liste
            )
        ''')

        # Création de la table pour les produits si elle n'existe pas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID auto-incrémenté
                nom_categorie TEXT NOT NULL,           -- Nom de la catégorie associée
                nom_produit TEXT NOT NULL,             -- Nom du produit
                prix_produit TEXT,                     -- Prix du produit (peut être NULL)
                reference_produit TEXT,                -- Référence du produit (peut être NULL)
                url_produit TEXT NOT NULL UNIQUE,      -- URL du produit (unique)
                FOREIGN KEY (nom_categorie) REFERENCES categories(nom_categorie)  -- Lien avec la table des catégories
            )
        ''')
        self.connection.commit()  # Sauvegarde des modifications

    def process_item(self, item, spider):
        """
        Méthode pour traiter chaque item extrait par le spider.
        Enregistre les données dans la table appropriée selon le type de spider.

        Args:
            item (dict): L'item extrait par le spider.
            spider (scrapy.Spider): Le spider en cours d'exécution.

        Returns:
            dict: L'item traité, tel qu'il a été reçu.
        """
        if spider.name == "categorie":
            # Insérer ou ignorer les catégories déjà présentes
            self.cursor.execute('''
                INSERT OR IGNORE INTO categories (nom_categorie, url_categorie, is_page_list)
                VALUES (?, ?, ?)
            ''', (
                item['nom_categorie'],  # Nom de la catégorie
                item['url_categorie'],  # URL de la catégorie
                item['is_page_list']    # Indicateur si c'est une page liste
            ))
        elif spider.name == "page_produit":
            # Insérer ou ignorer les produits déjà présents
            self.cursor.execute('''
                INSERT OR IGNORE INTO produits (nom_categorie, nom_produit, prix_produit, reference_produit, url_produit)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                item['nom_categorie'],   # Nom de la catégorie associée
                item['nom_produit'],     # Nom du produit
                item['prix_produit'],    # Prix du produit
                item['reference_produit'],  # Référence du produit
                item['url_produit']      # URL du produit
            ))
        self.connection.commit()  # Sauvegarde des modifications dans la base de données
        return item

    def close_spider(self, spider):
        """
        Méthode appelée lorsque le spider est fermé.
        Ferme la connexion à la base de données SQLite.

        Args:
            spider (scrapy.Spider): Le spider en cours d'exécution.
        """
        self.connection.close()  # Fermeture propre de la connexion
