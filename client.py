import sys, os
import socket

class ClientBase:
    def __init__(self, timeout: int=60, buffer: int=1024):
        self.socket = None
        self.timeout = timeout
        self.buffer = buffer
        self.close()

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.close()
        except:
            pass

    def connect(self, address: str, family: int, type: int, proto: int):
        self.path = address
        self.socket = socket.socket(family, type, proto)
        self.socket.settimeout(self.timeout)

        try:
            self.socket.connect(self.path)
        except socket.error as e:
            print(f'{e}')
            sys.exit(1)

    def send(self, message: str=""):
        flag = False
        
        try:
            while True:
                if message == "":
                    m_send = input('Your input ----> ')
                else:
                    m_send = message
                    flag = True

                self.socket.sendall(m_send.encode('utf-8'))
                m_recv = self.socket.recv(self.buffer).decode('utf-8')
                print(m_recv)

                if flag:
                    break
        except TimeoutError as e:
            print(f'{e}')
        except BrokenPipeError as e:
            print(f'{e}')
        finally:
            print("Closing current connection")
            self.close()

class UnixClient(ClientBase):
    def __init__(self, path: str = 'server.sock'):
        self.path = path
        super().__init__()
        super().connect(self.path, socket.AF_UNIX, socket.SOCK_STREAM, 0)
        super().send()


if __name__ == "__main__":
    UnixClient()