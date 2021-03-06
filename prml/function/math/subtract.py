import numpy as np
from prml.tensor.tensor import Tensor
from prml.function.function import Function
from prml.function.array.broadcast import broadcast_to


class Subtract(Function):
    """
    subtract arguments element-wise
    """

    def _check_input(self, x, y):
        x = self._convert2tensor(x)
        y = self._convert2tensor(y)
        if x.shape != y.shape:
            shape = np.broadcast(x.value, y.value).shape
            if x.shape != shape:
                x = broadcast_to(x, shape)
            if y.shape != shape:
                y = broadcast_to(y, shape)
        return x, y

    def _forward(self, x, y):
        x, y = self._check_input(x, y)
        self.x = x
        self.y = y
        return Tensor(x.value - y.value, function=self)

    def _backward(self, delta):
        dx = delta
        dy = -delta
        self.x.backward(dx)
        self.y.backward(dy)


def subtract(x, y):
    return Subtract().forward(x, y)


def rsubtract(x, y):
    return Subtract().forward(y, x)
