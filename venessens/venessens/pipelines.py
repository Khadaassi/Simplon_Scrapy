import sqlite3
from venessens.items import CategorieItem, ProduitItem
from itemadapter import ItemAdapter
import sqlite3

class DataBasePipeline :
    def open_spider(self, spider):
        self.connection = sqlite3.connect("venessens.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Produits(
                            nom_categorie VARCHAR(50),
                            nom_produit VARCHAR(100),
                            prix_produit VARCHAR(20),
                            reference_produit INT PRIMARY KEY,
                            url_produit VARCHAR(255)
                            ) """)
        
    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT OR IGNORE INTO Produits 
                                (nom_categorie, nom_produit, prix_produit, reference_produit, url_produit) 
                                VALUES (?, ?, ?, ?, ?)""",
                                (item['nom_categorie'], item['nom_produit'], item['prix_produit'], 
                                item['reference_produit'], item['url_produit']))
            self.connection.commit()
        except sqlite3.Error as e:
            spider.logger.error(f"Erreur lors de l'insertion dans Produits : {e}")
        return item
    
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
        try:
            self.cursor.execute("""INSERT OR IGNORE INTO Categories 
                                (nom_categorie, url_categorie, is_page_list) 
                                VALUES (?, ?, ?)""",
                                (item['nom_categorie'], item['url_categorie'], item['is_page_list']))
            self.connection.commit()
        except sqlite3.Error as e:
            spider.logger.error(f"Erreur lors de l'insertion dans Categories : {e}")
        return item


    def close_spider(self, spider):
        self.connection.close()


# class DataBasePipeline:
#     def open_spider(self, spider):
#         self.connection = sqlite3.connect("venessens.db")
#         self.cursor = self.connection.cursor()
#         self.cursor.execute("""CREATE TABLE IF NOT EXISTS Produits(
#                             nom_categorie VARCHAR(50),
#                             nom_produit VARCHAR(100),
#                             prix_produit VARCHAR(20),
#                             reference_produit INT PRIMARY KEY,
#                             url_produit VARCHAR(255)
#                             )""")
        
#     def process_item(self, item, spider):
#         try:
#             self.cursor.execute("""INSERT INTO Produits 
#                                 (nom_categorie, nom_produit, prix_produit, reference_produit, url_produit)
#                                 VALUES (?,?,?,?,?)""",
#                                 (item['nom_categorie'], item['nom_produit'], item['prix_produit'], item['reference_produit'], item['url_produit']))
#             self.connection.commit()
#         except sqlite3.IntegrityError:  # Gérer les doublons si nécessaire
#             spider.logger.warning(f"Duplicate product with reference {item['reference_produit']}, skipping...")
#         return item
    
#     def close_spider(self, spider):
#         self.connection.close()
