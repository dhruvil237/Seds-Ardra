import math

#function for finding coodrinates given the ratio itdivides the line into
def find_coordinates(ratio, x1, y1, x2, y2):
    x = x1 + ratio * (x2 - x1)
    y = y1 + ratio * (y2 - y1)
    return x, y

#function to get ratio in which the point on line segment divides the line segment
def find_ratio(x1, y1, x2, y2, x, y):
    x_diff = x2 - x1
    y_diff = y2 - y1
    x_diff_sq = x_diff * x_diff
    y_diff_sq = y_diff * y_diff
    numerator = x_diff_sq + y_diff_sq
    denominator = (x - x1) * x_diff + (y - y1) * y_diff
    ratio = denominator / numerator
    return ratio


#function to find equation of line given two points
def find_equation(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return m, c

#function to find intersection of two lines
def find_intersection(m1, c1, m2, c2):
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    return x, y


CamX,CamY = 300828, 4956483 
A = 95.1 
pitch = -42.6/180*3.14159 
dir = -163.2/180*3.14159 


Cf = 4.49 
SX = 6.3 
aspect = 0.75 
Sd = SX * math.sqrt(1+aspect**2) 


ratXh = SX/Cf/2 
ratYh = aspect * ratXh 
ccf = math.sqrt(1+ratYh**2) 
phiXh,phiYh = math.atan(ratXh),math.atan(ratYh) 

Kc = A/math.tan(-pitch*phiYh) 
Kf = A/math.tan(-pitch+1*phiYh)
Kb = A/math.tan(-pitch+(-1*phiYh))

Rc = math.sqrt(A**2+Kc**2) 
Rf = math.sqrt(A**2+Kf**2)
Rb = math.sqrt(A**2+Kb**2)
Wch = Rc * ratXh /1 
Wfh = Rf * ratXh / ccf
Wbh = Rb * ratXh / ccf

Centre_W,Centre_K = 0,Kc
BR_K = Kf
BL_K = BR_K
TR_K = Kb
TL_K = TR_K
BL_W = Wfh
BR_W = -BL_W
TL_W = Wbh 
TR_W = -TL_W


Centre_x = CamX + (Centre_W) * math.cos(dir) + (Centre_K) * math.sin(dir)
BR_x = CamX + (BR_W) * math.cos(dir) + (BR_K) * math.sin(dir)
BL_x = CamX + (BL_W) * math.cos(dir) + (BL_K) * math.sin(dir)
TR_x = CamX + (TR_W) * math.cos(dir) + (TR_K) * math.sin(dir)
TL_x = CamX + (TL_W) * math.cos(dir) + (TL_K) * math.sin(dir)
Centre_y = CamY - (Centre_W) * math.sin(dir) + (Centre_K) * math.cos(dir)
BR_y = CamY - (BR_W) * math.sin(dir) + (BR_K) * math.cos(dir)
BL_y = CamY - (BL_W) * math.sin(dir) + (BL_K) * math.cos(dir)
TR_y = CamY - (TR_W) * math.sin(dir) + (TR_K) * math.cos(dir)
TL_y = CamY - (TL_W) * math.sin(dir) + (TL_K) * math.cos(dir)

imagesize = [640,480]
point = [320,240]
ratio_x=find_ratio(imagesize[0],0,0,0,point[0],0)
ratio_y=find_ratio(0,imagesize[1],0,0,0,point[1])


x1,y1=find_coordinates(ratio_x,BL_x,BL_y,BR_x,BR_y)
x2,y2=find_coordinates(ratio_y,BL_x,BL_y,TL_x,TL_y)
x3,y3=find_coordinates(ratio_x,TL_x,TL_y,TR_x,TR_y)
x4,y4=find_coordinates(ratio_y,BR_x,BR_y,TR_x,TR_y)

m1,c1=find_equation(x1,y1,x3,y3)
m2,c2=find_equation(x2,y2,x4,y4)

print(find_intersection(m1,c1,m2,c2))


# print(Centre_x, Centre_y)
# print(BR_x, BR_y)
# print(BL_x, BL_y)
# print(TR_x, TR_y)
# print(TL_x, TL_y)


