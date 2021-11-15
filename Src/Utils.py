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

    def fft_truncation(self, cutoff):
        fft = self.fft()
        self.data = np.fft.ifft(fft[:cutoff])

    def to_window(self, window_size: int = 100) -> windows:
        """
        Cuts data into windows with a size of window_size. Data at the end of the array will be truncated if they
        can't evenly fit.

        :param window_size: The length of each window.
        :return: Object containing all windows as well as their size.
        """
        window_list = []
        for i in range(self.data.size - window_size * 2):
            window_list.append(
                self.data[i + window_size:i + window_size * 2].reshape((1, window_size))
            )

        return windows(np.array(window_list), window_size)

    @staticmethod
    def batch_to_window(fp_objects: list[Fiber_Photometry], window_size: int = 100) -> list[windows]:
        """
        Cuts uses to_window on list of Fiber_Photometry objects.

        :param fp_objects: List of Fiber_Photometry objects.
        :param window_size: The length of each window.
        :return: List of Objects containing all windows of each Fiber_Photometry object and their size.
        """
        batch_windows = []
        for i in fp_objects:
            batch_windows.append(i.to_window(window_size))

        return batch_windows



@dataclass
class windows:
    data: np.ndarray
    window_size: int

    def save(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as file:
            return pickle.load(file)

