import sqlite3

class VenessensPipeline:
    def open_spider(self, spider):
        # Connexion à la base de données SQLite
        self.connection = sqlite3.connect("venessens.db")
        self.cursor = self.connection.cursor()

        # Création des tables si elles n'existent pas encore
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_categorie TEXT NOT NULL,
                url_categorie TEXT NOT NULL UNIQUE,
                is_page_list BOOLEAN NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_categorie TEXT NOT NULL,
                nom_produit TEXT NOT NULL,
                prix_produit TEXT,
                reference_produit TEXT,
                url_produit TEXT NOT NULL UNIQUE,
                FOREIGN KEY (nom_categorie) REFERENCES categories(nom_categorie)
            )
        ''')
        self.connection.commit()

    def process_item(self, item, spider):
        if spider.name == "categorie":
            # Insertion ou mise à jour des catégories
            self.cursor.execute('''
                INSERT OR IGNORE INTO categories (nom_categorie, url_categorie, is_page_list)
                VALUES (?, ?, ?)
            ''', (
                item['nom_categorie'],
                item['url_categorie'],
                item['is_page_list']
            ))
        elif spider.name == "page_produit":
            # Insertion ou mise à jour des produits
            self.cursor.execute('''
                INSERT OR IGNORE INTO produits (nom_categorie, nom_produit, prix_produit, reference_produit, url_produit)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                item['nom_categorie'],
                item['nom_produit'],
                item['prix_produit'],
                item['reference_produit'],
                item['url_produit']
            ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        # Fermeture de la connexion à la base de données
        self.connection.close()
