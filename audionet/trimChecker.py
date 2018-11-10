from pathlib import Path
import librosa

path_list = [
    str(Path("./audionet/hiroshiba_normal/hiroshiba_normal_001.wav")),
    str(Path("./audionet/hiroshiba_normal/hiroshiba_normal_002.wav")),
    str(Path("./audionet/hiroshiba_normal/hiroshiba_normal_003.wav")),

    str(Path("./audionet/tsuchiya_normal/tsuchiya_normal_001.wav")),
    str(Path("./audionet/tsuchiya_normal/tsuchiya_normal_002.wav")),
    str(Path("./audionet/tsuchiya_normal/tsuchiya_normal_003.wav")),
]

for i, path in enumerate(path_list):
    full_wave, sr = librosa.core.load(path)
    trimed, _ = librosa.effects.trim(full_wave, top_db=40, frame_length=int(sr*0.1))
    librosa.output.write_wav(Path("results")/f"{i}.wav", trimed, sr)
