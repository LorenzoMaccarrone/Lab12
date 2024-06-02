import copy

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

    def getCammino(self, n):
        self._bestPath = []
        self._bestObjFun = 0
        #dobbiamo trovare il cammino a peso massimo provando a partire da ogni nodo del grafo!!!
        for v0 in self._nodes:
            self._nodoPartenza=v0
            parziale = [v0]
            self._ricorsione(parziale, n)
        return self._bestPath, self._bestObjFun

    def _ricorsione(self, parziale, n):
        #controlliamo se siamo in una soluzione ammissibile
        #se voglio due archi potrò al massimo esplorare 3 nodi
        #quindi il numero di nodi ammissibili è il numero di archi+1
        if len(parziale) == n+1:
            return
        #controlliamo se questa nuova soluzione è migliore delle altre e se verifica la condizione
        #tale per cui è una soluzinoe valida ovvero il nodo di arrivo è uguale a quello di partenza
        #la soluzione migliore è una soluzione in cui viene rispettata la condizione finale
        #altrimenti non è una soluzione interessante e non c'è la salviamo
        if self.getObjFun(parziale) > self._bestObjFun and parziale[-1] == self._nodoPartenza:
            self._bestObjFun = self.getObjFun(parziale)
            self._bestPath = copy.deepcopy(parziale)

        #continuo la ricorsione cercando il vicino di peso massimo
        listaVicinoPeso=[]
        tuplaVicinoPeso=()
        for i in self._grafo.neighbors(parziale[-1]):
            tuplaVicinoPeso=i, self._grafo[parziale[-1]][i]["weight"]
            listaVicinoPeso.append(tuplaVicinoPeso)
        #prendendo tutti i nodi rischiamo di prendere nodi non connessi!!
        #dobbiamo tenere conto di questa condizione:
        if len(listaVicinoPeso)==0:
            return
        else:
            listaVicinoPeso.sort(key=lambda tuplaVicinoPeso:tuplaVicinoPeso[1], reverse=True)
            #dobbiamo mettere la condizione per cui non cicla su nodi già presenti nel path!

            for tupla in listaVicinoPeso:
                if tupla not in parziale:
                    parziale.append(tupla[0])
                    break


            #a questo punto ho aggiunto il nodo che mi interessa alla ricorsione quindi
            #richiamo la ricorsione con il nuo parziale
            self._ricorsione(parziale,n)
            #facciamo backtracking
            parziale.pop()

    #con questa funzione calcolo il peso del percorso
    def getObjFun(self, listOfNodes):
        objVal = 0
        for i in range(0, len(listOfNodes)-1):
            objVal += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]

        return objVal


    #helper function
    def printGraphDetails(self):
        print(f"Num nodi: {len(self._grafo.nodes)}")
        print(f"Num archi: {len(self._grafo.edges)}")

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)



