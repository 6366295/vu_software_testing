import unittest
from phone import Phonebook

class MyTest(unittest.TestCase):
    def setUp(self):
        #setup before tests
        
    def tearDown(self):
        #cleanup after tests
    
    def test(self):
           phonebook = Phonebook.__new__(Phonebook)
           phonebook.parse_phonebook("phonebok.txt")
           
    def test2(self):
           phonebook = Phonebook.__new__(Phonebook)
           phonebook.parse_phonebook("phonebo.txt")
            
           
        


