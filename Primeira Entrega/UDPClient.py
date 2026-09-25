#
#  UDPClient.py
#  Primeira Entrega
#
#  Created by Maria Clara Rodrigues de Almeida on 23/09/26.
#

from socket import *
import funcoes

# Cria socket UDP
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(10)
## ACIMA já temos o socket UDP do cliente implementado ##

## ABAIXO temos um teste de comunicação ##

# Posteriormente implementaremos a lógica de 
# reconstrução e armazenamento  
# do arquivo recebido do servidor

# Mensagem
tamanho_chunk = 1024



# Enviando a mensagem e aguardando a resposta
nome = input("fale o nome do arquivo que você quer enviar: ")

clientSocket.sendto(nome.encode(),(serverName, int(serverPort)))
funcoes.enviar("arquivos/" + nome, (serverName, int(serverPort)), clientSocket)
Address = funcoes.baixar("arquivos/" + "cliente_" + nome, clientSocket)


#modifiedMessage = encodedModified.decode()
#print("server_ " + modifiedMessage)
print("client_ Compreensível. Tenha um bom dia!")
clientSocket.close()
print("client_ Conexão fechada.")
