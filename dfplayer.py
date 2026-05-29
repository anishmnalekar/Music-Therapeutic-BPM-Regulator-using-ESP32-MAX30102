from machine import UART
import time

class DFPlayer:
    def __init__(self, uart_id=2, tx=17, rx=16, baud=9600, timeout=200):
        self.uart = UART(uart_id, tx=tx, rx=rx, baudrate=baud, timeout=timeout)
        time.sleep_ms(200)

    def _send_command(self, cmd, param=0):
        high = (param >> 8) & 0xFF
        low = param & 0xFF
        checksum = 0 - (0xFF + 0x06 + cmd + 0x00 + high + low)
        checksum &= 0xFFFF
        c_high = (checksum >> 8) & 0xFF
        c_low = checksum & 0xFF

        buf = bytearray([0x7E, 0xFF, 0x06, cmd, 0x00, high, low, c_high, c_low, 0xEF])
        self.uart.write(buf)

    def volume(self, level):  # 0–30 on DFPlayer Mini
        level = max(50, min(80, int(level)))
        self._send_command(0x06, level)

    def play_folder_track(self, folder, track):  # folder: 1..99, track: 1..255
        param = (folder << 8) | track
        self._send_command(0x0F, param)

    def stop(self):
        self._send_command(0x16, 0)

    def pause(self):
        self._send_command(0x0E, 0)

    def resume(self):
        self._send_command(0x0D, 0)

