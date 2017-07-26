import unittest

from hi_detector import HiDetector


class TestHiDetector(unittest.TestCase):
    def test_detects_english_hi(self):
        self.assertTrue(HiDetector.is_greeting("hi"))
        self.assertTrue(HiDetector.is_greeting("HI"))
        self.assertTrue(HiDetector.is_greeting("Hi"))
        self.assertTrue(HiDetector.is_greeting("hi!"))
        self.assertTrue(HiDetector.is_greeting("hi !!!"))
        self.assertTrue(HiDetector.is_greeting("hi :)"))
        self.assertTrue(HiDetector.is_greeting("hi."))
        self.assertTrue(HiDetector.is_greeting("hi?"))
        self.assertTrue(HiDetector.is_greeting("hi\/"))

        self.assertTrue(HiDetector.is_greeting("hello"))

    def test_detects_russian_hi(self):
        self.assertTrue(HiDetector.is_greeting("привет"))
        self.assertTrue(HiDetector.is_greeting("Привет"))
        self.assertTrue(HiDetector.is_greeting("Привет!"))
        self.assertTrue(HiDetector.is_greeting("привет !!!"))

    def test_dont_detect_generic_message(self):
        self.assertFalse(HiDetector.is_greeting("I dont think we should handle that"))
        self.assertFalse(HiDetector.is_greeting("So what?"))
        self.assertFalse(HiDetector.is_greeting("ok"))
        self.assertFalse(HiDetector.is_greeting("OK"))
        self.assertFalse(HiDetector.is_greeting("OK!"))

    def test_don_detect_massage_containing_hi(self):
        self.assertFalse(HiDetector.is_greeting("Hi! How about tomorrow?"))
        self.assertFalse(HiDetector.is_greeting("Newer say Hi!"))
        self.assertFalse(HiDetector.is_greeting("Newer say hi"))
        self.assertFalse(HiDetector.is_greeting("Is it hi or not?"))
