# Quick Test 

import RPi.GPIO as GPIO
from time import sleep


# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

REGISTER_CLK_PIN = 22
SERIAL_CLK_PIN = 27
SERIN_PIN = 17
# REGISTER_CLK_PIN = 15
# SERIAL_CLK_PIN = 13
# SERIN_PIN = 11
# SEROUT_PIN = 14

CLK_TIME = 0.001 # 10µs
SETTLE_TIME = 0.001 # 10µs

def pulse_ser_clk():
    GPIO.output(SERIAL_CLK_PIN, GPIO.HIGH)
    sleep(CLK_TIME)
    GPIO.output(SERIAL_CLK_PIN, GPIO.LOW)
    sleep(CLK_TIME)

def pulse_register_clk():
    GPIO.output(REGISTER_CLK_PIN, GPIO.HIGH)
    sleep(CLK_TIME)
    GPIO.output(REGISTER_CLK_PIN, GPIO.LOW)
    sleep(CLK_TIME)

def write_char(value :bool):
    assert type(value) == bool
    GPIO.output(SERIN_PIN, value)
    sleep(SETTLE_TIME)
    pulse_ser_clk()

def write_word(input :str):
    assert len(input) == 8
    for char in input:
        if char == "1":
            char_bool = True
        elif char == "0":
            char_bool = False
        else: 
            raise(ValueError())
        write_char(char_bool)

def latch():
    pulse_register_clk()
    pass

def write_and_load(input :str, reversed :bool = False):
    if reversed:
        input = input[::-1]
    write_word(input)
    latch()

def initialize_gpio():
    GPIO.setup(REGISTER_CLK_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SERIAL_CLK_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SERIN_PIN, GPIO.OUT, initial=GPIO.LOW)

def execute_test():
    initialize_gpio()
    print("Let's get this party started!")
    print("Set Serial to 1")
    GPIO.output(SERIN_PIN, GPIO.HIGH)
    sleep(1)
    BLINKENLIGHTS = 0.2
    write_and_load("10101010")
    sleep(BLINKENLIGHTS)
    write_and_load("01010101")
    sleep(BLINKENLIGHTS)
    write_and_load("10101010")
    sleep(BLINKENLIGHTS)
    write_and_load("00000000")
    sleep(1)
    sleep(BLINKENLIGHTS)
    write_and_load("00000001")
    sleep(BLINKENLIGHTS)
    write_and_load("00000001")
    sleep(BLINKENLIGHTS)
    write_and_load("00000010")
    sleep(BLINKENLIGHTS)
    write_and_load("00000100")
    sleep(BLINKENLIGHTS)
    write_and_load("00001000")
    sleep(BLINKENLIGHTS)
    write_and_load("00010000")
    sleep(BLINKENLIGHTS)
    write_and_load("00100000")
    sleep(BLINKENLIGHTS)
    write_and_load("01000000")
    sleep(BLINKENLIGHTS)
    write_and_load("10000000")
    sleep(BLINKENLIGHTS)
    write_and_load("00000000")
    sleep(BLINKENLIGHTS)

    for x in range(256):
        s = "{:08b}".format(x)
        # print(s)
        write_and_load(s, reversed = True)
        sleep(BLINKENLIGHTS/4)
    for x in range(256):
        s = "{:08b}".format(x)
        # print(s)
        write_and_load(s)
        sleep(BLINKENLIGHTS/4)

if __name__ == "__main__":
    execute_test()