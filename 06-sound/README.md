# Advanced Constructs

Signal Basics
- sample rate: number of samples per second
- we process the signal in equal-sized chunks
- 𝑃 is the (time) length of the analysis window
- 𝑁 is the number of samples
- use non-overlapping analysis windows

Input
- a .wav ϐile, PCM, sample rate 8–48 kHz
- such that it will be accepted by wave.open
- may be stereo or mono, 16 bit samples
- average the channels for stereo input
- ignore the ϐinal (incomplete) analysis window
- you can use struct.unpack to decode the samples

Output
- a peak is a frequency component with amplitude ≥ 20𝑎
- where 𝑎 is the average amplitude in the same window
- print the highest- and lowest-frequency peak encountered
- in the form low = 37, high = 18000
- print no peaks if there are no peaks
- the numbers are in Hz, precision = exactly 1Hz

Invocation & Hints
- invocation: ./peaks.py audio.wav
- the output goes to stdout
- only a single line for the entire ϐile
- think about how precision relates to 𝑁
- generate simple sine wave inputs for testing
- also a sum of sine waves at different frequencies

        ./peaks.py Mono_random.wav