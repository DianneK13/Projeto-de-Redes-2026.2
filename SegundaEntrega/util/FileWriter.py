class FileWriter:
    def __init__(self, file_path):
        #self.file_size = 0
        self.file = open(file_path, "wb")

    def write_buffer(self, buff, size=-1):
        if size < 0:
            size = len(buff)

        written = self.file.write(buff[:size])
        #self.file_size += written

    def close(self):
        self.file.close()
