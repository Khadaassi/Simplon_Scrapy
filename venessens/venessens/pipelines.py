from venessens.items import CategorieItem, ProduitItem
from itemadapter import ItemAdapter
import sqlite3

class ProduitPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("venessens.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Produits(
                            nom_categorie VARCHAR(50),
                            nom_produit VARCHAR(100),
                            prix_produit VARCHAR(20),
                            reference_produit VARCHAR(50) PRIMARY KEY,
                            url_produit VARCHAR(255)
                            ) """)

    def process_item(self, item, spider):
        if isinstance(item, ProduitItem):  # Vérification du type d'item
            self.cursor.execute("""INSERT OR IGNORE INTO Produits 
                                VALUES (?,?,?,?,?)
                                """,
                                (item['nom_categorie'], item['nom_produit'], item['prix_produit'], 
                                 item['reference_produit'], item['url_produit']))
            self.connection.commit()
            return item
        else:
            return item  # Passe l'item au prochain pipeline

    def close_spider(self, spider):
        self.connection.close()


class CategoriesPipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.connect("venessens.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Categories(
                            nom_categorie VARCHAR(100) PRIMARY KEY,
                            url_categorie VARCHAR(500),
                            is_page_list BOOLEAN
                            ) """)

    def process_item(self, item, spider):
        if isinstance(item, CategorieItem):
            spider.logger.info(f"Processing CategorieItem: {item}")
            self.cursor.execute("""INSERT OR IGNORE INTO Categories 
                                VALUES (?,?,?)
                                """,
                                (item['nom_categorie'], item['url_categorie'], item['is_page_list']))
            self.connection.commit()
        return item


    def close_spider(self, spider):
        self.connection.close()
