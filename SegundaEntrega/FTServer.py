import sys
from socket import *
from rdt.RDTSocket import RDTSocket
from util.FileReader import *
from util.FileWriter import *

class FTServer:
    #arquivos FT (file transfer) são responsáveis pela leitura/escrita e segmentação de arquivos

    def __init__(self, serverPort):
        self.rdtServer = RDTSocket.server(serverPort) #instância de RDTSocket

    def receiveFile (self, path): #receber arquivos do RDTServer
        nome = self.rdtServer.rdtRcv()

        if nome:
            print(f"(servidor) arquivo {nome} recebido")
            
            download = path + nome.decode() #transforma de volta em txt
            fileWriter = FileWriter(download) #abre arquivo pra escrever ele localmente

            buffer = self.rdtServer.rdtRcv()
            while buffer:
                fileWriter.write_buffer(buffer)
                buffer = self.rdtServer.rdtRcv() #recebe buffer do rdtServer

            print("(servidor) armazenou o arquivo recebido.")
            return download

    def sendFile(self, fileName): #enviar arquivo pro rdtServer
        fileReader = FileReader(fileName, self.rdtServer.payload()) #instância do FileReader

        #lê arquivo (em segmentos) q vai mandar
        buffer = fileReader.read_buffer()
        while buffer is not None:
            if not self.rdtServer.rdtSend(buffer): #manda buffer com os dados pro rdtServer
                print("(servidor) cliente não responde, envio abortado.")
                return
            buffer = fileReader.read_buffer()
        
        self.rdtServer.rdtSend(b"") # sinaliza fim de arquivo com pacote vazio

        print("(servidor) enviou o arquivo de volta.")
        print()

def main():

    ftServer = FTServer(12000)
    local = "arquivos/ServerMemory/" + "servidor_"

    print("O servidor está a postos! Pronto para receber!")
    print()
    
    while True:
        # Recebe o pacote do cliente junto com o endereço 
        # de onde ele está vindo.
        nome = ftServer.receiveFile(local)

        if nome:
            ftServer.sendFile(nome) #retorna arquivo pro cliente  

if __name__ == "__main__":
  sys.exit(main())