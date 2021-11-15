from __future__ import annotations

import datetime
import glob
import pickle
from dataclasses import dataclass

import numpy as np
import tdt
from typing import Type


@dataclass
class __data_class__:
    data: np.ndarray

    def save(self, path: str) -> None:
        """
        Saves object to path.

        :param path: Path to save to.
        """
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, path: str) -> __data_class__:
        """
        Loads object from path.

        :param path: Path to load from.
        :return: Loaded object.
        """
        with open(path, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def batch_save(objs: list[__data_class__], path: str) -> None:
        """
        Saves a list of objects to path. Labeled by object index in list.

        :param objs: List of objects.
        :param path: Where the objects should be saved.
        """
        for i in range(len(objs)):
            objs[i].save(path + str(i) + '.pkl')

    @classmethod
    def batch_load(cls, path: str) -> list[__data_class__]:
        """
        Loads a list of objects from folder.

        :param path: Path to folder.
        :return: List of objects.
        """
        obj_files = []
        for file_path in glob.glob(path + "*.pkl"):
            obj_files.append(cls.load(file_path))

        return obj_files


@dataclass
class Fiber_Photometry(__data_class__):
    """
    A data class containing Fiber Photometry data and parameters.
    """

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
        temp_data = self.data[0][:-(self.data[0].shape[0] % window_size)]
        return windows(
            temp_data.reshape((int(temp_data.shape[0] / window_size), window_size)),
            window_size)

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
class windows(__data_class__):
    """
    A data class containing Fiber Photometry data cut to window_size.
    """
    window_size: int
