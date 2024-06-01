from database.DAO import DAO
from model.model import Model

myModel= Model()


retailer= myModel.creaGrafo(0,"Italy")
for ret in retailer:
    print(f"{ret}")