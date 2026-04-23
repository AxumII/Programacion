import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

class FlexibleMLP(nn.Module):
    def __init__(self, input_size, hidden_layers, num_classes, activation_fn=nn.ReLU):
        super(FlexibleMLP, self).__init__()
        layers = []
        in_dim = input_size