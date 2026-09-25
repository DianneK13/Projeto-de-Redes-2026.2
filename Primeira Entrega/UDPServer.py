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
tamanho_chunk = 1024


print("O servidor está a postos! Pronto para receber!")

while True:
    # Recebe o pacote do cliente junto com o endereço 
    # de onde ele está vindo.
    with open("download.txt", 'ab') as output: #abro o arquivo que vai salvar a mensagem transmitida pelo servidor
        while True:
            message, clientAddress = serverSocket.recvfrom(2048) # Por que bufsize = 2048? # 
                                                                 # Já que os pacotes que o servidor vai
                                                                 # receber têm 1024 bytes, melhor garantir
                                                                 # com o dobro para não perder nada(BUF_SIZE)
            if not message: #recebe o pacote vazio
                break
            print("Segmentou\n")
            output.write(message)

    with open("arquivo.txt", 'rb') as arquivo: #mesma lógica da parte do cliente para enviar
        while True:
            data = arquivo.read(tamanho_chunk)
            if not data:
                break
            serverSocket.sendto(data, clientAddress)
        serverSocket.sendto(b"", clientAddress)

    # Abaixo devemos implementadar a lógica de 
    # reconstrução, armazenamento e devolução 
    # do arquivo para o cliente

    # TESTE DE COMUNICAÇÃO FUNCIONANDO #
    #modifiedMessage = message.decode()
    #print("client_ " + modifiedMessage)

    print("server_mensagem recebida" )
