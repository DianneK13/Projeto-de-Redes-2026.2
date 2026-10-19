import sys
from socket import *
from rdt.RDTServer import *
from util.FileReader import *
from util.FileWriter import *

class FTServer:
    #arquivos FT (file transfer) são responsáveis pela leitura/escrita e segmentação de arquivos
    #os segmentos que FTServer faz são enviados para RDTServer

    def __init__(self, serverPort):
        self.rdtServer = RDTServer(serverPort) #instância de RDTServer

    def receiveFile (self, path): #receber arquivos do RDTServer
        nome, clientAddress = self.rdtServer.receiveBuffer()

        if nome:
            print(f"(servidor) arquivo {nome} recebido")
            
            download = path + nome.decode() #transforma de volta em txt
            fileWriter = FileWriter(download) #abre arquivo pra escrever ele localmente

            buffer, clientAddress = self.rdtServer.receiveBuffer()
            while buffer:
                fileWriter.write_buffer(buffer)
                buffer, clientAddress = self.rdtServer.receiveBuffer() #recebe buffer do rdtServer

            print("(servidor) armazenou o arquivo recebido.")
            return download, clientAddress

    def sendFile(self, fileName, clientAddress): #enviar arquivo pro RDTServer
        fileReader = FileReader(fileName, self.rdtServer.payload()) #instância do FileReader

        #lê arquivo (em segmentos) q vai mandar
        buffer = fileReader.read_buffer()
        while buffer is not None:
            self.rdtServer.sendBuffer(buffer, clientAddress) #manda buffer com os dados pro rdtServer
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
            ftServer.sendFile(nome, clientAddress) #retorna arquivo pro cliente
            num_arquivo = num_arquivo + 1   

if __name__ == "__main__":
  sys.exit(main())