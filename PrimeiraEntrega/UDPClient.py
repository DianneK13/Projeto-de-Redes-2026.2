from socket import *
from funcoes import *

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