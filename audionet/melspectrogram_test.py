import librosa

wave, sr = librosa.core.load("./data/hiroshiba_normal/hiroshiba_normal_003.wav", sr=None)
print(f"input shape: {wave.shape}")

C = librosa.feature.melspectrogram(wave, sr=sr, n_fft=2048, hop_length=512, power=1.0)
print(f"mel-spectrogram: {C.shape}")
