import sys
import socket

class ClientBase:
    def __init__(self, timeout=60, buffer=1024):
        self.socket = None
        self.address = None
        self.settimeout = timeout
        self.buffer = buffer


    def connect(self, address, family: int, type: int, proto: int):
        self.address = address
        self.socket = socket.socket(family, type, proto)
        self.socket.settimeout(self.settimeout)
        
        try:
            self.socket.connect(self.address)
        except socket.error as e:
            print(f"error: {e}")
            sys.exit(1)

    def send(self, message: str = "") -> None:
        flag = False

        try:
            while True:
                if message == "":
                    m_send = input("> ")
                else:
                    m_send = message
                    flag = True
                
                self.socket.send(m_send.encode('utf-8'))
                m_recv = self.socket.recv(self.buffer).decode('utf-8')
                self.received(m_recv)

                if flag:
                    break
        except TimeoutError:
            print('Socket timeout, ending listening for server messages')

        self.close()

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    def received(self, message: str):
        print(message)


class UnixCliend(ClientBase):
    def __init__(self, path: str= 'server.sock'):
        self.server = path
        super().__init__(timeout = 60, buffer = 1024)
        super().connect(self.server, socket.AF_UNIX, socket.SOCK_STREAM, 0)
        super().send()

if __name__ == '__main__':
    UnixCliend()
