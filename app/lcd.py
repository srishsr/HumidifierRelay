# SPDX-FileCopyrightText: 2018 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# Modified by Jonathan Seyfert, 2022-01-22
# to keep code from crashing when WiFi or IP is unavailable
from datetime import datetime
from subprocess import PIPE, Popen
from time import perf_counter, sleep

import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_dht
import board
import digitalio
import pwmio

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)

brightness = pwmio.PWMOut(board.D8, frequency=5000, duty_cycle=0)
brightness.duty_cycle = 0
brightness_value = 0
brightness_dir = 1

sensor1 = adafruit_dht.DHT11(board.D9)
sensor2 = adafruit_dht.DHT11(board.D27)

relay = digitalio.DigitalInOut(board.D21)
relay.direction = digitalio.Direction.OUTPUT
relay_state = False

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)


def setup_button(button):
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP


north_button = digitalio.DigitalInOut(board.D26)
setup_button(north_button)
east_button = digitalio.DigitalInOut(board.D16)
setup_button(east_button)
south_button = digitalio.DigitalInOut(board.D20)
setup_button(south_button)
west_button = digitalio.DigitalInOut(board.D19)
setup_button(west_button)


def get_sensor(sensor) -> tuple[float, float] | None:
    try:
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        return temperature_c, humidity
    except RuntimeError as error:
        print(error.args[0])
        sleep(2.0)
        return None


def get_button(button) -> bool:
    return button.value


# looking for an active Ethernet or WiFi device
def find_interface():
    #    dev_name = 0 # sets dev_name so that function does not return Null and crash code
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(":")[1]
            return dev_name
    return 1  # avoids returning Null if "state UP" doesn't exist


# find an active IP on the first LIVE network device
def parse_ip():
    if interface == 1:  # if true, no device is in "state UP", skip IP check
        return "not assigned "  # display "IP not assigned"
    ip = "0"
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(" ")[5]
            ip = ip.split("/")[0]
            return ip  # returns IP address, if found
    return (
        "pending      "  # display "IP pending" when "state UP", but no IPv4 address yet
    )


# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode("ascii")


# wipe LCD screen before we start
lcd.clear()


# before we start the main loop - detect active network device and ip address
# set timer to = perf_counter(), for later use in IP update check
interface = find_interface()
ip_address = parse_ip()
ip_timer = perf_counter()
message_timer = perf_counter()
brightness_timer = perf_counter()
sensor_timer = perf_counter()

while True:
    now = perf_counter()
    # check for new IP addresses, at a slower rate than updating the clock
    if now - ip_timer >= 15:
        interface = find_interface()
        ip_address = parse_ip()
        ip_timer = now

    if now - message_timer >= 0.1:
        # date and time
        lcd_line_1 = datetime.now().strftime("%b %d  %H:%M:%S\n")

        # current ip address
        lcd_line_2 = "IP " + ip_address

        # combine both lines into one update to the display
        lcd.message = lcd_line_1 + lcd_line_2
        message_timer = now

    if now - brightness_timer >= 0.01:
        brightness.duty_cycle = brightness_value * 65535
        brightness_value += brightness_dir * 0.01
        brightness_timer = now
        if brightness_value >= 1:
            brightness_dir = -1
        if brightness_value <= 0:
            brightness_dir = 1
        brightness_value = max(0, min(1, brightness_value))

    if now - sensor_timer >= 1.0:
        sensor1_data = get_sensor(sensor1)
        sensor2_data = get_sensor(sensor2)
        print(sensor1_data, sensor2_data)
        sensor_timer = now
        relay_state = not relay_state
        relay.value = relay_state
    # print(
    #     get_button(north_button),
    #     get_button(east_button),
    #     get_button(south_button),
    #     get_button(west_button),
    # )
    sleep(0.001)
