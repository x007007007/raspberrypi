import time
import RPi.GPIO as GPIO
import sys

try:
    GPIO.setmode(GPIO.BCM)
    
    GPIO_TRIGGER = 2
    GPIO_ECHO = 3
    
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)
    
    while True:
        out_time_a = 0 
        out_time_b = 0
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.5)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()

        while GPIO.input(GPIO_ECHO)==0:
            if out_time_a > 10000:
                out_time_b = float("inf")
                break
            start = time.time()
            out_time_a += 1

        while GPIO.input(GPIO_ECHO)==1:
            if out_time_b > 100000000:
                break
            stop = time.time()
            out_time_b += 1
        sys.stdout.write("\r{}      ".format((stop -start) * 16650))
        sys.stdout.flush()
except:
    import traceback
    traceback.print_exc()
finally:
    GPIO.cleanup()

