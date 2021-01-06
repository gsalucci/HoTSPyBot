from TrackableEntity import TrackableEntity,Hero
import cv2
assignedIds = []
def filterFunc(id):
    res = True
    for aId in assignedIds:
        res &= aId != id
    return res

def getAllIds(distances):
    allIds = []
    for curr in distances:
        allIds.extend(map(lambda tup: tup[0],curr))
    return allIds

class EntityManager:
    def __init__(self, trackerType="CSRT"):
        self.colorNames=['blue','red']
        self.colors = {"blue":(255,0,0), "red": (0,0,255)}
        self.trackerTypes = {
            'BOOSTING':"TrackerBoosting_create",
            'MIL':"TrackerMIL_create",
            'KCF':"TrackerKCF_create",
            'TLD':"TrackerTLD_create",
            'MEDIANFLOW':"TrackerMedianFlow_create",
            'GOTURN':"TrackerGOTURN_create",
            'MOSSE':"TrackerMOSSE_create",
            'CSRT':"TrackerCSRT_create"
        }
        self.trackerType = trackerType
        self.entities = dict((cName,[]) for cName in self.colorNames)
        self.maxDistance = 150

    def createAndTrackEntity(self,x,y,w,h,colorName,image):
        # entity = TrackableEntity(x,y,w,h)
        if h >= 8 and h <= 16:
            tracker = getattr(cv2,self.trackerTypes[self.trackerType])()
            entity = Hero(x,y,colorName=colorName)
            entity.color = self.colors[colorName]
            entity.setTracker(tracker,image, (x,y,w,h))
            self.entities[colorName].append(entity)
            return entity

    def updateEntities(self,contours, image, colorName):
        # assignedIds = []
        toPop = []
        #Aggiorno entity esistenti, rimuovo quelle non più visibili
        if len(self.entities[colorName]) > 0:
            distances = []
            for i,entity in enumerate(self.entities[colorName]):
                distances.append([])
                for j,c in enumerate(contours):
                    x,y,w,h = cv2.boundingRect(c)
                    distances[i].append((j,entity.getDistanceFromPoint(x,y), False))
                distances[i].sort(key=lambda tup: tup[1])                
                ok,bbox = entity.updateTracker(image)
                # print(f"bbox: {bbox}")
                if ok:
                    # aggiorna posizione entity con risultato di bbox
                    entity.setPosition(bbox[0],bbox[1])
                else:
                    print(colorName,"tracker error on",i)
                    toPop.append(i)
            if len(toPop) > 0:
                print(colorName,"removing",len(toPop),"entities")
            for i in sorted(toPop,reverse=True):
                self.entities[colorName][i].deleteTracker()
                self.entities[colorName].pop(i)
            # print(colorName,"After",len(self.entities[colorName]))
            #Determino a quali punti ricevuti associare una nuova entity
            for i,distanceArray in enumerate(distances):
                for k, (j, distance, isOwn) in enumerate(distanceArray):
                    #se distanza è minore di soglia e non è già assegnato
                    if distance < self.maxDistance and not any(map(lambda filteredArray: filteredArray[0][2],map(lambda internalArray: list(filter(lambda tupla: tupla[0] == j,internalArray)),distances))):
                        distances[i][k] = (distances[i][k][0],distances[i][k][1],True)
                        assignedIds.append(j)
                        break
            #determino nuovi punti
            uniques = set(getAllIds(distances))
            unassignedContours = list(filter(filterFunc,uniques))
            for i in unassignedContours:
                x,y,w,h = cv2.boundingRect(contours[i])
                self.createAndTrackEntity(x,y,w,h,colorName,image)
            return self.entities[colorName]
        else:
            for c in contours:
                x,y,w,h = cv2.boundingRect(c)
                self.createAndTrackEntity(x,y,w,h,colorName,image)
            return self.entities[colorName]
                        