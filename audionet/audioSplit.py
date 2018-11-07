from pathlib import Path
import librosa

path_list = [
    str(Path("./audionet/neko_000.mp3")),
    # str(Path("./audionet/noja_001.mp3")),
    # str(Path("./audionet/noja_002.mp3")),
    # str(Path("./audionet/noja_003.mp3")),
    # str(Path("./audionet/noja_004.mp3")),
    # str(Path("./audionet/noja_005.mp3")),
]

total_sec = 0
print(path_list)
for i, path in enumerate(path_list):
    print(path)
    full_wave, sr = librosa.core.load(path)
    split_points = librosa.effects.split(full_wave, top_db=40, frame_length=int(22050*0.3))
    for j, audio_range in enumerate(split_points):
        print(f"{j}: {audio_range}")
        file_name = f"{i}.{j}.wav"
        criterion_sec = 0.005 * 128
        range_sec = (audio_range[1] - audio_range[0])/22050
        if range_sec > criterion_sec:
            wave = full_wave[audio_range[0]:audio_range[1]]
            librosa.output.write_wav(Path("results")/file_name, wave, sr)
            total_sec += range_sec
print(f"total sample length: {total_sec} [sec]")
