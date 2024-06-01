from database.DB_connect import DBConnect
from model.retailers import Retailers
from model.connessioni import Connessioni


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
    def getAllEdges(paese,anno,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tab1.Retailer_code as Retailer1, tab2.Retailer_code as Retailer2, count(distinct(tab1.Product_number)) as peso
                        from
                        (
                        select gds.Retailer_code, gr.Retailer_name , gds.Product_number, gds.Quantity, gds.Date 
                        from go_daily_sales gds , go_retailers gr 
                        where gds.Retailer_code = gr.Retailer_code 
                        and gr.Country = %s
                        and YEAR(gds.`Date`) = %s
                        ) as tab1,
                        (
                        select gds.Retailer_code, gr.Retailer_name , gds.Product_number, gds.Quantity, gds.Date 
                        from go_daily_sales gds , go_retailers gr 
                        where gds.Retailer_code = gr.Retailer_code 
                        and gr.Country = %s
                        and YEAR(gds.`Date`) = %s
                        )as tab2
                        where tab1.Product_number = tab2.Product_number
                        and tab1.Retailer_code<tab2.Retailer_code
                        group by tab1.Retailer_code, tab2.Retailer_code"""

        cursor.execute(query, (paese,anno,paese,anno))
        # usando la mappa passata possiamo appendere direttamente gli oggetti di tipo retailer
        # conoscendone solo l'identificativo.
        for row in cursor:
            result.append(Connessioni(idMap[row["Retailer1"]], idMap[row["Retailer2"]],row["peso"]))

        cursor.close()
        conn.close()
        return result

