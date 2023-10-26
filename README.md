# 74hc595 Library

Simple Library for my Shift Register Board.

## Usage

Connect `Serin`, `serial clock` and `register clock` to GPIO pins on the Raspberry Pi.
Use the GPIO numbers that are GPIOXX and not the pin numbers.

Connect `CLR` Pin to `3.3V` to enable storage in the serin-serout chain (we have a pull-down instead of a pull-up).
Connect `CLR` to a GPIO pin if you need to clear at some point in the program.

Connect `OE` to a GPIO if you need to disable the outputs at some point in the program. 

## Open Issues

### Hardware

* LEDs are quite bright --> Increase Resistors to 100 Ohm
* Pull-DOWN resistor on clear/reset should be an Pull-UP resistor
* can we squeeze the leyout so that we are one row smaller on a prototyping board


### Software

* Expand to multiple Shiftregisters
* Fix the Linting 
* Tune the delays so we don't waste time sleeping
