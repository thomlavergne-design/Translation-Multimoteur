import serial
import time

BMAC=serial.Serial(port="COM4",baudrate=11250,timeout=1000)
time.sleep(2)

Message= "03 REQUEST_VERSION"+"\n"
BMAC.write(Message.encode())

TempsTimeout=time.time()
while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = BMAC.readline().decode().strip()
                        print(response)
                        break

BMAC.close()