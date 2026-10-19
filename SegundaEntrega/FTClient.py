import sys
import random
from socket import *
from rdt.RDTClient import *
from util.FileReader import *
from util.FileWriter import *

class FTClient:

  def __init__(self, serverName, serverPort):
    self.rdtClient = RDTClient(serverName, serverPort)

  def sendFile(self, folder, fileName):
    encodedFileName = fileName.encode() #transformar nome do arquivo (txt) em bytes pra poder enviar

    #1. enviando nome do arquivo
    self.rdtClient.sendBuffer(encodedFileName)

    #2. enviando conteúdo do arquivo
    #Util.enviar(folder + fileName, (self.serverName, self.serverPort), self.clientSocket)
    fileReader = FileReader(folder + fileName, self.rdtClient.payload())

    buffer = fileReader.read_buffer()
    while buffer is not None:
      self.rdtClient.sendBuffer(buffer)
      buffer = fileReader.read_buffer()
    
    self.rdtClient.sendBuffer(b"") # sinaliza fim de arquivo com pacote vazio

  def receiveFile(self, fileName):
    fileWriter = FileWriter(fileName)

    count = 1
    buffer = self.rdtClient.receiveBuffer()
    while buffer:
      fileWriter.write_buffer(buffer)
      count += 1
      buffer = self.rdtClient.receiveBuffer()
    print(f"arquivo foi segmentado {count} vezes")

  def close(self):
    self.rdtClient.close()
    
def main():
  ftClient = FTClient("localhost", 12000)

  #lista de arquivos existentes
  arquivos = ['faroeste.txt', 'Megadeth.mp3', 'voce.png', 'zero.png'] 

  #usuário decide qual arquivo enviar
  print("arquivos:")
  for i in arquivos:
    print(f'\t{i}')
  nome = input("fale o nome do arquivo que você quer enviar: ")

  if not nome:
    nome = arquivos[random.randrange(len(arquivos))]
    print(f"arquivo escolhido: {nome}")

  #caso usuário digite um arquivo que não existe
  while nome not in arquivos:
    print(f'arquivo {nome} não existe.')
    print("arquivos:")
    for i in arquivos:
      print(f'\t{i}')
    nome = input("fale o nome do arquivo que você quer enviar: ")

  # cliente enviando a mensagem e aguardando a resposta do servidor
  ftClient.sendFile("arquivos/ClientMemory/", nome)
  print("(cliente) enviou arquivo para o servidor.")

  ftClient.receiveFile("arquivos/ClientMemory/" + "cliente_" + nome)
  print("(cliente) recebeu o arquivo de resposta do servidor")

  print("(cliente) Compreensível. Tenha um bom dia!")
  ftClient.close()
  print("(cliente) Conexão fechada.")

  return 0

if __name__ == "__main__":
  sys.exit(main())