import unittest
from main import cmd_reader
from phone import Phonebook
from StringIO import StringIO
import sys

class MyTest(unittest.TestCase):
    def test(self):
       try: 
           out = StringIO()
           sys.stdout = out
           phonebook = Phonebook("phoneboo.txt")
           print(out.getvalue().strip())
       except Exception:
           print "error({0}): {1}".format(e.errno, e.strerror)


