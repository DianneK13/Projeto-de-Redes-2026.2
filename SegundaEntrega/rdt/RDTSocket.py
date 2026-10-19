from socket import AF_INET, SOCK_DGRAM, socket as create_socket

class RDTSocket:

  BLOCK_LEN = 1024

  TIMEOUT = 10

  def __init__(self, socket):
    self.socket = socket

  @classmethod
  def client(cls, serverName, serverPort):
    # Cria socket UDP
    sock = create_socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(cls.TIMEOUT)
    client = cls(sock)
    client.serverName = serverName
    client.serverPort = int(serverPort)
    return client

  @classmethod
  def server(cls, serverPort):
    sock = create_socket(AF_INET, SOCK_DGRAM)
    # Atribui endereço IP e número de porta ao socket
    sock.bind(('', int(serverPort)))
    return cls(sock)

  def sendBuffer(self, buffer, clientAddress):
    self.socket.sendto(buffer, (self.serverName, self.serverPort))
  
  def receiveBuffer(self):
    buffer, clientAddress = self.socket.recvfrom(self.BLOCK_LEN)
    return buffer, clientAddress

  def close(self):
    self.socket.close()
  
  def payload(self):
    return self.BLOCK_LEN                                                                   