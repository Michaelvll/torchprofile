__all__ = ['Variable']


class Variable:
    def __init__(self, name, dtype, shape):
        self.name = name
        self.value = None
        self.dtype = dtype
        self.shape = shape

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        self._dtype = dtype.lower()

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    def size(self):
        return self._shape

    def __repr__(self):
        text = '%' + self.name + ' : '
        if self.value is not None:
            text += str(self.value)
        else:
            text += self.dtype
            if self.shape is not None:
                text += '[' + ', '.join([str(shape) for shape in self.shape]) + ']'
        return text