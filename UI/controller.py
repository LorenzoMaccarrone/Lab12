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
        if self._view.ddcountry.value is None:
            self._view.create_alert("Selezionare paese ( Country )")

        self._model.creaGrafo(self._view.ddyear.value,self._view.ddcountry.value)




    def handle_volume(self, e):
        pass


    def handle_path(self, e):
        pass
