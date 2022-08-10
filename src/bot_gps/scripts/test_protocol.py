#!/usr/bin/env python3

import serial
import protocol_parse
import time
import logging

if  __name__== "__main__":

    serial_port = '/dev/ttyUSB0'
    serial_baud = 460800
   
    decoder = protocol_parse.DecodeDynamic()

    try:
        sp = serial.Serial(port=serial_port, baudrate=serial_baud)

        try:
    
            while True:

                count = sp.inWaiting()
                data = bytes()
                if  count>0:
                    data = sp.read(count)
                
                for byte in data:
                    nmea_bytes =  decoder.parse_stream(byte)
                    if nmea_bytes is not None:
                        print(nmea_bytes) 

                time.sleep(0.02)

        except serial.serialutil.SerialException:
            sp.close()  # Close GPS serial port
    except serial.SerialException as ex:
        logging.error("open serial failed")