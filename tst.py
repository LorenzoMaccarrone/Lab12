tuplaAcqua= ("acqua", 1)
tuplaBirra= ("birra", 4)
tuplaAranciata= ("Aranciata", 3)
tuplaCocacola= ("cocacola", 2)

listaProdotti=[]
listaProdotti.append(tuplaAcqua)
listaProdotti.append(tuplaAranciata)
listaProdotti.append(tuplaBirra)
listaProdotti.append(tuplaCocacola)
listaProdotti.sort(key=lambda tupla: tupla[1], reverse=True)
print(listaProdotti[0][0])
