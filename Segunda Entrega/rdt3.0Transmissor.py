from socket import *
from funcoes import *

'''
# Cria socket UDP
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Atribui endereço IP e número de porta ao socket
serverSocket.bind(('', serverPort))
num_arquivo = 0

print("O servidor está a postos! Pronto para receber!")

while True:
    # Recebe o pacote do cliente junto com o endereço 
    # de onde ele está vindo.
    nome, clientAddress = serverSocket.recvfrom(tamanho_chunk)
    if nome:
        print(f"(servidor) arquivo {nome} recebido")
        tipo = definir_arquivo_nome(nome.decode())
        download = "arquivos/ServerMemory/" + "servidor_" + nome.decode()
        baixar(download, serverSocket)
        print("(servidor) armazenou o arquivo recebido.")
        enviar(download, clientAddress, serverSocket)
        print("(servidor) enviou o arquivo de volta.")
        num_arquivo = num_arquivo + 1
'''

class FSM_Transmissor:
  def __init__(self):
    self.estados = {
      "estado_espera_0_cima": self.estado_espera_0_cima,
      "estado_espera_1_cima": self.estado_espera_1_cima,
      "estado_espera_ACK0": self.estado_espera_ACK0,
      "estado_espera_ACK1": self.estado_espera_ACK1
    }
    self.estado_atual = "estado_espera_0_cima"

  def transicao(self, evento):
    if evento in ["recebeu_dados_0",
                  "recebeu_dados_1",
                  "timeout",
                  "recebeu_ACK0",
                  "recebeu_ACK1"  
                  ]: 
      self.estado_atual = self.estados[self.estado_atual](evento)
    else:
      print(f"evento inválido: {evento}")

  def estado_espera_0_cima(self, evento):
    if evento == "recebeu_dados_0":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_ACK0"

    return self.estado_atual

  def estado_espera_1_cima(self, evento):
    if evento == "recebeu_dados_1":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_ACK1"

    return self.estado_atual

  def estado_espera_ACK0(self, evento):
    if evento == "timeout":
      #CÓDIGO
      self.estado_atual = "estado_espera_ACK0"

    elif evento == "recebeu_ACK0":
      #CÓDIGO
      self.estado_atual = "estado_espera_1_cima"

    return self.estado_atual

  def estado_espera_ACK1(self, evento):
    if evento == "timeout":
      #CÓDIGO
      self.estado_atual = "estado_espera_ACK1"

    elif evento == "recebeu_ACK1":
      #CÓDIGO
      self.estado_atual = "estado_espera_0_cima"

    return self.estado_atual