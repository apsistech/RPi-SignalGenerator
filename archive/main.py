#!/usr/bin/python
import sys
import smbus
import time
import rpi_siggen

#bus = smbus.SMBus(1)

rpi_siggen = rpi_siggen.RPi_SignalGenerator()

rpi_siggen.set_frequency(float(sys.argv[1]))
rpi_siggen.set_attenuation(float(sys.argv[2]))
rpi_siggen.update()
print rpi_siggen.calculate_frequency()
