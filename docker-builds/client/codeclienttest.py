from .codeclient import CodeClient
import unittest
import threading
import warnings
import signal
import socket
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

    def thread_code_client(self,client):
        warnings.filterwarnings(action="ignore", 
                                message="unclosed", 
                                category=ResourceWarning)
        client.run()
        pass

    def alarm_handler(self, signum, frame):
        raise TimeoutError('Timeout!')

    # ToDo: add test for infinite loop i.e. the server does not send back before timeout
    def test_handle_connection(self):
        # set up server socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('', 0))
        port = serversocket.getsockname()[1]
        serversocket.listen(1) # become a server socket, maximum 1 connections
    
        code = "print(\"Hello\")"
        flags = "-g -O3"
        inputs = ["INPUT_0","INPUT_1","INPUT_2"]

        client = CodeClient('',port,code,flags,inputs)
        client_thread = threading.Thread(target=self.thread_code_client,args=[client])
        client_thread.start()

        signal.signal(signal.SIGALRM, self.alarm_handler)
        signal.alarm(5)
        connection, address = serversocket.accept()
        
        # reset alarm
        signal.alarm(10)

        # recv flags code num_inputs inputs
        client_flags = connection.recv(client.BLOCK_SIZE).replace(b'\0',b'').decode("utf-8")
        client_code = connection.recv(client.BLOCK_SIZE).replace(b'\0',b'').decode("utf-8")
        client_num_inputs = int(connection.recv(client.BLOCK_SIZE).replace(b'\0',b'').decode("utf-8"))
        client_inputs = []
        for i in range(client_num_inputs):
            client_inputs += [connection.recv(client.BLOCK_SIZE).replace(b'\0',b'').decode("utf-8")]
        
        # send comp log and outputs
        comp_log = "COMPILATION LOG\n"
        connection.send(client.make_block(comp_log))
        
        # send run logs
        run_logs = []
        for i in range(client_num_inputs):
            run_logs += ["OUTPUT_"+str(i)]
            connection.send(client.make_block(run_logs[i]))
        serversocket.close()

        client_thread.join()

        # check that all messages were sent properly
        self.assertEqual(code,client_code)
        self.assertEqual(flags,client_flags)
        self.assertEqual(len(inputs),client_num_inputs)
        self.assertEqual(comp_log,client.compilation_log)
        for i in range(len(run_logs)):
            self.assertEqual(run_logs[i],client.run_logs[i])

        # build the final expected log
        exp_log = comp_log
        for i in range(len(inputs)):
            exp_log += "Input: " + inputs[i] + "\n"
            exp_log += "Output: \n" + run_logs[i] + "\n"

        self.assertEqual(exp_log,client.log)


if __name__ == '__main__':
    unittest.main()
