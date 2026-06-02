# A simple DDS

This program implements a simple 24 bits low frequency DDS. The
maximum (and default) clock frequency is 100 kHz, it can be reduced
via software. The vertical resolution is 12 bits. The output range is
limited to 0..5 V and centered around 2.5V. A DC block capacitor
should be added to obtain a signal centered around 0 V. A low pass
filter at about 40% of the clock frequency can be used to remove the
discretization noise. For example a second order Sallen-Kay filter
could be a good choice.  The amplitude can be programmed with 10 bits
resolution (0=off, 1023=full scale).

An auxiliary digital output copies the MSB of the phase counter so it generates a square wave with a duty cycle of
(almost) 50%.

A second digital output stays high when the program is inside the periodic IRQ routine driving the dds.

## Input/Output Connections
 
| Name | Pin | Description |
|------|-----|-------------|
| A0   | JP1 4   | Analog Output |
| D12  | JP2 15  | Digital Ouput (MSB of phase counter)|
| D10  | JP2 13  | IRQ Monitor (High when in the periodic IRQ routine)|


## Commands

| Command | Par. Type | Range | Units | Description |
|---------|-----------|-------|-------|-------------|
| TS      | `uint`    | [10..10<sup>6</sup>]  | us | Set Sampling Period |
| FR      | `double`  | [0.1,10000] | Hz | Set Output Frequency |
| AM      | `uint`    | [0,1023]  | A.U. | Set Output Amplitude |
| RS      |  `none`   |   |  | Reset to Defaults |

