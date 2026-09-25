#
#  UDPServer.py
#  Primeira Entrega
#
#  Created by Maria Clara Rodrigues de Almeida on 23/09/26.
#

from socket import *
import funcoes
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
    
    clientAddress = funcoes.baixar("arquivos/download.txt", serverSocket)
    
    '''
    message, clientAddress = serverSocket.recvfrom(tamanho_chunk)
    if message:
        count = 1
        with open("arquivos/download.txt", 'wb') as output: #abro o arquivo que vai salvar a mensagem transmitida pelo servidor
            output.write(message)
            while True:
                message, clientAddress = serverSocket.recvfrom(tamanho_chunk) # Por que bufsize = 2048? # 
                                                                    # Já que os pacotes que o servidor vai
                                                                    # receber têm 1024 bytes, melhor garantir
                                                                    # com o dobro para não perder nada(BUF_SIZE)
                if not message: #recebe o pacote vazio
                    break
                count = count+1
                output.write(message)
        print("segmentou",count)
    '''
    funcoes.enviar("arquivos/download.txt", clientAddress, serverSocket)

    # Abaixo devemos implementadar a lógica de 
    # reconstrução, armazenamento e devolução 
    # do arquivo para o cliente

    # TESTE DE COMUNICAÇÃO FUNCIONANDO #
    #modifiedMessage = message.decode()
    #print("client_ " + modifiedMessage)

    print("server_mensagem recebida" )
