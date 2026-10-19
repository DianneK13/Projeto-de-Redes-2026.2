from socket import *

class RDTServer:

  BLOCK_LEN = 1024

  def __init__(self, serverPort):
    self.socket = socket(AF_INET, SOCK_DGRAM)
    # Atribui endereço IP e número de porta ao socket
    self.socket.bind(('', int(serverPort)))

  def sendBuffer(self, buffer, destination):
    self.socket.sendto(buffer, destination)
  
  def receiveBuffer(self):
    buffer, clientAddress = self.socket.recvfrom(self.BLOCK_LEN)
    return buffer, clientAddress

  def close(self):
    self.socket.close()
  
  def payload(self):
    return self.BLOCK_LEN  