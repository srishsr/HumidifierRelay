from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import cast

import adafruit_character_lcd.character_lcd as characterlcd
import board
import digitalio
import pwmio

from app.devices.io.io_write_process import IoWriteProcess


class LcdSpecialCharacter(Enum):
    UP_ARROW = 0
    DOWN_ARROW = 1


@dataclass
class LcdData:
    lines: list[str]
    brightness: float | None = None
    clear: bool = False


class Lcd(IoWriteProcess[LcdData]):
    def __init__(self):
        self.lcd_columns = 16
        self.lcd_rows = 2

        lcd_rs = digitalio.DigitalInOut(board.D22)
        lcd_en = digitalio.DigitalInOut(board.D17)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d6 = digitalio.DigitalInOut(board.D23)
        lcd_d7 = digitalio.DigitalInOut(board.D18)

        self.stored_characters = {
            LcdSpecialCharacter.UP_ARROW: bytes(
                [0x0, 0x0, 0x4, 0xE, 0x1F, 0x0, 0x0, 0x0]
            ),
            LcdSpecialCharacter.DOWN_ARROW: bytes(
                [0x0, 0x0, 0x1F, 0xE, 0x4, 0x0, 0x0, 0x0]
            ),
        }

        self.lcd = characterlcd.Character_LCD_Mono(
            lcd_rs,
            lcd_en,
            lcd_d4,
            lcd_d5,
            lcd_d6,
            lcd_d7,
            self.lcd_columns,
            self.lcd_rows,
        )
        self.brightness = pwmio.PWMOut(board.D8, frequency=5000, duty_cycle=0)
        self.queue: Queue[LcdData] = cast(Queue[LcdData], Queue())
        self.prev_command: LcdData | None = None

        super().__init__(self.queue)

    def set_message(
        self, lines: list[str], clear: bool = False, brightness: float | None = None
    ) -> None:
        new_command = LcdData(lines, clear=clear, brightness=brightness)
        if new_command == self.prev_command:
            return
        self.prev_command = new_command
        self.queue.put(new_command)

    def set_brightness(self, brightness: float) -> None:
        self.set_message([], brightness=brightness)

    def first_tick(self) -> None:
        self._apply_message([], clear=True)
        self._apply_brightness(1.0)
        self._apply_special_characters()

    def tick(self, data: LcdData) -> None:
        self._apply_message(data.lines, data.clear)
        if data.brightness is not None:
            self._apply_brightness(data.brightness)

    def _apply_special_characters(self) -> None:
        for character, data in self.stored_characters.items():
            self.lcd.create_char(character.value, data)

    def _apply_message(self, lines: list[str], clear: bool) -> None:
        if clear:
            self.lcd.clear()
        text = []
        for line in lines:
            if isinstance(line, str):
                text.append(line)
        self.lcd.message = "\n".join(text)

    def _apply_brightness(self, brightness: float) -> None:
        brightness = max(0.0, min(1.0, brightness)) * 65535
        self.brightness.duty_cycle = int(brightness)
