from commands import cmd_dict

import sys

phonebook = {}

def parse_phonebook():
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
					phonebook[number] = name
					i = i+1

					# Limit phonebook entries number to 20
					# Ommitted numbers don't count
					if i > 20:
						break
				else:
					print "Ommitted entry: [" + str(number) + ", " + str(name) + "]	"
	except:
		print "Phonebook file '" + FILENAME + "' could not be loaded!"
		print "Simulation Stopped"

		sys.exit()

	print "Finished loading in " + str(len(phonebook)) + " numbers"

	return 0

def cmdline_reader():
	# Catch SIGINTS (Ctrl-C) and EOFError (Ctrl-D)
	try:
		cmd = raw_input("> ")
	except (KeyboardInterrupt, EOFError) as e:
		print e
		return ""

	return cmd

def cmd_interpreter(cmd):
	# Split command string
	# TODO: This makes exiting using "phone exit phone etc..." possible
	#         or "exit phone etc..."
	cmd = cmd.split(' ')

	# Catch non-existing commands
	# TODO: No feedback though
	try:
		if len(cmd) == 1:
			cmd_dict[cmd[0]](0, 0)
		elif len(cmd) == 2:
			cmd_dict[cmd[0]](cmd[1], 0)
		else:
			cmd_dict[cmd[0]](cmd[1], cmd[2])
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

	parse_phonebook()

	while 1:
		cmd = cmdline_reader()

		cmd_interpreter(cmd)

	return 0

if __name__ == '__main__':
	main()