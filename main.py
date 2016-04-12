from commands import UserCommands
from phone_data import PhoneData

import sys

def parse_phonebook():
	phonebook = {}
	i = 0

	# Use a default input, if non is given
	try:
		FILENAME = sys.argv[1]
	except IndexError as e:
		FILENAME = "phonebook.txt"

	print "Loading in '" + FILENAME + "'"

	# Load in a phonebook
	try:
		with open(FILENAME) as f:
			for line in f:
				number, name = line.split(' ', 1)
				number = number.strip()
				name = name.strip()

				if number.isdigit() and (len(number) == 5) and name.isalpha() and (len(name) <= 12):
					#phonebook[number] = name
					phonebook[i] = PhoneData(number, name)
					i = i+1

					# Limit phonebook entries number to 20
					# Ommitted entries don't count
					if i > 20:
						break
				else:
					print "Ommitted entry: [" + str(number) + ", " + str(name) + "]	"
	except:
		print "Phonebook file '" + FILENAME + "' could not be loaded!"
		print "Simulation Stopped"

		sys.exit()

	print "Finished loading in " + str(len(phonebook)) + " numbers"

	return phonebook

def cmdline_reader():
	# Catch SIGINTS (Ctrl-C) and EOFError (Ctrl-D)
	try:
		cmd = raw_input("> ")
	except (KeyboardInterrupt, EOFError) as e:
		print e
		return ""

	return cmd

def cmd_interpreter(cmd, cmd_dict):
	# Split command string
	# TODO: This makes exiting using "phone exit phone" possible
	#         but not through "exit phone somethiing"
	cmd = cmd.split(' ')

	# Catch non-existing commands
	# TODO: No feedback though
	try:
		if len(cmd) == 1:
			cmd_dict[cmd[0]]()
		elif len(cmd) == 2:
			cmd_dict[cmd[0]](phone=cmd[1])
		else:
			cmd_dict[cmd[1]](phone1=cmd[0], phone2=cmd[2])
	except KeyError as e:
		return 1

	return 0

def main():
	print "Welcome to the Telephone Switching Simulation (Alpha)"
	print ""
	print "|-------------------------------------------------|" 
	print "| Enter the 'help' command to learn about all the |" 
	print "| commands that you can use in this simulator     |"
	print "|-------------------------------------------------|" 
	print ""

	phonebook = parse_phonebook()

	cmdlist = UserCommands(phonebook)

	cmd_dict = {
		"exit" : cmdlist.cmd_exit,
		"help" : cmdlist.cmd_help,
		"call" : cmdlist.cmd_call,
		"offhook" : cmdlist.cmd_offhook,
		"onhook" : cmdlist.cmd_onhook,
		"transfer" : cmdlist.cmd_transfer,
		"conference" : cmdlist.cmd_conference,
		"status" : cmdlist.cmd_status
	}

	while 1:
		cmd = cmdline_reader()

		cmd_interpreter(cmd, cmd_dict)

	return 0

if __name__ == '__main__':
	main()