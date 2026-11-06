# A dual pulse generator

This program implements dual channel digital output (0..5 V) pulse
generator with programmable duty cycle. It uses a 48 MHz clock so it
has a maximum operating frequency of 24 MHz with a resolution of about
21 ns since it uses internal 32 bits counters as dividers by *n*.  The
duty cycle is programmable with the same resolution.  Except for the
main clock the two channels are completely independent.

The possibility to generate *m* pulses and then stop is not
implemented but should be easy to add.

## Input/Output Connections
 
| Name | Pin   | Description         |
|------|-------|---------------------|
| D7   | J2 10 | Digital Ouput Ch. 1 |
| D2   | J2 5  | Digital Ouput Ch. 2 |



## Commands

| Command | Par. Type | Range          | Units   | Description       |
|---------|-----------|----------------|---------|-------------------|
| S1      | *none*    |                |         | Stop Ch. 1        |
| S2      | *none*    |                |         | Stop Ch. 2        |
| R1      | *none*    |                |         | Run Ch. 1         |
| R2      | *none*    |                |         | Run Ch. 2         |
| P1      | *double*  | [0.042..10^9^] | &#956;s | Period Ch. 1      |
| P2      | *double*  | [0.042..10^9^] | &#956;s | Period Ch. 2      |
| U1      | *double*  | [0.021..P1[    | &#956;s | Up time for Ch. 1 |
| U2      | *double*  | [0.021..P2[    | &#956;s | Up time for Ch. 2 |
| I1      | *bool*    | 0,1            |         | Invert Ch. 1      |
| I2      | *bool*    | 0,1            |         | Invert Ch. 2      |
| SY      | *none*    |                |         | Sync. the outputs |
| RS      | *none*    |                |         | Reset to Defaults |

