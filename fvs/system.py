class System():
    def __init__(self, *args, **kwargs):
        self.devices = {}
        self.functions = {}

    def __repr__(self):
        devices = ', '.join(str(key) for key in self.devices.keys())
        return '{}({})'.format(type(self), devices)

    def __len__(self):
        return len(self.devices)

    def __setitem__(self, key, val):
        self.devices[str(key)] = val

    def __getitem__(self, key):
        return self.devices[str(key)]

    def __iter__(self):
        return iter(self.devices.items())

    def update(self):
        for device in self.devices.values():
            device.update()
