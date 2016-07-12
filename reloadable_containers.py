# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import time
import json


class Reloadable(ABC):
    """
    This class wraps a container and expose all its methods. It reloads its
    content after `reload_every_secs` from `path`.
    """
    def __init__(self, path, reload_every_secs=60):
        self._path = path
        self._last_update = time.time()
        self._reload_every_secs = reload_every_secs
        self._initialize_data()
        self.reload()

    def reload(self):
        """Method intended to extend in child class."""
        self._last_update = time.time()
        try:
            with open(self._path) as f:
                self._fill_data(f)
        except FileNotFoundError:
            self._initialize_data()

    @abstractmethod
    def _initialize_data(self):
        """Change container to initial state"""
        pass

    @abstractmethod
    def _fill_data(self, fp):
        """Fill data from file to container self._data"""
        pass

    def access(self):
        if time.time() - self._last_update > self._reload_every_secs:
            self.reload()

    def __getattr__(self, item):
        return getattr(self._data, item)

    def __len__(self):
        self.access()
        return self._data.__len__()

    def __getitem__(self, item):
        self.access()
        return self._data.__getitem__(item)

    def __setitem__(self, key, value):
        self.access()
        return self._data.__setitem__(key, value)

    def __delitem__(self, key):
        self.access()
        return self._data.__delitem__(key)

    def __iter__(self):
        self.access()
        return self._data.__iter__()

    def __reversed__(self):
        self.access()
        return self._data.__reversed__()

    def __contains__(self, item):
        self.access()
        return self._data.__contains__(item)

    def __str__(self):
        self.access()
        return self._data.__str__()

    def __repr__(self):
        self.access()
        return "<Reloadable: %r, reload_every: %d>" % (self._data, self._reload_every_secs)


class ReloadableList(Reloadable):
    def _initialize_data(self):
        self._data = []

    def _fill_data(self, fp):
        self._data = [line.strip() for line in fp if line.strip()]


class ReloadableJson(Reloadable):
    def _initialize_data(self):
        self._data = {}

    def _fill_data(self, fp):
        self._data = json.load(fp)




