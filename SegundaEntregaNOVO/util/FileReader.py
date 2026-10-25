class FileReader: #le arquivo de dado local
    def __init__(self, file_path, blockSize=1024):
        self.index = 0
        self.blockSize = blockSize
        self.file = open(file_path, "rb")
        self.file_size = self.file.seek(0, 2)
        self.file.seek(0)

    def read_buffer(self):
        #"cursor" que começa no início do arquivo
        #vai avançando conforme o blocksize 
        #retorna os dados daquele segmento
        if self.index >= self.file_size:
            return None

        data = self.file.read(min(self.blockSize, self.file_size - self.index))
        if not data:
            return None

        self.index += len(data)
        return data

    def close(self):
        self.file.close()