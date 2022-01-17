from __future__ import annotations

import dill
import glob
from abc import ABC, abstractmethod, abstractproperty
import tdt
import sys, inspect


class FileSaveIO(ABC):
    @abstractmethod
    def save(self, file_path: str) -> None:
        """
        Saves object to path.

        :param file_path:  Path to save to.
        """
        pass

    @staticmethod
    def batch_save(objs: list[FileSaveIO], folder_path: str, extension: str = "pkl") -> None:
        """
        Saves a list of objects to path. Labeled by object index in list.

        :param extension: File extension type.
        :param objs: List of objects.
        :param folder_path: Where the object should be saved.
        """

        for i in range(len(objs)):
            objs[i].save(folder_path + str(i) + '.' + extension)


class FileLoadIO(ABC):
    @staticmethod
    @abstractmethod
    def load(file_path: str) -> FileLoadIO:
        """
        Loads object from path.

        :param file_path: Path to load from.
        :return: Loaded object.
        """
        pass

    @classmethod
    def batch_load(cls, folder_path: str, extension: str = "pkl") -> list[FileLoadIO]:
        """
        Loads a list of objects from folder.

        :param extension: File extension type.
        :param folder_path: Path to folder.
        :return: List of objects.
        """

        obj_files = []
        for file_path in glob.glob(folder_path + "*." + extension):
            obj_files.append(cls.load(file_path))

        return obj_files


class PicklableIO(FileSaveIO, FileLoadIO):
    def save(self, file_path: str) -> None:
        """
        Saves object to path.

        :param file_path: Path to save to.
        """
        with open(file_path, 'wb') as file:
            dill.dump(self, file)

    @staticmethod
    def load(file_path: str) -> PicklableIO:
        """
        Loads object from path.

        :param file_path: Path to load from.
        :return: Loaded object.
        """
        with open(file_path, 'rb') as file:
            return dill.load(file)

    @staticmethod
    def batch_save(objs: list[PicklableIO], folder_path: str, extension: str = "pkl") -> None:
        """
        Saves a list of objects to path. Labeled by object index in list.

        :param extension: File extension type.
        :param objs: List of objects.
        :param folder_path: Where the objects should be saved.
        """
        for i in range(len(objs)):
            objs[i].save(folder_path + str(i) + '.' + extension)

    @classmethod
    def batch_load(cls, folder_path: str, extension: str = "pkl") -> list[PicklableIO]:
        """
        Loads a list of objects from folder.

        :param extension: File extension type.
        :param folder_path: Path to folder.
        :return: List of objects.
        """
        obj_files = []
        for file_path in glob.glob(folder_path + "*." + extension):
            obj_files.append(cls.load(file_path))

        return obj_files


class TdtIO(FileLoadIO):
    @classmethod
    def load(cls, file_path: str) -> TdtIO:
        """
                Loads Fiber Photometry data from TDT file and outputs Fiber Photometry object.

                :rtype: Fiber Photometry
                :param file_path: Path to tdt folder.
                :return: Fiber Photometry object.
                """
        tdt_object = tdt.read_block(file_path)
        return cls(
            tdt_object.streams.LMag.data[0],
            tdt_object.epocs.Tick.onset,
            tdt_object.epocs.Tick.offset,
            tdt_object.info.duration
        )


class IOManager:
    def __init__(self):
        clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        