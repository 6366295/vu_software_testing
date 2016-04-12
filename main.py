from commands import cmd_dict

FILENAME = "phonebook.txt"

phonenumbers = {}

def parse_phonebook():
	try:
		with open(FILENAME) as f:
			for line in f:
				number, name = line.split(' ', 1)
				number = number.strip()
				name = name.strip()
				if number.isdigit() and (len(number) == 5) and name.isalpha() and (len(name) <= 12):
					phonenumbers[number] = name
	except:
		print "Could not load phonebook!"

def main():
	parse_phonebook()

	#print "Phonenumber dictionary:"
	#print phonenumbers

	print "Welcome to the Telephone Switching Simulation (Alpha)"
	print ""
	print "|-------------------------------------------------|" 
	print "| Enter the 'help' command to learn about all the |" 
	print "| commands that you can use in this simulator     |"
	print "|-------------------------------------------------|" 
	print ""

	while 1:
		# Catch SIGINTS (Ctrl-C) and EOFError (Ctrl-D)
		try:
			cmd = raw_input("> ")
		except (KeyboardInterrupt, EOFError) as e:
			# Needed for split function
			cmd = ""

			print e

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
			pass

	return 0

if __name__ == '__main__':
	main()