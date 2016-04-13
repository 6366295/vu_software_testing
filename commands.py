import sys

class UserCommands:
	def __init__(self, phonebook):
		self.phonebook = phonebook

		self.cmd_dict = {
			"exit" : self.cmd_exit,
			"help" : self.cmd_help,
			"call" : self.cmd_call,
			"offhook" : self.cmd_offhook,
			"onhook" : self.cmd_onhook,
			"transfer" : self.cmd_transfer,
			"conference" : self.cmd_conference,
			"status" : self.cmd_status
		}

	def cmd_exit(self, *args, **kwargs):
		sys.exit()

	def cmd_help(self, *args, **kwargs):
		pass

	def cmd_status(self, *args, **kwargs):
		# Print the status of all phones and if applicable, who they are talking to
		for key, value in self.phonebook.iteritems():
			print key[0], key[1]
			print "\t", value.status, value.hears, value.phone2, value.phone3


	def cmd_call(self, *args, **kwargs):
		# phone1 will call phone2
		phone1 = kwargs['phone1']
		phone2 = kwargs['phone2']

		if self.phonebook.has_key(phone1):
			phone1_state = self.phonebook[phone1]

			if phone1_state.status == "onhook":
				if phone1_state.hears != "ringing":
					phone1_state.hears = "silence"
					print phone1 + " hears " + phone1_state.hears
			else:
				if self.phonebook.has_key(phone2):
					phone2_state = self.phonebook[phone2]

					if phone1_state.hears == "ringback":
						print phone1 + " is already calling " + phone1_state.phone2
					elif phone1_state.hears == "talking":
						print "You are already in a call!"
					elif phone2_state.hears == "talking" or phone2_state.hears == "ringing"  or phone2_state.hears == "ringback" or phone2_state.status == "offhook":
						phone1_state.hears = "busy"
						print phone1 + " hears " + phone1_state.hears
					else:
						phone1_state.hears = "ringback"
						phone2_state.hears = "ringing"
						phone1_state.phone2 = phone2
						phone2_state.phone2 = phone1
						print phone1 + " hears " + phone1_state.hears
						print phone2 + " hears " + phone2_state.hears
				else:
					phone1_state = "denial"
					print phone1 + " hears " + phone1_state.hears
		else:
			print phone1 + " does not exist!"

	def cmd_offhook(self, *args, **kwargs):
		# phone is taken offhook and dialtone should be played (responded)
		# self.phonebook[kwargs['phone']]
		phone = kwargs['phone']

		if self.phonebook.has_key(phone):
			phone_state = self.phonebook[phone]

			if phone_state.status == "offhook":
				print phone + " is already offhook"
			else:
				if phone_state.hears == "ringing":
					phone2 = phone_state.phone2
					phone2_state = self.phonebook[phone2]

					if phone_state.transfer:
						phone_state.status = "offhook"
						phone_state.hears = "talking"
						phone_state.phone2 = phone2_state.phone2

						phone2_state.hears = "silence"
						phone2_state.phone2 = None
						phone2_state.phone3 = None
						phone_state.transfer = False

						phone2 = phone_state.phone2
						phone2_state = self.phonebook[phone2]
						phone2_state.phone2 = phone

						print phone + " and " + phone2 + " are " + phone_state.hears
					elif phone_state.conference:
						phone_state.status = "offhook"
						phone_state.hears = "talking"
						phone_state.phone3 = phone2_state.phone2

						phone2_state.hears = "talking"
						phone2_state.conference = True

						phone3 = phone_state.phone3
						phone3_state = self.phonebook[phone3]
						phone3_state.phone3 = phone
						phone3_state.conference = True

						print phone + " and " + phone2 + " and " + phone3 + " are " + phone_state.hears
					else:
						phone_state.status = "offhook"
						phone_state.hears = "talking"
						phone2_state.hears = "talking"

						print phone + " and " + phone2 + " are " + phone_state.hears
				else:
					phone_state.status = "offhook"
					phone_state.hears = "dialtone"
					print phone + " hears " + phone_state.hears
		else:
			print phone + " does not exist!"

	def cmd_onhook(self, *args, **kwargs):
		# phone is put back on the hook, closing the call, other phone should be
		# notified if a call was active
		phone = kwargs['phone']

		if self.phonebook.has_key(phone):
			phone_state = self.phonebook[phone]

			if phone_state.status == "onhook":
				print phone + " is already onhook"
			else:
				if phone_state.hears == "talking":
					if phone_state.conference:
						phone2 = phone_state.phone2
						phone2_state = self.phonebook[phone2]

						phone3 = phone_state.phone3
						phone3_state = self.phonebook[phone3]

						phone_state.hears = "silence"
						phone_state.status = "onhook"
						phone_state.phone2 = None
						phone_state.phone3 = None

						phone_state.conference = False
						phone2_state.conference = False
						phone3_state.conference = False

						if phone == phone2_state.phone2:
							phone2_state.phone2 = phone2_state.phone3
							phone2_state.phone3 = None
						elif phone == phone2_state.phone3:
							phone2_state.phone3 = None

						if phone == phone3_state.phone2:
							phone3_state.phone2 = phone3_state.phone3
							phone3_state.phone3 = None
						elif phone == phone3_state.phone3:
							phone3_state.phone3 = None

						print phone2_state.phone2 + " and " + phone3_state.phone2 + " are " + phone2_state.hears
					else:
						phone2 = phone_state.phone2
						phone2_state = self.phonebook[phone2]

						phone_state.hears = "silence"
						phone_state.status = "onhook"
						phone_state.phone2 = None

						phone2_state.hears = "silence"
						phone2_state.phone2 = None

						if phone_state.transfer:
							phone2 = phone_state.phone3
							phone2_state = self.phonebook[phone2]
							phone_state.phone3 = None
							phone_state.transfer = False

							phone2_state.hears = "silence"
							phone2_state.phone2 = None
							phone2_state.transfer = False

						print phone2 + " hears " + phone2_state.hears
				else:
					if phone_state.phone2 != None:
						phone2 = phone_state.phone2
						phone2_state = self.phonebook[phone2]

						phone2_state.hears = "silence"
						phone2_state.phone2 = None

						phone_state.phone2 = None

					phone_state.status = "onhook"
					phone_state.hears = "silence"
		else:
			print phone + " does not exist!"

	def cmd_transfer(self, *args, **kwargs):
		# After phone1 and phone2 are talking:
		# transfers a call between phone1 and phone2 to a call between phone3 and 
		# phone2
		phone1 = kwargs['phone1']
		phone2 = kwargs['phone2']

		if self.phonebook.has_key(phone1):
			phone1_state = self.phonebook[phone1]

			if phone1_state.hears != "talking":
				print "No transfers when you are not in a call!"
			else:
				if self.phonebook.has_key(phone2):
					phone2_state = self.phonebook[phone2]

					if phone1_state.hears == "ringback":
						print phone1 + " is already calling " + phone1_state.phone2
					elif phone2_state.hears == "talking" or phone2_state.hears == "ringing"  or phone2_state.hears == "ringback" or phone2_state.status == "offhook":
						phone1_state.hears = "busy"
						print phone1 + " hears " + phone1_state.hears
						phone1_state.hears = "talking"
					else:
						phone1_state.hears = "ringback"
						phone2_state.hears = "ringing"
						phone1_state.phone3 = phone2
						phone2_state.phone2 = phone1
						print phone1 + " hears " + phone1_state.hears
						print phone2 + " hears " + phone2_state.hears
						phone2_state.transfer = True
						phone1_state.transfer = True
				else:
					phone1_state = "denial"
					print phone1 + " hears " + phone1_state.hears
		else:
			print phone1 + " does not exist!"
		

	def cmd_conference(self, *args, **kwargs):
		# After phone1 and phone2 are talking:
		# Either phone1 or phone2 conferences phone3, which is then added to the call
		# phone1 and phone2 and phone3 are talking.
		phone1 = kwargs['phone1']
		phone2 = kwargs['phone2']

		if self.phonebook.has_key(phone1):
			phone1_state = self.phonebook[phone1]

			if phone1_state.hears != "talking":
				print "No conferences when you are not in a call!"
			else:
				if self.phonebook.has_key(phone2):
					phone2_state = self.phonebook[phone2]

					if phone1_state.hears == "ringback":
						print phone1 + " is already calling " + phone1_state.phone2
					elif phone2_state.hears == "talking" or phone2_state.hears == "ringing"  or phone2_state.hears == "ringback" or phone2_state.status == "offhook":
						phone1_state.hears = "busy"
						print phone1 + " hears " + phone1_state.hears
						phone1_state.hears = "talking"
					else:
						phone1_state.hears = "ringback"
						phone2_state.hears = "ringing"
						phone1_state.phone3 = phone2
						phone2_state.phone2 = phone1
						print phone1 + " hears " + phone1_state.hears
						print phone2 + " hears " + phone2_state.hears
						phone2_state.conference = True
				else:
					phone1_state = "denial"
					print phone1 + " hears " + phone1_state.hears
		else:
			print phone1 + " does not exist!"
