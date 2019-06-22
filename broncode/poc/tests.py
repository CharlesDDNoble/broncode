from django.test import TestCase
from .codehandler import CodeHandler
import socket

# Create your tests here.

class CodeHandlerTestCase(TestCase):
    def setUp(self):
        pass

    def test_make_block(self):
        handler = CodeHandler(host = '', port = 4000, code = '', flags = '')
        
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

    def test_handle_connection(self):
        #set-up a mock server for handler to connect to
        
        #TODO: need to spawn separate thread for the server
        #should move this server set up code to some other method

        #TODO: Test these cases:
        #   inf-loop: should timeout
        #   good code: should output expected value
        #   error in code: should output correct error statement
        host = ''
        port = 7000
        msg = ''
        handler = CodeHandler(host = host, port = port, code = '', flags = '')
        socket.setdefaulttimeout(handler.max_time)
        BLOCK_SIZE = 4096 #senc/recv message size
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        err = 'There was an undefined error in the test_handle_connection\n'

        try:
            #set up server socket
            serversocket.bind((host, port))
            serversocket.listen(1) # become a server socket, maximum 1 connections    
        except OSError as ose:
            serversocket.close()
            serversocket = 0
            print(err+str(ose))
        except Exception as ex:
            serversocket.close()
            serversocket = 0
            print(err+str(ex))
        
        if serversocket:
            log = handler.handle_connection()
            #TODO: write code to verify output