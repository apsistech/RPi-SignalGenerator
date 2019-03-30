#!/usr/bin/python
import RPi.GPIO
import time
import spidev

le_pin = 25
data_pin = 10
clk_pin = 11
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(le_pin, RPi.GPIO.OUT)
RPi.GPIO.setup(data_pin, RPi.GPIO.OUT)
RPi.GPIO.setup(clk_pin, RPi.GPIO.OUT)

'''spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 9600
spi.mode = 0

spi.writebytes([0x3C, 0x80, 0xAC])'''

def write_register(value):
    RPi.GPIO.output(clk_pin, 0)
    time.sleep(0.001)
    RPi.GPIO.output(le_pin, 0)
    time.sleep(0.001)

    for n in range(0, 32):
        RPi.GPIO.output(data_pin, (value >> (31-n)) & 0x01)
        time.sleep(0.001)
        RPi.GPIO.output(clk_pin, 0)
        time.sleep(0.001)
        RPi.GPIO.output(clk_pin, 1)
        time.sleep(0.001)

    RPi.GPIO.output(clk_pin, 0)
    time.sleep(0.001)

    RPi.GPIO.output(le_pin, 1)
    time.sleep(0.001)
    RPi.GPIO.output(le_pin, 0)
    time.sleep(0.001)

write_register(0x580005)
write_register(0xAC8024)
#write_register(0xAC803C)
write_register(0x4B3)
write_register(0x4E42)
write_register(0x8008011)
write_register(0x500000)

#spi.close()
RPi.GPIO.cleanup()
