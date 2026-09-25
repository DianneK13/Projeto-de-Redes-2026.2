from socket import *
from funcoes import *

# Cria socket UDP
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(10)

# Enviando a mensagem e aguardando a resposta
nome = input("fale o nome do arquivo que você quer enviar: ")

clientSocket.sendto(nome.encode(),(serverName, int(serverPort)))
enviar("arquivos/" + nome, (serverName, int(serverPort)), clientSocket)
print("(cliente) enviou arquivo para o servidor.")
Address = baixar("arquivos/" + "cliente_" + nome, clientSocket)


print("client_ Compreensível. Tenha um bom dia!")
clientSocket.close()
print("client_ Conexão fechada.")