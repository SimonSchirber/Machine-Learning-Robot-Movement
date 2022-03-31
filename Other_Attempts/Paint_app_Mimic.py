## info at https://pyautogui.readthedocs.io/en/latest/quickstart.html
# Cordinates are 0, 0 at top left corner of the screen, on this computer 3256, 2400
## paint application at 2521, 2350
## red paint at 2666, 406
import pyautogui as pg
import pickle
import time
from tkinter import *
from tkinter import filedialog
import os
import subprocess
import sys

def move_and_click (x, y, duration):
    pg.moveTo(x,y,dur) # move mouse to x, y,  in duration (seconds)
    pg.click(x,y) #click cordinate

size = pg.size() # list size of screen
x_tot = size[0] #x dimension
y_tot = size[1] #y dimension screen

#Cordinates in Paint
pencil_x = 569 #pencil location to draw in paint
pencil_y = 171
size_menu_x = 1514 #select dropdown width menu of pencil
size_menu_y = 193
large_size_x = 1503 #select large width pencil
large_size_y = 614
paint_black_x = 1829 #black color location (full screen)
paint_black_y = 142

dur = .5 #time in seconds to make movements

def open_file():
    my_file = filedialog.askopenfilename()
    return my_file

file_to_draw = open_file()
print("got file")
with open(file_to_draw, "rb") as new_filename:
    simon_painting = pickle.load(new_filename)


command_1 = "cd C:\Windows\System32" #navigate to paint
command_2 = "start mspaint.exe" #start paint
os.system(command_1)
os.system(command_2)
move_and_click(pencil_x, pencil_y, dur) #click on pencil
move_and_click(paint_black_x, paint_black_y, dur) #Click on black paint
move_and_click(size_menu_x, size_menu_y, dur)
move_and_click(large_size_x, large_size_y, dur)

try:
    start = simon_painting[0]
    pg.moveTo(start[0], start[1], dur) #move to start of painting
    for cord in simon_painting:
        pg.dragTo(cord[0], cord[1])
except KeyboardInterrupt: #when delete or ctrl +c hit exit drawing
    sys.exit(1)


# on_screen = pg.onScreen(current_position) #return true if cordinates are on the screen
# pg.moveRel(x_rel, y_rel, dur) #move xcordinate relative to screen

print("finished")


