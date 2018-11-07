# 1~L   ## len() == L
# 1~Ns == [0,0, ...]    ## Len() == Ns
# L-(Ne-1) ~ L == [0,0,...] ## Len() == Ne

sampling_rate = 16000
length_total_sec = 2
length_total = int(sampling_rate * length_total_sec)
length_non_audio_start = int(sampling_rate*0.05)
length_non_audio_end = int(sampling_rate*0.05)
length_window = int(sampling_rate*0.3)

L = length_total
Ns = length_non_audio_start
Ne = length_non_audio_end
W = length_window

n_zero = 0

for x in range(1, L):
    end = x + (W-1)
    if x <= Ns:
        if end <= Ns:
            n_zero += W
        elif end < (L - (Ne-1)):
            n_zero += Ns - x + 1
        else:
            n_zero += (Ns - x + 1) + (end - (L-(Ne-1)) + 1)
    elif x < (L-(Ne-1)):
        if end < (L - (Ne-1)):
            n_zero += 0
        else:
            n_zero += end - (L-(Ne-1)) + 1
    else:
        n_zero += W

expectation = n_zero/L
print(f"E(n_zero) = {expectation}[samples]")
print(f"ratio = {expectation/L}")
