from sys import argv
from math import log2
import wave
import struct
import numpy as np

notes = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'bes', 'b']


def frequency_to_pitch(base_pitch, frequency):
    octave_length = 12
    # (middle C) = 69 + x => x = -9/12
    scaled = base_pitch * pow(2, - (octave_length + 9)/octave_length)
    distance = octave_length * (log2(frequency) - log2(scaled))

    tone_index = int(distance % octave_length)
    octave_index = int(distance // octave_length)
    cents = int(100 * (distance % 1))
    # print(tone_index, octave_index, cents)

    if cents > 50:
        tone_index += 1
        cents -= 100

    if tone_index >= octave_length:
        tone_index -= octave_length
        octave_index += 1

    tone_name = notes[tone_index]
    if octave_index >= 0:
        octave_suffix = "'" * octave_index
    else:
        octave_suffix = ',' * octave_index

    return "{}{}{}".format(tone_name, octave_suffix, cents)


def peak_clustering(peaks):
    if len(peaks) == 0:
        return []

    cluster = []
    clusters = []
    peak_distance = 1  # Hz
    for frequency, amplitude in peaks:
        if len(cluster) > 0:
            previous_freq = cluster[-1][0]
            if previous_freq == frequency - peak_distance:
                cluster += [(frequency, amplitude)]
            else:
                max_from_clusters = max(
                    cluster, key=lambda pair: pair[1]
                )
                clusters += [max_from_clusters]
                cluster = [(frequency, amplitude)]
        else:
            cluster = [(frequency, amplitude)]

        if len(cluster) > 0:
            max_from_cluster = max(
                cluster, key=lambda pair: pair[1]
            )
            clusters += [max_from_cluster]

    clusters = filter(lambda pair: pair[0] != 0, clusters)
    return list(clusters)


def process_input(data, stereo):
    out = []
    if stereo:
        for i in range(0, len(data), 2):
            c = data[i:i + 2]
            out.append((c[0] + c[1])/2.0)
    else:
        out = data
    return out


def get_peaks(window):
    amplitudes = np.fft.rfft(window)
    avg = sum([np.abs(b) for b in amplitudes])/len(amplitudes)

    peaks = []
    for fr, amplitude in enumerate(amplitudes):
        if np.abs(amplitude) >= avg:
            peaks.append((fr, np.abs(amplitude)))
    return peaks


def main():
    standard_pitch = int(argv[1])
    filename = argv[2]
    print(frequency_to_pitch(standard_pitch, 115))

    with wave.open(filename, 'rb') as wav_file:
        channels = wav_file.getnchannels()
        framerate = wav_file.getframerate()
        number_of_frames = wav_file.getnframes()
        stereo = True if channels == 2 else False
        data_bytes = wav_file.readframes(number_of_frames)
        data = [x for x in struct.unpack('{}h'.format(
            channels * number_of_frames), data_bytes)]

        window_size = int(framerate * 0.1)

        window = []
        peaks = []
        window_start = 0.0
        window_end = 0.1

        fin = []

        while data:
            frames = data[:window_size]
            del data[:window_size]
            if len(frames) == window_size:
                window += process_input(frames, stereo)

                if len(window) < framerate:
                    continue

                while len(window) > framerate:
                    del window[:window_size]

                peaks = get_peaks(window)
                # print(peaks)

                clusters = peak_clustering(peaks)
                # print(clusters)
                clusters = sorted(peaks, key=lambda p: p[1])
                clusters = clusters[-3:]
                # print(clusters)

                out = []
                for cluster in sorted(clusters, key=lambda p: p[0]):
                    out.append(frequency_to_pitch(standard_pitch, cluster[0]))

                fin.append({
                    'start': window_start,
                    'end': window_end,
                    'line': ' '.join(out)
                })
                window_start += 0.1
                window_end += 0.1

        # print(fin)
        for l in fin:
            print('%.1f-%.1f %s' % (l['start'], l['end'], l['line']))


if __name__ == '__main__':
    main()
