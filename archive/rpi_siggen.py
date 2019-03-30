#!/usr/bin/python
import smbus

class RPi_SignalGenerator:
    def __init__(self):
        bus = smbus.SMBus(1)

        # Initialize step attenuator
        bus.write_byte_data(0x22, 0x0C, 0x00)
        bus.write_byte_data(0x22, 0x0D, 0x00)

        # Initialize oscillator
        #bus.write_byte_data(0x23, 0x0C, 0x00)
        #bus.write_byte_data(0x23, 0x0D, 0x02)
        #bus.write_byte_data(0x23, 0x0E, 0x00)

        bus.close()

    def update(self):
        self.update_step_attenuator()
        self.update_oscillator()

    def set_frequency(self, frequency_hz=100.0e6):
        ref_freq = 10.0e6
        if frequency_hz >= 81e6 and frequency_hz < 162e6:
            self.NA = 0b110
            self.M = int((frequency_hz / ref_freq)*2*16)

        elif frequency_hz > 162e6 and frequency_hz < 324e6:
            self.NA = 0b101
            self.M = int((frequency_hz / ref_freq)*2*8)

        elif frequency_hz > 324e6 and frequency_hz < 648e6:
            self.NA = 0b100
            self.M = int((frequency_hz / ref_freq)*2*4)

        elif frequency_hz > 648e6 and frequency_hz < 1296e6:
            self.NA = 0b001
            self.M = int((frequency_hz / ref_freq)*2*2)

        elif frequency_hz > 1296e6 and frequency_hz < 2592e6:
            self.NA = 0b000
            self.M = int((frequency_hz / ref_freq)*2*1)

    def set_attenuation(self, value_db=0.0):
        if value_db < 0.0:
            value_db = 0.0

        elif value_db > 31.5:
            value_db = 31.5

        self.step_attenuator_word = int((31.5 - value_db)*0x3F/31.5) & 0x3F
        print bin(self.step_attenuator_word)

    # Internal use functions
    def calculate_frequency(self):
        ref_freq = 10e6

        p_value = 0
        if self.P == 0:
            p_value = 2
        elif self.P == 1:
            p_value = 4

        na_value = 0
        if self.NA == 0b000:
            na_value = 1

        elif self.NA == 0b001:
            na_value = 2

        elif self.NA == 0b010:
            na_value = 3

        elif self.NA == 0b011:
            na_value = 6

        elif self.NA == 0b100:
            na_value = 4

        elif self.NA == 0b101:
            na_value = 8

        elif self.NA == 0b110:
            na_value = 16

        out_freq = (ref_freq / p_value) * self.M / na_value
        return out_freq
    
    def update_step_attenuator(self):
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x22, 0x05, (self.step_attenuator_word << 1) + 0x00)
        bus.write_byte_data(0x22, 0x05, (self.step_attenuator_word << 1) + 0x01)
        bus.write_byte_data(0x22, 0x05, (self.step_attenuator_word << 1) + 0x00)
        bus.close()
        
    def update_oscillator(self):
        bus = smbus.SMBus(1)
        self.pin_values['NPLOAD'] = 0
        self.pin_values['NB2'] = 0
        self.pin_values['NB1'] = 0
        self.pin_values['NB0'] = 0
        self.pin_values['NA2'] = (self.NA >> 2) & 0x01
        self.pin_values['NA1'] = (self.NA >> 1) & 0x01
        self.pin_values['NA0'] = (self.NA >> 0) & 0x01

        self.pin_values['P'] = 0
        self.pin_values['LEV_SEL'] = 1
        self.pin_values['NMR'] = 1
        self.pin_values['REF_SEL'] = 1
        self.pin_values['NBYPASS'] = 0

        self.pin_values['M9'] = (self.M >> 9) & 0x01
        self.pin_values['M8'] = (self.M >> 8) & 0x01
        self.pin_values['M7'] = (self.M >> 7) & 0x01
        self.pin_values['M6'] = (self.M >> 6) & 0x01
        self.pin_values['M5'] = (self.M >> 5) & 0x01
        self.pin_values['M4'] = (self.M >> 4) & 0x01
        self.pin_values['M3'] = (self.M >> 3) & 0x01
        self.pin_values['M2'] = (self.M >> 2) & 0x01
        self.pin_values['M1'] = (self.M >> 1) & 0x01
        self.pin_values['M0'] = (self.M >> 0) & 0x01

        port0_byte = 0x00
        port1_byte = 0x00
        port2_byte = 0x00

        for key in self.pin_map:
            if self.pin_map[key][0] == 0:
                port0_byte = port0_byte + (self.pin_values[key] << self.pin_map[key][1])

            if self.pin_map[key][0] == 1:
                port1_byte = port1_byte + (self.pin_values[key] << self.pin_map[key][1])

            if self.pin_map[key][0] == 2:
                port2_byte = port2_byte + (self.pin_values[key] << self.pin_map[key][1])

        bus.write_byte_data(0x23, 0x04, port0_byte)
        bus.write_byte_data(0x23, 0x05, port1_byte)
        bus.write_byte_data(0x23, 0x06, port2_byte)
        bus.close()

    # Step attenuator parameters
    step_attenuator_word = 0x3F

    # Oscillator parameters
    M = 300
    NA = 6
    P = 0

    pin_values = {}
    pin_map = {}
    pin_map['NPLOAD'] = (0, 0)
    pin_map['NB2'] = (0, 1)
    pin_map['NB1'] = (0, 2)
    pin_map['NB0'] = (0, 3)
    pin_map['NA2'] = (0, 4)
    pin_map['NA1'] = (0, 5)
    pin_map['NA0'] = (0, 6)
    pin_map['P'] = (0, 7)
    pin_map['LEV_SEL'] = (1, 0)
    pin_map['NMR'] = (1, 2)
    pin_map['REF_SEL'] = (1, 3)
    pin_map['NBYPASS'] = (1, 4)
    pin_map['M9'] = (1, 5)
    pin_map['M8'] = (1, 6)
    pin_map['M7'] = (1, 7)
    pin_map['M6'] = (2, 0)
    pin_map['M5'] = (2, 1)
    pin_map['M4'] = (2, 2)
    pin_map['M3'] = (2, 3)
    pin_map['M2'] = (2, 4)
    pin_map['M1'] = (2, 5)
    pin_map['M0'] = (2, 6)
