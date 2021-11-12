from __future__ import annotations

import datetime
import glob
import pickle
from dataclasses import dataclass

import numpy as np
import tdt


@dataclass
class Fiber_Photometry:
    data: np.ndarray
    onset: np.ndarray
    offset: np.ndarray
    duration: datetime.timedelta

    @classmethod
    def load_from_tdt(cls, path: str) -> Fiber_Photometry:
        """
        Loads Fiber Photometry data from TDT file and outputs Fiber Photometry object.

        :rtype: Fiber Photometry
        :param path: Path to tdt folder.
        :return: Fiber Photometry object.
        """
        tdt_object = tdt.read_block(path)

        return cls(
            tdt_object.streams.LMag.data,
            tdt_object.epocs.Tick.onset,
            tdt_object.epocs.Tick.offset,
            tdt_object.info.duration
        )

    def save(self, path: str) -> None:
        """
        Saves Fiber Photometry Object to pkl file.

        :param path: Path to file.
        """
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, path: str) -> Fiber_Photometry:
        """
        Loads Fiber Photometry Object from pkl file.

        :param path: Path to file.
        :return: Fiber Photometry Object.
        """
        with open(path, 'rb') as file:
            return pickle.load(file)

    @classmethod
    def batch_load(cls, path: str) -> list[Fiber_Photometry]:
        """
        Loads a folder of Fiber Photometry pkl files.

        :param path: Path to folder.
        :return: List of Fiber Photometry Objects.
        """
        fp_files = []
        for file_path in glob.glob(path + "*"):
            fp_files.append(cls.load(file_path))

        return fp_files

    @staticmethod
    def batch_save(fp_object, path: str) -> None:
        """
        Saves list of Fiber Photometry Objects to a folder as pkl files.

        :param fp_object: List of Fiber Photometry Objects.
        :param path: Path to folder.
        """
        i = 0
        for file in fp_object:
            file.save(path + "/" + str(i) + ".pkl")
            i += 1

    @classmethod
    def batch_load_from_tdt(cls, path: str) -> list[Fiber_Photometry]:
        """
        Loads Fiber Photometry Objects to a list from folder of TDT folders.

        :param path: Path to folder of TDT folders.
        :return: List of Fiber Photometry Objects.
        """
        fp_file = []
        for file_path in glob.glob(path + "*"):
            fp_file.append(cls.load_from_tdt(file_path))

        return fp_file

    def fft(self) -> np.ndarray:
        """
        Preforms Fourier transform on data.

        :return: Fourier transformed data.
        """
        return np.array([np.fft.fft(data) for data in self.data])
