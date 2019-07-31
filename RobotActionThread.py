
import threading
import time
import Queue

class RobotActionThread(threading.Thread):
	def __init__(self, robotList):
		super(RobotActionThread, self).__init__() 
		self.robotList = robotList
		self.daemon = True
		self.go = False
		self.stop = False

		self.movements = Queue.Queue()

		#self.run()

		return

	def run(self):
		while not self.stop:
			#print 'lets go again'
			for robot in self.robotList:
				if robot and self.go:

					ground_l = robot.get_floor(0)
					ground_r = robot.get_floor(1)
					prior = None
					#print 'FOWARD WORKING!!!!!!!'
					if self.movements.empty() == False:
						m = self.movements.get()
						if(m == 'forward'):
							self.run_forward(robot, prior)
						elif(m == 'left'):
							self.move_left(robot)
						elif(m == 'right'):
							self.move_right(robot)
						#prior = m
					#self.run_forward(robot)
		

		return


	def move_right(self, robot):
		ground_l = robot.get_floor(0)
		ground_r = robot.get_floor(1)
		counter = 0
		robot.set_wheel(0, 30)
		robot.set_wheel(1, 0)
		time.sleep(1.6)
		'''while ground_r < 50 and self.go and counter < 30:
			#print 'moving right !!!!!!!'
			ground_l = robot.get_floor(0)
			ground_r = robot.get_floor(1)
			#print "Right " + str(ground_r)
			robot.set_wheel(1, 0)
			robot.set_wheel(0, 30)
			counter = counter + 1
			time.sleep(0.1)'''

		robot.set_wheel(1, 0)
		robot.set_wheel(0, 0)
		return

	def stop_robot(self, robot):
		robot.set_wheel(1, 0)
		robot.set_wheel(0, 0)

	def move_left(self, robot):
		ground_l = robot.get_floor(0)
		ground_r = robot.get_floor(1)
		counter = 0
		#print("RIGHTT " + str(ground_r))
		#print("LEFT " + str(ground_r))
		robot.set_wheel(1, 30)
		robot.set_wheel(0, 0)
		time.sleep(1.8)
		'''while ground_l < 50 and self.go and counter < 30:
			#print 'moving left !!!!!!!'
			ground_l = robot.get_floor(0)
			ground_r = robot.get_floor(1)
			#print("RIGHTT " + str(ground_r))
			#print("LEFT " + str(ground_r))
			robot.set_wheel(1, 30)
			robot.set_wheel(0, 0)
			counter = counter + 1
			time.sleep(0.1)''' 
		robot.set_wheel(1, 0)
		robot.set_wheel(0, 0)
		return


	def run_forward(self, robot, prior):
		ground_l = robot.get_floor(0)
		ground_r = robot.get_floor(1)
		#print 'FOWARD WORKING!!!!!!!'
		print ground_r
		print ground_l
		robot.set_wheel(1, 30)
		robot.set_wheel(0, 30)

		time.sleep(0.6)

		while self.go:
			#print 'running forward  AGAIIIIN!!!!!!!'
			print prior
			if((ground_l > 30 and ground_r > 30) or prior == 'forward'):

				print ('left: ' + str(ground_l))
				print ('right: ' + str(ground_r))
				ground_l = robot.get_floor(0)
				ground_r = robot.get_floor(1)
			

				if(ground_r < ground_l + 5 and ground_r < 50): #dark tape to the right, therefore turn right
					robot.set_wheel(1, 0)
					robot.set_wheel(0, 10 + ground_l-ground_r)

				elif(ground_l < ground_r + 5 and ground_l < 50): #dark tape to the left, therefore turn left
					robot.set_wheel(1, 10+ ground_r-ground_l)
					robot.set_wheel(0, 0)
				else:
					robot.set_wheel(1, 20)
					robot.set_wheel(0, 20)
			else:
				break
			#time.sleep(0.2)
		robot.set_wheel(1, 0)
		robot.set_wheel(0, 0)

		return



