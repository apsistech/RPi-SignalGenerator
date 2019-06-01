#!/usr/bin/python
import smbus

bus = smbus.SMBus(1)
bus.write_byte_data(0x68, 0x0E, 0x00)
bus.write_byte_data(0x23, 0x0C, 0b11111100)
bus.write_byte_data(0x23, 0x04, 0b10)

x = (bus.read_byte_data(0x23, 0x02) << 16) + (bus.read_byte_data(0x23, 0x01) << 8) + bus.read_byte_data(0x23, 0x00)

F = [0] * 24;
for n in range(2, 24):
    F[n] = (x >> n) & 0x01

C = [0] * 24
C[0] = F[0]
C[22] = 0
#C[22] = F[1]
C[21] = F[2]
C[19] = F[3]
C[20] = F[4]
C[12] = F[5]
C[13] = F[6]
C[14] = F[7]

C[15] = F[8]
C[18] = F[9]
C[16] = F[10]
C[17] = F[11]
C[23] = F[12]
C[1] = F[13]
C[2] = F[14]
C[3] = F[15]

C[6] = F[16]
C[4] = F[17]
C[5] = F[18]
C[11] = F[19]
C[10] = F[20]
C[9] = F[21]
C[7] = F[22]
C[8] = F[23]

#C[12] = 1
print F[0:8]
print C

count = 0
for n in range(0, 24):
    count = count + (C[n] << n)

freq_measured_khz = (2*64*count/1e6)
print 'Freq = %.2f MHz' % freq_measured_khz
