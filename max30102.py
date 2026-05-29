import time

REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01
REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03
REG_FIFO_WR_PTR   = 0x04
REG_OVF_COUNTER   = 0x05
REG_FIFO_RD_PTR   = 0x06
REG_FIFO_DATA     = 0x07
REG_FIFO_CONFIG   = 0x08
REG_MODE_CFG      = 0x09
REG_SPO2_CFG      = 0x0A
REG_LED1_PA       = 0x0C  # IR
REG_LED2_PA       = 0x0D  # RED

class MAX30102:
    def __init__(self, i2c, address=0x57):
        self.i2c = i2c
        self.addr = address
        self.reset()
        self.init()
        self.clear_fifo()

    def _write(self, reg, val):
        self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def _read(self, reg, n=1):
        return self.i2c.readfrom_mem(self.addr, reg, n)

    def reset(self):
        self._write(REG_MODE_CFG, 0x40)
        time.sleep_ms(100)
        self._read(REG_INTR_STATUS_1, 1)
        self._read(REG_INTR_STATUS_2, 1)

    def init(self):
        self._write(REG_INTR_ENABLE_1, 0xC0)  # A_FULL_EN + PPG_RDY_EN
        self._write(REG_INTR_ENABLE_2, 0x00)
        self._write(REG_FIFO_CONFIG, 0b01110000)  # SMP_AVE=8, rollover, A_FULL=0
        self._write(REG_SPO2_CFG,   0b01011111)  # ADC=4096nA, 100Hz, 411us/18-bit
        self._write(REG_LED1_PA,    0x24)        # IR
        self._write(REG_LED2_PA,    0x24)        # RED
        self._write(REG_MODE_CFG,   0x03)        # SpO2 (RED+IR)

    def clear_fifo(self):
        self._write(REG_FIFO_WR_PTR, 0x00)
        self._write(REG_OVF_COUNTER, 0x00)
        self._write(REG_FIFO_RD_PTR, 0x00)

    def read_fifo_sample(self):
        data = self._read(REG_FIFO_DATA, 6)
        ir  = ((data[0] << 16) | (data[1] << 8) | data[2]) & 0x3FFFF
        red = ((data[3] << 16) | (data[4] << 8) | data[5]) & 0x3FFFF
        return ir, red

