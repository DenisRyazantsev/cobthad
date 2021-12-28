from unittest import TestCase

from Header import Header


class TestHeader(TestCase):

    def test_initLevel_belowZero_exceptionThrown(self):
        with self.assertRaises(ValueError):
            Header(-1, "test")

    def test_initLevel_OneHundred_noExceptionThrown(self):
        Header(100, "test")

    def test_initTitle_emptyString_exceptionThrown(self):
        with self.assertRaises(ValueError):
            Header(0, "")

    def test_initTitle_OneChar_noExceptionThrown(self):
        Header(0, "A")

    def test_getLevel_fifty_equal(self):
        test_level = 50
        header = Header(test_level, "test")

        self.assertEqual(header.get_level(), test_level)

    def test_getTitle_testTitle_equal(self):
        test_title = "test"
        header = Header(0, test_title)

        self.assertEqual(header.get_title(), test_title)
