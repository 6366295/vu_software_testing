from commands import UserCommands
from phone import PhoneState
from phone import Phonebook

import sys

'''
 Function returns string (user input or empty)
'''
def cmd_reader():
    # REQ??
    # Catch SIGINTS (Ctrl-C) and EOF (Ctrl-D)
    try:
        '''
        TODO: Not using raw_input gave me a IOError, 
              when input: Ctrl-C then imediatly Ctrl-D
        '''
        # sys.stdout.write('> ')
        # cmd = sys.stdin.readline().strip()
        cmd = raw_input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print e

        return ""

    return cmd

'''
 Function does nothing if command is not in cmd_dict
'''
def cmd_interpreter(cmd, cmd_dict):
    # Split command string
    # TODO: This makes exiting using "phone exit phone" possible
    #       but not through "exit phone somethiing"
    cmd = cmd.split(' ')

    # Catch non-existing commands
    try:
        if len(cmd) == 1:
            cmd_dict[cmd[0]]()
        elif len(cmd) == 2:
            cmd_dict[cmd[1]](phone=cmd[0])
        else:
            cmd_dict[cmd[1]](phone1=cmd[0], phone2=cmd[2])
    # TODO: REQ??
    except KeyError as e:
        print "Wrong command or wrong use of the command"

        return

def main():
    # Program opening message
    print "|---------------------------------------------------|"
    print "|\033[95m Welcome to the Telephone Switching Simulation 1.0 \033[0m|"
    print "|---------------------------------------------------|"
    print "|            \ ___                 ___ /            |"
    print "|           --|_  \               /  _|--           |"
    print "|            /  \  |             |  /  \            |"
    print "|                | |             | |                |"
    print "|                | |             | |                |"
    print "|              _/  |             |  \_              |"
    print "|             |___/-----.....-----\___|             |"
    print "\                                                   /"
    print " |-------------------------------------------------|" 
    print " |-------------------------------------------------|" 
    print ""

    # REQ01
    # Get user specified phonebook filename
    # Use default phonebook filename, if user did not specify any
    try:
        filename = sys.argv[1]
    except IndexError as e:
        filename = "phonebook.txt"

    # Initialize Phonebook class
    phonebook = Phonebook()

    # REQ01
    phonebook.parse_phonebook(filename)

    # Give phonebook dictionary to UserCommand to use
    user_commands = UserCommands(phonebook)

    # CLI loop
    while 1:
        # Get user input command
        cmd = cmd_reader()

        # Execute command based on contents of the commands
        cmd_interpreter(cmd, user_commands.cmd_dict)

if __name__ == '__main__':
    main()