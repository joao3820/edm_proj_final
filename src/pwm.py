from machine import Pin, PWM

class Led:
    def __init__(self, pin_no):
        self.pin_no = pin_no
        self.led = PWM(Pin(self.pin_no))
        self.led.freq(100)

    def duty(self, other):
        duty_cycle = int(other*1023*3.3/(2.5*4095))  # 3.3V corresponde a 4095; logo, como o painel só vai até 2.5, a conta é esta que aqui apresentamos
        self.led.duty(duty_cycle)
