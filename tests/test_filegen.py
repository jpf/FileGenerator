import unittest
from StringIO import StringIO
from filegenerator import FileGenerator


class TestFilegen(unittest.TestCase):
    def setUp(self):
        self.inputs = ['a', 'bb', 'ccc', 'dddd', 'eeeee', 'ffffff']
        self.f = FileGenerator()

    @unittest.skip('.read not implemented in this version')
    def old_test_stringio(self):
        si = StringIO()
        fg = self.f
        for i in self.inputs:
            si.write(i)
            fg.write(i)
        si.seek(0)
        expected = si.read()
        actual = fg.read()
        self.assertEqual(expected, actual)

    def test_stringio(self):
        si = StringIO()
        fg = self.f
        for i in self.inputs:
            si.write(i)
            fg.write(i)
        si.seek(0)
        expected = si.read()
        actual = ''
        for element in fg.read_generator():
            actual += element
        self.assertEqual(expected, actual)
