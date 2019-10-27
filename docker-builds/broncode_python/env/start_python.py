from executors.pythonexecutor import PythonExecutor
from codeserver import CodeServer


def main():
    # Modify these variables for the specific language
    host = ''
    port = 4001
    Executor = PythonExecutor
    
    server = CodeServer(host,port,Executor)
    server.handle_connection()

if __name__ == "__main__":
    main()
