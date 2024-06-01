from database.DAO import DAO
from model.model import Model

myModel= Model()
result= myModel._addEdges("France",2015)

print(len(result))

