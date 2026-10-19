from socket import *
from rdt.RDTServer import RDTServer

class RDTClient:

  BLOCK_LEN = RDTServer.BLOCK_LEN #tamanho do payload que vai ser enviado/recebido

  def __init__(self, serverName, serverPort, timeout=10):
    # Cria socket UDP
    self.serverName = serverName
    self.serverPort = int(serverPort) 
    self.socket = socket(AF_INET, SOCK_DGRAM)
    self.socket.settimeout(timeout)

    #self.nseq = 0

    #máquinas de estado de transmissor e receptor que ligam cliente e servidor
    #self.fsmTrans = FSM_Transmissor(self.socket, (serverName, int(serverPort)))
    #self.fsmRecp = FSM_Receptor(self.socket)

  def sendBuffer(self, buffer):
    #pega dado do buffer e passa pro servidor
    #IMPLEMENTAR RDT 3.0 AQUI!!!!!!!
    self.socket.sendto(buffer, (self.serverName, self.serverPort)) 
  
  def receiveBuffer(self):
    #recebe dados do servidor
    #IMPLEMENTAR RDT 3.0 AQUI!!!!
    buffer, clientAddress = self.socket.recvfrom(self.BLOCK_LEN)
    return buffer

  def close(self):
    self.socket.close()
  
  def payload(self):
    return self.BLOCK_LEN                                                                   