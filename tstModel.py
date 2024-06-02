from database.DAO import DAO
from model.model import Model

myModel= Model()
myModel.creaGrafo(2015,"France")
result= myModel.volumi()

for r in result:
    print(f"{r[0]} --> {r[1]}")

