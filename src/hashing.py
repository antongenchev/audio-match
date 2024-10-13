import binascii
import hashlib
from typing import List, Tuple
from src.database_connection import get_db_connection

def generate_hashes(peaks:List[Tuple[int, int]], fan_value:int=10) -> List[Tuple[str, int]]:
    '''
    Generate hashes given a list of peaks and a fan_value. The peaks in the list must be ordered by time.
    Each hash is generate using the time difference of two peaks and their frequenct bins

    Parameters:
        peaks: a list of tuples, each tuple representing a single peak.
            The tuples consist of two integers: the time bin and the frequency bin
        fan_value: an integer parameter describing how close two peaks have to create a hash.
            fan_value=10 means that each peak will be considered as a pair with its 9 closest neighbours.
    Returns:
        A list of tuples consisting of the string hash and the time bin of the first peak for the hash
    '''
    hashes = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            # Consider each pair of peaks (i,i+1), (i,i+2), ..., (i,i+fan_value-1)
            if (i + j) < len(peaks): # Make sure we don't index out of range
                f1 = peaks[i][1]
                f2 = peaks[i + j][1]
                t1 = peaks[i][0]
                t2 = peaks[i + j][0]
                t_delta = t2 - t1
                # Calcuate the SHA-1 hash of the peak pair
                h = hashlib.sha1(f"{str(f1)}{str(f2)}{str(t_delta)}".encode('utf-8'))
                hashes.append((h.hexdigest(), t1)) # sha1 hash = 20 bytes -> 40 hexadecimal symbols
    return hashes

def save_hashes(audio_id:int, hashes:List[Tuple[str, int]]):
    '''
    Save a list of hashes to the database

    Parameters:
        audio_id: the id of the song in the database
        hashes: a list of tuples. Each tuple consisting of a hash and a time offset
    '''
    with get_db_connection() as connection:
        try:
            cursor = connection.cursor()
            # Turn the hashes from strings to bytes and add the song and insert them in the audio_hashes table
            hashes_with_song_id = [(audio_id, binascii.unhexlify(hash_value), time_offset) for hash_value, time_offset in hashes]
            cursor.executemany("INSERT INTO audio_fingerprints (audio_id, fingerprint, time_offset) VALUES (%s, %s, %s)",
                               hashes_with_song_id)
            connection.commit()
        finally:
            cursor.close()