import librosa
import numpy as np

def bias_phase(C, type="noise"):
    bias = np.random.randn(C.shape[0], C.shape[1])
    if type == "uniform":
        # shift = 2.5
        shift = np.random.rand()
        bias.fill(shift)
    if type == "channel_uniform":
        for i in range(bias.shape[0]):
            single_f_seq = bias[i:i+1, :]
            single_f_seq.fill(np.random.rand())
            bias[i:i+1, :] = single_f_seq
    print(bias)
    # rorate based on arg (*exp(j*arg))
    return C * np.exp(1j*bias)



def rainbowgram2wave(set, hop_length=256):
    normed_log_mag = set[0]
    normed_if_arg = set[1]

    # normalized log magnitude => magnitude
    mag = np.exp(normed_log_mag)

    # normalized IF -> phase
    if_arg = np.pi * normed_if_arg
    phase_unwrapped = np.cumsum(if_arg, axis=1)
    arg = phase_unwrapped

    # 1. make (mag + 0j)
    # 2. rorate based on arg (*exp(j*arg))
    C = (mag + 0j) * np.exp(1j*arg)
    # C = bias_phase(C, type="uniform")
    reconstructed_wave = librosa.core.istft(C, hop_length=hop_length)
    return reconstructed_wave


def wave2rainbowgram(wav, n_fft=1024, hop_length=256):
    """
    Convert a wavefrom into frequency-domain time series
    Args:
        wav (numpy.ndarray(n,)):
    Returns:
        ndarray[2, 1 + n_fft/2, frame_num]: [mag&arg, frequency, time]
    """
    # time -> frequency Transform
    C = librosa.stft(wav, n_fft=n_fft, hop_length=hop_length)
    mag, arg = np.abs(C), np.angle(C, deg=False)
    print(f"C: {C.shape}")
    ## magnitude => intensity scaling mag
    logMag = np.log(mag)
    processed_mag = logMag

    # max, min = logMag.max(), logMag.min()
    # mean = (max+min)/2
    # normedLogMag = (logMag - mean)/(max - mean)
    # processed_mag = normedLogMag

    # frequency scaling
    # melFilter = librosa.filters.mel(16000, 2048, n_mels=1025)
    # for i in range(0, 1025):
    #     print(melFilter[i:i+1,:].max())
    # print(f"mag dim: {normedLogMag.shape}")
    # print(f"melFitler: {melFilter.shape}")
    # print(melFilter)
    # melProcessedMag = np.dot(melFilter, normedLogMag)
    # print(f"dot produt dim: {melProcessedMag.shape}")
    # melLogScaledMag = np.pad(melProcessedMag, [(0,0), (0,2)], "constant", constant_values=-1)
    # melLogScaledMag = normedLogMag

    ## IF-nize
    phase_unwrapped = np.unwrap(arg)
    diff = np.diff(phase_unwrapped, n=1) # finite difference
    if_arg = np.concatenate([phase_unwrapped[:,0:1], diff], axis=1)
    normed_if_arg = if_arg/np.pi
    processed_arg = normed_if_arg
    return np.array([processed_mag, processed_arg])


# path = "testaudio.wav"
# path = "sec4.wav"
# wave, sr = librosa.core.load(path, sr=16000)
# wave = wave[:64000]
# print(f"shape of wave: {wave.shape}")
# processedMag, scaledIF = wave2rainbowgram(wave)
# print("processedMag:")
# print(processedMag)
# print("partly")
# print(processedMag[10:15, 100:115])
# print(scaledIF)
# print(f"IF max: {scaledIF.max()}, min: {scaledIF.min()}")
# print(f"shape of processedMag: {processedMag.shape}")
# import matplotlib.pyplot as plt
#
# plt.imshow(IF)
# plt.show()
# import matplotlib
# import matplotlib.pyplot as plt
# matplotlib.rcParams['svg.fonttype'] = 'none'
#
# # Plotting functions
# cdict  = {'red':  ((0.0, 0.0, 0.0),
# (1.0, 0.0, 0.0)),
#
# 'green': ((0.0, 0.0, 0.0),
# (1.0, 0.0, 0.0)),
#
# 'blue':  ((0.0, 0.0, 0.0),
# (1.0, 0.0, 0.0)),
#
# 'alpha':  ((0.0, 1.0, 1.0),
# (1.0, 0.0, 0.0))
# }
#
# my_mask = matplotlib.colors.LinearSegmentedColormap('MyMask', cdict)
# plt.register_cmap(cmap=my_mask)
#
def plot_rainbowgram(rainbowgrams, rows=2, cols=4, col_labels=[], row_labels=[]):
  """
    Plot rainbowgram
    Args:
        rainbowgrams ([(mag, IF)]): list of rainbowgram datum (tuple of power and IF)
  """
  # prepare graph overview
  fig, axes = plt.subplots(rows, cols, sharex=True, sharey=True)
  fig.subplots_adjust(left=0.1, right=0.9, wspace=0.05, hspace=0.1)
  # prepare subplot
  for i, path in enumerate(rainbowgrams):
    row = i / cols
    col = i % cols
    if rows == 1:
      ax = axes[col]
    elif cols == 1:
      ax = axes[row]
    else:
      ax = axes[row, col]

    ax.matshow(dphase[::-1, :], cmap=plt.cm.rainbow)
    ax.matshow(mag[::-1, :], cmap=my_mask)

    # cmap : Colormap
    ax.set_axis_bgcolor('white')
    ax.set_xticks([]); ax.set_yticks([])
    if col == 0 and row_labels:
      ax.set_ylabel(row_labels[row])
    if row == rows-1 and col_labels:
      ax.set_xlabel(col_labels[col])
