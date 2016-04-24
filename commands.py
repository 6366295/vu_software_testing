import sys

class UserCommands:
    def __init__(self, phonebook):
        self.phonebook = phonebook

        # REQ04
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
        sys.exit()

    def cmd_help(self, *args, **kwargs):
        pass

    # REQ14
    def cmd_status(self, *args, **kwargs):
        # Print the status of all phones and if applicable, who they are talking to
        print "\033[1m{0:5}\t| {1:12}\t| {2:8}| {3:9}| {4:14}|\033[0m".format("Number","Name","State","Hears", "Participant(s)")
        print 8*'-'+'+'+15*'-'+'+'+9*'-'+'+'+10*'-'+'+'+15*'-'+'+'+18*'-'
        for key, value in self.phonebook.iteritems():
            if value.transfer:
                trans_string = "transferring"
            elif value.conference:
                trans_string = "conferencing"
            else:
                trans_string = ""
            
            if value.connected_phone1 != None:
                print "{0:5}\t| {1:12}\t| {2:8}| {3:9}| {4:14}| {5}".format(key[0], key[1], value.status, value.hears, value.connected_phone1.name, trans_string)
            else:
                print "{0:5}\t| {1:12}\t| {2:8}| {3:9}| {4:14}| {5}".format(key[0], key[1], value.status, value.hears, "", trans_string)

            if value.connected_phone2 != None:
                print "{0:5}\t| {0:12}\t| {0:8}| {0:9}| {1:14}| {0}".format("", value.connected_phone2.name)

            # print key[0],"\t", key[1],"\t\t\t", value.status, value.hears, value.phone2, value.phone3, value.transfer, value.conference
            # print "\tState: ", value.status, value.hears, value.phone2, value.phone3, value.transfer, value.conference
            print "{0:5}\t| {0:12}\t| {0:8}| {0:9}| {0:14}| {0}".format("")
            print 8*'-'+'+'+15*'-'+'+'+9*'-'+'+'+10*'-'+'+'+15*'-'+'+'+18*'-'
            
        # print 80*'-'
        return

    def cmd_call(self, *args, **kwargs):
        phone1 = kwargs['phone1']
        phone2 = kwargs['phone2']

        if self.phonebook.has_key(phone1):
            phone1_state = self.phonebook[phone1]
        else:
            print phone1 + " does not exist!"

            return

        if phone1_state.check_onhook():
            if self.phonebook.has_key(phone2):
                phone1_state.call_response(self.phonebook[phone2])
            else:
                phone1_state.denial_response()

                return

        return

    def cmd_offhook(self, *args, **kwargs):
        # phone is taken offhook and dialtone should be played (responded)
        phone = kwargs['phone']

        if self.phonebook.has_key(phone):
            phone_state = self.phonebook[phone]
        else:
            print phone + " does not exist!"

            return

        if phone_state.check_offhook():
            phone_state.offhook_response()

        return

    def cmd_onhook(self, *args, **kwargs):
        # phone is put back on the hook, closing the call, other phone should be
        # notified if a call was active
        # TODO: onhooking while conference calling process is still in process
        #       apparently only the conference initiator will mess up if it onhooks while it started a conference call
        phone = kwargs['phone']

        if self.phonebook.has_key(phone):
            phone_state = self.phonebook[phone]
        else:
            print phone + " does not exist!"

            return

        if phone_state.check_onhook():
            phone_state.onhook_response()

        return

    def cmd_transfer(self, *args, **kwargs):
        # After phone1 and phone2 are talking:
        # transfers a call between phone1 and phone2 to a call between phone3 and 
        # phone2
        phone1 = kwargs['phone1']
        phone2 = kwargs['phone2']

        if self.phonebook.has_key(phone1):
            phone1_state = self.phonebook[phone1]
        else:
            print phone1 + " does not exist!"

            return

        if phone1_state.check_onhook():
            if phone1_state.check_transfer():
                if self.phonebook.has_key(phone2):
                    phone1_state.transfer_response(self.phonebook[phone2])
                else:
                    phone1_state.denial_response2()

                    return

        return

    def cmd_conference(self, *args, **kwargs):
        # After phone1 and phone2 are talking:
        # Either phone1 or phone2 conferences phone3, which is then added to the call
        # phone1 and phone2 and phone3 are talking.
        phone1 = kwargs['phone1']
        phone2 = kwargs['phone2']

        if self.phonebook.has_key(phone1):
            phone1_state = self.phonebook[phone1]
        else:
            print phone1 + " does not exist!"

            return

        if phone1_state.check_onhook():
            if phone1_state.check_conference():
                if self.phonebook.has_key(phone2):
                    phone1_state.conference_response(self.phonebook[phone2])
                else:
                    phone1_state.denial_response2()

                    return

        return