from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        #è sempre meglio crearsi una mappa con tutti i retailer per lavorare più
        #agilmente con gli oggetti (chiave--> retailer_code
        #                           valore--> Oggetto Retailer).
        #in tutte le funzioni dove servono dei retailers bisogna passare anche la mappa
        #per poter immagazzinare direttamente gli oggetto nei risultati
        self._retailers= DAO.getAllRetailers()
        self._idMap= {}
        for retailer in self._retailers:
            self._idMap[retailer.Retailer_code] = retailer
        #creo il grafo vuoto
        self._grafo = nx.Graph()
        #creo le variabili per la ricorsione
        self._bestPath = []
        self._bestObjFun = 0

    def getCountry(self):
        return DAO.getAllNations()

    def creaGrafo(self,anno, paese):
        #creare i nodi (come variabili di classe)
        self._nodes=DAO.getNodes(paese, self._idMap)
        #aggiungere i nodi al grafo
        self._grafo.add_nodes_from(self._nodes)
        #creare gli archi
        #aggiungere gli archi al grafo
        #questi ultimi due punti li facciamo in una funzione ad hoc
        self._addEdges(paese,anno)

    def _addEdges(self, paese ,anno):
        #implementiamo la richiesta relativa agli edges
        allConnessioni= DAO.getAllEdges(paese, anno,self._idMap)
        for c in allConnessioni:
            if c.Retailer1 in self._grafo and c.Retailer2 in self._grafo:
                self._grafo.add_edge(c.Retailer1, c.Retailer2, weight=c.peso)

    def volumi(self):
        '''
         1. controllo i vicini del primo nodo e sommo i pesi dei loro archi
         2. mi salvo tale variabile in una dizionario con retailer e volume di vendita
         3. ripeto quest'operazione per tutti i nodi del grafo
         4. stampo a video il nome del retailer --> volume di vendita
        '''
        result=[] #lista che faccio diventare lista di tuple
        for v in self._grafo:
            vicini= self._grafo.neighbors(v)
            volume = 0
            tupla=()
            for w in vicini:
                volume += self._grafo[v][w]["weight"]
            tupla= v, volume
            result.append(tupla)
            result.sort(key=lambda tupla: tupla[1], reverse=True)
        return result


    #helper function
    def printGraphDetails(self):
        print(f"Num nodi: {len(self._grafo.nodes)}")
        print(f"Num archi: {len(self._grafo.edges)}")

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)



