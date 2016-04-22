import sys

class Phonebook(dict):
    def __setitem__(self, key, item): 
        # REQ15, REQ16
        # Dictonary only takes unique names and numbers
        if self.has_key(key[0]) or self.has_key(key[1]):
            return KeyError

        # REQ01
        # Dictionary only takes tuples with length two
        if type(key) == tuple and len(key) == 2:
            super(Phonebook, self).__setitem__(key, item)

    # REQ05
    # This dictionary can get items using one element of a tuple
    def __getitem__(self, key):
        try:
            for k in self.keys():
                if key in k:
                    return super(Phonebook, self).__getitem__(k)

            return super(Phonebook, self).__getitem__(key)
        except KeyError as e:
            return "Phone " + str(e) + " does not exist in phonebook!"

    # REQ05
    # This dictionary can check if key is in dictionary using one element of a tuple
    def has_key(self, k):
        found = False

        for key in self.keys():
            if k in key:
                found = True
                break

        return found

    # REQ02
    # Check phone number validity
    def validate_number(self, number):
    	if number.isdigit() and len(number) == 5:
    		return True
    	else:
    		return False

    # REQ03
    # Check name validity
    def validate_name(self, name):
    	if name.isalpha() and len(name) <= 12:
    		return True
    	else:
    		return False

    # REQ01
    # Load in a phonebook from a file
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
                        self.__setitem__((number, name), PhoneState(number, name))

                        # REQ01
                        # Limit phonebook entries to twenty entries
                        # TODO: REQ??
                        # Ommitted entries don't count
                        if self.__len__() > 20:
                            break
                    else:
                        # REQ01
                        #   Print list of ommitted entries
                        print "! Ommitted entry: [" + str(number) + ", " + str(name) + "] "
        # TODO: REQ??
        except (IOError, ValueError):
            print "! Phonebook file '" + filename + "' could not be loaded!"
            print "! Simulation Stopped"

            sys.exit()

        # REQ01
        if self.__len__() < 2:
            print "! You at least two numbers in order to use this program"
            print "! Simulation Stopped"

            sys.exit()

        # REQ01
        # Print loading status
        print "! Finished loading in " + str(self.__len__()) + " number(s) \n"

'''
 REQ06
 status: onhook or offhook
 hears: silence, dialtone, ringback, ringing, busy, denial, talking
'''
class PhoneState:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.status = "onhook"
        self.hears = "silence"
        self.transfer = False
        self.conference = False

        self.connected_phone1 = None
        self.connected_phone2 = None

    # REQ12
    def check_onhook(self):
        if self.status == "onhook" and self.hears == "ringing":
            print self.name + " is being called, offhook to answer"

            return False
        elif self.status == "onhook" and self.hears == "silence":

            print self.name + " hears " + self.hears

            return False
        else:
            return True

    # REQ13
    def check_offhook(self):
        if self.status == "offhook":

            print self.name + " is already offhook"

            return False
        else:
            return True

    def check_transfer(self):
        # Not in call, so no transfers possible
        if self.hears != "talking":
            self.denial_response()

            return False
        # No transfers, when in conference
        elif self.conference:
            self.denial_response2()

            return False
        else:
            return True

    def check_conference(self):
        # Not in call, so no conference possible
        if self.hears != "talking":
            self.denial_response()

            return False
        # More than three way conference not allowed
        elif self.conference:
            self.denial_response2()

            return False
        else:
            return True

    def call_response(self, phone2_state):
        if self.hears == "ringback":
            print self.name + " is already calling " + self.connected_phone1.name
        elif self.hears == "talking":
            print self.name + " is already talking to " + self.connected_phone1.name                
        elif self.hears == "busy" or self.hears == "denial" or self.hears == "silence":
            print self.name + " already tried to call or have been talking before, onhook and then offhook to try again"
        # REQ10
        elif phone2_state.status == "offhook" or phone2_state.hears == "ringing":
            self.hears = "busy"

            print self.name + " hears " + self.hears
        elif self.hears == "dialtone":
            self.connected_phone1 = phone2_state

            self.hears = "ringback"
            self.connected_phone1.hears = "ringing"

            self.connected_phone1.connected_phone1 = self

            print self.name + " hears " + self.hears
            print self.connected_phone1.name + " hears " + self.connected_phone1.hears

            return 0

        return 1

    def offhook_response(self):
        if self.hears == "ringing":
            if self.transfer:
                self.status = "offhook"
                self.hears = "talking"

                self.connected_phone2 = self.connected_phone1.connected_phone1

                self.connected_phone1.connected_phone2 = None
                self.connected_phone1.connected_phone1 = None

                self.connected_phone1.hears = "silence"
                self.connected_phone1.transfer = False

                print self.connected_phone1.name + " hears " + self.connected_phone1.hears

                self.connected_phone1 = self.connected_phone2
                self.connected_phone2 = None
                self.connected_phone1.connected_phone1 = self

                self.transfer = False
                self.connected_phone1.transfer = False
                
                print self.name + " and " + self.connected_phone1.name + " are " + self.hears
            elif self.conference:
                self.status = "offhook"
                self.hears = "talking"

                self.connected_phone2 = self.connected_phone1.connected_phone1
                self.connected_phone2.connected_phone2 = self

                self.connected_phone1.hears = "talking"
                
                print self.name + " and " + self.connected_phone1.name + " and " + self.connected_phone2.name + " are " + self.hears
            else:
                self.status = "offhook"
                self.hears = "talking"
                self.connected_phone1.hears = "talking"

                print self.name + " and " + self.connected_phone1.name + " are " + self.hears
        elif self.hears == "silence":
            self.status = "offhook"
            self.hears = "dialtone"

            print self.name + " hears " + self.hears

        return 0

    def onhook_response(self):
        if self.transfer:
            if self.hears == "talking":
                self.connected_phone1.connected_phone2.connected_phone1 = None
                self.connected_phone1.connected_phone2.hears = "silence"
                self.connected_phone1.connected_phone2.transfer = False

                self.connected_phone1.connected_phone2 = None
                self.connected_phone1.connected_phone1 = None
                self.connected_phone1.hears = "silence"
                self.connected_phone1.transfer = False

                print self.connected_phone1.name + " hears " + self.connected_phone1.hears

                self.connected_phone1 = None
                self.status = "onhook"
                self.hears = "silence"
                self.transfer = False
            elif self.hears == "ringback":
                self.connected_phone2.connected_phone1 = None
                self.connected_phone2.hears = "silence"
                self.connected_phone2.transfer = False

                self.connected_phone1.connected_phone1 = None
                self.connected_phone1.hears = "silence"
                self.connected_phone1.transfer = False

                print self.connected_phone1.name + " hears " + self.connected_phone1.hears

                self.connected_phone1 = None
                self.connected_phone2 = None
                self.status = "onhook"
                self.hears = "silence"
                self.transfer = False
        elif self.conference:
            if self.hears == "talking":
                if self.connected_phone2 == None:
                    self.connected_phone1.connected_phone1 = self.connected_phone1.connected_phone2
                    self.connected_phone1.connected_phone2 = None
                    self.connected_phone1.connected_phone1.conference = False
                    self.connected_phone1.conference = False
                    self.conference = False

                    self.connected_phone1 = None
                    self.status = "onhook"
                    self.hears = "silence"
                else:
                    print self.connected_phone1.name + " and " + self.connected_phone2.name + " are " + self.hears

                    if self.name == self.connected_phone1.connected_phone1.name:
                        self.connected_phone1.connected_phone1 = self.connected_phone1.connected_phone2
                        self.connected_phone1.connected_phone2 = None
                    elif self.name == self.connected_phone1.connected_phone2.name:
                        self.connected_phone1.connected_phone2 = None

                    if self.name == self.connected_phone2.connected_phone1.name:
                        self.connected_phone2.connected_phone1 = self.connected_phone2.connected_phone2
                        self.connected_phone2.connected_phone2 = None
                    elif self.name == self.connected_phone2.connected_phone2.name:
                        self.connected_phone2.connected_phone2 = None

                    self.status = "onhook"
                    self.hears = "silence"
                    self.conference = False
                    self.connected_phone1.conference = False
                    self.connected_phone2.conference = False
                    self.connected_phone1 = None
                    self.connected_phone2 = None

                    print self.name + " hears " + self.hears
            elif self.hears == "ringback":
                self.connected_phone1.connected_phone1 = None
                self.connected_phone2.connected_phone1 = None

                self.connected_phone1.hears = "silence"
                self.connected_phone2.hears = "silence"

                print self.connected_phone1.name + " hears " + self.connected_phone1.hears

                self.status = "onhook"
                self.hears = "silence"
                self.conference = False
                self.connected_phone1.conference = False
                self.connected_phone2.conference = False
                self.connected_phone1 = None
                self.connected_phone2 = None
        else:
            if self.hears == "dialtone" or self.hears == "denial" or self.hears == "busy" or self.hears == "silence":
                self.status = "onhook"
                self.hears = "silence"
            elif self.hears == "ringback":
                self.connected_phone1.hears = "silence"
                self.connected_phone1.connected_phone1 = None
                self.connected_phone1 = None

                self.hears = "silence"
                self.status = "onhook"
            elif self.hears == "talking":
                self.connected_phone1.hears = "silence"

                print self.connected_phone1.name + " hears " + self.connected_phone1.hears

                self.connected_phone1.connected_phone1 = None
                self.connected_phone1 = None

                self.hears = "silence"
                self.status = "onhook"

    def transfer_response(self, phone2_state):
        if self.hears == "ringback":
            print self.name + " is already transfer calling " + self.connected_phone2.name              
        # REQ10
        elif phone2_state.status == "offhook" or phone2_state.hears == "ringing":
            self.hears = "busy"

            print self.name + " hears " + self.hears

            self.hears = "talking"
        else:
            self.connected_phone2 = phone2_state
            self.connected_phone2.connected_phone1 = self

            self.hears = "ringback"
            self.connected_phone2.hears = "ringing"

            print self.name + " hears " + self.hears
            print self.connected_phone2.name + " hears " + self.connected_phone2.hears

            self.transfer = True
            self.connected_phone2.transfer = True
            self.connected_phone1.transfer = True

            return 0

        return 1

    def conference_response(self, phone2_state):
        if self.hears == "ringback":
            print self.name + " is already conference calling " + self.connected_phone2.name              
        # REQ10
        elif phone2_state.status == "offhook" or phone2_state.hears == "ringing":
            self.hears = "busy"

            print self.name + " hears " + self.hears

            self.hears = "talking"
        else:
            self.connected_phone2 = phone2_state
            self.connected_phone2.connected_phone1 = self

            self.hears = "ringback"
            self.connected_phone2.hears = "ringing"

            print self.name + " hears " + self.hears
            print self.connected_phone2.name + " hears " + self.connected_phone2.hears

            self.conference = True
            self.connected_phone2.conference = True
            self.connected_phone1.conference = True

            return 0

        return 1

    # REQ11
    def denial_response(self):
        self.hears = "denial"

        print self.name + " hears " + self.hears

    # REQ11
    def denial_response2(self):
        self.hears = "denial"

        print self.name + " hears " + self.hears

        self.hears = "talking"