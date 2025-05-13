import pandas as pd
import numpy as np
import scipy.stats as st

class Bootstrap:
    def __init__(self, data):
        self.data = np.array(data) 
        
        self.resample_data = self.resample()


    def resample(self, n_resamples=1000):
        """Realiza n_resamples muestras bootstrap"""
        n = len(self.data)
        self.samples = np.random.choice(self.data, size=(n_resamples, n), replace=True)
        return self.samples

    