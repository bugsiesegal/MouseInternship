from __future__ import annotations

import glob

import dill
import tdt

from .Utils import FiberPhotometry


def load(path: str) -> object:
    if path[path.find('.') + 1:] == "pkl":
        with open(path, 'rb') as file:
            return dill.load(file)
    elif path[path.find('.') + 1:] == "tdt":
        tdt_object = tdt.read_block(path)

        return FiberPhotometry(
            tdt_object.streams.LMag.data,
            tdt_object.epocs.Tick.onset,
            tdt_object.epocs.Tick.offset,
            tdt_object.info.duration
        )


def batch_load(path: str) -> list[object]:
    data = []
    for i in glob.glob(path + "*"):
        data.append(load(i))

    return data


def save(cls: object, path: str) -> None:
    if path[path.find('.') + 1:] == "pkl":
        with open(path, 'wb') as file:
            dill.dump(cls, file)


def batch_save(cls: list[object], path: str) -> None:
    n = 0
    for i in cls:
        save(i, path + str(n))
        n += 1
