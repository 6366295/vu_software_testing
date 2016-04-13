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
		# if "bar" in self.phonebook.keys()[0]:
		# 	print self.phonebook.keys()[0]
		# print self.phonebook
		# print self.phonebook["barsd"]
		# print kwargs

		sys.exit()

	def cmd_help(self, *args, **kwargs):
		pass

	def cmd_status(self, *args, **kwargs):
		# Print the status of all phones and if applicable, who they are talking to
		pass

	def cmd_call(self, *args, **kwargs):
		# phone1 will call phone2
		print kwargs

	def cmd_offhook(self, *args, **kwargs):
		# phone is taken offhook and dialtone should be played (responded)
		print kwargs

	def cmd_onhook(self, *args, **kwargs):
		# phone is put back on the hook, closing the call, other phone should be
		# notified if a call was active
		print kwargs

	def cmd_transfer(self, *args, **kwargs):
		# After phone1 and phone2 are talking:
		# transfers a call between phone1 and phone2 to a call between phone3 and 
		# phone2
		print kwargs

	def cmd_conference(self, *args, **kwargs):
		# After phone1 and phone2 are talking:
		# Either phone1 or phone2 conferences phone3, which is then added to the call
		# phone1 and phone2 and phone3 are talking.
		print kwargs