from termcolor import colored
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


adjSheet = dict()       #{str():list(set())}
stationList = list()    #все станции метро по порядку
forkStationDict = dict()
setStationList = list() #множество станций текущей ветки 
curStationList = list() #переменная содержащая станции текущей ветки
curStr = str() 
curList = []
i,j = 0,1

#Этап 1
f = open(r"./Files/SaintPMetro.xlsx", "r")
f.readline()
f.readline()
while True:
    temp=0
    curStr = f.readline()
    curList = curStr.replace('\n','').split('\t')
    if(curStr=="\n"):
        for st in range(len(curStationList)):
            adjSheet[curStationList[st]]=setStationList[st]
        i=0
        j+=1
        curStationList.clear()
        setStationList.clear()
        continue
    elif(curStr==""): 
        for st in range(len(curStationList)):
            adjSheet[curStationList[st]]=setStationList[st]
        curStationList.clear()
        setStationList.clear()    
        break
    elif(i==0):
        setStationList.append(set())
        setStationList.append(set())
        for elm in curList:
            if(elm!="" and curList.index(elm)!=j-1):
                setStationList[i].add(elm)
            elif(elm!="" and curList.index(elm)==j-1):
                stationList.append(elm)
                curStationList.append(elm)
            if(elm!=""):
                temp+=1
                setStationList[i+1].add(elm)
        if(temp>1):forkStationDict[curStationList[-1]]=list(filter(lambda x: x!=""and x!=curStationList[-1], curList))
    elif(i!=0):
        setStationList.append(set())
        for elm in curList:
            if(elm!=""and curList.index(elm)!=j-1):
                setStationList[i].add(elm)
            elif(elm!="" and curList.index(elm)==j-1):
                stationList.append(elm)
                curStationList.append(elm)
            if(elm!=""):
                temp+=1
                setStationList[i-1].add(elm)
                setStationList[i+1].add(elm)
        if(temp>1):forkStationDict[curStationList[-1]]=list(filter(lambda x: x!=""and x!=curStationList[-1], curList))
    i+=1
f.close()



# Этап 2 добавляю недостающие связи

copyAdjSheet2=adjSheet.copy()
copyAdjSheet=adjSheet.copy()
for forkItm in forkStationDict.items():
    for forkSttn in forkItm[1]:
        adjSheet[forkItm[0]]=copyAdjSheet[forkItm[0]].union(copyAdjSheet[forkSttn])
        adjSheet[forkItm[0]].difference_update({forkItm[0]})

# for pair in adjSheet.items():
#     print(pair[0]+"<--------",end="")
#     print(pair[1])
# print()

#заполнение матрицы смежности
lenMatr = len(stationList)
adjMatrixMetro =[[0] * lenMatr for _ in range(lenMatr)]

for i in range(lenMatr):
    for j in range(lenMatr):
        for iterSetSttn in adjSheet[stationList[i]]:
            if(stationList[j]==iterSetSttn):
                adjMatrixMetro[i][j]=1
                break



#вывод матрицы        
# for i in range(lenMatr):
#     print(str(i+1).ljust(2),end=') ')
#     for j in range(lenMatr):
#         if(adjMatrixMetro[i][j]==0):
#             print(colored(adjMatrixMetro[i][j],'red'), sep='',end='')
#         else:
#             print(colored(adjMatrixMetro[i][j],'green'), sep='',end='')
#     print()




# print('Введите число и получите станцию: ')
# while True:
#     b = int(input())
#     if(b==-1):
#         for i in range(lenMatr):
#             print(str(i).ljust(2),end=') ')
#             for j in range(lenMatr):
#                 if(adjMatrixMetro[i][j]==0):
#                     print(colored(adjMatrixMetro[i][j],'red'), sep='',end='')
#                 else:
#                     print(colored(adjMatrixMetro[i][j],'green'), sep='',end='')
#             print()
#         continue
#     elif(b==-2):
#         break
#     print(stationList[b])


G = nx.from_numpy_array(np.array(adjMatrixMetro))




mapping = dict()
 
for i in range(len(stationList)): # создаем список замены номер станции - ее название
    mapping[i]=stationList[i]


# объединяем станции перехода, сокращая граф
for curStation in forkStationDict.keys():
    numCurStation = stationList.index(curStation)
    forkSttions = list(filter(lambda x:  x in forkStationDict.keys(), forkStationDict[curStation]))
    for st in forkSttions:
        numSt = stationList.index(st) 
        if(numCurStation in G): 
            mapping[numCurStation]=mapping[numCurStation]+"\n"+stationList[numSt] #дополняем список замены. Станциями перехода на узле
            for numStationGraph in G[numSt]:
                if(numCurStation!=numStationGraph and not stationList[numStationGraph] in forkSttions):
                    G.add_edge(numCurStation,numStationGraph)
            G.remove_node(numSt)

            

#раскрашиваем граф
colorMap = []
for node in G:
    if stationList[node] in forkStationDict.keys():
        colorMap.append("grey")
    elif node<=18:
        colorMap.append("red")
    elif 19<=node<=36:
        colorMap.append("blue")    
    elif 37<=node<=48:
        colorMap.append("green")
    elif 49<=node<=58:
        colorMap.append("yellow")
    elif 59<=node<=73:
        colorMap.append("purple")


# переименовываем граф
G = nx.relabel_nodes(G, mapping)
#выводим граф

# выводим матрицу смежности для готового графа
# A = nx.adjacency_matrix(G, nodelist=None, dtype=None, weight="weight")
# for i in A.toarray():
#     print(*i,sep="")

nx.draw_spring(G,node_color=colorMap,with_labels=True,alpha= 0.6, node_size=1000)
plt.show() 





