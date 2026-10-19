import sys
from socket import *
from rdt.RDTServer import *
from util.FileReader import *
from util.FileWriter import *

class FTServer:
    def __init__(self, serverPort):
        self.rdtServer = RDTServer(serverPort)

    def receiveFile (self, path):
        # Recebe o pacote do cliente junto com o endereço 
        # de onde ele está vindo.
        #nome, clientAddress = self.serverSocket.recvfrom(Util.tamanho_chunk)
        nome, clientAddress = self.rdtServer.receiveBuffer()

        if nome:
            print(f"(servidor) arquivo {nome} recebido")
            #tipo  = Util.definir_arquivo_nome(nome.decode())
            download = path + nome.decode()
            fileWriter = FileWriter(download)

            #Util.baixar(download, self.serverSocket)
            buffer, clientAddress = self.rdtServer.receiveBuffer()
            while buffer:
                fileWriter.write_buffer(buffer)
                buffer, clientAddress = self.rdtServer.receiveBuffer()

            print("(servidor) armazenou o arquivo recebido.")
            return download, clientAddress

    def sendFile(self, fileName, clientAddress):
        #Util.enviar(fileName, clientAddress, self.serverSocket)
        fileReader = FileReader(fileName, self.rdtServer.payload())

        buffer = fileReader.read_buffer()
        while buffer is not None:
            self.rdtServer.sendBuffer(buffer, clientAddress)
            buffer = fileReader.read_buffer()
        
        self.rdtServer.sendBuffer(b"", clientAddress) # sinaliza fim de arquivo com pacote vazio

        print("(servidor) enviou o arquivo de volta.")

def main():

    ftServer = FTServer(12000)
    local = "arquivos/ServerMemory/" + "servidor_"
    num_arquivo = 0

    print("O servidor está a postos! Pronto para receber!")

    while True:
        # Recebe o pacote do cliente junto com o endereço 
        # de onde ele está vindo.
        nome, clientAddress = ftServer.receiveFile(local)

        if nome:
            ftServer.sendFile(nome, clientAddress)
            num_arquivo = num_arquivo + 1   

if __name__ == "__main__":
  sys.exit(main())