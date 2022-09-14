import pygame
import sys
import random
import math

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 700))

# colours
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

obs=[[184, 296, 83], [243, 553, 42], [358, 287, 54], [363, 411, 32], [265, 438, 58], [372, 600, 70], [494, 551, 39], [684, 232, 36], [618, 359, 49], [665, 576, 51], [116, 148, 60]]

inwayObs=[[116, 148, 60, 181.02486017119307], [358, 287, 54, 272.0340882158825], [665, 576, 51, 419.903290146232]]

WP = [[5, 5, 's'], [148.52357916894326, 97.57959938634471, 'c'], [156.7531155333266, 103.9638378792214, 'l'], [314.45958747428296, 318.9410782080127, 'c'], [324.92792789670386, 329.6876802695382, 'l'], [630.2885977135892, 613.3646698274046, 'c'], [643.5921235934427, 622.2893381650847, 'l'], [790, 690, 'f']]
while True:
    screen.fill(white)
    for event in pygame.event.get():
        # Allowing program to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    for i in range(len(WP)):
        pygame.draw.circle(screen,blue,WP[i][0:2],2)
        if WP[i][-1]=='l' or WP[i][-1]=='s':
            pygame.draw.line(screen,black,WP[i][0:2],WP[i+1][0:2])
            
    for i in inwayObs:
        pygame.draw.circle(screen,green,i[0:2],i[2])
        pygame.draw.circle(screen,blue,i[0:2],i[2]-5)
    pygame.display.update()
    clock.tick(3)

    

