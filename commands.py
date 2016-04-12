import sys

def cmd_exit(dummy1, dummy2):
	sys.exit()

def cmd_help(dummy1, dummy2):
	pass

def status(dummy1, dummy2):
	# Print the status of all phones and if applicable, who they are talking to
	pass

def call(phone1, phone2):
	# phone1 will call phone2
	pass

def offhook(phone, dummy1):
	# phone is taken offhook and dialtone should be played (responded)
	pass

def onhook(phone, dummy1):
	# phone is put back on the hook, closing the call, other phone should be
	# notified if a call was active
	pass

def transfer(phone1, phone3):
	# After phone1 and phone2 are talking:
	# transfers a call between phone1 and phone2 to a call between phone3 and 
	# phone2
	pass

def conference(phone, phone3):
	# After phone1 and phone2 are talking:
	# Either phone1 or phone2 conferences phone3, which is then added to the call
	# phone1 and phone2 and phone3 are talking.
	pass

cmd_dict = {
	"exit" : cmd_exit,
	"help" : cmd_help,
	"call" : call,
	"offhook" : offhook,
	"onhook" : onhook,
	"transfer" : transfer,
	"conference" : conference,
	"status" : status
	}

def main():
	return 0

if __name__ == '__main__':
	main()