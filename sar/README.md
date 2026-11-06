# 8 bit Successive approximations AD converter

This program implements an 8 bits *successive approximations* ADC for
signals between 0 and 5 V.  It uses the internal analog comparator and
a dedicated 8 bits DAC internally connected to the inverting input of
the comparator. The conversion clock runs, by default, at 100 kHz so a
full conversion requires 80 &#956;s. The ADC is continuously running.

A digital *CONV* signal goes high at the beginning of each conversion
and can be used as a trigger.  The output of the comparator is
available at the *Comparator Output* pin so looking at its 8 values
after a *CONV* rising edge provides the result of the conversion from
MSB to LSB.  The analog value applied at the inverting input of the
comparator is presented to the A0 pin so the binary tree explored
during the conversion can be observed.

## Input/Output Connections
 
| Name | Pin   | Description       |
|------|-------|-------------------|
| A5   | J1 9  | Analog Input      |
| D12  | J2 15 | Comparator Output |
| D11  | J2 14 | CONV              |
| A0   | J1 4  | Analog Monitor    |
| D10  | J2 13 | ISR Monitor       |

## Commands

| Command | Par. Type | Range                | Units   | Description  |
|---------|-----------|----------------------|---------|--------------|
| TS      | *uint*    | [10..10<sup>6</sup>] | &#956;s | Timer period |
| RS      | *none*    |                      |         | Reset        |

