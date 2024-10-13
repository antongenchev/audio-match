import unittest
import numpy as np
from src.audio_processing import load_audio, calculate_spectrogram

class TestAudioProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        try:
            self.audio, self.sr = load_audio('tests/test_data/test_audio.wav')
        except Exception as e:
            print(f'Error loading the aduio: {e}')

    def test_calculate_spectrogram(self):
        spectrogram = calculate_spectrogram(self.audio)
        self.assertEqual(type(spectrogram), np.ndarray)
        self.assertEqual(spectrogram.shape, (1025, 8262))
        spectrogram = calculate_spectrogram(self.audio, n_fft=1024)
        self.assertEqual(spectrogram.shape, (513, 8262))
