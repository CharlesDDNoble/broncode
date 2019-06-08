from django.test import TestCase
from codehandler import CodeHandler

# Create your tests here.

class CodeHandlerTestCase(TestCase):
    def setUp(self):
        

    def test_make_block(self):
        # NO MESSAGE
        handler = CodeHandler(host = '', port = 4000, code = '', flags = '')
        msg = handler.make_block('')
        self.assertEqual(len(msg) == handler.BLOCK_SIZE)