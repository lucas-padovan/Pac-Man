import sys
import Tkinter as tk
import threading
import Queue
import time
import math

val = 1

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

class PacMan(threading.Thread):

	def __init__(self, canvas, lines, n_pac_balls, pac_balls, pac_balls_coord):
		super(PacMan, self).__init__() 
		self.daemon = True

		self.n_pac_balls = n_pac_balls
		self.pac_balls = pac_balls
		self.pac_balls_coord = pac_balls_coord

		self.canvas = canvas
		self.lines = lines

		self.pac_man = self.canvas.create_oval(112-12, 112-12,112+12,112+12, fill="yellow")
		self.pac_man_x = 112
		self.pac_man_y = 112

		self.orientation = 'down'

		self.movements = ''

		self.intersec = set()
		self.find_intersections()

	def compare_point(self, p1, p2):
		if(p1.x == p2.x and p1.y == p2.y):
			return True
		else:
			return False

	def printIntersec(self):
		res = '['
		for point in self.intersec:
			res += ', [%d, %d]' % (point.x, point.y)
		res += ']\n\n\n'
		print res
		return

	'''def not_duplicate(self, p1):
		res = True
		for i in range(0, len(self.intersec)):
			p2 = self.intersec[i]
			if(self.compare_point(p1, p2)):
				res = False
				break
		return res '''


	def find_intersections(self):
		for i in range (0, len(self.lines) -1):
			line = self.lines[i]

			p1 = Point(line[0], line[1])
			p2 = Point(line[2], line[3])

			for j in range (i+1, len(self.lines)):
				linha = self.lines[j]
				if(j != i): 
					p3 = Point(linha[0], linha[1])
					p4 = Point(linha[2], linha[3])
					if self.compare_point(p1, p3):
						self.intersec.add(p1)
					if self.compare_point(p1, p4):
						self.intersec.add(p1) 
					if self.compare_point(p2, p3):
						self.intersec.add(p2)
					if self.compare_point(p2, p4): 
						self.intersec.add(p1)
		
		return 





	
	def run(self):
		while True:
			if self.movements != '':
				m = self.movements
				if(m == 'up'):
					self.move_up()
				elif(m == 'down'):
					self.move_down()
				elif(m == 'left'):
					self.move_left()
				elif(m == 'right'):
					self.move_right()



	def authorize_movement(self, x1, y1, type_mov):
		res = False

		for line in self.lines:
			l_x1 = line[0]
			l_y1 = line[1]
			l_x2 = line[2]
			l_y2 = line[3]

			aux_x1 = x1
			aux_y1 = y1

			m1 = 0
			m2 = 0

			dis1 = math.sqrt((x1-l_x1) * (x1-l_x1) + (y1-l_y1) * (y1-l_y1))
			dis2 = math.sqrt((x1-l_x2) * (x1-l_x2) + (y1-l_y2) * (y1-l_y2))

			if(type_mov == 'up'):
				aux_y1 -= val


			elif(type_mov == 'down'):
				aux_y1 += val

			elif(type_mov == 'left'):
				aux_x1 -= val

			elif(type_mov == 'right'):
				aux_x1 += val

			if (aux_x1 - x1) == 0:
				m1 = -1
			else: 	
				m1 = (aux_y1 - y1) / (aux_x1 - x1) 

			if(l_x2 - l_x1 == 0): 
				m2 = -1
			else: 
				m2 = (l_y2 - l_y1) / (l_x2 - l_x1) 



			if(l_x1  + val >= x1 and x1 + val >= l_x2 and l_y1 + val >= y1 and y1 + val  >= l_y2 and m1 == m2):
				#self.pac_man_x = l_x1
				#self.pac_man_y = l_y1
				#if dis1 < 5:
				#	print 'first 1'
				#	self.pac_man_x = l_x1
				#	self.pac_man_x = l_y1
				'''else:
					print 'second 1'
					self.pac_man_y = l_y1
				'''
 				res = True
				break 
			elif(l_x2 + val >= x1 and x1 + val  >= l_x1 and l_y2 + val >= y1 and y1 + val >= l_y1  and m1 == m2):
				#self.pac_man_x = l_x1
				#self.pac_man_y = l_y1
				'''if l_x1 == l_x2:
					print 'first 2'
					self.pac_man_x = l_x1
				else:
					print 'second 2'
					self.pac_man_y = l_y1
				'''
				#if dis2 < 5:
				#	print 'first 1'
				#	self.pac_man_x = l_x2
				#	self.pac_man_x = l_y2
				res = True
				break

		return res

	def checkIfInColision(self):
		point_pacman = Point(self.pac_man_x, self.pac_man_y)
		if(point_pacman in self.intersec):
			self.movements = ''

	def move_up(self):
		while True and self.movements == 'up':
			authorization = self.authorize_movement(self.pac_man_x, self.pac_man_y - val, 'up')
			if(authorization):
				self.orientation = 'up'
				self.pac_man_y = self.pac_man_y - val
				self.canvas.move(self.pac_man,0, -val)
				self.checkIfInIntersection()
				self.detect_colision()
			else:
				break 
			time.sleep(0.06)
		return

	def move_left(self):
		while True and self.movements == 'left':
			authorization = self.authorize_movement(self.pac_man_x - val, self.pac_man_y, 'left')
			if(authorization):
				self.orientation = 'left'
				self.pac_man_x = self.pac_man_x - val
				self.canvas.move(self.pac_man,-val, 0)
				self.checkIfInIntersection()
				self.detect_colision()  
			else:
				break 
			time.sleep(0.06)
		return

	def move_down(self): 

		while True and self.movements == 'down':
			print 'hey11'
			authorization = self.authorize_movement(self.pac_man_x, self.pac_man_y + val, 'down')
			if(authorization):
				print 'hey22'
				self.orientation = 'down'
				self.pac_man_y = self.pac_man_y + val
				self.canvas.move(self.pac_man,0, val) 
				self.checkIfInIntersection() 
				self.detect_colision()
			else:
				break 
			time.sleep(0.06)
		return

	def move_right(self) : 
		while True and self.movements == 'right':
			authorization = self.authorize_movement(self.pac_man_x + val, self.pac_man_y, 'right')
			if(authorization):
				self.orientation = 'right'
				self.pac_man_x = self.pac_man_x + val
				self.canvas.move(self.pac_man,val, 0)
				self.checkIfInIntersection()
				self.detect_colision()
			else:
				break 
			time.sleep(0.06)
		return


	def detect_colision(self):
		for i in range(0, len(self.pac_balls_coord)):
			#print self.n_pac_balls

			coord = self.pac_balls_coord[i]

			
			coordx = coord[0]
			coordy = coord[1]

			if(coordx != -1 and coordy != -1):
				x = self.pac_man_x
				y = self.pac_man_y

				dis = math.sqrt((x-coordx) * (x-coordx) + (y-coordy) * (y-coordy))


				if(dis < 10):

					print type(self.n_pac_balls)
					
					#dontknow = self.pac_balls[i]
					self.canvas.delete(self.pac_balls[i])
					self.pac_balls_coord[i][0] = -1
					self.pac_balls_coord[i][1] = -1
					self.n_pac_balls = self.n_pac_balls - 1





