#import statements
import math, sys, pygame, random,pyproj,utm
from pygame import display,draw,event
from pyproj import Proj, transform
import xlwt
import xlrd
from os import listdir
from os.path import isfile, join
import pandas as pd
import csv 
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
import openpyxl

#defining colours
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
BLACK= (   0,   0,  0)

box = (1200, 650)
running = True
ar=[]
wp=[]
di={}
n=0
m=0
ch=-1

win=pygame.display
z=[1200,650]
screen=win.set_mode(z)
def drawCirc(x0,x1,x2,col):
    pygame.draw.circle(screen,col,(x0,x1),x2)
def boundary(st,s,cr1,cr2,cr3,cr4):
    flag=0
    k1=(cr1[1]-st[1])/(s[1]-st[1])
    if(k1>0 and k1<1):
        flag=1
        return flag
    k2=(cr2[0]-st[0])/(s[0]-st[0])
    if(k2>0 and k2<1):
        flag=1
        return flag
    k3=(cr4[1]-st[1])/(s[1]-st[1])
    if(k3>0 and k3<1):
        flag=1
        return flag
    k4=(cr3[0]-st[0])/(s[0]-st[0])
    if(k4>0 and k4<1):
        flag=1
        return flag
    return flag
        
def root(num):
    return math.sqrt(num)
def closest_circ(st,ed):
    ex=st[0]
    ey=st[1]
    dx=ed[0]-st[0]
    dy=ed[1]-st[1]
    a=(dx*dx)+(dy*dy)
    for i in range(0,n):
        zerone=0
        p=ar[i][0]
        q=ar[i][1]
        r=ar[i][2]
        
        b=2*((ex*dx)+(ey*dy)-(dx*p)-(dy*q))
        c=(ex*ex)+(ey*ey)-(2*ex*p)-(2*ey*q)+(p*p)+(q*q)-(r*r)
        dis=(b*b)-(4*a*c)
        if(dis>0):
            s1=(-b + root(dis))/(2*a)
            s2=(-b - root(dis))/(2*a)
            if(0<=s1<=1 and 0<=s2<=1):
                if(s1<s2):
                    sol=s1
                    zerone=1
                else:
                    sol=s2
                    zerone=1
            elif(0<=s1<=1):
                sol=s1
                zerone=1
            elif(0<=s2<=1):
                sol=s2
                zerone=1
        if(zerone==1):
            di[i]=sol
        else:
            di[i]=9999
    val=9999
    pos=0
    count=0
    for i in range(n):
        if(di[i]<val):
            count+=1  
    for i in range(0,n):
        if(di[i]<val):
            val=di[i]
            pos=i
    return pos,count
def draw_tan(st,ed,pos):
    xc=st[0]-ar[pos][0]
    yc=st[1]-ar[pos][1]
    if yc==0:
        yc=0.1
    co=(ar[pos][0]*ar[pos][0])+(ar[pos][1]*ar[pos][1])-(ar[pos][2]*ar[pos][2])-(ar[pos][0]*st[0])-(ar[pos][1]*st[1])
    at=1+((xc/yc)*(xc/yc))
    bt=((2*co*xc)/(yc*yc))-(2*ar[pos][0])+(( 2*ar[pos][1]*xc)/yc)
    ct=((co*co)/(yc*yc))+((2*ar[pos][1]*co)/yc)+(ar[pos][0]*ar[pos][0])+(ar[pos][1]*ar[pos][1])-(ar[pos][2]*ar[pos][2])
    dist=(bt*bt)-(4*at*ct)
    if(dist>0):
        #points on the circle where the tangent meets it are solx1,y1,x2,y2
        solx1=(-bt+root(dist))/(2*at)
        solx2=(-bt-root(dist))/(2*at)
        soly1=-(co+(xc*solx1))/yc
        soly2=-(co+(xc*solx2))/yc
        #gap between tangent to circle
        #extended points above the circle= sdx1,sdx2,sdy1,sdy2
        sdx1=ar[pos][0]+1.1*(solx1-ar[pos][0])
        sdx2=ar[pos][0]+1.1*(solx2-ar[pos][0])
        sdy1=ar[pos][1]+1.1*(soly1-ar[pos][1])
        sdy2=ar[pos][1]+1.1*(soly2-ar[pos][1])
        #distance b/w start point and centre of circle d1,d2 
        d1=root((st[0]-sdx1)*(st[0]-sdx1)+(st[1]-sdy1)*(st[1]-sdy1))
        d2=root((st[0]-sdx2)*(st[0]-sdx2)+(st[1]-sdy2)*(st[1]-sdy2))
        #extension
        #Note:- The ((ar[pos][2]+d1)/d1) is a coefficient for deciding extensions
        sx1=st[0]+((ar[pos][2]+d1)/d1)*(sdx1-st[0])
        sx2=st[0]+((ar[pos][2]+d2)/d2)*(sdx2-st[0])
        sy1=st[1]+((ar[pos][2]+d1)/d1)*(sdy1-st[1])
        sy2=st[1]+((ar[pos][2]+d2)/d2)*(sdy2-st[1])
        pygame.draw.line(screen,BLACK,st,(int(sx1),int(sy1)),1)
        pygame.draw.line(screen,BLACK,st,(int(sx2),int(sy2)),1)
        pygame.draw.line(screen,BLACK,(int(sx1),int(sy1)),ed,1)
        pygame.draw.line(screen,BLACK,(int(sx2),int(sy2)),ed,1)
        pygame.display.update()
        return sx1,sx2,sy1,sy2
def CartLat(A):
    B=[]
    #inputEPSG= 3857
    #outputEPSG=4326
    #point=ogr.Geometry(ogr.wkbPoint)
    #for x in range(len(A)):
    #point.Addpoint(302.22,273.98)
    #inSpatialRef=osr.SpatialReference()
    #inSpatialRef.ImportFromEPSG(inputEPSG)

    #outSpatialRef=osr.SpatialReference()
    #outSpatialRef.ImportFromEPSG(outputEPSG)

    #coordTransform= osr.CoordinateTransformation(inSpatialRef,outSpatialRef)
    #point.Transform(coordTransform)
    
   # print(point.GetX(),point.GetY())
    
    '''inProj=Proj(init='epsg:3857')
    outProj=Proj(init='epsg:4326')
    for x in range(len(A)):
        B.append(transform(inProj,outProj,A[x][0],A[x][1]))
    print(B)'''
    p=pyproj.Proj("+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=6378137 +b=6378137 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
    for x in range(0,len(A)):
       B.append(p(A[x][0],A[x][1],inverse=True))
    return (B)
def LatCart(B):
    C=[]
    crs_wgs = pyproj.Proj(init='epsg:4326') 
    crs_bng = pyproj.Proj(init='epsg:3857')
    for x in range(0,len(B)):
        C.append(pyproj.transform(crs_wgs,crs_bng,B[x][0],B[x][1]))
    return (C)

def sub(st,ed,ar,cor1,cor2,cor3,cor4):
   
    A=[]
    while(1):
                pygame.draw.line(screen,BLACK,st,ed,1)
                pygame.display.update()
                pos,count=closest_circ(st,ed)
                if count==0:
                    pygame.draw.line(screen,RED,st,ed,2)
                    A.append(ed)
                    pygame.display.update()
                    break
                sx1,sx2,sy1,sy2=draw_tan(st,ed,pos)
                s1=(sx1,sy1)
                s2=(sx2,sy2)
                flag1=boundary(st,s1,cor1,cor2,cor3,cor4)
                flag2=boundary(st,s2,cor1,cor2,cor3,cor4)
                if(flag1==1):
                    pygame.draw.line(screen,RED,st,s2,2)
                    st=s2
                    A.append(s2)
                    continue
                elif(flag2==1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    st=s1
                    A.append(s1)
                    continue
                pos1,count1=closest_circ(st,s1)
                pos2,count2=closest_circ(st,s2)
                tsel=0
                if(count1!=0 and count2!=0):
                    if(count1>count2):
                        sub(st,s2,ar)
                        break
                    elif(count2>count1):
                        sub(st,s1,ar)
                        break
                    else:
                        pos3,count3=closest_circ(s1,ed)
                        pos4,count4=closest_circ(s2,ed)
                        if(count3>count4):
                            sub(st,s2,ar)
                            break
                        elif(count4>count3):
                            sub(st,s1,ar)
                            break
                        else:
                            d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                            d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                            if(d1>d2):
                                sub(st,s2,ar)
                                break
                            else:
                                sub(st,s1,ar)
                                break
                elif(count1>count2):
                    pygame.draw.line(screen,RED,st,s2,2)
                    A.append(s2)
                    tsel=1
                    pygame.display.update()
                elif(count2>count1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    A.append(s1)
                    pygame.display.update()
                else:
                    pos3,count3=closest_circ(s1,ed)
                    pos4,count4=closest_circ(s2,ed)
                    if(count3>count4):
                        pygame.draw.line(screen,RED,st,s2,2)
                        A.append(s2)
                        tsel=1
                        pygame.display.update()
                    elif(count4>count3):
                        pygame.draw.line(screen,RED,st,s1,2)
                        A.append(s1)
                        pygame.display.update()
                    else:
                        d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                        d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                        if(d1>d2):
                            pygame.draw.line(screen,RED,st,s2,2)
                            A.append(s2)
                            tsel=1
                            pygame.display.update()
                        else:
                            pygame.draw.line(screen,RED,st,s1,2)
                            A.append(s1)
                            pygame.display.update()
                if(tsel==0):
                    pos,count3=closest_circ(s1,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s1,ed,2)
                        A.append(ed)
                        pygame.display.update()
                        break
                    else:
                        tsel=2
                else:
                    pos,count3=closest_circ(s2,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s2,ed,2)
                        A.append(ed)
                        pygame.display.update()
                        break
                    else:
                        tsel=3
                if(tsel==2):
                    st=s1
                if(tsel==3):
                    st=s2                
def main():
    flag=0
    global running, screen
    global n,m
    A=[]
    B=[]
    C=[]
    pygame.init()
    screen = pygame.display.set_mode(box)
    pygame.display.set_caption("TANGENT_TEST_MOD")
    screen.fill(WHITE)

    #making border of green colour
    cor1=(20,20)
    cor2=(1180,20)
    cor3=(20,630)
    cor4=(1180,630)
    pygame.draw.line(screen,GREEN,cor1,cor2,2)
    pygame.draw.line(screen,GREEN,cor1,cor3,2)
    pygame.draw.line(screen,GREEN,cor3,cor4,2)
    pygame.draw.line(screen,GREEN,cor4,cor2,2)
    pygame.display.update()

    #reading the coordinates of waypoints and obstacles
    file=open("./tan_input.txt","r")
    m=int(file.readline())
    for i in range(0,m):
        p=file.readline()
        imp=tuple(int(x.strip()) for x in p.split(','))
        wp.append(imp)
        drawCirc(wp[i][0],wp[i][1],8,BLUE)
    
    n=int(file.readline())   
    for i in range(0,n):
        p=file.readline()
        inp=tuple(int(x.strip()) for x in p.split(','))
        ar.append(inp)
        drawCirc(ar[i][0],ar[i][1],ar[i][2],BLACK)
    
    pygame.display.update()
    count=0
    st_count=0
    ed_count=1
    
    while running:
        while ed_count<m:
            st=(wp[st_count][0],wp[st_count][1])
            ed=(wp[ed_count][0],wp[ed_count][1])
            while(1):
                pygame.draw.line(screen,BLACK,st,ed,1)          #draws black line directly connecting two waypoints
                pygame.display.update()
                pos,count=closest_circ(st,ed)                   #draws circle around the waypoint
                if count==0:
                    pygame.draw.line(screen,GREEN,st,ed,1)      #draws green line if the waypoint is the last one and breaks the loop
                    A.append(st)
                    pygame.display.update()
                    break
                sx1,sx2,sy1,sy2=draw_tan(st,ed,pos)             #returns the coord of the tangent line
                s1=(sx1,sy1)
                s2=(sx2,sy2)
                flag1=boundary(st,s1,cor1,cor2,cor3,cor4)
                flag2=boundary(st,s2,cor1,cor2,cor3,cor4)
                if(flag1==1):
                    pygame.draw.line(screen,RED,st,s2,2)        #draws the selected path in red line (of two tangents)
                    A.append(s2)
                    st=s2
                    continue
                elif(flag2==1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    A.append(s1)
                    st=s1
                    continue
                pos1,count1=closest_circ(st,s1)
                pos2,count2=closest_circ(st,s2)
                tsel=0
                if(count1!=0 and count2!=0):
                    if(count1>count2):
                        sub(st,s2,ar,cor1,cor2,cor3,cor4)
                        st=s2
                        A.append(s2)
                        continue
                    elif(count2>count1):
                        sub(st,s1,ar,cor1,cor2,cor3,cor4)   
                        st=s1
                        A.append(s1)                
                        continue
                    else:
                        pos3,count3=closest_circ(s1,ed)
                        pos4,count4=closest_circ(s2,ed)
                        if(count3>count4):
                            sub(st,s2,ar,cor1,cor2,cor3,cor4)
                            st=s2
                            A.append(s2)
                            continue
                        elif(count4>count3):
                            sub(st,s1,ar,cor1,cor2,cor3,cor4)
                            st=s1
                            A.append(s1)
                            continue
                        else:
                            d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                            d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                            if(d1>d2):
                                sub(st,s2,ar,cor1,cor2,cor3,cor4)
                                st=s2
                                A.append(s2)
                                continue
                            else:
                                sub(st,s1,ar,cor1,cor2,cor3,cor4)
                                st=s1
                                A.append(s1)
                                continue
             #starts now bend point
                elif(count1>count2):
                    pygame.draw.line(screen,RED,st,s2,2)
                    A.append(s2)
                    tsel=1
                    pygame.display.update()
                elif(count2>count1):
                    pygame.draw.line(screen,RED,st,s1,2)
                    A.append(s1)
                    pygame.display.update()
                else:
                    pos3,count3=closest_circ(s1,ed)
                    pos4,count4=closest_circ(s2,ed)
                    if(count3>count4):
                        pygame.draw.line(screen,RED,st,s2,2)
                        A.append(s2)
                        tsel=1
                        pygame.display.update()
                    elif(count4>count3):
                        pygame.draw.line(screen,RED,st,s1,2)
                        A.append(s1)
                        pygame.display.update()
                    else:
                        d1=((s1[0]-ed[0])*(s1[0]-ed[0]))+((s1[1]-ed[1])*(s1[1]-ed[1]))
                        d2=((s2[0]-ed[0])*(s2[0]-ed[0]))+((s2[1]-ed[1])*(s2[1]-ed[1]))
                        if(d1>d2):
                            pygame.draw.line(screen,RED,st,s2,2)
                            A.append(s2)
                            tsel=1
                            pygame.display.update()
                        else:
                            pygame.draw.line(screen,RED,st,s1,2)
                            A.append(s1)
                            pygame.display.update()
                if(tsel==0):
                    pos,count3=closest_circ(s1,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s1,ed,2)
                        A.append(s1)
                        pygame.display.update()
                        break
                    else: 
                        tsel=2
                else:
                    pos,count3=closest_circ(s2,ed)
                    if(count3==0):
                        pygame.draw.line(screen,RED,s2,ed,2)
                        A.append(s2)
                        pygame.display.update()
                        break
                    else:
                        tsel=3
                if(tsel==2):
                    st=s1
                if(tsel==3):
                    st=s2
            st_count=st_count+1
            ed_count=ed_count+1
        ev = pygame.event.get()
        for event in ev:            
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

    B=[]
    # A= List of all the turn-points.    
    B.extend(CartLat(list(set(A)))) 
    # print(B)
    C.extend(LatCart(B))

    df = pd.read_table('./opp.txt',error_bad_lines=False) 
    df.to_excel('./output.xlsx', 'Sheet2')
    #print("The original excel sheet ka dataframe \n")
    #print(df)
    #print("Ye rahi original excel")
    #senpai=pd.read_excel('C:/SEDS/output.xlsx')
    #print(senpai)
    myworkbook=openpyxl.load_workbook("./output.xlsx")
    worksheet= myworkbook['Sheet2']
    
   
    

    x=2
    for i in range(0, len(B)):
        worksheet['I'+str(x)]=B[i][0]
        worksheet['J'+str(x)]=B[i][1]
        x=x+1

    worksheet['A1']=" "
    worksheet['B1']=" "
    worksheet['C1']=" "
    worksheet['D1']=" "
    worksheet['E1']=" "
    worksheet['F1']=" "
    worksheet['G1']=" "
    worksheet['H1']=" "
    worksheet['I1']=" " 
    worksheet['K1']=" "
    worksheet['L1']=" "  

    print('length of B=',len(B))
    for y in range(7,len(B)+2):
        if((worksheet['I'+str(y)])!=''):
            worksheet['A'+str(y)]=y-1
            worksheet['B'+str(y)]="0"
            worksheet['C'+str(y)]="3"
            worksheet['D'+str(y)]="21"
            worksheet['E'+str(y)]="0"
            worksheet['F'+str(y)]="0"
            worksheet['G'+str(y)]="0"
            worksheet['H'+str(y)]="0"
            worksheet['K'+str(y)]="0"
            worksheet['L'+str(y)]="1"

    
    myworkbook.save("./output.xlsx")
    #Now change the excel file to a text file .
 
    print(pd.__version__) 
    excel = pd.read_excel('./output.xlsx',dtype=object,index_col=0) 
    print("excel ye rahi bc \n",excel)
    excel1=pd.DataFrame(excel)
    print("Printing that dataframe")
    print(excel1,"\n")
    
    excel1.columns=['','','','','','','','','','','']
    excel1=excel1.to_string(na_rep="")
    print(excel1)

    outfile=open('./output.txt','w')
    outfile.write('QGC WPL 110')
    outfile.write(excel1)
    outfile.close()



    from pathlib import Path
    p = Path('./output.txt')
    p.rename(p.with_suffix('.waypoints'))

if __name__ == '__main__':
    main()