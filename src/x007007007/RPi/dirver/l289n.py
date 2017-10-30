from .base_gpio import BaseGPIOModule, GPIOPin


class L289nGPIOModule(BaseGPIOModule):
    IN1 = GPIOPin()
    IN2 = GPIOPin()
    IN3 = GPIOPin()
    IN4 = GPIOPin()
    ENA = GPIOPin(pwm=True)
    ENB = GPIOPin(pwm=True)


