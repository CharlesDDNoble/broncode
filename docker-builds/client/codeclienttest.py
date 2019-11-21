from .codeclient import CodeClient
import unittest
import os

class CodeClientTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_make_block(self):
        handler = CodeClient(host = '', port = 4000, code = '', flags = '')
        
        # NO MESSAGE
        inp = b''
        exp = b'\0'*handler.BLOCK_SIZE
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE < BLOCK_SIZE
        inp = b'Hello'
        exp = b'Hello' + b'\0'*(handler.BLOCK_SIZE-5)
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE == BLOCK_SIZE
        inp = b'A'*handler.BLOCK_SIZE
        exp = b'A'*handler.BLOCK_SIZE
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE > BLOCK_SIZE
        inp = b'B'*(handler.BLOCK_SIZE+10)
        exp = b'B'*handler.BLOCK_SIZE
        out = handler.make_block(inp)
        self.assertEqual(len(out),handler.BLOCK_SIZE)
        self.assertEqual(out,exp)

    def thread_code_client():
        pass

    def test_handle_connection(self):
        server = CodeServer('',0,None)
        server_thread = threading.Thread(target=self.thread_handle_connection,args=[server])
        server_thread.start()

if __name__ == '__main__':
    unittest.main()
