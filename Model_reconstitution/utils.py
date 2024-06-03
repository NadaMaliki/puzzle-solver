import math 
import numpy as np  # type: ignore
import matplotlib.pyplot as plt # type: ignore

def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.axis("off")
    plt.imshow(inp)

def perfect_sqr(num):
    """
    checks whether a number is perfect square.
    """

    sqr = math.sqrt(num)

    return (num - sqr == 0)