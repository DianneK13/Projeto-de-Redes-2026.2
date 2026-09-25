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
tamanho_chunk = 1024



# Enviando a mensagem e aguardando a resposta

with open("arquivo.txt", 'rb') as arquivo: #abro o arquivo da mensagem que vai ser transmitida
    while True: 
        data = arquivo.read(tamanho_chunk) #leio até o tamanho bater o 1024 bytes
        if not data:
            break
        clientSocket.sendto(data, (serverName, int(serverPort)))
    clientSocket.sendto(b"", (serverName, int(serverPort))) #pacote vazio para reconhecer o fim da transmissão

# Cliente recebe uma resposta do servidor

    with open("cliente_recebe.txt", 'ab') as output: # abro o arquivo que recebe a mensagem que volta do servidor
        while True:
            encodedModified = clientSocket.recv(2048) 
            # Por que bufsize = 2048? # 
            # Já que os pacotes que o servidor vai
            # receber têm 1024 bytes, melhor garantir
            # com o dobro para não perder nada(BUF_SIZE)
            if not encodedModified: #recebe um pacote vazio, que representa o fim da mensagem
                break
            print("segmentou\n")
            output.write(encodedModified) # escrevo o pacote recebido do servidor no arquivo


#modifiedMessage = encodedModified.decode()
#print("server_ " + modifiedMessage)
print("client_ Compreensível. Tenha um bom dia!")
clientSocket.close()
print("client_ Conexão fechada.")
