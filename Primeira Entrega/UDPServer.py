from socket import *
from funcoes import *

# Cria socket UDP
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Atribui endereço IP e número de porta ao socket
serverSocket.bind(('', serverPort))
num_arquivo = 0

print("O servidor está a postos! Pronto para receber!")

while True:
    # Recebe o pacote do cliente junto com o endereço 
    # de onde ele está vindo.
    nome, clientAddress = serverSocket.recvfrom(tamanho_chunk)
    if nome:
        print(f"(servidor) arquivo {nome} recebido")
        tipo = definir_arquivo_nome(nome.decode())
        download = "arquivos/ServerMemory/" + "servidor_" + nome.decode()
        baixar(download, serverSocket)
        print("(servidor) armazenou o arquivo recebido.")
        enviar(download, clientAddress, serverSocket)
        print("(servidor) enviou o arquivo de volta.")
        num_arquivo = num_arquivo + 1