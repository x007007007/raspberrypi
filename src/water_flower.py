import RPi.GPIO as gpio
import time

class IrrigateHandler(object):
    pass


class Irrigate(object):
    throttle = 0

    PWM_BCM = 26
    IN1_BCM = 19
    IN2_BCM = 13

    Moto_Vcc = 6
    Moto_Vcc_Min = 5
    Moto_Vcc_Max = 12
    Vcc = None
    hold_time = 0.01

    _stop_signal = False

    def __init__(self, I1=None, I2=None, pwm=None, Vcc=12):
        self.IN1_BCM = I1 if I1 else self.IN1_BCM
        self.IN2_BCM = I2 if I2 else self.IN2_BCM
        self.PWM_BCM = pwm if pwm else self.PWM_BCM
        self.Vcc = Vcc

    def __enter__(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.PWM_BCM, gpio.OUT)
        gpio.setup(self.IN1_BCM, gpio.OUT)
        gpio.setup(self.IN2_BCM, gpio.OUT)
        gpio.output(self.PWM_BCM, gpio.LOW)
        gpio.output(self.IN1_BCM, gpio.HIGH)
        gpio.output(self.IN2_BCM, gpio.LOW)
        return self

    def __exit__(self, *args, **kwargs):
        gpio.cleanup()

    def _calculate(self):
        normal_rate = (self.Vcc + self.Moto_Vcc)  / self.Moto_Vcc
        max_rate = (self.Vcc + self.Moto_Vcc_Max) / self.Moto_Vcc_Max
        min_rate = (self.Vcc + self.Moto_Vcc_Min) / self.Moto_Vcc_Min

    def get_interval(self):
        return (1 * self.hold_time, 1 * self.hold_time)

    def run(self, max_time=None):
        start_time = time.time()
        while not self._stop_signal:
            if max_time is not None:
                if time.time() - start_time > max_time:
                    break
            stop, run = self.get_interval()
            gpio.output(self.PWM_BCM, gpio.HIGH)
            time.sleep(run)
            gpio.output(self.PWM_BCM, gpio.LOW)
            time.sleep(stop)
        else:
            gpio.output(self.PWM_BCM, LOW)
        self._stop_signal = False



if __name__ == "__main__":
    with Irrigate() as fp:
        fp.run(5)
