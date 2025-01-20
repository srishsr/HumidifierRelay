import time

import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_dht
import board
import digitalio
import pwmio


def setup_button(button: digitalio.DigitalInOut) -> None:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP


class TestDevices:
    def __init__(self) -> None:
        self.relay = digitalio.DigitalInOut(board.D13)
        self.relay.direction = digitalio.Direction.OUTPUT
        lcd_columns = 16
        lcd_rows = 2

        lcd_rs = digitalio.DigitalInOut(board.D22)
        lcd_en = digitalio.DigitalInOut(board.D17)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d6 = digitalio.DigitalInOut(board.D23)
        lcd_d7 = digitalio.DigitalInOut(board.D18)

        self.lcd = characterlcd.Character_LCD_Mono(
            lcd_rs,
            lcd_en,
            lcd_d4,
            lcd_d5,
            lcd_d6,
            lcd_d7,
            lcd_columns,
            lcd_rows,
        )
        self.brightness = pwmio.PWMOut(board.D8, frequency=5000, duty_cycle=0)

        self.sensor1 = adafruit_dht.DHT11(board.D9)
        self.sensor2 = adafruit_dht.DHT11(board.D27)

        self.buttons = {
            "north": digitalio.DigitalInOut(board.D6),
            "east": digitalio.DigitalInOut(board.D10),
            "south": digitalio.DigitalInOut(board.D11),
            "west": digitalio.DigitalInOut(board.D26),
        }

        for button in self.buttons.values():
            setup_button(button)

        self.start_time = time.perf_counter()
        self.prev_relay = False

    def tick_lcd(self) -> None:
        dt = time.perf_counter() - self.start_time
        # ramp brightness 0..65535 up and down every second
        brightness = abs((dt % 1) - 0.5) * 2
        brightness = int(max(0, min(65535, brightness * 65535)))
        self.lcd.message = f"Hello, World!\n{dt:.1f}"
        self.brightness.duty_cycle = brightness

    def tick_relay(self) -> None:
        self.relay.value = not self.prev_relay
        self.prev_relay = not self.prev_relay

    def tick_sensors(self) -> None:
        for sensor in (self.sensor1, self.sensor2):
            try:
                temperature_c = sensor.temperature
                humidity = sensor.humidity
                print(f"Temp: {temperature_c} C, Humidity: {humidity}%")
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(1.0)

    def tick_buttons(self) -> None:
        all_data = []
        for name, button in self.buttons.items():
            is_pressed = not button.value
            all_data.append((name, is_pressed))
        print(all_data)

    def tick(self) -> None:
        self.tick_lcd()
        self.tick_relay()
        self.tick_sensors()
        self.tick_buttons()


def main() -> None:
    tester = TestDevices()
    while True:
        tester.tick()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
