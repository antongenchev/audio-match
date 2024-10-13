import librosa
import numpy as np
import matplotlib.pyplot as plt
from src.audio_processing import peaks_ij_to_tf

'''
This file includes functions for visualising and plotting results for development purposes
'''

def plot_spectrogram(spectrogram:np.ndarray, sr:int=44100):
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(spectrogram, sr=sr, x_axis='time', y_axis='log', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.show()
