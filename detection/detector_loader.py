import importlib
import inspect
from pathlib import Path
from abc import ABC


def load_detectors(folder):

    detectors = []

    folder_path = Path(folder)

    for file in folder_path.glob("*_detector.py"):

        # Skip helper/base files
        if file.stem in ["base_detector","new_detector"]:
            continue

        module_name = (
            str(file)
            .replace("\\", ".")
            .replace("/", ".")
            .replace(".py", "")
        )

        module = importlib.import_module(module_name)

        for _, cls in inspect.getmembers(module, inspect.isclass):

            # Only classes defined in this module
            if cls.__module__ != module.__name__:
                continue

            # Skip abstract classes
            if inspect.isabstract(cls):
                continue

            detectors.append(cls())

    return detectors