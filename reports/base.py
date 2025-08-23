from abc import ABC, abstractmethod


class BaseReport(ABC):
    def __init__(self, logs):
        self.logs = logs

    @abstractmethod
    def generate(self):
        """Return list of rows for tabulate"""

    @abstractmethod
    def headers(self):
        """Return list of headers"""
