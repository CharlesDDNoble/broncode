from executors.cexecutor import CExecutor
from codeserver import CodeServer


def main():
    host = ''
    port = 4000
    Executor = CExecutor
    server = CodeServer(host,port,Executor)
    server.handle_connection()

if __name__ == "__main__":
    main()
