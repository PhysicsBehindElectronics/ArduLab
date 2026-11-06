

# Oscilloscope

This program implements a simple two channel oscilloscope. It can be
used to acquire low frequency (up to 50 kHz) signals when a digital
oscilloscope is not available.
 
The device has the following limitations:
  * Minimum sampling interval is 10 &#956;s, so the Nyquist band is limited to 50 kHz.
  * Fixed vertical scale input range: from 0 to 5V[^1] with 14 bits resolution i.e. 0.3 mV. 
  * Fixed number of points per trace *N* = 1000.
  * Very primitive trigger, see below.
  * The python GUI runs only in single scan mode: you have to press the *RUN* button each time to retrigger "the instrument". 

[^1]: Do not exceed these limits or the Arduino will be damaged. If you need a broader input voltage interval you must build a front-end using an opamp.

## Triggering
There are two trigger modes:
  * Software: acquisition is started after receiving the *AR* command.
  * External: according to the signal applied to the A9 pin. Both level and polarity can be controlled.
Triggering on CH1 or CH2, therefore, requires placing a jumper by hand between A5 and A1 or A2. The first point in the spectra is within one sampling interval

## Input/Output Connections
 
| Name | Pin   | Description                               |
|------|-------|-------------------------------------------|
| A1   | J1 5  | Chan. 1 Input                             |
| A2   | J1 6  | Chan. 2 Input                             |
| A5   | J1 9  | Ext. trigger Input                        |
| D10  | J2 13 | ISR Monitor (High when executing the ISR) |

## Commands

| Command | Par. Type | Range       | Units   | Description                            |
|---------|-----------|-------------|---------|----------------------------------------|
| CH      | *uint*    | [0..3]      | none    | Turn Ch *n* On (0=both Off, 3=both On) |
| AR      | *none*    |             |         | Arm trigger                            |
| CA      | *none*    |             |         | Abort acquisition                      |
| DT      | *uint*    | [10..10^6^] | &#956;s | Set sampling time                      |
| EX      | *bool*    | 0,1         |         | Use external trigger                   |
| TL      | *double*  | [0..5]      | V       | Set ext. trigger level                 |
| TP      | *bool*    | 0,1         |         | Set ext. trigger edge (0=pos.)         |
| RD      | *uint*    | [1..3]      | none    | Read Ch *n* (3=both)                   |

The *RD n* commands return a binary stream of 2000 bytes per channel. Each couple of bytes is a *uint* number in the [0..2^14^-1] range. See the python code.
