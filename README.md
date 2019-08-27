# RadioLoop
Raspberry Pi Zero - based audio slicer / sampler / looper with pitch and time modulation. Intended for use with a small portable FM radio

- Uses AnalogPin library (https://github.com/Fordi/rpi-analog-pin) to read analog potentiometers with the Pi Zero, without an ADC - just using 2 extra capacitors (1uF) and resistors (2.2k) - one for each potentiomenter. 