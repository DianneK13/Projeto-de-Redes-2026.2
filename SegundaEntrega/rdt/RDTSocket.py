import random
import struct
import time
from socket import AF_INET, SOCK_DGRAM, gethostbyname, timeout, socket as create_socket

class RDTSocket:

  BLOCK_LEN = 1024

  TIMEOUT = 0.1 #em segundos
  MAX_RETRIES = 15 #retransmissões antes de desistir do pacote

  #simulação de canal não confiável (probabilidades entre 0 e 1)
  LOSS_PROB = 0.1
  CORRUPT_PROB = 0.1

  # cabeçalho: tipo, seq, checksum
  HEADER = struct.Struct('!BBH')
  HEADER_LEN = HEADER.size
  #campo "tipo" do cabeçalho vai ser 0 se pacote contém dados, 1 se é um ACK
  DATA = 0 
  ACK = 1

  def __init__(self, socket, peer=None):
    self.socket = socket
    self.peer = peer #endereço do outro lado da comunicação
    self.ctrlSend = True #True: próximo pacote enviado tem seq 0
    self.ctrlRcv = True #True: espera receber pacote com seq 0

  #@classmethod simula dois inits. Um pra inicializar socket do tipo cliente e outro pra tipo servidor
  @classmethod
  def client(cls, serverName, serverPort):
    #cria socket UDP do cliente
    sock = create_socket(AF_INET, SOCK_DGRAM)
    #resolve o nome para comparar com o endereço devolvido pelo recvfrom
    return cls(sock, (gethostbyname(serverName), int(serverPort)))

  @classmethod
  def server(cls, serverPort):
    #cria socket UDP do servidor
    sock = create_socket(AF_INET, SOCK_DGRAM)
    #atribui endereço IP e número de porta ao socket
    sock.bind(('', int(serverPort)))
    return cls(sock)

  def rdtSend(self, data):
    seq = 0 if self.ctrlSend else 1 #fica alternando número de seq
    sndpkt = self._makePkt(self.DATA, seq, data)
    self.udtSend(sndpkt)
    deadline = time.monotonic() + self.TIMEOUT #calcula até quando vai esperar o ack
    retries = 0

    # Espera por ACK
    while True:
      try:
        restante = deadline - time.monotonic()
        if restante <= 0:
          raise timeout

        self.socket.settimeout(restante) #fica sempre atualizando o timer
        rcvpkt, addr = self.udtRcv()

      except timeout:
        print("TIMEOUT!!!!!!!!!!!!!!")
        #se der timeout, manda dnv e reinicia o timer (a não ser q o limite de retransmissões seja atingido)
        if retries == self.MAX_RETRIES:
          return False #outro lado não responde mais
          print("número de tentativas chegou ao limite.")

        retries += 1
        print(f"retries = {retries}")
        self.udtSend(sndpkt)
        print("retransmitindo pacote...")
        deadline = time.monotonic() + self.TIMEOUT
        continue

      if addr != self.peer:
        #novo cliente chegou: o anterior já terminou e só perdeu o último ACK
        return False

      #se chegou aqui é pq recebeu um pacote e agora vai extrair o conteúdo dele
      pkt = self._parse(rcvpkt)
      if pkt is None:
        continue #pacote corrompido (não faz nada, só vai retransmitir se der timeout)

      tipo, rcvseq, _ = pkt
      if tipo == self.ACK and rcvseq == seq:
        print(f"ACK {rcvseq} chegou.")
        break #ack certo chegou (vai sair do loop e consequentemente parar o timer)

      ultimo = 1 if self.ctrlRcv else 0
      if tipo == self.DATA and rcvseq == ultimo:
        #situação de troca. lado que antes estava esperando o último ack agora é o receptor.
        #ack se perdeu, ent esse outro lado manda pacote com dados e com o último ack esperado
        #reenvia ack com último número de sequencia
        self.udtSend(self._makePkt(self.ACK, ultimo))
      #ACK errado (não faz nada, só vai retransmitir se der timeout)

    self.ctrlSend = not self.ctrlSend #inverter nseq
    return True

  def rdtRcv(self):
    self.socket.settimeout(None) #receptor não tem timer
    while True:
      rcvpkt, addr = self.udtRcv()
      if addr != self.peer:
        #servidor descobre o endereço do cliente pelo pacote recebido
        #novo cliente: sequências recomeçam do 0
        self.peer = addr
        self.ctrlSend = self.ctrlRcv = True

      esperado = 0 if self.ctrlRcv else 1
      pkt = self._parse(rcvpkt)

      if pkt is not None:
        tipo, seq, data = pkt
        if tipo == self.ACK:
          continue #não é pro receptor receber ACK. se receber, é ACK atrasado de um envio já concluído
        if seq == esperado:
          break

      #se chegou aqui, ou pkt é None (corrompido) ou seq != esperado (duplicado). Reenvia último ACK
      self.udtSend(self._makePkt(self.ACK, 1 - esperado))
      print(f"reenviando último ACK ({1 - esperado})")

    #se chegou aqui, recebeu o pacote certo. Manda ACK dele
    self.udtSend(self._makePkt(self.ACK, esperado))
    print(f"ACK {esperado} enviado.")
    self.ctrlRcv = not self.ctrlRcv #inverte nseq
    return data

  def udtSend(self, pkt):
    if random.random() < self.LOSS_PROB: #simular perda
      return #pacote perdido (retorna None)

    if random.random() < self.CORRUPT_PROB: #simular corrupção
      pkt = bytearray(pkt)
      pkt[random.randrange(len(pkt))] ^= 0xFF #inverte os bits de um byte

    self.socket.sendto(pkt, self.peer)

  def udtRcv(self):
    return self.socket.recvfrom(self.BLOCK_LEN)

  def _makePkt(self, tipo, seq, data=b""): #se não for passado data ele faz pacote sem payload
    checksum = self._checksum(self.HEADER.pack(tipo, seq, 0) + data) #faz calculo com header com checksum zerado
    return self.HEADER.pack(tipo, seq, checksum) + data

  def _parse(self, pkt):
    #retorna (tipo, seq, data) ou None se o pacote estiver corrompido
    if len(pkt) < self.HEADER_LEN:
      return None
    tipo, seq, checksum = self.HEADER.unpack(pkt[:self.HEADER_LEN])
    data = pkt[self.HEADER_LEN:]
    if checksum != self._checksum(self.HEADER.pack(tipo, seq, 0) + data):
      return None #retorna None se checksum não bate, pra indicar q o pacote foi corrompido
    return tipo, seq, data

  @staticmethod
  def _checksum(pkt):
    #soma de palavras de 16 bits em complemento de 1
    if len(pkt) % 2:
      pkt += b"\0" #adiciona um byte caso o número seja ímpar
    soma = 0
    for i in range(0, len(pkt), 2):
      soma += (pkt[i] << 8) | pkt[i + 1]
      soma = (soma & 0xFFFF) + (soma >> 16)
    return ~soma & 0xFFFF

  def close(self):
    self.socket.close()

  def payload(self):
    return self.BLOCK_LEN - self.HEADER_LEN
