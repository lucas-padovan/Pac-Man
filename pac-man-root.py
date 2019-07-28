
import sys
sys.path.append('../')
import threading
import time

from RobotActionThread import *
from HamsterAPI.comm_ble import RobotComm

import Tkinter as tk



class GUI(object):
	def __init__(self, gui_root, robot_actions):
		self.gui_root = gui_root
		self.canvas = None
		self.robot_actions = robot_actions
		self.pac_man = None
		self.initUI()
		self.gui_root.bind('<KeyPress>', self.keydown)
		return


	def rectangle(self, coordx, coordy): #top left
		self.canvas.create_rectangle(coordx, coordy, coordx+25, coordy+25,outline="green",fill='black')
		return

	def keydown(self, event):
		if(event.char == 'w'):
			self.move_up()
			print("w")
		elif(event.char == 'a'): 
			self.move_left()
			print("a")
		elif(event.char == 's'): 
			self.move_down()
			print("s")
		elif(event.char == 'd'): 
			self.move_right()

	def move_up(self):
		self.canvas.move(self.pac_man,0, -10) 
		return

	def move_left(self):
		self.canvas.move(self.pac_man,-10, 0)  
		return

	def move_down(self): 
		self.canvas.move(self.pac_man,0, 10)  
		return

	def move_right(self): 
		self.canvas.move(self.pac_man,10, 0)
		return


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

	root.mainloop()


	comm.stop()
	comm.join()

	return

if __name__ == "__main__":
	sys.exit(main())