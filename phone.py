import sys

class Phonebook(dict):
    # REQ02
    #   Check phone number validity
    def validate_number(self, number):
    	if number.isdigit() and len(number) == 5:
    		return True
    	else:
    		return False

    # REQ03
    #   Check name validity
    def validate_name(self, name):
    	if name.isalpha() and len(name) <= 12:
    		return True
    	else:
    		return False

    # REQ01
    #   Load in a phonebook from a file
    def parse_phonebook(self, filename):
        print "! Loading in '" + filename + "'"

        # Catch non-existing filenames
        try:
            # Open file
            with open(filename) as f:
                for line in f:
                    number, name = line.split(' ', 1)

                    # TODO: REQ??
                    # Remove trailing characters, before validating them
                    number = number.strip()
                    name = name.strip()

                    # (REQ02, REQ03)
                    if self.validate_number(number) and self.validate_name(name):
                        # (REQ15, REQ16)
                        self.__setitem__((number, name), PhoneState())

                        # REQ01
                        #   Limit phonebook entries to twenty entries
                        # TODO: REQ??
                        # Ommitted entries don't count
                        if self.__len__() > 20:
                            break
                    else:
                        # REQ01
                        #   Print list of ommitted entries
                        print "! Ommitted entry: [" + str(number) + ", " + str(name) + "] "
        # TODO: REQ??
        except IOError:
            print "! Phonebook file '" + filename + "' could not be loaded!"
            print "! Simulation Stopped"

            sys.exit()

        # REQ01
        #   Print loading status
        print "! Finished loading in " + str(self.__len__()) + " number(s) \n"
    
    def __setitem__(self, key, item): 
        # REQ15, REQ16
        #   Dictonary only takes unique names and numbers
        if self.has_key(key[0]) or self.has_key(key[1]):
            return KeyError

        # REQ01
        #   Dictionary only takes tuples with length two
        if type(key) == tuple and len(key) == 2:
            super(Phonebook, self).__setitem__(key, item)

    # This dictionary can get items using one element of a tuple
    def __getitem__(self, key):
        try:
            for k in self.keys():
                if key in k:
                    return super(Phonebook, self).__getitem__(k)

            return super(Phonebook, self).__getitem__(key)
        except KeyError as e:
            return "Phone " + str(e) + " does not exist in phonebook!"

    # This dictionary can check if key is in dictionary using one element of a tuple
    def has_key(self, k):
        found = False

        for key in self.keys():
            if k in key:
                found = True
                break

        return found

'''
 status: onhook or offhook
 hears: silence, dialtone, ringback, ringing, busy, denial, talking
 talkingto: list of connected phones (by names or number (or both?))
'''
class PhoneState:
    def __init__(self):
        self.status = "onhook"
        self.hears = "silence"
        self.phone2 = None
        self.phone3 = None
        self.transfer = False
        self.conference = False