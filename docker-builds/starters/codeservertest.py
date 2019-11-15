from .codeserver import CodeServer
import unittest

from time import sleep
import socket
import signal
import socket

class CodeServerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_timeout(self):
        server = CodeServer(0,0,None)
        server.max_time = 1
        
        signal.signal(signal.SIGALRM, server.alarm_handler)
        
        has_timed_out = False

        try:
            signal.alarm(server.max_time)
            sleep(5)
        except TimeoutError:
            has_timed_out = True

        self.assertTrue(has_timed_out)

    def test_make_block(self):
        server = CodeServer(0,0,None)
        
        # NO MESSAGE
        inp = b''
        exp = b'\0'*server.BLOCK_SIZE
        out = server.make_block(inp)
        self.assertEqual(len(out),server.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE < BLOCK_SIZE
        inp = b'Hello'
        exp = b'Hello' + b'\0'*(server.BLOCK_SIZE-5)
        out = server.make_block(inp)
        self.assertEqual(len(out),server.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE == BLOCK_SIZE
        inp = b'A'*server.BLOCK_SIZE
        exp = b'A'*server.BLOCK_SIZE
        out = server.make_block(inp)
        self.assertEqual(len(out),server.BLOCK_SIZE)
        self.assertEqual(out,exp)

        # MESSAGE > BLOCK_SIZE
        inp = b'B'*(server.BLOCK_SIZE+10)
        exp = b'B'*server.BLOCK_SIZE
        out = server.make_block(inp)
        self.assertEqual(len(out),server.BLOCK_SIZE)
        self.assertEqual(out,exp)

    # ToDo: Set this test up to use mock object for socket connection
    def test_handle_connection(self):
        pass

if __name__ == '__main__':
    unittest.main()
