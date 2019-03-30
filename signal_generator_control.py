#!/usr/bin/python
import smbus

class SignalGeneratorControl:
    def __init__(self):
        self.switch_setting = 0x00
        self.atten_setting = 0x00

        bus = smbus.SMBus(1)

        # Initialize step attenuator
        bus.write_byte_data(0x22, 0x0C, 0x00)
        bus.write_byte_data(0x22, 0x0D, 0x00)
        bus.close()

    def set_switch_setting(self, switch_setting = None):
        if switch_setting != None:
            self.switch_setting = switch_setting

        bus = smbus.SMBus(1)
        bus.write_byte_data(0x22, 0x04, (self.switch_setting & 0x0F) << 4)
        bus.close()

    def set_attenuation(self, value_db=0.0):
        if value_db < 0.0:
            value_db = 0.0

        elif value_db > 31.5:
            value_db = 31.5

        self.atten_setting = int((31.5 - value_db)*0x3F/31.5) & 0x3F
        print bin(self.atten_setting)

        bus = smbus.SMBus(1)
        bus.write_byte_data(0x22, 0x05, (self.atten_setting << 2) + 0x00)
        bus.write_byte_data(0x22, 0x05, (self.atten_setting << 2) + 0x02)
        bus.write_byte_data(0x22, 0x05, (self.atten_setting << 2) + 0x00)
        bus.close()

if __name__ == '__main__':
    signal_generator_control = SignalGeneratorControl()
    signal_generator_control.set_switch_setting(0b0111)
    signal_generator_control.set_attenuation(0.0)

