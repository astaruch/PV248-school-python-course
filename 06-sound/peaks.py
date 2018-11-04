from sys import argv
import numpy as np
import struct
import wave


def get_window(data, mono, framerate):
    window = []
    current_sample = 0
    data_it = struct.iter_unpack('h', data)
    for data_tuple in data_it:
        channel_1 = data_tuple[0]
        channel_2 = 0
        if not mono:
            try:
                channel_2 = next(data_it)[0]
            except StopIteration:
                print('Invalid source file.', StopIteration)
                break
        window.append((channel_1 + channel_2) / 2)
        current_sample += 1
        if current_sample == framerate:
            yield window
            del window[:]
            current_sample = 0


def analyze_window(window, low, high):
    amplitudes = np.abs(np.fft.rfft(window))
    peaks = np.argwhere(amplitudes >= 20 * np.average(amplitudes))
    if len(peaks) > 0 and peaks.min() < low:
        low = peaks.min()
    if len(peaks) and peaks.max() > high:
        high = peaks.max()
    return (low, high)


def main():
    filename = argv[1]
    with wave.open(filename, 'rb') as wav_file:
        # number_of_samples = wav_file.getnframes() / wav_file.getframerate()
        framerate = wav_file.getframerate()
        mono = True if wav_file.getnchannels == 1 else False
        data = wav_file.readframes(wav_file.getnframes())
    low = np.inf
    high = -np.inf

    for window in get_window(data, mono, framerate):
        (low, high) = analyze_window(window, low, high)

    if np.isfinite(low) and np.isfinite(high):
        print('low = {}, high = {}'.format(low, high))
    else:
        print('no peaks')


if __name__ == '__main__':
    main()
