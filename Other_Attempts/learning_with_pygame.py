
from types import DynamicClassAttribute
import pygame
import time
import math
import csv
import os
import sys
import json


drawing = [] #where data will go
list_of_actions = []# what is getting stored for json
json_dict =[] #list of list of actions for each charter
app_open = False #if paint app open or closed
drawing_available = False #start with no drawing present
last_pos = None #initially no last position
headers = ["x_pos", "y_pos", "Magnitudue", "Radians", "Degrees", "Dx", "Dy", "Length Change", "Total dist Traveled", "percent traveled","accurate angle"]
running = True
last_angle = None # use to check if gone more than 365 degrees in angle calc
over_365 = False #check if gone more than 365 deg
num_over =0 #number of times over 365

def len_change(dx, dy):
    mag = math.sqrt((dx) ** 2 + (dy) ** 2)
    return(mag)
def angle_calc(dy, dx):
    global last_angle
    global over_365
    global num_over
    angle_rad = math.atan2((-dy), dx)
    if angle_rad < 0:
        angle_rad += 2*3.14159
    angle_deg = math.degrees(angle_rad)
    if last_angle == None:  
        last_angle = angle_deg
        return(angle_deg)
        # if angles passes 360 lin from bottom to top, add 365 to angle
    elif (last_angle - angle_deg) > 200:
        num_over += 1
        last_angle = angle_deg
        angle_deg += 365*num_over
        over_365 = True
        return(angle_deg)
    elif over_365:
        last_angle = angle_deg
        angle_deg += 365*num_over
        return(angle_deg)
    last_angle = angle_deg
    return(angle_deg)

#create directory with you name choosing, chane working directory to that folder
folder_name = input('name the folder:')
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
    print("Directory " , folder_name ,  " Created ")
else:
    print("Directory " , folder_name ,  " already exists, quitting")
    sys.exit()
os.chdir(folder_name)

pygame.init()
pygame.display.set_caption('Surgery Learning')
def reset_screen():
    # Fill the background with white
    screen.fill((255, 255, 255))
    # draw surgery box
    pygame.draw.rect(screen, (0, 0, 0), (150, 0, 700 - 150, 500), width=1)
    # draw mimic box
    pygame.draw.rect(screen, (0, 0, 0), (700, 0, 700 - 150, 500), width=1)
    #draw joystick box
    pygame.draw.rect(screen, (0, 0, 255), (0, 500-150, 150, 150), width=1)
    # draw joystick circle
    pygame.draw.circle(screen, (255, 0, 0), (75, 500 - 75), 70)
    pygame.display.flip()
screen = pygame.display.set_mode([700+550, 500])
reset_screen()

#Define tuple mouse clicks
LEFT = 1
left_click = False

#Clock
clock = pygame.time.Clock()
time_since_last_run = 0
pygame.display.flip()

while running:  
    dt = clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            json_dictionary = {}
            json_dictionary[folder_name] = json_dict
            with open ("actions.json","w") as fp:
                json.dump(json_dictionary, fp)
            print("actions.json data file saved")
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            left_click = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            left_click = False
            last_pos = None
        if event.type == pygame.MOUSEMOTION:
            mcord = pygame.mouse.get_pos()
            if left_click == True:
                if (150 < mcord[0] < 700 and 0 < mcord[1] < 500):
                    ##Live Surgeon Position
                    if last_pos == None:
                        last_pos = mcord
                    pygame.draw.circle(screen, (0, 0, 0), mcord, 2)
                    pygame.draw.line(screen, (0,0,0), last_pos, mcord, 4)
                    last_pos = mcord
                    x = mcord[0]
                    y = mcord[1]
                    drawing.append([x,y])
                    time.sleep(.001)
                    drawing_available = True  
    if (drawing_available== True) and (left_click == False):   #let go of left click and drawing available, stop recording    
        i= 0
        #add magnitude of vector movement and angle
        for index, cordinates in enumerate(drawing):
            if index - 1 >= 0:
                dy = (cordinates[1]-drawing[index-1][1])
                dx = (cordinates[0]-drawing[index-1][0])
                #magnitude of vector formula
                mag = math.sqrt((dx ** 2) + (dy ** 2))
                angle_rad = math.atan2((-dy), dx)
                angle_deg = math.degrees(angle_rad)
                length_change = len_change(dx,dy)
                tot_traveled += length_change
            else:
                mag = 0 # if first element, no magnitude
                angle_deg = 0
                angle_rad = 0
                dx = 0
                dy = 0
                length_change = 0
                tot_traveled = 0
            cordinates.append(mag)
            cordinates.append(angle_rad)
            cordinates.append(angle_deg)
            cordinates.append(dx)
            cordinates.append(dy)
            cordinates.append(length_change)
            cordinates.append(tot_traveled)
            list_of_actions.append([mag,angle_rad])
        #set min distance traveled to check angle
        for index, cordinates in enumerate(drawing):
            int_distance_cells = 1
            pix_traveled = 0
            pixel_min_traveled_check = 20
            x_start = drawing[index][0]
            y_start = drawing[index][1]
            percent_goal = drawing[index][-1]/tot_traveled
            drawing[index].append(percent_goal)

            #add accurate angle based on minimum pixels traveled
            while pix_traveled < pixel_min_traveled_check:
                #exit check if reached last cell
                try:
                    a =drawing[index+int_distance_cells][-1] 
                except:
                    break
                pix_traveled += drawing[index+int_distance_cells][-2]
                x_finish = drawing[index+int_distance_cells][0]
                y_finish = drawing[index+int_distance_cells][1]
                int_distance_cells +=1
            #middle_cell = int(round(int_distance_cells/2))
            ddx =  x_finish - x_start
            ddy =  y_finish - y_start
            ac_angle_deg = angle_calc(ddy, ddx)
            drawing[index].append(ac_angle_deg)
            
        #add headers to csv
        drawing.insert(0, headers)

        #iterate file saving with numbers
        while os.path.exists(str(folder_name) + "_%s.csv" % i): #if the file already exists name it with incrementing number
            i += 1
        with open(str(folder_name) + "_%s.csv" % i, "w", newline ='') as f:
            wr = csv.writer(f)
            wr.writerows(drawing)
            print("file saved as " + str(folder_name) + "_%s.csv" % i)
        drawing = [] #where data will go
        app_open = False #if paint app open or closed
        drawing_available = False #start with no drawing present
        reset_screen()
        #add to database file, list of actions
        json_dict.append(list_of_actions)
        list_of_actions = []
        #redeclare angles
        last_angle = None # use to check if gone more than 365 degrees in angle calc
        over_365 = False #check if gone more than 365 deg
        num_over =0 #number of times over 365
    pygame.draw.circle(screen, (255, 0, 0), (75, 500-75), 70)
    pygame.display.flip()
print("exiting")
pygame.quit()



