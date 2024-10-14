import numpy as np
import binascii
from collections import Counter
from src.database_connection import get_db_connection
from src.audio_processing import calculate_spectrogram, load_audio, find_spectrogram_peaks, peaks_ij_to_tf
from src.hashing import generate_hashes

def recognise_audio(audio:np.ndarray, top_h:int=5):
    '''
    top_n - How many of the best matches to show. i.e. return the top nth
    '''
    spectrogram = calculate_spectrogram(audio)
    peaks = find_spectrogram_peaks(spectrogram)
    hashes = generate_hashes(peaks)
    binary_hashes = [(binascii.unhexlify(x[0]), x[1]) for x in hashes]
    potential_matches = {} # keys are audio ids, difference between time offsets
    with get_db_connection() as connection:
        try:
            cursor = connection.cursor()
            for binary_hash, time_offset in binary_hashes:
                cursor.execute(" SELECT audio_id, time_offset FROM audio_fingerprints WHERE fingerprint = %s", (binary_hash,))
                rows = cursor.fetchall()
                for row in rows:
                    if row[0] not in potential_matches.keys():
                        potential_matches[row[0]] = []
                    potential_matches[row[0]].append(row[1] - time_offset)
        except:
            cursor.close()
    rated_matches = {}
    for song_id, time_diffs in potential_matches.items():
        rated_matches[song_id] = Counter(time_diffs).most_common(1)[0]
    # sorted_matches = [(audio_id, offset, number of matches),...]
    sorted_matches = [(key, value[0], value[1]) for key, value in sorted(rated_matches.items(), key=lambda item: item[1][1], reverse=True)]
    sorted_matches.extend([None] * (top_h - len(sorted_matches)))
    result = {
        'num_hasehs': len(hashes),
        'top_matches': [sorted_matches][:top_h],
        }
    return result