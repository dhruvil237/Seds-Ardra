import geopy
from geopy import distance
import math
# from t3 import getCircleIntersections

def euclidDist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**.5

def get_intersections(c1, r0, c2, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1
    x0=c1[0]
    y0=c1[1]
    x1=c2[0]
    y1=c2[1]
    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3),(x4, y4)

# latLong=[(-35.363278,149.165239),
latLong=[(-35.36502830,149.16232110),
(-35.36166860,149.15730000),
(-35.35883370,149.16229960),
(-35.35997120,149.16916610),
(-35.36352350,149.16807170)]

cartesianPts=[(0,0),(distance.distance(latLong[0],latLong[1]).meters,0)]

r1=distance.distance(latLong[0],latLong[2]).meters
r2=distance.distance(latLong[1],latLong[2]).meters

p1,p2=get_intersections(cartesianPts[0],r1,cartesianPts[1],r2)

if p1[1]>0:
    cartesianPts.append(p1)
else:
    cartesianPts.append(p2)

for i in cartesianPts:
    print(i)
print("-------------------------------------------")

for i in range(3,len(latLong)):
    r1=distance.distance(latLong[0],latLong[i]).meters
    r2=distance.distance(latLong[1],latLong[i]).meters
    r3=distance.distance(latLong[2],latLong[i]).meters
    # print("-----------------------------------------")
    print(r1,r2,r3)
    p1,p2=get_intersections(cartesianPts[0],r1,cartesianPts[1],r2)
    # print("-----------------------------------------")
    print(p1,p2)
    # print("-----------------------------------------")
    if euclidDist(p1,cartesianPts[2])-r3 < euclidDist(p2,cartesianPts[2])-r3:
        cartesianPts.append(p1)
    else:
        cartesianPts.append(p2)
    print(euclidDist(p1,cartesianPts[2])-r3,euclidDist(p2,cartesianPts[2])-r3)
    print("-------------------------------------------")
    print("-------------------------------------------")
    print("-------------------------------------------")

    # print(distance.distance(latLong[i],latLong[i+1]).meters)

for i in cartesianPts:
    print(i)