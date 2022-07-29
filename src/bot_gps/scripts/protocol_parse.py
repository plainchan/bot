

class Decoder:
    def __init__(self):
        self.byteCount = 0
        self.buffer = bytes()


    def parse_stream(self,byte):
        self.buffer +=byte
        
    

    