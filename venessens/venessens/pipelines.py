import sqlite3
from venessens.items import CategorieItem, ProduitItem
from itemadapter import ItemAdapter


# class VenessensPipeline:
#     def process_item(self, item, spider):
#         return item

# class DataBasePipeline :
#     def open_spider(self):
#         self.connection = sqlite3.connect("venessens.db")
#         self.cursor = self.connection.cursor()
#         self.create_table()

#     def create_table(self) :
#         self.cursor.execute("""CREATE TABLE IF NOT EXISTS Produits(
#                             reference_produit INT PRIMARY KEY,
#                             nom_categorie VARCHAR(50),
#                             nom_produit VARCHAR(100),
#                             prix_produit VARCHAR(20),
#                             url_produit VARCHAR(255)
#                             ) """)
#     def process_item(self, item):
#         self.cursor.execute("""INSERT INTO Produits 
#                             VALUES (?,?,?,?,?)
#                             """,
#                             (item['nom_categorie'], item['nom_produit'], item['prix_produit'], item['reference_produit'], item['url_produit']))
        

#         self.connection.commit()
#         return item
    
#     def close_spider(self):
#         self.connection.close()
                            
    
                    

                            # prix_produit DECIMAL(10, 2),
                            # devise_produit VARCHAR(10),
                            # unite_produit VARCHAR(10),


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
        self.cursor.execute("""INSERT INTO Produits 
                            VALUES (?,?,?,?,?)
                            """,
                            (item['nom_categorie'], item['nom_produit'], item['prix_produit'], item['reference_produit'], item['url_produit']))
        

        self.connection.commit()
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
        self.cursor.execute("""INSERT INTO Categories 
                            VALUES (?,?,?)
                            """,
                            (item['nom_categorie'], item['url_categorie'], item['is_page_list']))
        

        self.connection.commit()
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
