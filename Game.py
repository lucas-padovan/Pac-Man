


class Game(object):
	def __init__(self, GUI, RobotActionThread):
		self.remaining_balls = None
		self.GUI = GUI
		self.RobotActionThread = RobotActionThread


	def check_game():
		if self.remaining_balls == 0:
			stopGame()

	def stopGame():
		GUI.stop()
		RobotActionThread.stop()




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