#!/usr/bin/python
import sys
import smbus

class FrontEndControl:
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

        rffe_v = 0b1000
        if self.switch_setting == 1:
            rffe_v = 0b0000

        elif self.switch_setting == 2:
            rffe_v = 0b0100

        elif self.switch_setting == 3:
            rffe_v = 0b0010

        elif self.switch_setting == 4:
            rffe_v = 0b0110

        elif self.switch_setting == 5:
            rffe_v = 0b0001

        elif self.switch_setting == 6:
            rffe_v = 0b0101

        elif self.switch_setting == 7:
            rffe_v = 0b0011

        elif self.switch_setting == 8:
            rffe_v = 0b0111

        else:
            print 'Error: Invalid switch setting'
            exit()

        bus = smbus.SMBus(1)
        bus.write_byte_data(0x22, 0x04, (rffe_v & 0x0F) << 4)
        bus.close()

    def set_attenuation(self, value_db=0.0):
        if value_db < 0.0:
            value_db = 0.0

        elif value_db > 31.5:
            value_db = 31.5

        self.atten_setting = int((31.5 - value_db)*0x3F/31.5) & 0x3F
        print 'atten setting:', bin(self.atten_setting)

        bus = smbus.SMBus(1)
        bus.write_byte_data(0x22, 0x05, (self.atten_setting << 2) + 0x00)
        bus.write_byte_data(0x22, 0x05, (self.atten_setting << 2) + 0x02)
        bus.write_byte_data(0x22, 0x05, (self.atten_setting << 2) + 0x00)
        bus.close()

if __name__ == '__main__':
    front_end_control = FrontEndControl()
    front_end_control.set_switch_setting(int(sys.argv[1]))
    front_end_control.set_attenuation(float(sys.argv[2]))
