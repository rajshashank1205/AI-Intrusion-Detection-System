from abc import ABC, abstractmethod


class BaseDetector(ABC):
    """
    Base class for every detector.

    Every detector must inherit from this class
    and implement the detect() method.
    """

    @abstractmethod
    def detect(self, features):
        """
        Analyze extracted flow features.

        Returns:
            dict containing detection result
        """
        pass