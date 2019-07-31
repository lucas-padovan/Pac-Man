
import sys
sys.path.append('../')
import threading
import time
import math

from RobotActionThread import *
from PacMan import *
from Ghost import *
from HamsterAPI.comm_ble import RobotComm

import Tkinter as tk



class GUI(object):
	def __init__(self, gui_root, pac_actions):
		self.gui_root = gui_root
		self.canvas = tk.Canvas(self.gui_root, bg='red', width=1000, height=500)
		self.canvas.pack()

		self.pac_actions = pac_actions
		self.lines = []
			

		self.n_pac_balls = 3
		self.pac_balls = []
		self.pac_balls_coord = []		

		self.initUI()
		self.gui_root.bind('<KeyPress>', self.keydown)

		self.PacMan = PacMan(self.canvas, self.lines, self.n_pac_balls, self.pac_balls, self.pac_balls_coord)

		self.Ghost = Ghost(self.canvas, self.lines, 212, 162)

		self.PacMan.start()

		
		return



	def rectangle(self, coordx, coordy): #top left
		self.canvas.create_rectangle(coordx, coordy, coordx+25, coordy+25,outline="green",fill='black')
		return

	def SetPacManMovement(self, key):

		pacman = self.PacMan

		ableToMove = False

		x = pacman.pac_man_x
		y = self.PacMan.pac_man_y

		auth_up = pacman.authorize_movement(x, y-3, 'up')
		auth_down = pacman.authorize_movement(x, y+3, 'down')
		auth_right = pacman.authorize_movement(x+3, y, 'right')
		auth_left = pacman.authorize_movement(x-3, y, 'left')

		if(pacman.orientation == 'up'):
			if(key == 'w' and auth_up):
				self.PacMan.orientation = 'up'
				self.PacMan.movements = 'up'
				ableToMove = True
			elif(key == 'a'and auth_left):  #all right
				#self.PacMan.movements = 'left'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'left'
				ableToMove = True
			elif(key == 'd' and auth_right):
				#self.PacMan.movements = 'right'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'right'
				ableToMove = True

		elif(pacman.orientation == 'down'):
			if(key == 'w' and auth_down):
				self.PacMan.movements = 'down'
				self.PacMan.orientation = 'down'
				ableToMove = True
			elif(key == 'a' and auth_right):
				#self.PacMan.movements = 'right'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'right'
				ableToMove = True
			elif(key == 'd'and auth_left):
				#self.PacMan.movements = 'left'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'left'
				ableToMove = True

		elif(pacman.orientation == 'left'):
			if(key == 'w'and auth_left):
				self.PacMan.movements = 'left'
				self.PacMan.orientation = 'left'
				ableToMove = True
			elif(key == 'a'and auth_down):
				#self.PacMan.movements = 'down'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'down'
				ableToMove = True
			elif(key == 'd'and auth_up):
				#self.PacMan.movements = 'up'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'up'
				ableToMove = True

		elif(pacman.orientation == 'right'):
			if(key == 'w'and auth_right):
				self.PacMan.movements = 'right'
				self.PacMan.orientation = 'right'
				ableToMove = True
			elif(key == 'd'and auth_down):
				#self.PacMan.movements = 'down'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'down'
				ableToMove = True
			elif(key == 'a'and auth_up):
				#self.PacMan.movements = 'up'
				self.PacMan.movements = ''
				self.PacMan.orientation = 'up'
				ableToMove = True
		return ableToMove



	def keydown(self, event):
		#self.checkGame()
		if(event.char == 'w'):
			#self.PacMan.movements = 'forward'
			permission = self.SetPacManMovement('w') 
			if permission: 
				self.pac_actions.movements.put('forward')
			#print("w")
		elif(event.char == 'a'): 
			#self.PacMan.move_left()
			#self.PacMan.movements = 'left' 
			permission = self.SetPacManMovement('a') 
			if permission: 
				self.pac_actions.movements.put('left')
			#print("a")
		elif(event.char == 'd'): 
			permission = self.SetPacManMovement('d') 
			if permission: 
				self.pac_actions.movements.put('right')
		#self.detect_colision()

	def line(self, x1, y1, x2, y2):
		self.canvas.create_line(x1, y1, x2, y2, fill='blue')
		self.lines.append([x1, y1, x2, y2])

	
	'''def detect_colision(self):
		for i in range(0, len(self.pac_balls_coord)):
			print self.n_pac_balls

			coord = self.pac_balls_coord[i]

			
			coordx = coord[0]
			coordy = coord[1]

			if(coordx != -1 and coordy != -1):
				x = self.PacMan.pac_man_x
				y = self.PacMan.pac_man_y

				dis = math.sqrt((x-coordx) * (x-coordx) + (y-coordy) * (y-coordy))


				if(dis < 10):
					
					self.canvas.delete(self.pac_balls[i])
					self.pac_balls_coord[i][0] = -1
					self.pac_balls_coord[i][1] = -1
					self.n_pac_balls = self.n_pac_balls - 1''' 


	def pac_ball(self, x, y):
		self.pac_balls.append(self.canvas.create_oval(x-6, y-8,x+6,y+8, fill="white"))
		coords = [x,y]
		self.pac_balls_coord.append(coords)


	def draw_grid(self):
		'''self.rectangle(100, 100)
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
		self.rectangle(150, 200) '''

		start = 100
		end = 325
		increment = 25
 
		for i in range(start,end,increment):
		    if(i != 200):
		        self.rectangle(i,100)
 
 
		self.rectangle(100,125)
		self.rectangle(175,125)
		self.rectangle(225,125)
		self.rectangle(300,125)
 
 
 
 
		for i in range(start,end,increment):
		    if not (i==125 or i==275):
		        self.rectangle(i,150)
 
 
 
 
		self.rectangle(100, 175)
		self.rectangle(150, 175)
		self.rectangle(250, 175)
		self.rectangle(300, 175)
 
		for i in range(start, end, increment):
			self.rectangle(i,200)
 
		self.rectangle(100, 225)
		self.rectangle(150, 225)
		self.rectangle(250, 225)
		self.rectangle(300, 225)

		for i in range(start,end,increment):
			if not (i==125 or i==275):
				self.rectangle(i,250)

				self.rectangle(100,275)
				self.rectangle(175,275)
				self.rectangle(225,275)
				self.rectangle(300,275)


		for i in range(start,end,increment):
			if(i != 200):
				self.rectangle(i,300)

			self.line(112, 112, 187, 112)
			self.line(237, 112, 312, 112)

			self.line(112, 312, 187, 312)
			self.line(237, 312, 312, 312)


			self.line(112, 112, 112, 312)
			self.line(312, 112, 312, 312)



			self.line(112, 212, 312, 212)
 
 
 
		self.line(187, 112, 187, 162)
		self.line(237, 112, 237, 162)
		self.line(162, 162, 262, 162)


		self.line(187, 262, 187, 312)
		self.line(237, 262, 237, 312)
		self.line(162, 262, 262, 262)
 
 
		self.line(162, 162, 162, 262)
		self.line(262, 162, 262, 262)

		self.pac_ball(162, 162)
		self.pac_ball(187, 262)
		self.pac_ball(262, 262)


		'''self.line(112, 112, 212, 112)
		self.line(112, 112, 112, 212)
		self.line(212, 112, 212, 212)
		self.line(112, 212, 212, 212)
		self.line(112, 162, 212, 162)
		self.line(162, 112, 162, 212)

		self.pac_ball(162, 162)
		self.pac_ball(212, 162)
		self.pac_ball(212, 212) '''



		return


	def initUI(self):


		button_go = tk.Button(self.gui_root, text='GO')
		button_go.pack(side='left')
		button_go.bind('<Button-1>', self.start_robot)


		button_exit = tk.Button(self.gui_root, text='EXIT')
		button_exit.pack(side='right')
		button_exit.bind('<Button-1>', self.stop_robot)

	



		self.draw_grid()

		return

	def start_robot(self, event=None):
		self.pac_actions.go = True
		return

	def stop_robot(self, event=None):
		self.pac_actions.stop = True
		self.gui_root.quit()	
		return


def main():
	
	maxRobotNum = 1
	
	comm = RobotComm(maxRobotNum)
	
	comm.start()
	
	robotList = comm.robotList

	action = RobotActionThread(robotList)
	
	action.start()
	

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