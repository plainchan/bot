
import struct

HEADER,GPS_TAG,IMU_TAG= (0x5E,0x55,0x41)


FRAME_HEADER_OFFSET = 1
FRAME_DATATAG_OFFSET = 2
FRAME_DATALEN_OFFSET = 4

FRAME_INFO_LEN = FRAME_DATALEN_OFFSET






class DecodeDynamic:
    
    def __init__(self) -> None:
        self.__streamBuffer = bytearray()
        self.__dataLen = 0
        self.__tag = 0
    
    def parse_stream(self,byte):
        self.__streamBuffer.append(byte)
    
        # frame header
        length  =  len(self.__streamBuffer)
        if length == FRAME_HEADER_OFFSET:
            if self.__streamBuffer[length - 1] != HEADER:
                self.__streamBuffer.clear()
        # data tag
        elif length == FRAME_DATATAG_OFFSET:
            self.__tag = self.__streamBuffer[length - 1]
        # data len
        elif length == FRAME_DATALEN_OFFSET:
            self.__dataLen = self.__streamBuffer[length - 1]  | self.__streamBuffer[length - 2] << 8  #大端模式

        # header(1) + tag(1) + len(2) + checksum(1) +frameID(1)
        elif length >= FRAME_INFO_LEN + self.__dataLen + 2:
            self.__checksum = self.__streamBuffer[FRAME_INFO_LEN + self.__dataLen]
            self.__dataFeild = self.__streamBuffer[FRAME_INFO_LEN:FRAME_INFO_LEN + self.__dataLen]
            self.__streamBuffer.clear();

            checksum = sum(self.__dataFeild)&0x000000ff
            if self.__tag == GPS_TAG:
                if self.__checksum == checksum:
                    return self.__dataFeild
        return None
    
    def __decode(self,dataFeild):
        pass



class DecodeFixBuffer:
    
    def __init__(self) -> None:
        self.__dataLen = 0
        self.__byteCount = 0
        self.__maxBuffSize = 1024
        self.__streamBuffer = bytearray(self.__maxBuffSize)

    
    def parse_stream(self,byte):
        self.__streamBuffer[self.__byteCount] =byte
        self.__byteCount +=1
        
        # header
        if self.__byteCount == FRAME_HEADER_OFFSET:
            if self.__streamBuffer[self.__byteCount-1] != HEADER:
                self.__byteCount == 0
                return None
        # tag
        elif self.__byteCount == FRAME_DATATAG_OFFSET:
            self.__tag = self.__streamBuffer[self.__byteCount-1]
        # len
        elif self.__byteCount == FRAME_DATALEN_OFFSET:
            self.__dataLen =  self.__streamBuffer[self.__byteCount-1] | self.__streamBuffer[self.__byteCount-2] << 8
        # header(1) + tag(1) + len(2) + checksum(1) +frameID(1)
        elif self.__byteCount >=FRAME_INFO_LEN + self.__dataLen + 2:
            self.__byteCount = 0
            self.__checksum = self.__streamBuffer[FRAME_INFO_LEN + self.__dataLen]
            self.__dataFeild = self.__streamBuffer[FRAME_INFO_LEN:FRAME_INFO_LEN + self.__dataLen]
             
            checksum = sum(self.__dataFeild)&0x000000ff

            if self.__tag == GPS_TAG:
                if self.__checksum == checksum:
                    return self.__dataFeild
            return self.__decode()

    def __decode(self,dataFeild):
        pass


