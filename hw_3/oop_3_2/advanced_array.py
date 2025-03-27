from mixins import ArithmeticMixin, FileIOMixin, DisplayMixin, PropertyMixin


class AdvancedArray(ArithmeticMixin, FileIOMixin, DisplayMixin, PropertyMixin):
    def __init__(self, data):
        self._data = None
        self.data = data
