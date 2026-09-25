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
num_arquivo = 0


print("O servidor está a postos! Pronto para receber!")

while True:
    # Recebe o pacote do cliente junto com o endereço 
    # de onde ele está vindo.
    nome, clientAddress = serverSocket.recvfrom(tamanho_chunk)
    if nome:
        tipo = funcoes.definir_arquivo_nome(nome.decode())
        download = "arquivos/" + "servidor_" + nome.decode()
        funcoes.baixar(download, serverSocket)
        funcoes.enviar(download, clientAddress, serverSocket)
        num_arquivo = num_arquivo + 1

    # Abaixo devemos implementadar a lógica de 
    # reconstrução, armazenamento e devolução 
    # do arquivo para o cliente

    # TESTE DE COMUNICAÇÃO FUNCIONANDO #
    #modifiedMessage = message.decode()
    #print("client_ " + modifiedMessage)

    print("server_mensagem recebida" )
