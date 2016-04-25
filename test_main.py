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
        self.user_commands.cmd_call(phone1=phone1, phone2="bar")
        self.assertEqual(phone1 +  " does not exist!", self.out.getvalue().strip())
    
    #Testing cmd_call 
    #b1-b2-b3-b5-b10
    def test2(self):
        phone1 = "foo"
        self.user_commands.cmd_call(phone1=phone1, phone2="bar")
        self.assertEqual(phone1 +  " hears silence", self.out.getvalue().strip())
    
    #Testing cmd_call
    #b1-b2-b3-b5-b6-b7-b10
    def test3(self):
        pass
        
        
        
           
            
           
        


