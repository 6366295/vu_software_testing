from commands import UserCommands
from phone import PhoneState
from phone import Phonebook

import sys

'''
 Function returns string (user input or empty)
'''
def cmd_reader():
    # Catch SIGINTS (Ctrl-C) and EOF (Ctrl-D)
    try:
        sys.stdout.write('> ')
        cmd = sys.stdin.readline().strip()
        # cmd = raw_input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print e

        return ""

    return cmd

'''
 Function does nothing of command is not in cmd_dict
'''
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
            cmd_dict[cmd[1]](phone=cmd[0])
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

    # Load phonebook into list of PhoneData classes
    # Use a default input, if non is given
    try:
        phonebook = Phonebook(sys.argv[1])
    except IndexError as e:
        phonebook = Phonebook("phonebook.txt")

    # Pass this lists to the UserCommands, so that the functions can use it
    user_commands = UserCommands(phonebook)

    while 1:
        # Get command from commandline
        cmd = cmd_reader()

        # Execute command based on contents of the commands
        cmd_interpreter(cmd, user_commands.cmd_dict)

    return 0

if __name__ == '__main__':
    main()