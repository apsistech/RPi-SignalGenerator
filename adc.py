#!/usr/bin/python
import smbus
import time

class AnalogToDigitalConverter:
    def __init__(self):
        pass

    # High level functions
    def Update(self):
        self.UpdateMeasurementData()

    def GetVoltage(self, channel_number):
        if channel_number < 0 or channel_number >= 8:
            return 0.00

        return self.adc_output[channel_number]

    def GetVoltages(self):
        return self.adc_output

    # Low level functions
    def UpdateMeasurementData(self):
        bus = smbus.SMBus(1)
        #self.adc_output_raw[0] = bus.read_word_data(0x08, 0b11001000)
        self.adc_output_raw[0] = bus.read_word_data(0x08, 0b10001000)
        self.adc_output_raw[2] = bus.read_word_data(0x08, 0b10011000)
        self.adc_output_raw[4] = bus.read_word_data(0x08, 0b10101000)
        self.adc_output_raw[6] = bus.read_word_data(0x08, 0b10111000)
        self.adc_output_raw[1] = bus.read_word_data(0x08, 0b11001000)
        self.adc_output_raw[3] = bus.read_word_data(0x08, 0b11011000)
        self.adc_output_raw[5] = bus.read_word_data(0x08, 0b11101000)
        self.adc_output_raw[7] = bus.read_word_data(0x08, 0b11111000)
        bus.close()

        for n in range(0, len(self.adc_output)):
            self.adc_output[n] = round(float(self.flip_endian(self.adc_output_raw[n]) >> 4) * 4.096 / (2**12), 2)

    def flip_endian(self, value):
        return (value >>  8) + ((value & 0xFF) << 8)
    

    # Register data
    adc_output_raw = [ 0x00 ] * 8

    # Measurement data
    adc_output = [ 0.00 ] * 8


if __name__ == '__main__':
    adc = AnalogToDigitalConverter()
    try:
        while 1:
            adc.Update()
            print adc.GetVoltages()
            time.sleep(1)

    except:
        print 'Done'
