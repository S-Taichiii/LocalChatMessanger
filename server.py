import os
import socket

class ServerBase:
    def __init__(self, timeout: int = 60, buffer: int = 1024):
        self.socket = None
        self.timeout = timeout
        self.buffer = buffer
        self.close()

    def __del__(self):
        self.close()

    def close(self) -> None:
        try:
            print('Closing current connection.')
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    def accept(self, address, family: int, typ: int, proto: int) -> None:
        self.socket = socket.socket(family, typ, proto)
        self.socket.settimeout(self.timeout)
        self.socket.bind(address)
        self.socket.listen(1)
        print('Server started : ', address)
        connection, client_address = self.socket.accept()

        while True:
            data = connection.recv(self.buffer)
            data_str = data.decode('utf-8')

            if data:
                resp = self.respond(data_str)
                connection.sendall(resp.encode('utf-8'))
            else:
                print('No data from ', client_address)
                break

        self.close()

    def respond(self, message: str) -> str:
        return ""
    

class UnixServer(ServerBase):
    def __init__(self, path: str = 'server.sock'):
        self.server = path
        self.delete()
        super().__init__(timeout = 60, buffer = 1024)
        super().accept(self.server, socket.AF_UNIX, socket.SOCK_STREAM, 0)

    def __dell__(self):
        self.delete()

    def delete(self):
        if os.path.exists(self.server):
            os.remove(self.server)

    def respond(self, message: str) -> str:
        print("received ----> ", message)
        return 'Server accepted!!!'
    

if __name__ == '__main__':
    UnixServer()