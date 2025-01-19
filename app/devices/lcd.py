from dataclasses import dataclass
from queue import Queue
from typing import cast

import adafruit_character_lcd.character_lcd as characterlcd
import board
import digitalio
import pwmio

from app.devices.io.io_write_process import IoWriteProcess


@dataclass
class LcdData:
    lines: list[str]
    brightness: float | None = None
    clear: bool = False


class Lcd(IoWriteProcess[LcdData]):
    def __init__(self):
        lcd_columns = 16
        lcd_rows = 2

        lcd_rs = digitalio.DigitalInOut(board.D22)
        lcd_en = digitalio.DigitalInOut(board.D17)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d6 = digitalio.DigitalInOut(board.D23)
        lcd_d7 = digitalio.DigitalInOut(board.D18)

        self.lcd = characterlcd.Character_LCD_Mono(
            lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
        )
        self.brightness = pwmio.PWMOut(board.D8, frequency=5000, duty_cycle=0)
        self.queue: Queue[LcdData] = cast(Queue[LcdData], Queue())

        super().__init__(self.queue)

    def set_message(
        self, lines: list[str], clear: bool = False, brightness: float | None = None
    ) -> None:
        self.queue.put(LcdData(lines, clear=clear, brightness=brightness))

    def set_brightness(self, brightness: float) -> None:
        self.queue.put(LcdData([], brightness))

    def first_tick(self) -> None:
        self._apply_message([], clear=True)
        self._apply_brightness(1.0)

    def tick(self, data: LcdData) -> None:
        self._apply_message(data.lines, data.clear)
        if data.brightness is not None:
            self._apply_brightness(data.brightness)

    def _apply_message(self, lines: list[str], clear: bool) -> None:
        if clear:
            self.lcd.clear()
        self.lcd.message = "\n".join(lines)

    def _apply_brightness(self, brightness: float) -> None:
        brightness = max(0.0, min(1.0, brightness)) * 65535
        self.brightness.duty_cycle = int(brightness)
