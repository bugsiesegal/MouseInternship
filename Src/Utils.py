import datetime
from dataclasses import dataclass
import tdt
import numpy as np


@dataclass
class PF:
    data: np.ndarray
    offset: np.ndarray
    onset: np.ndarray
    duration: datetime.timedelta

    @classmethod
    def load_from_tdt(cls, path):
        tdt_object = tdt.read_block(path)

        return cls(
            tdt_object.streams.LMag.data
        )