# Advanced Constructs 2, Pitfalls

Music Analysis
- invocation: ./music.py 440 audio.wav
- 440 is the frequency of the pitch a’
- audio.wav is the same as for exercise 6
- use a sliding window for .1 second precision
- print peak pitches instead of frequencies

: Output
01.0-02.3 e+0 gis+0 b+0
10.0-12.0 b'+10
12.0-12.7 C+0 e-3
- consider only the 3 most prominent peaks
- print 1 line for each segment with the same peaks
- print nothing for segments with no peaks
- order the peaks by increasing frequency

        ./music.py 440 ../06-sound/Mono_random.wav