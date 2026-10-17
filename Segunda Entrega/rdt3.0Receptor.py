from socket import *
from funcoes import *

'''
#lista de arquivos existentes
arquivos = ['faroeste.txt', 'Megadeth.mp3', 'voce.png', 'zero.png'] 

# Cria socket UDP
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(10)

#usuário decide qual arquivo enviar
print("arquivos:")
for i in arquivos:
  print(f'\t{i}')
nome = input("fale o nome do arquivo que você quer enviar: ")

#caso usuário digite um arquivo que não existe
while nome not in arquivos:
  print(f'arquivo {nome} não existe.')
  print("arquivos:")
  for i in arquivos:
    print(f'\t{i}')
  nome = input("fale o nome do arquivo que você quer enviar: ")

# cliente enviando a mensagem e aguardando a resposta do servidor
clientSocket.sendto(nome.encode(),(serverName, int(serverPort)))
enviar("arquivos/ClientMemory/" + nome, (serverName, int(serverPort)), clientSocket)
print("(cliente) enviou arquivo para o servidor.")
Address = baixar("arquivos/ClientMemory/" + "cliente_" + nome, clientSocket)
print("(cliente) recebeu o arquivo de resposta do servidor")

print("(cliente) Compreensível. Tenha um bom dia!")
clientSocket.close()
print("(cliente) Conexão fechada.")
'''

class FSM_Receptor:
  def __init__(self):
    self.estados = {
      "estado_espera_0_baixo": self.estado_espera_0_baixo,
      "estado_espera_1_baixo": self.estado_espera_1_baixo
    }
    self.estado_atual = "estado_espera_0_baixo"

  def transicao(self, evento):
    if evento in ["recebeu_0_corretamente",
                  "recebeu_1_corretamente",
                  "corrompido_ou_0_errado",  #estava esperando 1, veio 0
                  "corrompido_ou_1_errado"   #estava esperando 0, veio 1
                  ]: 
      self.estado_atual = self.estados[self.estado_atual](evento)
    else:
      print(f"evento inválido: {evento}")

  def estado_espera_0_baixo(self, evento):
    if evento == "recebeu_0_corretamente":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_1_baixo"

    elif evento == "corrompido_ou_1_errado":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_0_baixo"

    return self.estado_atual

  def estado_espera_1_baixo(self, evento):
    if evento == "recebeu_1_corretamente":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_0_baixo"

    elif evento == "corrompido_ou_0_errado":
      #CÓDIGO AQUI
      self.estado_atual = "estado_espera_1_baixo"

    return self.estado_atual
