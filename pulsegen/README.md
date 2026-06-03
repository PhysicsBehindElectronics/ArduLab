# A dual pulse generator

This program implements dual channel digital output (0..5 V) pulse
generator with programmable duty cycle. It uses a 48 MHz clock so it
has a maximum operating frequency of 24 MHz with a resolution of about
21 ns since it uses internal 32 bits counters as dividers by `n`.  The
duty cycle is programmable with the same resolution.  Except for the
main clock the two channels are completely independent.

The possibility to generate `m` pulses and then stop is not
implemented but should be easy to add.

## Input/Output Connections
 
| Name | Pin | Description |
|------|-----|-------------|
| D7  | JP2 8  | Digital Ouput Ch. 1|
| D2  | JP2 3  | Digital Ouput Ch. 2|


## Commands

| Command | Par. Type | Range | Units | Description |
|---------|-----------|-------|-------|-------------|
| S1      | `none`    |       |       | Stop Ch. 1  |
| S2      | `none`    |       |       | Stop Ch. 2  |
| R1      | `none`    |       |       | Run Ch. 1   |
| R2      | `none`    |       |       | Run Ch. 2   |
| P1      | `double`  | [0.042,4.2e9] |  us   | Period Ch. 1   |
| P2      | `double`  | [0.042,4.2e9] |  us   | Period Ch. 2   |
| U1      | `double`  | [0.021,P1[ |  us   | Up time for Ch. 1 |
| U2      | `double`  | [0.021,P2[ |  us   | Up time for Ch. 2 |
| RS      |  `none`   |            |       | Reset to Defaults |

where P`n` is the period of channel `n`.
