try:
    import RPi.GPIO as gpio
except:
    import x007007007.RPi.GPIO as gpio

class _GPIOPins(object):
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
            object.__setattribute__(self, key, value)


class GPIOPin(object):
    def __init__(self, required=False, pwm=False):
        self.required = required

    def __set__(self, instance, value):
        print(instance, value)

    def __get__(self, instance, owner):
        print(instance, owner)


class BaseGPIOModule(object):
    def __init__(self):
        self.gpio_pin = _GPIOPins()
        self.gpio = gpio
        gpio.setmode(gpio.BCM)

    def setup(self, *args, **kwargs):
        raise NotImplementedError

    def __enter__(self, *args, **kwargs):
        self.setup(*args, **kwargs)
        return self

    def __exit__(self, *args, **kwargs):
        for pin in self.gpio_pin._pins.values():
            gpio.setup(pin, gpio.IN)

    @classmethod
    def required_io_name(cls):
        raise NotImplementedError


