#!/usr/bin/python
import RPi.GPIO
import sys, time
from fractions import gcd

class ADF4351:
    def __init__(self):
        pass

    def initialize(self):
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(self.le_pin, RPi.GPIO.OUT)
        RPi.GPIO.setup(self.data_pin, RPi.GPIO.OUT)
        RPi.GPIO.setup(self.clk_pin, RPi.GPIO.OUT)
        
        RPi.GPIO.setup(self.ce_pin, RPi.GPIO.OUT)
        RPi.GPIO.output(self.ce_pin, 1)
        
        RPi.GPIO.setup(self.pdrf_pin, RPi.GPIO.OUT)
        RPi.GPIO.output(self.pdrf_pin, 1)
        
        RPi.GPIO.setup(self.ld_pin, RPi.GPIO.IN)

    def shutdown(self):
        RPi.GPIO.cleanup()

    def set_frequency(self, frequency=1e9):
        if frequency > 2.2e9 and frequency < 4.4e9:
            self.rf_divider_select_value = 0

        elif frequency >= 1.1e9 and frequency < 2.2e9:
            self.rf_divider_select_value = 1

        elif frequency >= 550e6 and frequency < 1.1e9:
            self.rf_divider_select_value = 2

        elif frequency >= 275e6 and frequency < 550e6:
            self.rf_divider_select_value = 3

        elif frequency >= 137.5e6 and frequency < 275e6:
            self.rf_divider_select_value = 4

        elif frequency >= 68.75e6 and frequency < 137.5e6:
            self.rf_divider_select_value = 5

        f_pfd = 25e6

        #print (frequency / f_pfd) * (2**self.rf_divider_select_value)
        self.int_value = int((frequency / f_pfd) * (2**self.rf_divider_select_value))

        #print self.int_value
        #print int(((frequency / f_pfd) * (2**self.rf_divider_select_value) - self.int_value) * 4095)
        self.frac_value = int(((frequency / f_pfd) * (2**self.rf_divider_select_value) - self.int_value) * 4095)
        self.modulus_value = 4095
        
        gcd_value = gcd(self.frac_value, self.modulus_value)
        self.frac_value = self.frac_value / gcd_value
        self.modulus_value = self.modulus_value / gcd_value

        print self.rf_divider_select_value, self.int_value, self.frac_value, self.modulus_value

    def write_registers(self):
        reg0 = 0b000
        reg0 = reg0 + (self.frac_value << 3)
        reg0 = reg0 + (self.int_value << 15)

        reg1 = 0b001
        reg1 = reg1 + (self.modulus_value << 3)
        reg1 = reg1 + (self.phase_value << 15)
        reg1 = reg1 + (self.prescaler_value << 27)
        reg1 = reg1 + (self.phase_adjust_value << 28)

        reg2 = 0b010
        reg2 = reg2 + (self.counter_reset_value << 3)
        reg2 = reg2 + (self.cp_three_state_value << 4)
        reg2 = reg2 + (self.power_down_value << 5)
        reg2 = reg2 + (self.pd_polarity_value << 6)
        reg2 = reg2 + (self.ldp_value << 7)
        reg2 = reg2 + (self.ldf_value << 8)
        reg2 = reg2 + (self.charge_pump_current_setting_value << 9)
        reg2 = reg2 + (self.double_buffer_value << 13)
        reg2 = reg2 + (self.r_counter_value << 14)
        reg2 = reg2 + (self.rdiv2_value << 24)
        reg2 = reg2 + (self.reference_doubler_value << 25)
        reg2 = reg2 + (self.muxout_value << 26)
        reg2 = reg2 + (self.low_noise_and_low_spur_modes_value << 29)

        reg3 = 0b011
        reg3 = reg3 + (self.clock_divider_value << 3)
        reg3 = reg3 + (self.clk_div_mode_value << 15)
        reg3 = reg3 + (self.csr_value << 18)
        reg3 = reg3 + (self.charge_cancel_value << 21)
        reg3 = reg3 + (self.abp_value << 22)
        reg3 = reg3 + (self.band_select_clock_mode_value << 23)

        reg4 = 0b100
        reg4 = reg4 + (self.output_power_value << 3)
        reg4 = reg4 + (self.rf_output_enable_value << 5)
        reg4 = reg4 + (self.aux_output_power_value << 6)
        reg4 = reg4 + (self.aux_output_enable_value << 8)
        reg4 = reg4 + (self.aux_output_select_value << 9)
        reg4 = reg4 + (self.mtld_value << 10)
        reg4 = reg4 + (self.vco_power_down_value << 11)
        reg4 = reg4 + (self.band_select_clock_divider_value << 12)
        reg4 = reg4 + (self.rf_divider_select_value << 20)
        reg4 = reg4 + (self.feedback_select_value << 23)

        reg5 = 0b101
        reg5 = reg5 + (0b11 << 19)
        reg5 = reg5 + (self.ld_pin_mode_value << 22)

        print '0x%x' % reg5
        print '0x%x' % reg4
        print '0x%x' % reg3
        print '0x%x' % reg2
        print '0x%x' % reg1
        print '0x%x' % reg0

        self.write_register(reg5)
        self.write_register(reg4)
        self.write_register(reg3)
        self.write_register(reg2)
        self.write_register(reg1)
        self.write_register(reg0)

        time.sleep(1)
        print RPi.GPIO.input(self.ld_pin)

    def write_register(self, value):
        RPi.GPIO.output(self.clk_pin, 0)
        RPi.GPIO.output(self.le_pin, 0)

        for n in range(0, 32):
            RPi.GPIO.output(self.data_pin, (value >> (31-n)) & 0x01)
            RPi.GPIO.output(self.clk_pin, 0)
            RPi.GPIO.output(self.clk_pin, 1)

        RPi.GPIO.output(self.clk_pin, 0)

        RPi.GPIO.output(self.le_pin, 1)
        RPi.GPIO.output(self.le_pin, 0)

    # Reg 0
    int_value = 160
    frac_value = 0

    # Reg 1
    phase_adjust_value = 0
    prescaler_value = 1
    phase_value = 1
    modulus_value = 2

    # Reg 2
    low_noise_and_low_spur_modes_value = 0b00
    muxout_value = 0b000
    reference_doubler_value = 0b0
    rdiv2_value = 0b0
    r_counter_value = 1
    double_buffer_value = 0b0
    charge_pump_current_setting_value = 0b0111
    ldf_value = 0b0
    ldp_value = 0b0
    pd_polarity_value = 0b1
    power_down_value = 0b0
    cp_three_state_value = 0b0
    counter_reset_value = 0b0

    # Reg 3
    band_select_clock_mode_value = 0b0
    abp_value = 0b0
    charge_cancel_value = 0b0
    csr_value = 0b0
    clk_div_mode_value = 0b00
    clock_divider_value = 150

    # Reg 4
    feedback_select_value = 0b1
    rf_divider_select_value = 0b010
    band_select_clock_divider_value = 200
    vco_power_down_value = 0b0
    mtld_value = 0b0
    aux_output_select_value = 0b0
    aux_output_enable_value = 0b0
    aux_output_power_value = 0b00
    rf_output_enable_value = 0b1
    output_power_value = 0b00

    # Reg 5
    ld_pin_mode_value = 0x01

    # SPI bus
    le_pin = 25
    #data_pin = 10
    #clk_pin = 11
    
    clk_pin = 10
    data_pin = 11
    ce_pin = 9
    pdrf_pin = 8
    ld_pin = 24

if __name__ == '__main__':
    adf4351 = ADF4351()
    adf4351.initialize()
    adf4351.set_frequency(float(sys.argv[1]))
    adf4351.write_registers()
    adf4351.shutdown()


