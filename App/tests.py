import unittest
import speech_recognition as sr
from Communication.SpeechIn import SpeechIn
from Communication import *

class MyFirstTests(unittest.TestCase):

    def test_input(self):
        self.assertEqual(SpeechIn(), "hey brian")