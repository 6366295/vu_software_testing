# python -m unittest test_main
import unittest
from commands import *
from phone import Phonebook
from commands import UserCommands
import sys
from StringIO import StringIO

class MyTest(unittest.TestCase):
    def setUp(self):
        #setup before tests
        self.phonebook = Phonebook()
        self.phonebook.parse_phonebook("phonebook.txt")
        self.user_commands = UserCommands(self.phonebook)
        self.saved_out = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out

    def tearDown(self):
        #cleanup after tests
        sys.stdout = self.saved_out

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
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "busy"
        value = self.phonebook[phone1].call_response(self.phonebook[phone3])
        self.assertEqual(value, 1)
        self.assertEqual(phone1 + " already tried to call or have been talking before, onhook and then offhook to try again", self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b6-b8-b14
    def test16(self):
        phone1 = "foo"
        phone2 = "bar"
        phone3 = "test"
        self.phonebook[phone1].hears = "denial"
        value = self.phonebook[phone1].call_response(self.phonebook[phone3])
        self.assertEqual(value, 1)
        self.assertEqual(phone1 + " already tried to call or have been talking before, onhook and then offhook to try again", self.out.getvalue().strip())

    #Testing call_response
    #b1-b3-b5-b6-b7-b8-b14
    def test17(self):
        phone1 = "foo"
        phone2 = "bar"
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
        self.phonebook[phone1].state = "offhook"
        self.phonebook[phone1].conference = True
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)

    #Testing cmd_conference
    #b1-b2-b3-b5-b6-b7-b9
    def test26(self):
        phone1 = "foo"
        phone2 = "testtttt"
        self.phonebook[phone1].state = "offhook"
        self.phonebook[phone1].conference = True
        self.phonebook[phone1].hears = "talking"
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 + " hears denial", self.out.getvalue().strip())

    #Testing cmd_conference
    #b1-b2-b3-b5-b6-b10
    def test27(self):
        phone1 = "foo"
        phone2 = "test"
        self.phonebook[phone1].state = "offhook"
        self.phonebook[phone1].conference = False
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)

    #Testing cmd_conference
    #b1-b2-b3-b5-b10
    def test28(self):
        phone1 = "foo"
        phone2 = "test"
        self.phonebook[phone1].state = "onhook"
        self.phonebook[phone1].conference = False
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)

    #Testing cmd_conference
    #b1-b2-b4
    def test29(self):
        phone1 = "foooooooo"
        phone2 = "test"
        self.user_commands.cmd_conference(phone1=phone1, phone2=phone2)
        self.assertEqual(phone1 + " does not exist!", self.out.getvalue().strip())







