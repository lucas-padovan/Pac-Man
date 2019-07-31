import sys
import random
import Tkinter as tk
import threading

class Ghost(threading.Thread):

	def __init__(self, canvas, lines, s_x, s_y):
		super(Ghost, self).__init__() 
		self.daemon = True

		self.canvas = canvas
		self.lines = lines

		self.ghost = self.canvas.create_oval(112-10, 112-10,112+10,112+10, fill="white")
		self.ghost_x = s_x
		self.ghost_y = s_y

		t_ghost_moving = threading.Thread(name='ghost mover', target=self.start_moving, args=(0, 0))
		t_ghost_moving.daemon = True
		t_ghost_moving.start()
		self.t_ghost_moving = t_ghost_moving

		self.orientation = 'down'

		self.movements = ''


	def start_moving(self, already_moving, zero):
		options = ['up', 'left', 'right']

		while True:
			n = random.randint(0, 2)

			pick = options[n]
		
			if direction > 0:
				direction = already_moving

			if direction == 1: #up
				if self.authorize_movement(self.ghost_x, self.ghost_y-3):
					self.move_up()
					direction = 1
					#self.start_moving(1)
				else:
					direction = 0
					#self.start_moving(0)

			elif direction == 2: #down
				if self.authorize_movement(self.ghost_x, self.ghost_y+3):
					self.move_down()
					direction = 2
					#self.start_moving(2)
				else:
					direction = 0
					#self.start_moving(0)

			elif direction == 3: #left
				if self.authorize_movement(self.ghost_x-3, self.ghost_y):
					self.move_left()
					direction = 3
					#self.start_moving(3)
				else:
					direction = 0
					#self.start_moving(0)

			elif direction == 4: #right
				if self.authorize_movement(self.ghost_x+3, self.ghost_y):
					self.move_right()
					direction = 4
					#self.start_moving(4)
				else:
					direction = 0
					#self.start_moving(0)




	def authorize_movement(self, x1, y1):
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

	def move_up(self):
		authorization = self.authorize_movement(self.ghost_x, self.ghost_y - 3)
		if(authorization):
			self.ghost_y = self.ghost_y - 3
			self.canvas.move(self.ghost,0, -3) 
		return

	def move_left(self):
		authorization = self.authorize_movement(self.ghost_x - 3, self.ghost_y)
		if(authorization):
			self.ghost_x = self.ghost_x - 3
			self.canvas.move(self.ghost,-3, 0)  
		return

	def move_down(self): 
		authorization = self.authorize_movement(self.ghost_x, self.ghost_y + 3)
		if(authorization):
			self.ghost_y = self.ghost_y + 3
			self.canvas.move(self.ghost,0, 10)  
		return

	def move_right(self): 
		authorization = self.authorize_movement(self.ghost_x + 3, self.ghost_y)
		if(authorization):
			self.ghost_x = self.ghost_x + 3
			self.canvas.move(self.ghost,3, 0)
		return

