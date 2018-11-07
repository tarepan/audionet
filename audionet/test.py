import librosa

weve, sr = librosa.core.load("./audionet/hiroshiba_normal_001.wav", sr=None)
print(sr)
