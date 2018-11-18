from functional import seq

from .feature_stat import getLogF0Stat, getMCEPStat
from .features import convertWavIntoF0seqMCEPseq

def waves2stats(wavelist, sr):
    """
    Calculate logF0 and MCEP's means/std from wavelist

    Args:
        wavelist ([np.ndarray(T,)]): list of waveforms
        sr (int): sampling rate of waveforms

    Returns:
        logF0_mean, logF0_std, MCEP_mean, MCEP_std
    """
    # [np.ndarray(1,T)] => [(np.ndarray(1, frames), np.ndarray(24MCEPs, frames)]
    f0seqs = []
    MCEPseqs = []
    cnt = 0
    for waveform in wavelist:
        f0seq, MCEPseq = convertWavIntoF0seqMCEPseq(waveform, sr)
        f0seqs.append(f0seq)
        MCEPseqs.append(MCEPseqs)
        print(f"extract f0 & MCEP #{cnt}")
        cnt+=1
    print("finish extracting")
    logF0_mean, logF0_std = getLogF0Stat(f0seqs)
    print("finish F0 stat analysis")
    MCEP_mean, MCEP_std = getMCEPStat(MCEPseqs)
    print("finish MCEP stat analysis")
    return logF0_mean, logF0_std, MCEP_mean, MCEP_std
