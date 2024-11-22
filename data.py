class Data:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __delitem__(self, key):
        del self.data[key]

    def read(self, id):
        return self.data[id]

    def read_all(self):
        return self.data

    def write(self, id, value):
        self.data[id.value] = value

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.data.copy()

    def get(self, key):
        return self.data.get(key)

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def pop(self, key):
        return self.data.pop(key)

    def popitem(self):
        return self.data.popitem()

    def setdefault(self, key, default=None):
        return self.data.setdefault(key, default)

    def update(self, other):
        self.data.update(other)

    def values(self):
        return self.data.values()
