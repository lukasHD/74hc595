'''Some module docstring'''

from time import sleep
from enum import Enum
from gpiozero import DigitalOutputDevice

# REGISTER_CLK_PIN = 37
# SERIAL_CLK_PIN = 35
# SERIN_PIN = 33
# REGISTER_CLR_PIN = 31
# OE_PIN= 29

# Use GPIO Numbers
# REGISTER_CLK_PIN = 19
# SERIAL_CLK_PIN = 26
REGISTER_CLK_PIN = 26
SERIAL_CLK_PIN = 19
SERIN_PIN = 13
REGISTER_CLR_PIN = 6
OE_PIN= 5

class Clocktype(Enum):
    """clocktype specifies if the clock is active on rising or falling edge"""

    RISING = 1
    FALLING = 2


class ClockPin(DigitalOutputDevice):
    """ClockPin Class extends a standard DigitalOutputDevice but alllows a pulse method"""

    def __init__(self, pin, clk_type: Clocktype = Clocktype.RISING, clk_time: float = 0.00000001):
        self.clk_time = clk_time 
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
    """simple library for a single 74hc595 Chip on a borad 
    with pullup/down on reset/clear and output enable
    """

    def __init__(
        self,
        serin_pin=SERIN_PIN,
        serin_clk_pin=SERIAL_CLK_PIN,
        register_clk_pin=REGISTER_CLK_PIN,
        clear_pin=REGISTER_CLR_PIN,
        output_en_pin=OE_PIN,
        number_of_chips: int = 1
    ) -> None:
        self.serial_in = DigitalOutputDevice(serin_pin, initial_value=False)
        # print("A")
        self.serial_clk = ClockPin(serin_clk_pin, clk_time=0.00000001)
        # print("B")
        self.register_clk = ClockPin(register_clk_pin, clk_time=0.00000001)
        # print("C")
        self.register_clr = DigitalOutputDevice(clear_pin, initial_value=True)
        # print("D")
        self.output_enable = DigitalOutputDevice(output_en_pin, initial_value=False)
        self.settle_time = 0.00000001  # 0.01µs
        # self.settle_time = 0.1  # 0.01µs
        assert number_of_chips > 0, "number_of_chips has to be positive integer"
        assert isinstance(number_of_chips, int) , "number_of_chips has to be integer"
        self.number_of_chips = number_of_chips
        self.word_length = 8*self.number_of_chips
        # print("E")

    def reset_sr(self):
        """Reset the SR to a clear State, does not effect the Outputs"""
        self.register_clr.off()
        sleep(self.settle_time * 5)
        self.register_clr.on()

    
    def reset(self):
        """Reset the SR and latch the values to the outputs"""
        self.reset_sr()
        self.latch()

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
        assert len(input_word) == self.word_length
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


def counter(sr: SR_74hc595, reverse_count :bool = False):
    for x in range(256):
        s = f"{x:08b}"
        sr.write_and_load(s, reverse_word=reverse_count)
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
    # sr.write_and_load("00000001")
    # sleep(BLINKENLIGHTS)
    BLINKENLIGHTS = 0.05
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
    # sr.write_and_load("10000000")
    # sleep(BLINKENLIGHTS)
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
    # sr.write_and_load("00000001")
    # sleep(BLINKENLIGHTS)
    # sr.write_and_load("00000000")
    # sleep(BLINKENLIGHTS)


def singe_pin_test(sr: SR_74hc595):
    print("CLR ON")
    sr.register_clr.on()
    sleep(5)
    print("CLR OFF")
    sr.register_clr.off()
    sleep(5)
    
    print("REGISTER CLK ON")
    sr.register_clk.on()
    sleep(5)
    print("REGISTER CLK OFF")
    sr.register_clk.off()
    sleep(5)
    
    print("SR CLK ON")
    sr.serial_clk.on()
    sleep(5)
    print("SR CLK OFF")
    sr.serial_clk.off()
    sleep(5)

    print("OUTPUT ENABLE ON")
    sr.output_enable.on()
    sleep(5)
    print("OUTPUT ENABLE OFF")
    sr.output_enable.off()
    sleep(5)

    print("SERIN ON")
    sr.serial_in.on()
    sleep(5)
    print("SERIN OFF")
    sr.serial_in.off()
    sleep(5)


def execute_test():
    sr = SR_74hc595(number_of_chips=1)
    sr.reset()
    
    # sr.register_clr.off()
    # sleep(1)
    # sr.register_clr.on()
    # sleep(1)
    # sr.output_enable.off()
    # sleep(1)

    # print("Set 1s")
    # sleep(1)
    # sr.write_and_load("11111111")
    # sleep(15)
    
    print("Let's get this party started!")
    sleep(1)
    checker(sr=sr)
    sleep(3)
    for _ in range (10):
        kit(sr=sr)
    sr.write_and_load("00000000")
    sleep(3)
    counter(sr=sr, reverse_count=True)
    sleep(3)
    counter(sr=sr, reverse_count=False)

    sleep(2)
    print("Reset now")
    sr.reset()


if __name__ == "__main__":
    execute_test()
