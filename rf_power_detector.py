#!/usr/bin/python
import smbus
import time

class RFPowerDetector:
    def __init__(self):
        pass

    def measure_power(self):
        bus = smbus.SMBus(1)

        '''m = (5+75)/(1.65)
        x = bus.read_i2c_block_data(0x14, 0b100000, 2);
        res = (x[0]<<8) + x[1];
        z = (res*3.3/(0xFFFF));

        bus.close()

        return (z-1.75)*m'''

        time.sleep(100e-3)
        x = bus.read_i2c_block_data(0x14, 0b100000, 2)
        time.sleep(100e-3)
        x = bus.read_i2c_block_data(0x14, 0b100000, 2)
        res = 3.3*((x[0]<<8) + x[1]) / 0xFFFF;
        res = (res-1.75)*(5+75)/(1.65)

        bus.close()

        return res

if __name__ == '__main__':
    rf_power_detector = RFPowerDetector()
    print rf_power_detector.measure_power()
