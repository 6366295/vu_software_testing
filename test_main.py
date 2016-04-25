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
        out = self.out.getvalue().strip()
        self.assertTrue(self.out.getvalue().strip())

    #Testing check_offhook
    #b1-b2
    def test8(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "offhook"
        self.phonebook[phone1].check_offhook()
        self.assertEqual(phone1 + " is already offhook", self.out.getvalue().strip())

    #Testing check_offhook
    #b1-b3
    def test9(self):
        phone1 = "foo"
        self.phonebook[phone1].status = "notoffhook"
        self.assertTrue(self.phonebook[phone1].check_offhook())




















