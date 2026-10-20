from socket import AF_INET, SOCK_DGRAM, socket as create_socket
from rdt.FSMTransmissor import FSM_Transmissor
from rdt.FSMReceptor import FSM_Receptor

class RDTSocket:

  BLOCK_LEN = 1024

  TIMEOUT = 10

  def __init__(self, socket, peer=None):
    self.socket = socket
    self.peer = peer # endereço do outro lado da comunicação
    self.transmissor = FSM_Transmissor(self)
    self.receptor = FSM_Receptor(self)

  @classmethod
  def client(cls, serverName, serverPort):
    # Cria socket UDP
    sock = create_socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(cls.TIMEOUT)
    return cls(sock, (serverName, int(serverPort)))

  @classmethod
  def server(cls, serverPort):
    sock = create_socket(AF_INET, SOCK_DGRAM)
    # Atribui endereço IP e número de porta ao socket
    sock.bind(('', int(serverPort)))
    return cls(sock)

  def rdtSend(self, buffer):
    self.socket.sendto(buffer, self.peer)
  
  def rdtReceive(self):
    # Servidor descobre o endereço do cliente pelo pacote recebido
    buffer, self.peer = self.socket.recvfrom(self.BLOCK_LEN)
    return buffer

  def close(self):
    self.socket.close()
  
  def payload(self):
    return self.BLOCK_LEN
