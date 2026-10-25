from socket import AF_INET, SOCK_DGRAM, socket as create_socket
from rdt.FSMTransmissor import FSM_Transmissor
from rdt.FSMReceptor import FSM_Receptor

class RDTSocket:

  BLOCK_LEN = 1024

  TIMEOUT = 10

  TIMER = 1 # tempo até retransmitir (timeout do rdt 3.0)

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

  def udt_send(self, pacote):
    # Usado pelas FSMs para enviar pacotes pela rede
    self.socket.sendto(pacote, self.peer)

  def rdtSend(self, buffer):
    # Evento "de cima": a FSM monta e envia o pacote
    self.transmissor.transicao("rdt_send", buffer)

    # Loop de eventos: roda até chegar o ACK esperado
    anterior = self.socket.gettimeout()
    self.socket.settimeout(self.TIMER)
    while self.transmissor.estado_atual in ["estado_espera_ACK0", "estado_espera_ACK1"]:
      try:
        pacote, _ = self.socket.recvfrom(self.BLOCK_LEN)
        evento = self.eventoTransmissor(pacote)
      except TimeoutError:
        evento = "timeout"
      self.transmissor.transicao(evento)
    self.socket.settimeout(anterior)

  def eventoTransmissor(self, pacote):
    # Converte o pacote recebido em "recebeu_ACK0", "recebeu_ACK1" ou "recebeu_corrompido"
    #CÓDIGO AQUI
    pass

  def rdtReceive(self):
    # Servidor descobre o endereço do cliente pelo pacote recebido
    buffer, self.peer = self.socket.recvfrom(self.BLOCK_LEN)
    return buffer

  def close(self):
    self.socket.close()
  
  def payload(self):
    return self.BLOCK_LEN
