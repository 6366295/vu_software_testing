import sys

class Phonebook(dict):
	def __init__(self, filename):
		self.filename = filename

		print "Loading in '" + self.filename + "'"

		# Load in a phonebook
		try:
			with open(self.filename) as f:
				for line in f:
					number, name = line.split(' ', 1)
					number = number.strip()
					name = name.strip()

					if number.isdigit() and (len(number) == 5) and name.isalpha() and (len(name) <= 12):
						#phonebook[number] = name
						self.__setitem__((number, name), PhoneData())

						# Limit phonebook entries number to 20
						# Ommitted entries don't count
						if self.__len__() > 20:
							break
					else:
						print "Ommitted entry: [" + str(number) + ", " + str(name) + "]	"
		except:
			print "Phonebook file '" + self.filename + "' could not be loaded!"
			print "Simulation Stopped"

			sys.exit()

		print "Finished loading in " + str(self.__len__()) + " number(s)"

	def __getitem__(self, key):
		try:
			for k in self.keys():
				if key in k:
			 		return super(Phonebook, self).__getitem__(k)

			return super(Phonebook, self).__getitem__(key)
		except KeyError as e:
			return "Phone " + str(e) + " does not exists!"

	def has_key(self, k):
		found = False

		for key in self.keys():
			if k in key:
				found = True

		return found

'''
 action: user input (call, offhook, onhook, transfer, conference)
 status: hears (dialtone, ringback, ringing, busy, denial, silence, talking, talking2)
 connectedto: list of connected phones (dictionary entry)
'''
class PhoneData:
	def __init__(self):
		self.action = "onhook"
		self.status = ""
		self.connectedto = []

	def update_action(self, action):
		self.action = action

	def update_status(self, status):
		self.status = status