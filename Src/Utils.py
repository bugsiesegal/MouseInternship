import datetime, pickle, glob
from dataclasses import dataclass
import tdt
import numpy as np


@dataclass
class Fiber_Photometry:
    data: np.ndarray
    onset: np.ndarray
    offset: np.ndarray
    duration: datetime.timedelta

    @classmethod
    def load_from_tdt(cls, path):
        tdt_object = tdt.read_block(path)

        return cls(
            tdt_object.streams.LMag.data,
            tdt_object.epocs.Tick.onset,
            tdt_object.epocs.Tick.offset,
            tdt_object.info.duration
        )

    def save(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    @classmethod
    def batch_load(cls, path):
        fp_files = []
        for file_path in glob.glob(path + "*"):
            fp_files.append(cls.load(file_path))

        return fp_files

    @staticmethod
    def batch_save(fp_object, path):
        i = 0
        for file in fp_object:
            file.save(path + "/" + str(i) + ".pkl")
            i += 1

    @classmethod
    def batch_load_from_tdt(cls, path):
        fp_file = []
        for file_path in glob.glob(path + "*"):
            fp_file.append(cls.load_from_tdt(file_path))

        return fp_file

    def fft(self):
        return np.array([np.fft.fft(data) for data in self.data])