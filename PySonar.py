# Licensed under the terms of the  GNU GENERAL PUBLIC LICENSE V2.

import time
import pygame as pg
import serial as s
from math import sqrt,sin
from os import chdir
import sys
import json


print ("Imports done...")
#DATA
all_serial = list()
sector1 = (27,171)
sector2 = (207,18)
sector3 = (436,29)
sector4 = (600,197)
sector5 = (589,426)
sector6 = (429,566)
sector7 = (201,570)
sector8 = (26,416)
middle = (319,304)

dis_x = 624

dis_y = 596

all_stuff = [0,0,0,0,0,0]   # This list contains the latest coordinates which have been parsed.

port = "/dev/ttyACM0"    # Put whatever port the arduino has been connected to here

#END_DATA

print("Connecting to Arduino on port: ", port,"......")
try:
	arduino = s.Serial(port,115200)  # Connect to serial port...
except Exception as exception:
	print("Please check and make sure the arduino has been connected on",port)
	sys.exit(1)
print("Connected.")

def int_map(n):
	n = int(n)
	n = n/70*dis_x/2  # Pretty simple, it maps the ping length, to the no. of pixels such that 70 cm (can be adjusted, just change the new max ping length) = 624/2 pixels.
	return n

def parse_serial():
	stuff = arduino.read(20)  # Gets 20 bytes of serial data
	stuff = str(stuff)[2:]    # converts the byte form into a str, gets rid of the b'
	stuff = stuff[:-1]        # and the ' in the end.
	all_serial = all_serial.append(stuff) # Just for the raw log of all input
	stuff = stuff.split("*")  # splits it into seperate pieces, the transfer protocol is like *ping|sector*ping|sector* , so this makes it into a list of ping|sector
	kk = 0
	try:
		while(kk<=len(stuff)):
			if(len(stuff[kk])<5):  # Basically what this thing does is that it checks for incomplete data, and then gets rid of it, the arduino is set to send data pellets exactly 5 chars long,
				del stuff[kk]      # 3 for the ping length, one for the | and one for the sector no.
				kk -= 1
			kk += 1
	except Exception:
		return(stuff)




def main():  
	ds = pg.display.set_mode((dis_x,dis_y))  # Sets up the display.
	pg.display.set_caption("Sonar System-180")  # The caption
	back = pg.image.load("sonar_main_2.jpg")    # Loads the background.
	dot = pg.image.load("sonar_dot.jpg")        # Loads the dots which plot the object positions
	ds.blit(back,(0,0))                         # Blits the background
	while True:
		a = parse_serial()               # Gets a list of the ping lengths + sector in ping|sector format
		s = list()                       # Declare the list s
		for i in a:
			s.append(i.split("|"))       # Now we get a list in which each element is a list containing the ping length and the sector respectively.
		for i in range(len(s)):          # One by one start assigning the each ping len + sector to a x,y coordinate and then putting them in all_stuff
			a = s[i]
			b = get_coords(a[0],a[1])    # gets the coords
		for i in range(len(all_stuff)):  # Now this bit takes the newly parsed and arranged coords in all_stuff and blits 'em
			if(all_stuff[i] == 0):       # If the value is 0, it means that the arduino didn't find any object, so we ignore it.
				pass
			else:
				a = all_stuff[i]
				a = get_coords(a,i)
				ds.blit(dot,a)          # Right here <-----
		for event in pg.event.get():
			if(event.type == pg.QUIT):  # Exit on getting a pygame.EXIT event.....
				with open("raw_serial_out.txt","a") as rsl:
					json.dump(rsl)
				print("Closing.....")
				sys.exit(0)
			elif(event.type == pg.KEYDOWN):  # In case the screen is full of dots and you want to reset, just press c,(NOT C!)
				if(event.key == pg.K_c):
					ds.blit(back,(0,0))      # Resets the background, clears everything.
					for i in range(len(all_stuff)):
						all_stuff[i] = 0     # Resets all_stuff
					pg.display.update()
		pg.display.update()   # Refreshes the display, ESSENTIAL!!

if __name__ == '__main__':
	try:
		main()
	except SystemExit:
		sys.exit(0)
	except Exception as exception:
		sys.exit(1)
