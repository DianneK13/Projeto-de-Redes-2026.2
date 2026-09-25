tamanho_chunk = 1024


def enviar(arquivo, destino, socket):
    with open(arquivo, 'rb') as output: #abro o arquivo da mensagem que vai ser transmitida
        while True: 
            data = output.read(tamanho_chunk) #leio até o tamanho bater o 1024 bytes
            if not data:
                break
            socket.sendto(data, destino)
        socket.sendto(b"", destino) #pacote vazio para reconhecer o fim da transmissão

def baixar(arquivo, socket):
    message, clientAddress = socket.recvfrom(tamanho_chunk)
    if message:
        count = 1
        with open(arquivo, 'wb') as output: #abro o arquivo que vai salvar a mensagem transmitida pelo servidor
            output.write(message)
            while True:
                message, clientAddress = socket.recvfrom(tamanho_chunk) 
                if not message: #recebe o pacote vazio
                    break
                count = count+1
                output.write(message)
        print(f"arquivo foi segmentado {count} vezes")
        return clientAddress

def definir_arquivo(tipo):
    if tipo == "txt":
        return ".txt"
    if tipo == "png":
        return ".png"

def definir_arquivo_nome(nome):
    arquivo = nome.split(".")
    return arquivo[-1]