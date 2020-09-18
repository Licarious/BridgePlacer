from PIL import Image, ImageDraw, ImageFilter
import math
import time
import copy

class ProvinceDefinition:
    id = 0
    red = 0
    green = 0
    blue = 0
    name = ""
    other_info = ""
    centerX = -1
    centerY = -1
    lastKnownY = -1
    allXY = []
    sumX=0
    sumY=0
    def __init__(self, id):
        self.id
        self.allXY = []

class Adjacency:
    prov1 = 0
    prov2 = 0
    betweenProv = 0
    type = "river_large"
    x1=0
    y1=0
    x2=0
    y2=0
    note=""
    midX = -1
    midY = -1

mapDefinition = open("Input/definition.csv")
adjacencies = open("Input/adjacencies_input.csv")

tmpImage = Image.open("Input/provinces.png")
drawReader = tmpImage.load()

provList = []
adjList = []

mapHight = tmpImage.size[1]

def readProvinceDeff():
    for province in mapDefinition:
        if province.strip().startswith("#"):
            pass
        else:
            tmpline = province.strip().split(';')
            try:
                province = ProvinceDefinition(int(tmpline[0].lstrip("#")))
                province.red = int(tmpline[1])
                province.id = int(tmpline[0].lstrip("#"))
                province.green = int(tmpline[2])
                province.blue = int(tmpline[3])
                province.name = tmpline[4]
                provList.append(province)
            except:
                pass
    pass
def readAdjacencies():
    count = 0
    for line in adjacencies:
        if line.strip().startswith("#"):
            pass
        else:
            tmpline = line.strip().split(';')
            try:
                if int (tmpline[0])>0 and "river" in tmpline[2]:
                    adj = Adjacency()
                    adj.prov1 = int (tmpline[0])
                    adj.prov2 = int (tmpline[1])
                    #adj.type = tmpline[2]
                    adj.betweenProv = int (tmpline[3])
                    #adj.x1 = tmpline[4]
                    #adj.y1 = tmpline[5]
                    #adj.x2 = tmpline[6]
                    #adj.y2 = tmpline[7]
                    adj.note = tmpline[8]
                    adjList.append(adj)
                    count+=1
            except:
                #print(line)
                pass
    print(count)

def getCenterOfWeight(prov):
    allXY = []
    xRange= range(0,tmpImage.size[0],1)
    yRange= range(0,tmpImage.size[1],1)
    sumX=0
    sumY=0
    provinceEnd = False
    for y in yRange:
        if provinceEnd:
            break
        else:
            for x in xRange:
                if drawReader[x,y] == (prov.red, prov.green, prov.blue):
                    allXY.append([x,y])
                    prov.lastKnownY = y
                    prov.allXY.append([x,y])
                    #print("%s - %i,%i"%(prov.name,x,y))
            if prov.lastKnownY > -1 and y > prov.lastKnownY + (tmpImage.size[1] * 1/256):
                provinceEnd = True
    for i in range(0,len(allXY)):
        sumX +=allXY[i][0]
        sumY +=allXY[i][1]
    try:
        prov.centerX = int(sumX/len(allXY))
        prov.centerY = int(sumY/len(allXY))
    except:
        pass
    print("%i , %i"%(prov.centerX,prov.centerY))

def getCenterOfWeight2(tupleList,lastY,tmpProvList):
    allXY = []
    xRange= range(0,tmpImage.size[0],1)
    yRange= range(0,tmpImage.size[1],1)
    sumX=0
    sumY=0
    provinceEnd = False
    internalProvList = copy.copy(tmpProvList)
    count=0

    for y in yRange:
        if y%128==0:
            print("%i%%"%((y*100)/tmpImage.size[1]))
            for i, prov in enumerate(lastY):
                if prov>-1 and prov<y-(tmpImage.size[1]/40):
                    #print(tupleList[i])
                    del lastY[i]
                    del tupleList[i]
                    del tmpProvList[i]
                    i-=1
                    count+=1
        for x in xRange:
            if drawReader[x,y] in tupleList:
                tmpProvList[tupleList.index(drawReader[x,y])].allXY.append([x,y])
                lastY[tupleList.index(drawReader[x,y])] = y
                #print(tmpProvList[tupleList.index(drawReader[x,y])].allXY)
    
        pass
    #print(tmpProvList[0].allXY)
    print(len(internalProvList))
    for prov in internalProvList:
        for i in range(0,len(prov.allXY)):
            prov.sumX +=prov.allXY[i][0]
            prov.sumY +=prov.allXY[i][1]
            #print(i)
        try:
            prov.centerX = int(prov.sumX/len(prov.allXY))
            prov.centerY = int(prov.sumY/len(prov.allXY))
        except:
            pass
        #print("%s\t-\t%i , %i"%(prov.name,prov.centerX,prov.centerY))

def getMidPoint(prov1, prov2, adj):
    #print("%s - %s"%(prov1.name,prov2.name))
    sumX1 = 0
    sumY1 = 0
    sumX2 = 0
    sumY2 = 0

    for i in range(0, len(prov1.allXY)):
        sumX1 += prov1.allXY[i][0]
        sumY1 += prov1.allXY[i][1]
    for i in range(0, len(prov2.allXY)):
        sumX2 += prov2.allXY[i][0]
        sumY2 += prov2.allXY[i][1]

    try:
        sumX1 = int(sumX1/len(prov1.allXY))
        sumY1 = int(sumY1/len(prov1.allXY))
        sumX2 = int(sumX2/len(prov2.allXY))
        sumY2 = int(sumY2/len(prov2.allXY))
    except:
        pass
    dist1 = 999999
    savedCord1 = [sumX1,sumY1]

    for j in prov1.allXY:
        tmpDist = math.sqrt(((sumX2 - j[0])**2 + (sumY2 - j[1])**2))
        if tmpDist <= dist1:
            dist1 = tmpDist
            savedCord1[0] = j[0]
            savedCord1[1] = j[1]
    #print(savedCord1)

    dist2 = 999999
    savedCord2 = [sumX2,sumY2]
    for j in prov2.allXY:
        tmpDist = math.sqrt(((sumX1 - j[0])**2 + (sumY1 - j[1])**2))
        if tmpDist <= dist2:
            dist2 = tmpDist
            savedCord2[0] = j[0]
            savedCord2[1] = j[1]
    #print(savedCord2)

    averageDistance = [ int((savedCord1[0] + savedCord2[0])/2) , int((savedCord1[1] + savedCord2[1])/2)]
    #print(averageDistance)
    adj.midX = averageDistance[0]
    adj.midY = mapHight - averageDistance[1]

def writeBridge():
    bridge = open("Output/bridge_out.txt", "w", encoding='utf-8-sig')
    count = 0
    for adj in adjList:
        count += 1
        foundprovs = 0
        prov1 = 0
        prov2 = 0
        for prov in provList:
            if prov.id == adj.prov1:
                print(prov.name)
                prov1 = prov
                if prov.centerX < 0:
                    getCenterOfWeight(prov)
                foundprovs +=1
            elif prov.id == adj.prov2:
                print(prov.name)
                prov2 = prov
                if prov.centerX < 0:
                    getCenterOfWeight(prov)
                foundprovs +=1
            if foundprovs == 2:
                getMidPoint(prov1, prov2, adj)
                #print(" found all breaking\n")
                print("\n")
                break
        #getCenterOfWeight(adjList[0], prov) #589844
        bridge.write("%i.000000"%adj.midX)
        bridge.write(" 2.000000 ")
        bridge.write("%i.000000"%adj.midY)
        bridge.write(" 0.000000 -0.410844 0.000000 -0.911706 1.000000 1.000000 1.000000\n")
        print(count)
    bridge.close()

def writeBridge2():
    bridge = open("Output/bridge_out.txt", "w", encoding='utf-8-sig')
    count = 0
    tupleList = []
    lastY = []
    tmpProvList = []
    tmpAdjList=[]
    for adj in adjList:
        tmpAdj = []
        prov1F = False
        prov2F = False
        for prov in provList:
            if prov.id == adj.prov1 or prov.id == adj.prov2:
                if not (prov.red,prov.green,prov.blue) in tupleList:
                    tupleList.append((prov.red,prov.green,prov.blue))
                    lastY.append(-1)
                    tmpProvList.append(prov)
                if prov.id == adj.prov1:
                    prov1F = True
                    tmpAdj.append(prov)
                elif prov.id == adj.prov2:
                    prov2F = True
                    tmpAdj.append(prov)
                if prov1F and prov2F:
                    tmpAdj.append(adj)
                    tmpAdjList.append(tmpAdj)
                    break
       
    getCenterOfWeight2(tupleList,lastY,tmpProvList)

    for adj in tmpAdjList:
        getMidPoint(adj[0], adj[1], adj[2])
        bridge.write("%i.000000"%adj[2].midX)
        bridge.write(" 2.000000 ")
        bridge.write("%i.000000"%adj[2].midY)
        bridge.write(" 0.000000 -0.410844 0.000000 -0.911706 1.000000 1.000000 1.000000\n")
    bridge.close()
pass
ts = time.time()
readProvinceDeff()
readAdjacencies()
writeBridge2()
#print(adjList[0].note)
ts2 = time.time()
print("%g Seconds"%(ts2 - ts))