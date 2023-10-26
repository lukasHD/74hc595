# Quick Test

from time import sleep
from enum import Enum
from gpiozero import DigitalOutputDevice

REGISTER_CLK_PIN = 22
SERIAL_CLK_PIN = 27
SERIN_PIN = 17
# SEROUT_PIN = 14


class Clocktype(Enum):
    """clocktype specifies if the clock is active on rising or falling edge"""

    RISING = 1
    FALLING = 2


class ClockPin(DigitalOutputDevice):
    """ClockPin Class extends a standard DigitalOutputDevice but alllows a pulse method"""

    def __init__(self, pin, clk_type: Clocktype = Clocktype.RISING):
        self.clk_time = 0.00001  # 10µs
        self.type = clk_type
        if clk_type == Clocktype.RISING:
            super().__init__(pin=pin, initial_value=False, active_high=True)
        else:
            super().__init__(pin=pin, initial_value=False, active_high=False)
        self.off()

    def pulse(self):
        """Pulse the Clock once with sleep at the start"""
        self.on()
        sleep(self.clk_time)
        self.off()
        sleep(self.clk_time)


class SR_74hc595:
    """simple library for a single 74hc595 Chip on a borad with pullup/down on reset/clear and output enable"""

    def __init__(
        self,
        serin_pin=SERIN_PIN,
        serin_clk_pin=SERIAL_CLK_PIN,
        register_clk_pin=REGISTER_CLK_PIN,
    ) -> None:
        self.serial_in = DigitalOutputDevice(serin_pin, initial_value=False)
        self.serial_clk = ClockPin(serin_clk_pin)
        self.register_clk = ClockPin(register_clk_pin)
        self.settle_time = 0.00001  # 10µs

    def write_char(self, value: bool) -> None:
        """Write single boolean value into the shift storage.
        Values of the shift not latched into the register.
        Call latch() to do so.
        """
        assert isinstance(value, bool)
        if value:
            self.serial_in.on()
        else:
            self.serial_in.off()
        sleep(self.settle_time)
        self.serial_clk.pulse()

    def write_word(self, input_word: str) -> None:
        """Write a whole word into the single shift register.
        ATTENTION: Asserts that the input_word is exactly 8 characters long.
        input_word can only contain the charcters '1' or '0'
        """
        assert len(input_word) == 8
        for char in input_word:
            if char == "1":
                char_bool = True
            elif char == "0":
                char_bool = False
            else:
                raise ValueError()
            self.write_char(char_bool)

    def latch(self) -> None:
        """Latch the values into the output registers.
        If N_Output_Enable is LOW then the values are present at the outputs.
        """
        self.register_clk.pulse()

    def write_and_load(self, input_word: str, reverse_word: bool = False) -> None:
        """write the word to the Shiftregister and latch it to the outputs.
        Allows a reversal of the value to tune LSB/MSB notation.
        """
        if reverse_word:
            input_word = input_word[::-1]
        self.write_word(input_word)
        self.latch()


BLINKENLIGHTS = 0.2


def counter1(sr: SR_74hc595):
    for x in range(256):
        s = f"{x:08b}"
        sr.write_and_load(s, reverse_word=True)
        sleep(BLINKENLIGHTS / 4)


def counter2(sr: SR_74hc595):
    for x in range(256):
        s = f"{x:08b}"
        sr.write_and_load(s)
        sleep(BLINKENLIGHTS / 4)


def checker(sr: SR_74hc595):
    sr.write_and_load("10101010")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("01010101")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("10101010")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("01010101")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000000")
    sleep(BLINKENLIGHTS)


def kit(sr: SR_74hc595):
    sr.write_and_load("00000001")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000001")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000010")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000100")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00001000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00010000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00100000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("01000000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("10000000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("01000000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00100000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00010000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00001000")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000100")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000010")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000001")
    sleep(BLINKENLIGHTS)
    sr.write_and_load("00000000")
    sleep(BLINKENLIGHTS)


def execute_test():
    sr = SR_74hc595()
    print("Let's get this party started!")
    sleep(1)
    checker(sr=sr)
    sleep(3)
    kit(sr=sr)
    sleep(3)
    counter1(sr=sr)
    sleep(3)
    counter2(sr=sr)


if __name__ == "__main__":
    execute_test()
