from functools import reduce
distances = [
    [(0,123,False),(1,213,False),(2,313,False),(3,123,False),(4,213,False),(5,313,False)],
    [(0,123,False),(1,213,False),(2,313,False),(3,123,False),(4,213,False),(5,313,False)],
    [(0,123,False),(1,213,False),(2,313,False),(3,123,False),(4,213,False),(5,313,False)]
]
assignedIds = []

def getAllIds(distances):
    allIds = []
    for curr in distances:
        allIds.extend(map(lambda tup: tup[0],curr))
    return allIds

def filterFunc(id, assignedIds):
    res = True
    for aId in assignedIds:
        res &= aId != id
    return res

assignedIds = []
for i, distanceArray in enumerate(distances):
    for k, (j, distance, isOwn) in enumerate(distanceArray):
        #se distanza è minore di soglia e non è già assegnato
        if distance < 200 and not any(map(lambda filteredArray: filteredArray[0][2],map(lambda internalArray: list(filter(lambda tupla: tupla[0] == j,internalArray)),distances))):
            print("tupla corrente",distances[i][k])
            distances[i][k] = (distances[i][k][0],distances[i][k][1],True)
            assignedIds.append(j)
            break
print(distances)
uniques = set(getAllIds(distances))
res = filter(filterFunc,uniques)
print("uniques",uniques,"assigned",assignedIds,"new",list(res))


    