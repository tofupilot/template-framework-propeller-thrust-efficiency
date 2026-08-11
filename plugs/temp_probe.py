"""Thermocouple probe. Registered twice in procedure.yaml with different
channels, showing multiple instances of one plug class."""

import numpy as np


class TempProbe:
    def __init__(self, channel):
        self.channel = channel
        self.rng = np.random.default_rng(100 + channel)
        self._base = 22.0
        print(f"Temp probe on channel {channel}")

    def read_series(self, n):
        """Return n samples of a slow thermal rise in °C."""
        rise = 30.0 if self.channel == 0 else 18.0
        return [
            round(self._base + rise * (i / max(n - 1, 1)) ** 1.5
                  + float(self.rng.normal(0, 0.2)), 2)
            for i in range(n)
        ]
