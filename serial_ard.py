import serial
import db

ser = serial.Serial('COM4',9600)
s = [0]
while True:
        read_serial=ser.readline().strip().decode()
        s=read_serial
        print (bytearray.fromhex(s).decode())
        #print (read_serial)
        #db.db(bytearray.fromhex(s).decode())
