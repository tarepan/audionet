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
    sets = seq(wavelist).map(lambda waveform: convertWavIntoF0seqMCEPseq(waveform, sr))
    f0seqs = sets.map(lambda set: set[0]).to_list()
    MCEPseqs = sets.map(lambda set: set[1]).to_list()
    logF0_mean, logF0_std = getLogF0Stat(f0seqs)
    MCEP_mean, MCEP_std = getMCEPStat(MCEPseqs)
    return logF0_mean, logF0_std, MCEP_mean, MCEP_std
