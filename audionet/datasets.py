import os
import librosa
from functional import seq


class Dataset(object):
    """An abstract class representing a Dataset.
    """

    def __getitem__(self, index):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __add__(self, other):
        return ConcatDataset([self, other])


class FileDataset(Dataset):
    """
    Dataset which load numpy npy dataset
    """

    def __init__(self, dirPath, recursive=False, transform=lambda ndarray: ndarray):
        """
        Args:
            dirPath (string): a Path of a directory which contains data
            recursive (bool): flag for recursive file finding
            transform (function): a transform function
        """
        self.dirPath = dirPath
        if(recursive == False):
            self.fileNames = seq(os.listdir(dirPath)).filter(lambda name: os.path.isfile(dirPath/name)).to_list()
        else:
            raise "Not yet implemented"
        self.transform = transform

    def __len__(self):
        """
        Return the size of this dataset (number of files)
        """
        return len(self.fileNames)

    def __getitem__(self, idx):
        """
        Load a file
        """
        raise NotImplementedError()


class MonoAudioDataset(FileDataset):
    """
    Monaural Audio Dataset
    """

    def __init__(self, dirPath, resampling_rate=None, transform=lambda wave: wave):
        """
        Args:
            dirPath (string): a Path of a directory which contains audio files
            resampling_rate (int): audio resampling rate
            transform (function): a transform function
        """
        super().__init__(dirPath, recursive=False, transform=transform)
        self.resampling_rate = resampling_rate

    def __getitem__(self, idx):
        """
        Load a audio file as a numpy.ndarray(T,) monaural waveform
        """
        name = self.fileNames[idx]
        filePath = self.dirPath/name
        waveform = librosa.core.load(filePath, sr = self.resampling_rate, mono = True)[0]
        return (self.transform(waveform), name)
