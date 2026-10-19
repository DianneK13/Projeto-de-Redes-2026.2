class FileReader:
    def __init__(self, file_path, blockSize=1024):
        self.index = 0
        self.blockSize = blockSize
        self.file = open(file_path, "rb")
        self.file_size = self.file.seek(0, 2)
        self.file.seek(0)

    def read_buffer(self):
        if self.index >= self.file_size:
            return None

        data = self.file.read(min(self.blockSize, self.file_size - self.index))
        if not data:
            return None

        self.index += len(data)
        return data

    def close(self):
        self.file.close()