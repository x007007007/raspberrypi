import RPi.GPIO as gpio
import time
import sys
import datetime
channel = 4

try:
    gpio.setmode(gpio.BCM)
    while True:
        time.sleep(1)
        data = []
        gpio.setup(channel, gpio.OUT)
        gpio.output(channel, gpio.LOW)
        time.sleep(0.02)
        gpio.output(channel, gpio.HIGH)
        gpio.setup(channel, gpio.IN)

        while gpio.input(channel) == gpio.LOW:
            continue
        while gpio.input(channel) == gpio.HIGH:
            continue
        j = 0
        while j < 40:
            k = 0
            while gpio.input(channel) == gpio.LOW:
                continue
            while gpio.input(channel) == gpio.HIGH:
                k += 1
                if k > 100:
                    break
            if k < 15:
                data.append(0)
            else:
                data.append(1)
            j += 1


        humidity_bit = data[:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]

        humidity = 0
        humidity_point = 0
        temperature = 0
        termerature_point = 0
        check = 0
        
        for i in range(8):
            humidity += humidity_bit[i] * 2 ** (7-i)
            humidity_point += humidity_point_bit[i] * 2 ** (7-i)
            temperature += temperature_bit[i] * 2 ** (7-i)
            temperature_point = temperature_point_bit[i] * 2 ** (7 -i)
            check += check_bit[i] * 2 ** (7 - i)
        
        tmp = humidity + humidity_point + temperature + temperature_point
        
        if check == tmp:
            sys.stdout.write("\r{} temperature: {}.{}, humidity:{}.{}".format(datetime.datetime.now(), temperature, temperature_point, humidity, humidity_point))
        sys.stdout.flush()
except:
    import traceback
    traceback.print_exc()
finally:
    gpio.cleanup()
