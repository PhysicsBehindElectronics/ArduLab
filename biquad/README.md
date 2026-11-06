

# Biquadratic filter

This program implements a generic biquadratic filter with Z-transform
$$
V(z) = \frac{a_0 + a_1 z^{-1}+a_2 z^{-2}}{1 - b_1 z^{-1} - b_2 z^{-2}}
$$
which leads to the difference equation

$$
y[n] = b_1 y[n-1] + b_2 y[n-2] + a_0 x[n] + a_1 x[n-1] + a_2 x[n-2] 
$$

The initial conditions $c_1=y[-1]$ and $c_2=y[-2]$ can also be set to specific values, if useful, otherwise they are set to 0.

After reset the circuit starts with preset 1 (see below). To setup an arbitrary filter stop the circuit with *ST* and change the coefficients $a_i, b_i$ and $c_i$ as desired. Type the coefficients as real numbers i.e. 1.414213562373... They will be converted internally as S7.24 numbers for $a_i, b_i$ and S15.16 for $c_i$. Restart the circuit with *RU* when done.

Please remember that the input voltage must be limited to [0..5] V.

## Presets
A few sets of coefficients that implement important circuits are preloaded in memory and can be recalled with the command *PR n*
where *n* is an integer between 1 and 7. A Table of the available presets is shown below. The values for time constants and
cut-off frequencies assume *T*=10 &#956;s.

| *n* | Description                                                                   |
|-----|-------------------------------------------------------------------------------|
| 1   | Copy input to output                                                          |
| 2   | Low pass filter with &#937; = 1 kHz i.e. f<sub>3dB</sub> &#8776; 159 Hz       |
| 3   | Derivator with &#120591; = 1 ms and *K*=10                                    |
| 4   | Integrator with &#120591; = 1 ms and *K*=10                                   |
| 5   | Phase shifter with &#120591; = 495 &#956;s i.e. f<sub>&#960;/2</sub> = 318 Hz |
| 6   | Harmonic oscillator with *f<sub>0</sub>*=1 kHz                                |
| 7   | Half integrator with *f<sub>0</sub>*=318 Hz                                   |
| 8   | Notch filter with *f<sub>0</sub>*=1 kHz and *a*=0.95                          |


## Input/Output Connections
 
| Name | Pin   | Description                               |
|------|-------|-------------------------------------------|
| A0   | J1 4  | DAC Output                                |
| A1   | J1 5  | ADC Input                                 |
| D10  | J2 13 | ISR Monitor (High when executing the ISR) |

## Commands

| Command | Par. Type | Range       | Units   | Description               |
|---------|-----------|-------------|---------|---------------------------|
| TS      | *uint*    | [10..10^6^] | &#956;s | Set Sampling Period       |
| ST      | *none*    |             |         | Stop Sampling             |
| RU      | *none*    |             |         | Resume Sampling           |
| A0      | *double*  | &#177;128   | none    | Set Coeff *a<sub>0</sub>* |
| A1      | *double*  | &#177;128   | none    | Set Coeff *a<sub>1</sub>* |
| A2      | *double*  | &#177;128   | none    | Set Coeff *a<sub>2</sub>* |
| B1      | *double*  | &#177;128   | none    | Set Coeff *b<sub>1</sub>* |
| B2      | *double*  | &#177;128   | none    | Set Coeff *b<sub>2</sub>* |
| C1      | *double*  | &#177;2048  | none    | Set Coeff *c<sub>1</sub>* |
| C2      | *double*  | &#177;2048  | none    | Set Coeff *c<sub>2</sub>* |
| PR      | *uint*    | [1..8]      | none    | Run Preset *n*            |




