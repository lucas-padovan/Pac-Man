
import threading

class RobotActionThread(threading.Thread):
	def __init__(self, robotList):
		super(RobotActionThread, self).__init__() 
		self.robotList = robotList
		self.go = False
		self.stop = False

		return



	def run(self):
		while not self.stop:
			for robot in self.robotList:
				if robot and self.go:

					ground_l = robot.get_floor(0)
					ground_r = robot.get_floor(1)

					print ('left: ' + str(ground_l))
					print ('right: ' + str(ground_r))

					if(ground_r < ground_l + 5 and ground_r < 50): #dark tape to the right, therefore turn right
						robot.set_wheel(1, 0)
						robot.set_wheel(0, 0 + ground_l-ground_r)

					elif(ground_l < ground_r + 5 and ground_l < 50): #dark tape to the right, therefore turn right
						robot.set_wheel(1, 0+ ground_r-ground_l)
						robot.set_wheel(0, 0)
					else:
						robot.set_wheel(1, 5)
						robot.set_wheel(0, 5)
		return



