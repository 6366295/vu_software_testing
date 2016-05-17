# python -m unittest test_main
import unittest
from commands import *
from phone import Phonebook
from main import *
import sys
from StringIO import StringIO
import os

class MyTest(unittest.TestCase):
    def setUp(self):
        #setup before tests
        self.phonebook = Phonebook()
        self.phonebook.parse_phonebook("phonebook.txt")
        self.user_commands = UserCommands(self.phonebook)
        self.saved_out = sys.stdout
        self.saved_inn = sys.stdin
        self.out = StringIO()
        self.inn = StringIO()
        sys.stdout = self.out
        sys.stdin = self.inn

    def tearDown(self):
        #cleanup after tests
        sys.stdout = self.saved_out
        sys.stdinn = self.saved_inn

   #Testing cmd_call
   #b1-b2-b4
    def test(self):
        phone1 = "foooo"
        phone2 = "bar"
        self.user_commands.cmd_call(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 +  " does not exist!", self.out.getvalue().strip())

    # #Testing cmd_call
    # #b1-b2-b3-b5-b10
    def test2(self):
        phone1 = "foo"
        phone2 = "bar"
        self.user_commands.cmd_call(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 +  " hears silence", self.out.getvalue().strip())

    #Testing cmd_call
    #b1-b2-b3-b5-b6-b7-b10
    def test3(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].hears = "dialtone"
        self.user_commands.cmd_call(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 + " hears ringback\n"+phone2+" hears ringing", self.out.getvalue().strip())

    #  #Testing cmd_call
    #  #b1-b2-b3-b5-b6-b8
    def test4(self):
        phone1 = "foo"
        phone2 = "doesnotexist"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].hears = "dialtone"
        self.user_commands.cmd_call(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 +  " hears denial", self.out.getvalue().strip())

     #Testing check_conference
     #b1-b2
    def test5(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].hears = "dialtone"
        self.phonebook[phone1].check_conference()
        self.assertEqual(phone1 + " hears denial", self.out.getvalue().strip())

    #Testing check_conference
    #b1-b3-b4
    def test6(self):
        phone1 = "foo"
        self.phonebook[phone1].conference = True
        self.phonebook[phone1].check_conference()
        self.assertEqual(phone1 + " hears denial", self.out.getvalue().strip())

    #Testing check_conference
    #b1-b3-b5
    def test7(self):
        phone1 = "foo"
        self.phonebook[phone1].conference = False
        self.phonebook[phone1].check_conference()
        self.assertTrue(self.out.getvalue().strip())

    #Testing check_offhook
    #b1-b2
    def test8(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "offhook"
        self.assertFalse(self.phonebook[phone1].check_offhook())
        self.assertEqual(phone1 + " is already offhook", self.out.getvalue().strip())

    #Testing check_offhook
    #b1-b3
    def test9(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "notoffhook"
        self.assertTrue(self.phonebook[phone1].check_offhook())

    #Testing check_onhook
    #b1-b2-b3
    def test10(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "onhook"
        self.phonebook[phone1].hears = "ringing"
        self.assertFalse(self.phonebook[phone1].check_onhook())
        self.assertEqual(phone1 + " is being called, offhook to answer", self.out.getvalue().strip())

    #Testing check_onhook
    #b1-b2-b4-b5-b6
    def test11(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "onhook"
        self.phonebook[phone1].hears = "silence"
        self.assertFalse(self.phonebook[phone1].check_onhook())
        self.assertEqual(phone1 + " hears silence", self.out.getvalue().strip())

    #Testing check_onhook
    #b1-b2-b4-b7
    def test12(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "onhook"
        self.phonebook[phone1].hears = "notsilence"
        self.assertTrue(self.phonebook[phone1].check_onhook())

    #Testing call_response
    #b1-b2-b14
    ##
    def test13(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].hears = "ringback"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        value = self.phonebook[phone1].call_response(self.phonebook[phone2])
        self.assertEqual(value, 1)
        self.assertEqual(phone1 + " is already calling " + phone2, self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b4-b14
    def test14(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        value = self.phonebook[phone1].call_response(self.phonebook[phone3])
        self.assertEqual(value, 1)
        self.assertEqual(phone1 + " is already talking to " + phone2, self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b8-b14
    def test15(self):
        phone1 = "foo"
        phone3 = "test"
        self.phonebook[phone1].hears = "busy"
        value = self.phonebook[phone1].call_response(self.phonebook[phone3])
        self.assertEqual(value, 1)
        self.assertEqual(phone1 + " already tried to call or have been talking before, onhook and then offhook to try again", self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b6-b8-b14
    def test16(self):
        phone1 = "foo"
        phone3 = "test"
        self.phonebook[phone1].hears = "denial"
        value = self.phonebook[phone1].call_response(self.phonebook[phone3])
        self.assertEqual(value, 1)
        self.assertEqual(phone1 + " already tried to call or have been talking before, onhook and then offhook to try again", self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b6-b7-b8-b14
    def test17(self):
        phone1 = "foo"
        phone3 = "test"
        self.phonebook[phone1].hears = "silence"
        value = self.phonebook[phone1].call_response(self.phonebook[phone3])
        self.assertEqual(value, 1)
        self.assertEqual(phone1 + " already tried to call or have been talking before, onhook and then offhook to try again", self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b6-b7-b9-b11-b14
    def test18(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "notsilence"
        self.phonebook[phone2].status = "offhook"
        value = self.phonebook[phone1].call_response(self.phonebook[phone2])
        self.assertEqual(value, 1)
        self.assertEqual(self.phonebook[phone1].hears, "busy")
        self.assertEqual(phone1 + " hears busy", self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b6-b7-b9-b10-b11-b14
    def test19(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "notsilence"
        self.phonebook[phone2].status = "notoffhook"
        self.phonebook[phone2].hears = "ringing"
        value = self.phonebook[phone1].call_response(self.phonebook[phone2])
        self.assertEqual(value, 1)
        self.assertEqual(self.phonebook[phone1].hears, "busy")
        self.assertEqual(phone1 + " hears busy", self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b6-b7-b9-b10-b12-b14
    def test20(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "notsilence"
        self.phonebook[phone2].status = "notoffhook"
        self.phonebook[phone2].hears = "notringingordialtone"
        value = self.phonebook[phone1].call_response(self.phonebook[phone2])
        self.assertEqual(value, 1)

    #Testing call_response
    #b1-b3-b5-b6-b7-b9-b10-b12-b13
    def test21(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone2].status = "notoffhook"
        self.phonebook[phone1].hears = "dialtone"
        value = self.phonebook[phone1].call_response(self.phonebook[phone2])
        self.assertEqual(value, 0)
        self.assertEqual(self.phonebook[phone1].connected_phone1, self.phonebook[phone2])
        self.assertEqual(self.phonebook[phone1].hears, "ringback")
        self.assertEqual(self.phonebook[phone1].connected_phone1.hears, "ringing")
        self.assertEqual(self.phonebook[phone1].connected_phone1.connected_phone1, self.phonebook[phone1])
        self.assertEqual(phone1 + " hears " + self.phonebook[phone1].hears + "\n" +
        self.phonebook[phone1].connected_phone1.name + " hears " + self.phonebook[phone1].connected_phone1.hears, self.out.getvalue().strip())

    #Testing check_transfer
    #b1-b2
    def test22(self):
        phone1 = "foo"
        self.phonebook[phone1].hears = "nottalking"
        self.assertFalse(self.phonebook[phone1].check_transfer())
        self.assertEqual(phone1 + " hears denial", self.out.getvalue().strip())

    #Testing check_transfer
    #b1-b3-b4
    def test23(self):
        phone1 = "foo"
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone1].conference = True
        self.assertFalse(self.phonebook[phone1].check_transfer())
        self.assertEqual(phone1 + " hears denial", self.out.getvalue().strip())

    #Testing check_transfer
    #b1-b3-b5
    def test24(self):
        phone1 = "foo"
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone1].conference = False
        self.assertTrue(self.phonebook[phone1].check_transfer())

    #Testing cmd_conference
    #b1-b2-b3-b5-b6-b7-b8-b10
    def test25(self):
        phone1 = "foo"
        phone2 = "test"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].conference = True
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)

    #Testing cmd_conference
    #b1-b2-b3-b5-b6-b7-b9
    def test26(self):
        phone1 = "foo"
        phone2 = "testtttt"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].conference = True
        self.phonebook[phone1].hears = "talking"
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 + " hears denial", self.out.getvalue().strip())

    #Testing cmd_conference
    #b1-b2-b3-b5-b6-b10
    def test27(self):
        phone1 = "foo"
        phone2 = "test"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].conference = False
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)

    #Testing cmd_conference
    #b1-b2-b3-b5-b10
    def test28(self):
        phone1 = "foo"
        phone2 = "test"
        self.phonebook[phone1].status = "onhook"
        self.phonebook[phone1].conference = False
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)

    #Testing cmd_conference
    #b1-b2-b4
    def test29(self):
        phone1 = "foooooooo"
        phone2 = "test"
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 + " does not exist!", self.out.getvalue().strip())

    #Testing cmd_interpreter
    #b1-b3-b4-b8
    def test30(self):
        valid_cmd = "status"
        cmd_interpreter(valid_cmd, self.user_commands.cmd_dict)
        self.assertNotEqual("Wrong command or wrong use of the command", self.out.getvalue().strip())

    #Testing cmd_interpreter
    #b1-b3-b5-b6-b8
    def test31(self):
        x = "call"
        y = "status"
        cmd_interpreter(x + " " + y, self.user_commands.cmd_dict)


    #Testing cmd_interpreter
    #b1-b3-b5-b7-b8
    def test32(self):
        x = "call"
        phone1 = "test"
        phone2 = "foo"
        cmd_interpreter(phone1 + " " + x + " " + phone2, self.user_commands.cmd_dict)

    #Testing cmd_interpreter
    #b2
    def test33(self):
        cmd = "fdjsafadklfasdfs"
        cmd_interpreter(cmd, self.user_commands.cmd_dict)
        self.assertEqual("Wrong command or wrong use of the command", self.out.getvalue().strip())

    #Testing cmd_offhook
    #b1-b2-b3-b5-b6-b7
    def test34(self):
       phone1 = "foo"
       self.phonebook[phone1].status = "offhook"
       self.user_commands.cmd_offhook(phone=phone1)

    #Testing cmd_offhook
    #b1-b2-b4
    def test35(self):
        phone1 = "doesnotexist"
        self.user_commands.cmd_offhook(phone=phone1)
        self.assertEqual(phone1 + " does not exist!", self.out.getvalue().strip())

    #Testing cmd_onhook
    #b1-b2-b3-b5-b6-b7
    def test36(self):
       phone1 = "foo"
       self.phonebook[phone1].status = "onhook"
       self.user_commands.cmd_onhook(phone=phone1)

    #Testing cmd_onhook
    #b1-b2-b4
    def test37(self):
        phone1 = "doesnotexist"
        self.user_commands.cmd_onhook(phone=phone1)
        self.assertEqual(phone1 + " does not exist!", self.out.getvalue().strip())

    # #Testing cmd_reader()
    # #b1-b3
    # def test38(self):
    #     self.inn.write("command")
    #     self.inn.flush()
    #     self.assertEqual(cmd_reader(), "command")


    #Testing cmd_reader()
    #b1 - b2
    # def test39(self):
    #     pass


    #Testing cmd_transfer
    #b1-b2-b3-b5-b6-b7-b8-b10
    def test40(self):
        phone1 = "foo"
        phone2 = "test"
        self.phonebook[phone1].status = "onhook"
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        # self.phonebook[phone1].transfer_response(self.phonebook[phone2])
        self.user_commands.cmd_transfer(phone1=phone1, phone2=phone2)

    #Testing cmd_transfer
    #b1-b2-b4
    def test41(self):
        phone1 = "foooo"
        phone2 = "test"
        self.user_commands.cmd_transfer(phone1=phone1, phone2=phone2)
        self.assertEqual( phone1 + " does not exist!", self.out.getvalue().strip())

    #Testing cmd_transfer
    #b1-b2-b3-b5-b6-b7-b9
    def test42(self):
        phone1 = "foo"
        phone2 = "doesnotexist"
        phone3 = "test"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone3]
        self.user_commands.cmd_transfer(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 + " hears denial", self.out.getvalue().strip())


    #Testing conference_response
    #b1-b2-b7
    def test43(self):
        phone1 = "foo"
        phone2 = "test"
        phone3 = "bar"
        phone4 = "asdf"
        self.phonebook[phone1].hears = "ringback"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone3]
        self.phonebook[phone1].conference_response(self.phonebook[phone4])
        self.assertEqual(phone1 + " is already conference calling " + self.phonebook[phone1].connected_phone2.name, self.out.getvalue().strip())

    #Testing conference_response
    #b1-b3-b5-b7
    def test44(self):
        phone1 = "foo"
        phone2 = "test"
        phone3 = "bar"
        self.phonebook[phone1].hears = "notringback"
        self.phonebook[phone1].conference = True
        self.phonebook[phone2].status = "offhook"
        self.phonebook[phone2].hears = "talking"
        self.phonebook[phone2].conference = True
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone2].connected_phone1 = self.phonebook[phone1]
        self.phonebook[phone3].status = "offhook"
        self.phonebook[phone1].conference_response(self.phonebook[phone3])
        self.assertEqual(phone1 + " hears busy", self.out.getvalue().strip())
        self.assertEqual(self.phonebook[phone1].hears, "talking")

    #Testing conference_response
    #b1-b3-b4-b6
    def test45(self):
        phone1 = "foo"
        phone2 = "test"
        phone3 = "bar"
        self.phonebook[phone1].hears = "notringback"
        self.phonebook[phone1].conference = True
        self.phonebook[phone2].status = "offhook"
        self.phonebook[phone2].hears = "talking"
        self.phonebook[phone2].conference = True
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone2].connected_phone1 = self.phonebook[phone1]
        self.phonebook[phone3].status = "notoffhook"
        self.phonebook[phone3].hears = "notringing"
        self.phonebook[phone1].conference_response(self.phonebook[phone3])

        self.assertEqual(self.phonebook[phone1].connected_phone2, self.phonebook[phone3])
        self.assertEqual(self.phonebook[phone1].connected_phone2.connected_phone1, self.phonebook[phone1])
        self.assertEqual(self.phonebook[phone1].hears, "ringback")
        self.assertEqual(self.phonebook[phone1].connected_phone2.hears, "ringing")
        self.assertTrue(self.phonebook[phone1].conference)
        self.assertTrue(self.phonebook[phone1].connected_phone1.conference)
        self.assertTrue(self.phonebook[phone1].connected_phone2.conference)

    #Testing get_item
    #b1-b2-b4-b5
    def test46(self):
        self.assertTrue(self.phonebook.__getitem__("foo"))

    #Testing get_item
    #b1-b3
    def test47(self):
        self.assertEqual("Phone 'doesnotexist' does not exist in phonebook!", self.phonebook.__getitem__("doesnotexist"))

    #Testing has_key
    #b1-b2-b3-b4
    def test48(self):
       self.assertTrue(self.phonebook.has_key("foo"))

    # #Testing main
    # #b1-b2-b4-b5
    # def test49(self):
    #     sys.argv[1] = "phonebook.txt"
    #     main()

    #Testing offhook_response
    #b1-b2-b9
    def test50(self):
        phone1 = "foo"
        self.phonebook[phone1].hears = "notringingorsilence"
        self.assertEqual(self.phonebook[phone1].offhook_response(), 0)

    #Testing offhook_response
    #b1-b2-b3-b9
    def test51(self):
        phone1 = "foo"
        self.phonebook[phone1].hears = "silence"
        self.assertEqual(self.phonebook[phone1].offhook_response(), 0)
        self.assertEqual(self.phonebook[phone1].status, "offhook")
        self.assertEqual(self.phonebook[phone1].hears, "dialtone")
        self.assertEqual(phone1 + " hears dialtone", self.out.getvalue().strip())

    #Testing offhook_response
    #b1-b4-b5-b9
    def test52(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "ringing"
        self.phonebook[phone1].transfer = True
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].connected_phone1.connected_phone1 = self.phonebook[phone1]
        self.phonebook[phone1].connected_phone1.status = "offhook"
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone3]
        self.phonebook[phone3].status = "offhook"
        self.phonebook[phone3].connected_phone1 = self.phonebook[phone1]
        self.assertEqual(self.phonebook[phone1].offhook_response(), 0)
        self.assertEqual("bar hears silence\nfoo and foo are talking", self.out.getvalue().strip())

    #Testing offhook_response
    #b1-b4-b6-b8-b9
    def test53(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].hears = "ringing"
        self.phonebook[phone1].transfer = False
        self.phonebook[phone1].conference = False
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.assertEqual(self.phonebook[phone1].offhook_response(), 0)
        self.assertEqual(self.phonebook[phone1].status, "offhook")
        self.assertEqual(self.phonebook[phone1].hears, "talking")
        self.assertEqual(self.phonebook[phone1].name + " and " + self.phonebook[phone1].connected_phone1.name + " are " + self.phonebook[phone1].hears, self.out.getvalue().strip())


    #Testing offhook_response
    #b1-b4-b6-b7
    def test54(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "ringing"
        self.phonebook[phone1].transfer = False
        self.phonebook[phone1].conference = True
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone3]
        self.phonebook[phone2].connected_phone1 = self.phonebook[phone1]
        self.assertEqual(self.phonebook[phone1].offhook_response(), 0)
        self.assertEqual(self.phonebook[phone1].name + " and " + self.phonebook[phone1].connected_phone1.name + " and " + self.phonebook[phone1].connected_phone2.name + " are " + self.phonebook[phone1].hears, self.out.getvalue().strip())

    #Testing onhook_response
    #b1-b2-b4-b30
    def test55(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone1].transfer = True
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone2].connected_phone1 = self.phonebook[phone1]
        self.phonebook[phone2].connected_phone2 = self.phonebook[phone3]
        self.phonebook[phone2].hears = "talking"
        self.phonebook[phone1].onhook_response()
        self.assertEqual(phone2 + " hears silence", self.out.getvalue().strip())


    #Testing onhook_response
    #b1-b2-b5-b7-b10
    def test56(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "ringback"
        self.phonebook[phone1].transfer = True
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone3]
        self.phonebook[phone2].connected_phone1 = self.phonebook[phone1]
        self.phonebook[phone1].onhook_response()
        self.assertEqual(phone2 + " hears silence"  , self.out.getvalue().strip())

    #Testing onhook_respone
    #b1-b3-b21-b23-b24-b25-b26-b27
    def test57(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].transfer = False
        self.phonebook[phone1].conference = False
        self.phonebook[phone1].hears = "ringback"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].onhook_response()
        self.assertEqual(self.phonebook[phone1].status, "onhook")

    #Testing onhook_response
    #b1-b3-b21-b22-b30
    def test58(self):
        phone1 = "foo"
        self.phonebook[phone1].transfer = False
        self.phonebook[phone1].conference = False
        self.phonebook[phone1].hears = "dialtone"
        self.phonebook[phone1].onhook_response()
        self.assertEqual(self.phonebook[phone1].status, "onhook")
        self.assertEqual(self.phonebook[phone1].hears, "silence")

    #Testing onhook_response
    #b1-b3-b21-b23-b24-b25-b26-b28-b29
    def test59(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].transfer = False
        self.phonebook[phone1].conference = False
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].onhook_response()
        self.assertEqual(self.phonebook[phone1].status, "onhook")
        self.assertEqual(self.phonebook[phone1].hears, "silence")

    #Testing onhook_response
    #b1-b3-b6-b9-b12-b13-b16-b17-b20
    def test60(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].transfer = False
        self.phonebook[phone1].conference = True
        self.phonebook[phone1].hears = "talking"
        self.phonebook[phone2].hears = "talking"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone3]
        self.phonebook[phone2].connected_phone1 = self.phonebook[phone1]
        self.phonebook[phone3].connected_phone1 = self.phonebook[phone1]
        self.phonebook[phone1].onhook_response()
        self.assertEqual(phone2 + " and " + phone3 + " are talking" + "\n" + phone1 + " hears silence", self.out.getvalue().strip())

    #Testing onhook_response
    #b1-b3-b6-b8-b11
    def test61(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].transfer = False
        self.phonebook[phone1].conference = True
        self.phonebook[phone1].hears = "ringback"
        self.phonebook[phone2].hears = "talking"
        self.phonebook[phone3].hears = "talking"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone3]
        self.phonebook[phone2].connected_phone1 = self.phonebook[phone1]

        self.phonebook[phone1].onhook_response()
        self.assertEqual(phone2+" hears silence", self.out.getvalue().strip())

    #Testing transfer_response
    #b1-b2-b7
    def test62(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].hears = "ringback"
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone2]
        self.assertEqual(self.phonebook[phone1].transfer_response(self.phonebook[phone2]), 1)
        self.assertEqual(phone1 + " is already transfer calling " + phone2, self.out.getvalue().strip())

    #Testing transfer_response
    #b1-b3-b5-b7
    def test63(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].hears = "notringback"
        self.phonebook[phone1].connected_phone2 = self.phonebook[phone2]
        self.phonebook[phone2].status = "offhook"
        self.phonebook[phone1].transfer_response(self.phonebook[phone2])
        self.assertEqual(phone1 + " hears busy", self.out.getvalue().strip())

    #Testing transfer_response
    #b1-b3-b4-b6
    def test64(self):
        phone1 = "foo"
        phone2 = "bar"
        self.phonebook[phone1].hears = "notringback"
        self.phonebook[phone1].connected_phone1 = self.phonebook[phone2]
        self.phonebook[phone2].status = "hears"
        self.phonebook[phone1].transfer_response(self.phonebook[phone2])
        self.assertEqual(phone1 +" hears ringback\n"+phone2+" hears ringing", self.out.getvalue().strip())

    #Testing validate_name
    #b1-b2-b3
    def test65(self):
        name = "validname"
        self.assertTrue(self.phonebook.validate_name(name))

    #Testng validate_name
    #b1-b4
    def test66(self):
        name = "1231412"
        self.assertFalse(self.phonebook.validate_name(name))

    #Testing validate_number
    #b1-b2-b3
    def test67(self):
        num = "12345"
        self.assertTrue(self.phonebook.validate_number(num))

    #Testing validate_number
    #b1-b4
    def test68(self):
        num = "notdigit"
        self.assertFalse(self.phonebook.validate_number(num))





















