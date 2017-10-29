import RPi.GPIO as gpio

class GPIOPin(object):
    def __init__(self):
        self._pins = {}

    def __getitem__(self, key):
        return self._pins[key]

    def __setitem__(self, key, value):
        self._pins[key] = value

    def __getattribute__(self, key):
        if not key.startswith("_"):
            return object.__getattribute__(self, "_pins")[key]
        else:
            return object.__getattribute__(self, key)

    def __setattribute__(self, key, value):
        if not key.startswith("_"):
            print(key,value)
            object.__getattribute__(self, "_pins")[key] = value
        else:
            print(ken, value)
            object.__setattribute__(self, key, value)


class BaseGPIOModule(object):

    def __init__(self):
        self.gpio_pin = GPIOPin()
        gpio.setmode(gpio.BCM)

    def __enter__(self, *args, **kwargs):
        self.setup(*args, **kwargs)
        return self

    def __exit__(self, *args, **kwargs):
        for pin in self.gpio_pin._pins.values():
            gpio.setup(pin, gpio.IN)

    @classmethod
    def required_io_name(cls):
        raise NotImplemented


