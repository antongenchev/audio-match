import librosa
import numpy as np
from statistics import NormalDist
from scipy.ndimage import label, maximum_position
from typing import Tuple, List

def load_audio(path:str)->Tuple[np.ndarray, int]:
    '''
    Load an audio file and return a 1D numpy array along with the sample rate

    Parameters:
        path: the path to the audio_file
    Returns:
        A tuple containing:
        - 1d numpy array. If the audio is stereo the two channels are averaged into 1
        - int which is the sample rate of the audio
    '''
    return librosa.load(path, sr=None)

def calculate_spectrogram(audio:np.ndarray, sr:int=44100, n_fft:int=2048, hop_length:int=512)->np.ndarray:
    '''
    Calculate the spectrogram of an audio signal provided as a numpy array.

    Parameters:
        audio: The audio signal represented as a 1D numpy array.
        sr: The sample rate of the audio signal. Default is 44100 Hz.
        n_fft: The number of samples for the Fast Fourier Transform (FFT).
            A higher value provides better frequency resolution but worse time resolution.
            Default is 2048.
        hop_length: The number of audio samples between successive FFT windows.
            Controls the overlap between frames. Default is 512.
    Returns:
        np.ndarray: A 2D numpy array representing the spectrogram of the audio.
        The values are in decibels (dB).
    '''
    spectrogram = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length)
    spectrogram_db = librosa.amplitude_to_db(np.abs(spectrogram), ref=np.max)
    return spectrogram_db

def find_spectrogram_peaks(spectrogram:np.ndarray, threshold:float=1) -> List[Tuple[int, int]]:
    '''
    Find the spectrogram peaks given a spectrogram

    Parameters:
        spectrogram: a numpy array where rows (the first index) is frequency bins and columns
            are time bins.
        threshold: disqualifies all points whose amplitude has z_score (normal distributiong) lower
            than the threshold. The point has to be significantly louder than the other points
    Returns:
        A list of tuples with the coordinates of the peaks inside the spectrogram.
        (x, y) -> x is the index of the time bin, y is the index of the frequency bin
    '''
    # Create a normal distribution from frequency intensities
    flattened = np.matrix.flatten(spectrogram)
    filtered = flattened[flattened > np.min(flattened)] # remove silence
    ndist = NormalDist(np.mean(filtered), np.std(filtered))
    zscore = np.vectorize(lambda x: ndist.zscore(x))
    zscore_matrix = zscore(spectrogram)
    mask_matrix = zscore_matrix > threshold # points above threshold vs ones below the threshold
    labelled_matrix, num_regions = label(mask_matrix) # label seperate islands of points above threshold
    label_indices = np.arange(num_regions) + 1
    peak_positions = maximum_position(zscore_matrix, labelled_matrix, label_indices)
    return peak_positions

def peaks_ij_to_tf(peaks:List[Tuple[int, int]], sr:int=41000, hop_length:int=512, n_fft:int=2048):
    '''
    Convert a list of peak coordinates (frequency_bin_index, time_bin_index) to (frequenct, time)

    Parameters:
        peaks: a list of tuples (x,y). x - index of frequency bin, y - index of time bin
        sr: the sample rate of the original audio
        hop_length: same as the parameter used when calculating the spectrogram using Short Term Fourier Transform
        n_fft: same as the parameter used when calculating the spectrogram using Short Term Fourier Transform
    '''
    times = librosa.frames_to_time([y for x, y in peaks], sr=41000, hop_length=512, n_fft=2048)
    frequencies = librosa.fft_frequencies(sr=sr)[[x for x, y in peaks]]
    peaks_ft = np.column_stack((frequencies, times))
    return peaks_ft
