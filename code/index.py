from pydub import AudioSegment
import numpy as np

def generate_hash(audio_file, chunk_size=2048):
    audio = AudioSegment.from_wav(audio_file)
    samples = np.array(audio.get_array_of_samples())

    hashes = []
    for i in range(0, len(samples), chunk_size):
        chunk = samples[i:i+chunk_size]
        fft_chunk = np.fft.fft(chunk)
        magnitude = np.log(np.abs(fft_chunk) + 1)
        avg_mag = np.average(magnitude)
        hash_val = 1 if magnitude[-1] > avg_mag else 0
        hashes.append(hash_val)

    return hashes

def compare_hashes(hash1, hash2):
    if len(hash1) != len(hash2):
        return False
    
    similarity = sum(bit1 == bit2 for bit1, bit2 in zip(hash1, hash2)) / len(hash1)
    return similarity

audio_file1 = 'drake.wav'
audio_file2 = 'dido.wav'

hash1 = generate_hash(audio_file1)
hash2 = generate_hash(audio_file2)

similarity = compare_hashes(hash1, hash2)

print(f'Similaridade: {similarity * 100:.2f}%')
