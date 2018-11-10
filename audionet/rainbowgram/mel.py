import numpy as np
from librosa.core import hz_to_mel
from librosa.core import mel_to_hz

def mel(sr, n_fft, n_mels=128, fmin=0.0, fmax=None, htk=False, norm=1):
    if fmax is None:
        fmax = float(sr) / 2

    if norm is not None and norm != 1 and norm != np.inf:
        raise ParameterError('Unsupported norm: {}'.format(repr(norm)))

    # Initialize the weights
    n_mels = int(n_mels)
    ## (n_mel, mag_dim)
    weights = np.zeros((n_mels, int(1 + n_fft // 2)))

    # Center freqs of each FFT bin
    ## [0, center0, center1, center2, ..]
    fftfreqs = fft_frequencies(sr=sr, n_fft=n_fft)
    print(f"fftfreqs: {fftfreqs}")
    # 'Center freqs' of mel bands - uniformly spaced between limits
    ## [center0, center1, center2, ...] all element is center frequency [Hz], which is binned based on mel-scale
    mel_f = mel_frequencies(n_mels + 2, fmin=fmin, fmax=fmax, htk=htk)
    print(f"mel_f: {mel_f}")
    fdiff = np.diff(mel_f) # finite diff -> width of mel-bin
    print(f"fdiff: {fdiff}")
    # apply subtract (a-b) to all combination of a & b
    ramps = np.subtract.outer(mel_f, fftfreqs)
    print(f"ramps[2]: {ramps[2]}") # vector
    # print(f"ramps shape: {ramps.shape}")
    # (mel_center - fft_center) for all combination
    # ramps.shape = (mel_f, fftfreqs)



    for i in range(n_mels):
        # lower and upper slopes for all bins
        ## a type of scaling
        lower = -ramps[i] / fdiff[i] # -1 * (vector indexed by j, mel[i] - normal[j])/ (<scalar> width of mel-bin [(mel)Hz])
        if i == 2:
            print(f"lower of i==2: {lower}")
        # print(f"fdiff[i]: {fdiff[i]}")
        upper = ramps[i+2] / fdiff[i+1] 

        # .. then intersect them with each other and zero
        # 0 <= weight[i] <=
        weights[i] = np.maximum(0, np.minimum(lower, upper))
        # print(f"weights[i]: {weights[i]}")
        # weights[i] is array
        # determine weight for single frequency bin
        ## mel_nized_value[mel_frequency_bin_i] = sigma_to_j w[i,j]*freq[j] (j == normal_frequency_bin_j)


    if norm == 1:
        # Slaney-style mel is scaled to be approx constant energy per channel
        enorm = 2.0 / (mel_f[2:n_mels+2] - mel_f[:n_mels])
        weights *= enorm[:, np.newaxis]

    # Only check weights if f_mel[0] is positive
    # if not np.all((mel_f[:-2] == 0) | (weights.max(axis=1) > 0)):
    #     # This means we have an empty channel somewhere
    #     warnings.warn('Empty filters detected in mel frequency basis. '
    #                   'Some channels will produce empty responses. '
    #                   'Try increasing your sampling rate (and fmax) or '
    #                   'reducing n_mels.')

    return weights

def fft_frequencies(sr=22050, n_fft=2048):
    return np.linspace(0,
                       float(sr) / 2,
                       int(1 + n_fft//2),
                       endpoint=True)

def mel_frequencies(n_mels=128, fmin=0.0, fmax=11025.0, htk=False):
    # 'Center freqs' of mel bands - uniformly spaced between limits
    min_mel = hz_to_mel(fmin, htk=htk)
    max_mel = hz_to_mel(fmax, htk=htk)

    mels = np.linspace(min_mel, max_mel, n_mels)

    return mel_to_hz(mels, htk=htk)

# print(mel(16000, 512, n_mels=128, htk=True))
print(mel(16000, 512, n_mels=128, htk=False))
