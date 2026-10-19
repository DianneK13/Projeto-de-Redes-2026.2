from socket import *

class RDTServer:

  BLOCK_LEN = 1024 #tamanho do payload que vai ser enviado/recebido

  def __init__(self, serverPort):
    #cria socket UDP
    self.socket = socket(AF_INET, SOCK_DGRAM)
    # Atribui endereço IP e número de porta ao socket
    self.socket.bind(('', int(serverPort)))

  def sendBuffer(self, buffer, destination): 
    #envia dados para o destino (parametrizado pois não se sabe o endereço do cliente de antemão)
    #IMPLEMENTAR RDT 3.0 AQUI!!!!!!!!!
    self.socket.sendto(buffer, destination)
  
  def receiveBuffer(self):
    #recebe dados do cliente
    #IMPLEMENTAR RDT 3.0 AQUI!!!!!
    buffer, clientAddress = self.socket.recvfrom(self.BLOCK_LEN)
    return buffer, clientAddress

  def close(self):
    self.socket.close()
  
  def payload(self):
    return self.BLOCK_LEN  