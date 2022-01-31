from __future__ import annotations

import datetime
import glob

from dataclasses import dataclass

import numpy as np
import os
import tdt


@dataclass
class FiberPhotometry:
    """
    A data class containing Fiber Photometry data and parameters.
    """
    data: np.ndarray
    onset: np.ndarray
    offset: np.ndarray
    duration: datetime.timedelta

    def fft(self) -> np.ndarray:
        """
        Preforms Fourier transform on data.

        :return: Fourier transformed data.
        """
        return np.array([np.fft.fft(data) for data in self.data])

    def fft_truncation(self, cutoff):
        fft = self.fft()
        self.data = np.fft.ifft(fft[:cutoff])

    def to_window(self, window_size: int = 100) -> Windows:
        """
        Cuts data into windows with a size of window_size. Data at the end of the array will be truncated if they
        can't evenly fit.

        :param window_size: The length of each window.
        :return: Object containing all windows as well as their size.
        """
        temp_data = self.data[:-(self.data.shape[0] % window_size)]
        return Windows(
            temp_data.reshape((int(temp_data.shape[0] / window_size), window_size)),
            window_size)

    @staticmethod
    def batch_to_window(fp_objects: list[FiberPhotometry], window_size: int = 100) -> list[Windows]:
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
class Windows:
    """
    A data class containing Fiber Photometry data cut to window_size.
    """
    data: np.ndarray
    window_size: int
