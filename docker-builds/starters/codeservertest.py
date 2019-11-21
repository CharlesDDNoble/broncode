from .codeserver import CodeServer
import unittest
from time import sleep
import warnings
import threading
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

    def thread_code_server(self,server):
        # filter out warnings about unclosed resources
        warnings.filterwarnings(action="ignore", message="unclosed", 
                         category=ResourceWarning)
        server.handle_connection(is_test=True)

    # ToDo: Set this test up to use mock object for socket connection
    
    def test_handle_connection(self):
        server = CodeServer('',0,None)
        server_thread = threading.Thread(target=self.thread_code_server,args=[server])
        server_thread.start()

        # wait until a port has been assigned to the server
        count = 100
        while not server.port and count > 0:
            count -= 1
            sleep(.1)

        # to see if a port was assigned
        self.assertTrue(server.port, "The server was not assigned a port by the OS before timeout!")
        
        socket.setdefaulttimeout(5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server.host,server.port))
        
        flags = "-g -O3"
        code = "print(\"Hello\")"
        inputs = ["INPUT_1","INPUT_2","INPUT_3"]
        num_inputs = str(len(inputs))

        # send all data to server
        sock.send(server.make_block(flags))
        sock.send(server.make_block(code))
        sock.send(server.make_block(num_inputs))
        for inp in inputs:
            sock.send(server.make_block(inp))

        # recv the outputs
        outputs = []
        for i in inputs:
            outputs += [sock.recv(server.BLOCK_SIZE).decode("utf-8").replace('\0','')]

        # test server recv
        self.assertEqual(server.flags,flags)
        self.assertEqual(server.code,code)
        self.assertEqual(server.num_inputs,num_inputs)
        for i in range(len(inputs)):
            self.assertEqual(server.inputs[i],inputs[i])

        # test server send
        self.assertEqual(len(outputs),len(inputs))        
        for i in range(len(outputs)):
            self.assertEqual(outputs[i],"OUTPUT_"+str(i))

        sock.close()
        server_thread.join()

if __name__ == '__main__':
    unittest.main()
