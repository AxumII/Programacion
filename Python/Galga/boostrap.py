import pandas as pd
import numpy as np
import scipy.stats as st

class Bootstrap:
    def __init__(self, data):
        self.data = np.array(data)  # Aseguramos que sea array

    def resample(self, n_resamples=1000):
        """Realiza n_resamples muestras bootstrap"""
        n = len(self.data)
        self.samples = np.random.choice(self.data, size=(n_resamples, n), replace=True)
        return self.samples

    def bootstrap_statistic(self, func=np.mean, n_resamples=1000):
        """Aplica una función estadística a cada remuestreo"""
        if not hasattr(self, 'samples'):
            self.resample(n_resamples)
        statistics = np.apply_along_axis(func, axis=1, arr=self.samples)
        return statistics
