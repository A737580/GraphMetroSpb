from termcolor import colored

adjSheet = dict()       #{str():list(set())}
stationList = list()    #все станции метро по порядку
forkStationDict = dict()
setStationList = list() #множество станций текущей ветки 
curStationList = list() #переменная содержащая станции текущей ветки
curStr = str() 
curList = []
i,j = 0,1

#Этап 1
f = open(r"../SaintPMetro.xlsx", "r")
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



# Этап 2


copyAdjSheet=adjSheet.copy()
for forkItm in forkStationDict.items():
    for forkSttn in forkItm[1]:
        adjSheet[forkItm[0]]=copyAdjSheet[forkItm[0]].union(copyAdjSheet[forkSttn])
        adjSheet[forkItm[0]].difference_update({forkItm[0]})

# for pair in adjSheet.items():
#     print(pair[0]+"<--------",end="")
#     print(pair[1])

#матрица смежности
lenMatr = len(stationList)
adjMatrixMetro =[[0] * lenMatr for _ in range(lenMatr)]

for i in range(lenMatr):
    for j in range(lenMatr):
        for iterSetSttn in adjSheet[stationList[i]]:
            if(stationList[j]==iterSetSttn):
                adjMatrixMetro[i][j]=1
                break
        
for i in range(lenMatr):
    for j in range(lenMatr):
        if(adjMatrixMetro[i][j]==0):
            print(colored(adjMatrixMetro[i][j],'red'), sep='',end='')
        else:
            print(colored(adjMatrixMetro[i][j],'green'), sep='',end='')
    print()