from .features import convertWavIntoF0seqMCEPseq

class ToNormedMCEPseq(object):
    """
    Convert waveform into a person-normalized MCEP sequence

    Args:
        MCEP_means
        MCEP_stds

    Returns:
        (numpy.ndarray) normalized MCEP sequence
    """
    def __init__(self, sampling_rate, MCEP_means, MCEP_stds):
        self.sampling_rate = sampling_rate
        self.MCEP_means = MCEP_means
        self.MCEP_stds = MCEP_stds

    def __call__(self, waveform):
        _, MCEPseq = convertWavIntoF0seqMCEPseq(waveform, self.sampling_rate)
        normedMCEPseq = (MCEPseq - self.MCEP_means)/self.MCEP_stds
        return normedMCEPseq
