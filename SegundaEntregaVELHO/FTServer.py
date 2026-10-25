import sys
from socket import *
from rdt.RDTSocket import RDTSocket
from util.FileReader import *
from util.FileWriter import *

class FTServer:
    #arquivos FT (file transfer) são responsáveis pela leitura/escrita e segmentação de arquivos
    #os segmentos que FTServer faz são enviados para RDTServer

    def __init__(self, serverPort):
        self.rdtServer = RDTSocket.server(serverPort) #instância de RDTSocket

    def receiveFile (self, path): #receber arquivos do RDTServer
        nome = self.rdtServer.rdtReceive()

        if nome:
            print(f"(servidor) arquivo {nome} recebido")
            
            download = path + nome.decode() #transforma de volta em txt
            fileWriter = FileWriter(download) #abre arquivo pra escrever ele localmente

            buffer = self.rdtServer.rdtReceive()
            while buffer:
                fileWriter.write_buffer(buffer)
                buffer = self.rdtServer.rdtReceive() #recebe buffer do rdtServer

            print("(servidor) armazenou o arquivo recebido.")
            return download

    def sendFile(self, fileName): #enviar arquivo pro RDTServer
        fileReader = FileReader(fileName, self.rdtServer.payload()) #instância do FileReader

        #lê arquivo (em segmentos) q vai mandar
        buffer = fileReader.read_buffer()
        while buffer is not None:
            self.rdtServer.rdtSend(buffer) #manda buffer com os dados pro rdtServer
            buffer = fileReader.read_buffer()
        
        self.rdtServer.rdtSend(b"") # sinaliza fim de arquivo com pacote vazio

        print("(servidor) enviou o arquivo de volta.")

def main():

    ftServer = FTServer(12000)
    local = "arquivos/ServerMemory/" + "servidor_"
    num_arquivo = 0

    print("O servidor está a postos! Pronto para receber!")

    while True:
        # Recebe o pacote do cliente junto com o endereço 
        # de onde ele está vindo.
        nome = ftServer.receiveFile(local)

        if nome:
            ftServer.sendFile(nome) #retorna arquivo pro cliente
            num_arquivo = num_arquivo + 1   

if __name__ == "__main__":
  sys.exit(main())