import sys
import os

FILENAME = "phonebook.txt"

phonenumbers = {}

def cmd_exit():
	os._exit(1)

def cmd_help():
    pass

def status():
    # Print the status of all phones and if applicable, who they are talking to
    pass

def call(phone1, phone2):
    # phone1 will call phone2
    pass

def offhook(phone):
    # phone is taken offhook and dialtone should be played (responded)
    pass

def onhook(phone):
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
    parse_phonebook()

    #print "Phonenumber dictionary:"
    #print phonenumbers

    print "Welcome to the Telephone Switching Simulation (Alpha) \n"
    print "Enter the 'help' command to learn about all the" 
    print "commands that you can use in this simulator"

    while 1:
    	# Catch SIGINTS (Ctrl-C) and EOFError (Ctrl-D)
    	try:
    		cmd = raw_input("> ")
    	except (KeyboardInterrupt, EOFError) as e:
    		print e

    	# Catch non-existing commands
    	try:
    		cmd_dict[cmd]()
    	except KeyError:
    		pass

    return 0

if __name__ == '__main__':
    main()