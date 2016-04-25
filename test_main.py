# python -m unittest test_main
import unittest
from commands import *
from phone import Phonebook 
from commands import UserCommands
import sys

class MyTest(unittest.TestCase):
    def setUp(self):
        #setup before tests
        self.phonebook = Phonebook()
        self.phonebook.parse_phonebook("phonebook.txt")
        self.user_commands = UserCommands(self.phonebook)
        
    def tearDown(self):
        #cleanup after tests
        pass
    
   #Testing cmd_call
   #b1-b2-b4
    def test(self):
        self.user_commands.cmd_call(phone1="foooooo", phone2="bar")
        
           
            
           
        


