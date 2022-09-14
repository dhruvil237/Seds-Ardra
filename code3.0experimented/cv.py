import cv2 
import random
import numpy as np
import math
# from t3 import * 

#function to find equation of line from two points
def eqOfLine(p1,p2):
    m=(p2[1]-p1[1])/(p2[0]-p1[0])
    c=p1[1]-m*p1[0]
    return m,c

#function to find distance between two points
def distance(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

#function to find foot of perpendicular
def footOfPerpendicular(m,c,x,y):
    return (x-c)/m,y

#function to find angle between two lines from slopes of lines
def angle(m1,m2):
    if m1==m2:
        return 0
    elif m1==0:
        return 90
    elif m2==0:
        return 90
    else:
        return math.degrees(math.atan(abs(m1-m2)/(1+m1*m2)))

#function to find if line intersects circle given line, circle, and foot of perpendicular
def lineInCircle(p1,p2,c):
    x1,y1=p1
    x2,y2=p2
    x,y=c
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    if d==c[2]:
        return True
    elif d>c[2]:
        return False
    else:
        m=(y2-y1)/(x2-x1)
        c=y1-m*x1
        x3=(c-c[2]**2/d)/(m**2+1)
        y3=m*x3+c
        if x3>=x and x3<=x2:
            return True
        else:
            return False

#function to check circle overlapping
def circleOverlapping(c1,c2):
    d=math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    if d<c1[2]+c2[2]:
        return True
    else:
        return False

#function to get the points of intersections of two circles
def getCircleIntersections(c1,c2):
    x1,y1=c1
    x2,y2=c2
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    if d==c1[2]+c2[2]:
        return (x1,y1),(x2,y2)
    elif d>c1[2]+c2[2]:
        return None
    else:
        m=(y2-y1)/(x2-x1)
        c=y1-m*x1
        x3=(c-c1[2]**2/d)/(m**2+1)
        y3=m*x3+c
        x4=(c-c2[2]**2/d)/(m**2+1)
        y4=m*x4+c
        return (x3,y3),(x4,y4)

#function to find points of tangency from a point to a circle
def getTangentPoints(p,c):
    x,y=p
    x1,y1=c
    d=math.sqrt((x-x1)**2+(y-y1)**2)
    if d==c[2]:
        return (x1,y1)
    elif d>c[2]:
        return None
    else:
        m=(y-y1)/(x-x1)
        c=y-m*x
        x2=(c-c[2]**2/d)/(m**2+1)
        y2=m*x2+c
        return (x2,y2)

#function to return internal if a point divides a line formed by two points internally or else returns external
def intOrExtDiv(p1,p2,p):
    m,c=eqOfLine(p1,p2)
    x,y=p
    x1,y1=p1
    x2,y2=p2
    if m==0:
        if x==x1:
            return "external"
        else:
            return "internal"
    else:
        x3,y3=footOfPerpendicular(m,c,x,y)
        if x3>=x1 and x3<=x2:
            return "internal"
        else:
            return "external"

def checkMultipleCircles(circle,obstacles):
    for i in obstacles:
        if circle!=i and circleOverlapping(circle,i):
            return "m"
    return "s"

image=np.zeros(shape=(700,700,3))
image=np.uint8(image)

obs=[]


phaltu=0
for i in range(15):
    while True:
        x=random.randint(100,700)
        y=random.randint(100,600)
        r=random.randint(20,75)
        numColl=0
        for j in obs:
            if circleOverlapping(c1=[x,y,r],c2=j):
                numColl+=1
                if numColl>phaltu:
                    break
        if numColl<phaltu+1:
            break
    cv2.circle(img=image,center=(x,y),radius=r,color=(0,0,255),thickness=1)
    obs.append([x,y,r])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

wayPoints=[]

for i in range(5):
    while True:
        if random.randint(0,100)>50:
            x=random.randint(10,100)
        else:
            x=random.randint(600,690)
        if random.randint(0,100)>50:
            y=random.randint(10,100)
        else:
            y=random.randint(600,690)
        numColl=0
        for j in obs:
            if circleOverlapping(c1=[x,y,5],c2=j):
                numColl+=1
                break
        for j in wayPoints:
            if circleOverlapping(c1=[x,y,5],c2=[j[0],j[1],5]):
                numColl+=1
                break
        if numColl==0:
            break
    cv2.circle(img=image,center=(x,y),radius=2,color=(0,255,0),thickness=-1)
    wayPoints.append([x,y])

for i in range(0,4):
    cv2.line(img=image,pt1=wayPoints[i],pt2=wayPoints[i+1],color=(255,255,255),thickness=1)



for i in contours:
    numCirc=0
    for j in obs:
        if cv2.pointPolygonTest(i, j[:2], False)==1:
            numCirc+=1
        if numCirc>=2:
            rect = cv2.minAreaRect(i)
            box = cv2.boxPoints(rect)
            # print(box)
            box = np.int0(box)
            cv2.drawContours(image,[box],0,(255,0,255),1)
            break


curPt=wayPoints[0]
nextPt=wayPoints[1]

temp=np.array(image)

while 1:
    for wp in wayPoints:
            print(wp)
    for i in wayPoints:
        cv2.circle(img=temp,center=(int(i[0]),int(i[1])),radius=2,color=(0,255,0),thickness=-1)

    for i in range(0,len(wayPoints)-1):
        cv2.line(img=temp,pt1=(int(wayPoints[i][0]),int(wayPoints[i][1])),pt2=(int(wayPoints[i+1][0]),int(wayPoints[i+1][1])),color=(0,255,255),thickness=1)

    for i in obs:
        cv2.circle(img=temp,center=(i[0],i[1]),radius=i[2]-10,color=(255,0,255),thickness=1)
        cv2.circle(img=temp,center=(i[0],i[1]),radius=i[2]-15,color=(0,255,255),thickness=1)
    cv2.imshow("frame",temp)
    cv2.waitKey()
    temp=np.array(image)

    print("Curpt:",curPt,"Nextpt:",nextPt)
    l=eqOfLine(curPt,nextPt)

    # Check for obstacles in the way
    bObs=[]
    for i in obs:
            p=footOfPerpendicular(l[0],l[1],i[0],i[1])
            if lineInCircle(l,i,p):
                if intOrExtDiv(curPt,nextPt,p)=="internal" and round(p[0],3)!=round(nextPt[0],3) and round(p[1],3)!=round(nextPt[1],3):
                    bObs.append([i[0],i[1],i[2],distance(i[0:2],curPt)])
        
    if len(bObs)>0:
        # We sort as per distance of obstacles
        bObs.sort(key=lambda x:x[-1])
        closestObs=bObs[0]
        if checkMultipleCircles(closestObs,obs)=='s':
            tangentPoint1,tangentPoint2=getTangentPoints(curPt,closestObs)
            l1=eqOfLine(curPt,tangentPoint1)
            l2=eqOfLine(curPt,tangentPoint2)
            if angle(l1[0],l[0])<=angle(l2[0],l[0]):
                temp=[tangentPoint1]
            else:
                temp=[tangentPoint2]

            a,b=getTangentPoints(nextPt,closestObs)

            if distance(a,temp[0])>=distance(b,temp[0]):
                targetPoint=b
            else:
                targetPoint=a

            maxChordLength=2*(10*(2*closestObs[-1]-10))**0.5
            ctr2=0
            while True:
                tempL=eqOfLine(temp[ctr2],nextPt)
                tempFOP=footOfPerpendicular(tempL,closestObs[0:2])
                if distance(closestObs[0:2],tempFOP)>closestObs[-1]-10:
                    break
                else:
                    if distance(temp[ctr2],targetPoint)<=maxChordLength:
                        temp.append(targetPoint)
                        break
                    else:
                        tempC=[temp[ctr2][0],temp[ctr2][1],maxChordLength]
                        a,b=getCircleIntersections(tempC,closestObs)
                        if distance(a,targetPoint)<=distance(b,targetPoint):
                            temp.append(a)
                        else:
                            temp.append(b)
                        ctr2+=1
            ind=wayPoints.index(curPt)
            for j in range(len(temp)):
                wayPoints.insert(ind+j+1,temp[j])
            curPt=wayPoints[ind+j+1]
            nextPt=wayPoints[ind+j+2]
        else:
            for c in contours:
                if cv2.pointPolygonTest(c, closestObs[:2], False)==1:
                    break
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box=box.tolist()
            print(box)
            d1=None
            p1=None
            p2=None
            d2=None
            for i in box:
                if d1!=None:
                    if distance(i,curPt)<d1:
                        p1=i
                else:
                    p1=i
                if d2!=None:
                    if distance(i,nextPt)<d2:
                        p2=i
                else:
                    p2=i
            indP1=box.index(p1)
            indP2=box.index(p2)
            if indP1==indP2:
                ind=wayPoints.index(curPt)
                wayPoints.insert(ind+1,p1)
                curPt=nextPt
                nextPt=wayPoints[ind+3]

            elif abs(indP1-indP2)==2:
                ind=wayPoints.index(curPt)
                wayPoints.insert(ind+1,p1)
                wayPoints.insert(ind+2,box[(indP1+1)%4])
                wayPoints.insert(ind+3,box[(indP1+2)%4])
                curPt=nextPt
                nextPt=wayPoints[ind+5]
            else:
                ind=wayPoints.index(curPt)
                wayPoints.insert(ind+1,p1)
                wayPoints.insert(ind+2,p2)
                curPt=nextPt
                nextPt=wayPoints[ind+4]
            
    else:
        curPt=nextPt
        if curPt==wayPoints[-1]:
            break
        nextPt=wayPoints[wayPoints.index(nextPt)+1]

for i in wayPoints:
    cv2.circle(img=image,center=(int(i[0]),int(i[1])),radius=2,color=(0,255,0),thickness=-1)

for i in range(0,len(wayPoints)-1):
    cv2.line(img=image,pt1=(int(wayPoints[i][0]),int(wayPoints[i][1])),pt2=(int(wayPoints[i+1][0]),int(wayPoints[i+1][1])),color=(0,255,255),thickness=1)

for i in obs:
    cv2.circle(img=image,center=(i[0],i[1]),radius=i[2]-10,color=(255,0,255),thickness=1)
    cv2.circle(img=image,center=(i[0],i[1]),radius=i[2]-15,color=(0,255,255),thickness=1)

cv2.imshow("frame",image)
cv2.waitKey()
cv2.destroyAllWindows()