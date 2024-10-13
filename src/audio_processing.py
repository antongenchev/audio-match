import librosa
import numpy as np
from typing import Tuple

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
