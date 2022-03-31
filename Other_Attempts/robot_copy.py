#key codes foud here https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
#right click to start and stop drawing/ mouse monitoring
from types import DynamicClassAttribute
import pyautogui as pg
import pygame
import win32api
import time
import math
import csv
import os
import sys

def main():

    drawing = [] #where data will go
    app_open = False #if paint app open or closed
    drawing_available = False #start with no drawing present
    headers = ["x_pos", "y_pos", "Magnitudue", "Radians", "Degrees", "Dx", "Dy"]

    #Commands to automatically open/close paint to draw
    command_1 = "cd C:\Windows\System32" #navigate to paint
    command_2 = "start mspaint.exe" #start paint
    command_3 = "taskkill /im mspaint.exe /t /f"# close paint

    #create directory with you name choosing, chane working directory to that folder
    folder_name = input('name the folder:')
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print("Directory " , folder_name ,  " Created ")
    else:
        print("Directory " , folder_name ,  " already exists, quitting")
        sys.exit()
    os.chdir(folder_name)

    #try:
    while True:
        spacebar = win32api.GetKeyState(0x20) #check for space bar clicked, quit function if thats the case
        left_click = win32api.GetKeyState(0x01)
        if not(app_open): #open paint if its not open
            os.system(command_1)
            os.system(command_2)
            app_open = True
        if left_click < 0:
            #if left click, start recording
            x,y = pg.position()
            #mcord = pygame.mouse.get_pos()
            #x = mcord[0]
            #y = mcord[1]
            drawing.append([x,y])
            time.sleep(.001)
            drawing_available = True
        elif (drawing_available== True):   #let go of left click and drawing available, stop recording
            i= 0
            #add magnitude of vector movement and angle
            for index, cordinates in enumerate(drawing):
                if index - 1 >= 0:
                    dy = (cordinates[1]-drawing[index-1][1])
                    dx = (cordinates[0]-drawing[index-1][0])
                    #magnitude of vector formula
                    mag = math.sqrt((dx ** 2) + (dy ** 2))
                    angle_rad = math.atan2(-dy, dx)
                    angle_deg = math.degrees(angle_rad)
                else:
                    mag = 0 # if first element, no magnitude
                    angle_deg = 0
                    angle_rad = 0
                    dx = 0
                    dy = 0
                cordinates.append(mag)
                cordinates.append(angle_rad)
                cordinates.append(angle_deg)
                cordinates.append(dx)
                cordinates.append(dy)
            #add headers to csv
            drawing.insert(0, headers)
            while os.path.exists(str(folder_name) + "_%s.csv" % i): #if the file already exists name it with incrementing number
                i += 1
            with open(str(folder_name) + "_%s.csv" % i, "w", newline ='') as f:
                wr = csv.writer(f)
                wr.writerows(drawing)
                print("file saved as " + str(folder_name) + "_%s.csv" % i)
            os.system(command_3)
            drawing = [] #where data will go
            app_open = False #if paint app open or closed
            drawing_available = False #start with no drawing present
        if spacebar < 0:
            os.system(command_3)
            break
    print("exiting")
    #except:
     #  print("failed unintentianlly")

if __name__ == "__main__":
    main()
