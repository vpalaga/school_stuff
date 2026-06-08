## derivation of sound equation (no help)
standard music follows this rule: **for every octave, the frequency doubles.**

for example, A3 → A4: 440hz → 880hz

this means:

$f(x) = m \times 2^x$

we also know that $f(1) = 1, f(2) = 2, f(3) = 4$

so, $m = \frac{1}{2}$ 

we need to shift the function, so $f(3)=440$

solve for $q$ at $x=3$: 

$$
\frac{2^{3+q}}{2}=440
$$
$$
2^{3 + q}=880
$$
$$
2^3 \times 2^q = 880
$$
$$
2^q = 110
$$

combine with original equation
$$
f(x) =\frac{2^x + 110}{2}
$$
and simplify into final form
$$
f(x)= 2^x \times 55
$$

``` python
import numpy as np
import sounddevice as sd

# Parameters
sample_rate = 44100  # samples per second
frequency = 440.0    # Hz (A4 note)
amplitude = 0.5

# Time variable (continuous phase)
phase = 0

def callback(outdata, frames, time, status):
    global phase
    t = (np.arange(frames) + phase) / sample_rate
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    outdata[:] = wave.reshape(-1, 1)
    phase += frames

# Open stream
with sd.OutputStream(channels=1, callback=callback, samplerate=sample_rate):
    print("Playing... Press Ctrl+C to stop")
    while True:
        pass
```