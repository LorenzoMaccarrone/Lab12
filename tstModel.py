from database.DAO import DAO
from model.model import Model

myModel= Model()
myModel.creaGrafo(2016,"Germany")
path,pesoMax=myModel.getCammino(5)
print(pesoMax)
for i in path:
    print(i)

