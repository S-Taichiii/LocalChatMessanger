import os
import socket
from faker import Faker

class ServerBase:
    def __init__(self, timeout=60, buffer=1024):
        self.socket = None
        self.timeout = timeout
        self.buffer = buffer
        self.close()

    def close(self) -> None:
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    def accept(self, address, family: int, type: int, proto: int):
        self.socket = socket.socket(family, type, proto)
        self.socket.settimeout(self.timeout)
        self.socket.bind(address)
        print('This server is wating for connecting with client.')
        self.socket.listen(1)

        try:
            connection, _ = self.socket.accept()
            print(f"Succesfully connected!!!")
            
            while True:
                m_recv = connection.recv(self.buffer).decode('utf-8')

                if m_recv:
                    resp = self.respond(m_recv)
                    connection.sendall(resp.encode('utf-8'))
                else:
                    break

        except TimeoutError as e:
            print(f'{e}')
        except BrokenPipeError as e:
            print(f'{e}')
        except ConnectionResetError as e:
            print(f'{e}')
        finally:
            print('Closing current connection.')
            self.close()

    def respond(self, message: str="") -> str:
        return ""
    
class UnixServer(ServerBase):
    def __init__(self, path: str = 'server.sock'):
        self.path = path
        self.delete()
        super().__init__()
        super().accept(self.path, socket.AF_UNIX, socket.SOCK_STREAM, 0)

    def delete(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def respond(self, message: str):
        print(f'Input --------> {message}')
        
        fake = Faker()
        resp = 'Server accepted!!! fake_name: {}'.format(fake.name())
        return resp
    
if __name__ == '__main__':
    UnixServer()