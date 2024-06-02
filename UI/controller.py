import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        nations=self._model.getCountry()
        for n in nations:
            self._view.ddcountry.options.append(ft.dropdown.Option(n))
        for i in range(2015,2019):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))
        self._view.update_page()

    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare anno")
            return #questi return vanno messi altrimenti il programma
                   # continua a girare anche senza aver inserito il valore
        if self._view.ddcountry.value is None:
            self._view.create_alert("Selezionare paese ( Country )")
            return #questi return vanno messi altrimenti il programma
                   # continua a girare anche senza aver inserito il valore

        self._model.creaGrafo(self._view.ddyear.value,self._view.ddcountry.value)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumNodi()} vertici"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumArchi()} archi"))
        #disabilito i DD e il bottone crea grafo coì che l'utente non possa fare danni selezinoando un altro
        #paese e un altro anno senza rilanciare l'applicazione
        #DA CONTROLLARE se fosse questa l'interpretazione, cioè se l'utente volesse calcolare per un'altra combinazione
        #paese anno deve rilanciare l'applicazione giusto?
        self._view.ddyear.disabled= True
        self._view.ddcountry.disabled= True
        self._view.btn_graph.disabled = True
        self._view.update_page()


    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        volumi=self._model.volumi()
        for r in volumi:
            self._view.txtOut2.controls.append(ft.Text(f"{r[0]} --> {r[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        nMinStr=self._view.txtN.value
        try:
            nMinInt=int(nMinStr)
        except ValueError:
            self._view.create_alert("Il valore inserito NON è intero")
            self._view.update_page()
            return #questi return vanno messi altrimenti il programma
                   # continua a girare anche senza aver inserito il valore

        if nMinInt<2:
            self._view.create_alert("Inserire valore maggiore di 2")
            self._view.update_page()
            return #questi return vanno messi altrimenti il programma
                   # continua a girare anche senza aver inserito il valore

        path,pesoMax= self._model.getCammino(nMinInt)
