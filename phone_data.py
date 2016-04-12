'''
 action: user input (call, offhook, onhook, transfer, conference)
 status: hears (dialtone, ringback, ringing, busy, denial, silence, talking, talking2)
 connectedto: list of connected phones (dictionary entry)
'''

class PhoneData:
	def __init__(self, number, name):
		self.number = number
		self.name = name
		self.action = ""
		self.status = ""
		self.connectedto = []

	def update_action(self, action):
		self.action = action

	def update_status(self, status):
		self.status = status