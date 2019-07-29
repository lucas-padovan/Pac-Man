
import sys
sys.path.append('../')
import threading
import time
import math

from RobotActionThread import *
from HamsterAPI.comm_ble import RobotComm

import Tkinter as tk



class GUI(object):
	def __init__(self, gui_root, robot_actions):
		self.gui_root = gui_root
		self.canvas = None
		self.robot_actions = robot_actions
		self.lines = []
		
		self.pac_man = None
		self.pac_man_x = 112
		self.pac_man_y = 112	

		self.pac_balls = []
		self.pac_balls_coord = []		

		self.initUI()
		self.gui_root.bind('<KeyPress>', self.keydown)

		
		return


	def rectangle(self, coordx, coordy): #top left
		self.canvas.create_rectangle(coordx, coordy, coordx+25, coordy+25,outline="green",fill='black')
		return

	def keydown(self, event):
		if(event.char == 'w'):
			self.move_up()
			#print("w")
		elif(event.char == 'a'): 
			self.move_left()
			#print("a")
		elif(event.char == 's'): 
			self.move_down()
			#print("s")
		elif(event.char == 'd'): 
			self.move_right()
		self.detect_colision()

	def move_up(self):
		authorization = self.authorize_movement(self.pac_man_x, self.pac_man_y - 10, 'up')
		if(authorization):
			self.pac_man_y = self.pac_man_y - 10
			self.canvas.move(self.pac_man,0, -10) 
		return

	def move_left(self):
		authorization = self.authorize_movement(self.pac_man_x - 10, self.pac_man_y, 'left')
		if(authorization):
			self.pac_man_x = self.pac_man_x - 10
			self.canvas.move(self.pac_man,-10, 0)  
		return

	def move_down(self): 
		authorization = self.authorize_movement(self.pac_man_x, self.pac_man_y + 10, 'down')
		if(authorization):
			self.pac_man_y = self.pac_man_y + 10
			self.canvas.move(self.pac_man,0, 10)  
		return

	def move_right(self): 
		authorization = self.authorize_movement(self.pac_man_x + 10, self.pac_man_y, 'right')
		if(authorization):
			self.pac_man_x = self.pac_man_x + 10
			self.canvas.move(self.pac_man,10, 0)
		return

	def line(self, x1, y1, x2, y2):
		self.canvas.create_line(x1, y1, x2, y2, fill='blue')
		self.lines.append([x1, y1, x2, y2])

	def authorize_movement(self, x1, y1, type):
		res = False

		for line in self.lines:
			l_x1 = line[0]
			l_y1 = line[1]
			l_x2 = line[2]
			l_y2 = line[3]


			if(l_x1 >= x1 and x1 >= l_x2 and l_y1 >= y1 and y1 >= l_y2):
				res = True
				break
			elif(l_x2 >= x1 and x1 >= l_x1 and l_y2 >= y1 and y1 >= l_y1):
				res = True
				break

		return res
	
	def detect_colision(self):
		for i in range(0, len(self.pac_balls_coord)):

			coord = self.pac_balls_coord[i]

			print type(coord)
			coordx = coord[0]
			coordy = coord[1]
			x = self.pac_man_x
			y = self.pac_man_y

			dis = math.sqrt((x-coordx) * (x-coordx) + (y-coordy) * (y-coordy))

			print dis

			if(dis < 10):
				self.pac_balls_coord.pop(i)
				self.canvas.delete(self.pac_balls[i])
				self.pac_balls.pop(i)



	def draw_grid(self):
		self.rectangle(100, 100)
		self.rectangle(125, 100)
		self.rectangle(150, 100)
		self.rectangle(175, 100)
		self.rectangle(200, 100)

		self.rectangle(100, 100)
		self.rectangle(100, 125)
		self.rectangle(100, 150)
		self.rectangle(100, 175)
		self.rectangle(100, 200)

		self.rectangle(200, 100)
		self.rectangle(200, 125)
		self.rectangle(200, 150)
		self.rectangle(200, 175)
		self.rectangle(200, 200)

		self.rectangle(100, 200)
		self.rectangle(125, 200)
		self.rectangle(150, 200)
		self.rectangle(175, 200)
		self.rectangle(200, 200)

		self.rectangle(100, 150)
		self.rectangle(125, 150)
		self.rectangle(150, 150)
		self.rectangle(175, 150)
		self.rectangle(200, 150)

		self.rectangle(150, 100)
		self.rectangle(150, 125)
		self.rectangle(150, 150)
		self.rectangle(150, 175)
		self.rectangle(150, 200)

		self.line(112, 112, 212, 112)
		self.line(112, 112, 112, 212)
		self.line(212, 112, 212, 212)
		self.line(112, 212, 212, 212)
		self.line(112, 162, 212, 162)
		self.line(162, 112, 162, 212)

		self.pac_balls.append(self.canvas.create_oval(162-6, 162-8,162+6,162+8, fill="white"))
		coords = [162,162]
		self.pac_balls_coord.append(coords)
		#print self.pac_balls_coord
		#ball2 = self.canvas.create_oval(112-12, 112-12,112+12,112+12, fill="white")
		#ball3 = self.canvas.create_oval(112-12, 112-12,112+12,112+12, fill="white")

		return


	def initUI(self):
		self.canvas = tk.Canvas(self.gui_root, bg='red', width=1000, height=500)
		self.canvas.pack()

		button_go = tk.Button(self.gui_root, text='GO')
		button_go.pack(side='left')
		button_go.bind('<Button-1>', self.start_robot)


		button_exit = tk.Button(self.gui_root, text='EXIT')
		button_exit.pack(side='right')
		button_exit.bind('<Button-1>', self.stop_robot)

	



		self.draw_grid()

		self.pac_man = self.canvas.create_oval(112-12, 112-12,112+12,112+12, fill="yellow")
		return

	def start_robot(self, event=None):
		self.robot_actions.go = True
		return

	def stop_robot(self, event=None):
		self.robot_actions.stop = True
		self.gui_root.quit()	
		return


def main():
	
	maxRobotNum = 1
	print 'debug 1'
	comm = RobotComm(maxRobotNum)
	print 'debug 2'
	comm.start()
	print 'debug 3'
	robotList = comm.robotList

	action = RobotActionThread(robotList)
	print 'debug 4'
	action.start()
	print 'debug 5'

	root = tk.Tk()

	root.geometry('1000x500')

	gui = GUI(root, action)

	action.line_limit = gui.lines

	root.mainloop()


	comm.stop()
	comm.join()

	return

if __name__ == "__main__":
	sys.exit(main())