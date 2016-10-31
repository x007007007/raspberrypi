import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)

class Moto(object):
    IN1 = 26
    IN2 = 19
    IN3 = 13  # GPIO.23
    IN4 = 6  # GPIO.22
    FNA = 21  # PIN 40

    def __init__(self):
        gpio.setmode(gpio.BCM)
        for pin in (self.IN1, self.IN2, self.IN3, self.IN4, self.FNA):
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, gpio.LOW)
        print("init")

    def out12forward(self):
        gpio.output(self.IN1, gpio.LOW)
        gpio.output(self.IN2, gpio.HIGH)

    def out12back(self):
        gpio.output(self.IN1, gpio.HIGH)
        gpio.output(self.IN2, gpio.LOW)

    def out12stop(self):
        gpio.output(self.IN1, gpio.LOW)
        gpio.output(self.IN2, gpio.LOW)

    def out34forward(self):
        gpio.output(self.IN3, gpio.HIGH)
        gpio.output(self.IN4, gpio.LOW)

    def out34back(self):
        gpio.output(self.IN3, gpio.LOW)
        gpio.output(self.IN4, gpio.HIGH)

    def out34stop(self):
        gpio.output(self.IN3, gpio.LOW)
        gpio.output(self.IN4, gpio.LOW)

    def forward(self):
        self.out12forward()
        self.out34forward()

    def back(self):
        self.out12back()
        self.out34back()

    def turna(self):
        self.out12back()
        self.out34forward()

    def turnb(self):
        self.out12forward()
        self.out34back()

    def turnAforward(self):
        self.out12stop()
        self.out34forward()

    def turnAback(self):
        self.out12back()
        self.out34stop()

    def turnBforward(self):
        self.out12forward()
        self.out34stop()

    def turnBback(self):
        self.out12stop()
        self.out34back()

    def start(self):
        gpio.output(self.FNA, gpio.HIGH)

    def stop(self):
        self.out12stop()
        self.out34stop()
        gpio.output(self.FNA, gpio.LOW)


if __name__ == "__main__":
    import threading
    import time
    import curses

    last_input_time = 0

    try:
        moto = Moto()
        def check_key():
            try:
                win = curses.initscr()
                win.addstr(10,10, "xxc 's car")
                while True:
                    chi = win.getch()
                    last_input_time = time.time()
                    ch = chr(chi)
                    if ch == "w":
                        win.addstr(11,10, "forward!")
                        moto.forward()
                        moto.start()
                    elif ch == "s":
                        win.addstr(11,10, "back    ")
                        moto.back()
                    elif ch in [" ", "x"]:
                        win.addstr(11,10, "stop!!   ")
                        moto.stop()
                    elif ch in ["\n", "\r", "X"]:
                        win.addstr(11,10, "start..   ")
                        moto.start()
                    elif ch == "a":
                        win.addstr(11, 10, "left      ")
                        moto.turna()
                    elif ch == "d":
                        win.addstr(11, 10, "right      ")
                        moto.turnb()
                    elif ch == "q":
                        win.addstr(11, 10, "         ")
                        moto.turnAforward()
                    elif ch == "e":
                        win.addstr(11, 10, "          ")
                        moto.turnBforward()
                    elif ch == "z":
                        win.addstr(11, 10, "           ")
                        moto.turnBback()
                    elif ch == "c":
                        win.addstr(11, 10, "           ")
                        moto.turnAback()
                    elif chi == 27:
                        print("good bye")
                        break
                    time.sleep(0.05)
                    win.addstr(20,0, "{}       ".format( chi))
            finally:
                curses.endwin()

        def timeout_check():
            gpio.setmode(gpio.BCM)
            while True:
                time.sleep(1)
                if time.time() - last_input_time > 1:
                    moto.stop()
        checker = threading.Thread(target=timeout_check)
        
        # checker.start()
        check_key() 
    except:
        import traceback
        traceback.print_exc()
    finally:
        gpio.cleanup()



