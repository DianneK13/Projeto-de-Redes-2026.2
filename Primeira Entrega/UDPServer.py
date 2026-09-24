#
#  UDPServer.py
#  Primeira Entrega
#
#  Created by Maria Clara Rodrigues de Almeida on 23/09/26.
#

from socket import *

# Cria socket UDP
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Atribui endereço IP e número de porta ao socket
serverSocket.bind(('', serverPort))

print("O servidor está a postos! Pronto para receber!")

while True:
    # Recebe o pacote do cliente junto com o endereço 
    # de onde ele está vindo.
    message, clientAddress = serverSocket.recvfrom(2048) # Por que bufsize = 2048? # 
                                                         # Já que os pacotes que o servidor vai
                                                         # receber têm 1024 bytes, melhor garantir
                                                         # com o dobro para não perder nada

    # Abaixo devemos implementadar a lógica de 
    # reconstrução, armazenamento e devolução 
    # do arquivo para o cliente

    # TESTE DE COMUNICAÇÃO FUNCIONANDO #
    modifiedMessage = message.decode()
    print("client_ " + modifiedMessage)

    response = "Quero não"
    print("server_ " + response)
    serverSocket.sendto(response.encode(), clientAddress)
