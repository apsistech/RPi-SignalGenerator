#!/usr/bin/python
import time
import numpy as np

from adf4351 import ADF4351
from rf_power_detector import RFPowerDetector

adf4351 = ADF4351()
adf4351.initialize()

rf_power_detector = RFPowerDetector()

handle = open('output.csv', 'w')

frequencies = np.linspace(800e6, 1100e6, 20)
for frequency in frequencies:
    adf4351.set_frequency(frequency)
    adf4351.write_registers()
    #time.sleep(1)
    #print '%.2f, %.2f' % (frequency/1e6, rf_power_detector.measure_power())
    #handle.write('%.2f, %.2f' % (frequency/1e6, rf_power_detector.measure_power()))

handle.close()
adf4351.power_down_value = 1
adf4351.write_registers()

adf4351.shutdown()

