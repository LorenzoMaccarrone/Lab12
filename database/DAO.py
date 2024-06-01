from database.DB_connect import DBConnect
from model.retailers import Retailers


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            result.append(Retailers(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNations():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct (gr.Country) 
                    from go_retailers gr"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(paese, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from go_retailers gr 
                    where gr.Country = %s"""

        cursor.execute(query, (paese,))
        #usando la mappa passata possiamo appendere direttamente gli oggetti di tipo retailer
        #conoscendone solo l'identificativo.
        for row in cursor:
            result.append(idMap[row["Retailer_code"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """"""

        cursor.execute(query, (anno,))
        # usando la mappa passata possiamo appendere direttamente gli oggetti di tipo retailer
        # conoscendone solo l'identificativo.
        for row in cursor:
            result.append(idMap[row["Retailer_code"]])

        cursor.close()
        conn.close()
        return result

