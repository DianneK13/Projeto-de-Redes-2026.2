#
#  UDPClient.py
#  Primeira Entrega
#
#  Created by Maria Clara Rodrigues de Almeida on 23/09/26.
#

from socket import *

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
message = "Quer hamburguer?"

# Enviando a mensagem e aguardando a resposta
clientSocket.sendto(message.encode(),(serverName, int(serverPort)))
print("client_ " + message)

# Cliente recebe uma resposta do servidor
encodedModified, serverAddress = clientSocket.recvfrom(2048)

modifiedMessage = encodedModified.decode()
print("server_ " + modifiedMessage)
print("client_ Compreensível. Tenha um bom dia!")
clientSocket.close()
print("client_ Conexão fechada.")
