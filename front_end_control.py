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
        bus.write_byte_data(0x22, 0x0E, 0x00)
        bus.close()

    def set_switch_setting(self, switch_setting = None):
        if switch_setting != None:
            self.switch_setting = switch_setting

        rffe_v = 0b00000001
        if self.switch_setting == 2:
            rffe_v = 0b00000100

        elif self.switch_setting == 4:
            rffe_v = 0b00010100

        elif self.switch_setting == 5:
            rffe_v = 0b01000000

        elif self.switch_setting == 6:
            rffe_v = 0b01000100

        elif self.switch_setting == 7:
            rffe_v = 0b01010000

        elif self.switch_setting == 8:
            rffe_v = 0b01010100

        else:
            print 'Error: Invalid switch setting'
            exit()

        bus = smbus.SMBus(1)
        bus.write_byte_data(0x22, 0x06, rffe_v)
        bus.close()

    def set_attenuation(self, value_db=0.0, atten_num=1):
        if value_db < 0.0:
            value_db = 0.0

        elif value_db > 31.25:
            value_db = 31.25

        if atten_num == 1 and value_db < 10.0:
            print 'Warning: Attenuator #1 setting clipped to 10.0 to protect second amplifier'
            self.atten_setting = 10.0

        self.atten_setting = int(0x7F*value_db/31.75) & 0x7F
        print 'atten setting:', bin(self.atten_setting)

        bus = smbus.SMBus(1)
        bus.write_byte_data(0x22, 0x05, self.atten_setting)

        if atten_num == 1:
            bus.write_byte_data(0x22, 0x04, 0b00000000)
            bus.write_byte_data(0x22, 0x04, 0b10000000)
            bus.write_byte_data(0x22, 0x04, 0b00000000)

        elif atten_num == 2:
            bus.write_byte_data(0x22, 0x04, 0b00000000)
            bus.write_byte_data(0x22, 0x04, 0b00100000)
            bus.write_byte_data(0x22, 0x04, 0b00000000)

        else:
            print 'Error: invalid attenuator number'
            exit()

        bus.close()

if __name__ == '__main__':
    front_end_control = FrontEndControl()
    front_end_control.set_switch_setting(int(sys.argv[1]))
    front_end_control.set_attenuation(float(sys.argv[2]), 1)
    front_end_control.set_attenuation(float(sys.argv[3]), 2)
    #front_end_control.set_attenuation(float(sys.argv[2]), 2)
