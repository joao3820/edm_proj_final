from MicroWebSrv2 import MicroWebSrv2
from machine import Pin, ADC
from utime import ticks_ms
from api import getTime
from ujson import dumps
from button import Button
from pwm import Led 

adc = ADC(Pin(33))
rLed = Led(21)
gLed = Led(19)
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)
tempo = ''
Volts = 0

myWebSockets = None

def OnWebSocketClosed(webSocket):
    global myWebSockets
    myWebSockets = None

def OnWebSocketAccepted(microWebSrv2, webSocket):
    global myWebSockets, Volts, tempo, graphdata
    if myWebSockets is None:
        print('WebSocket from {0}'.format(webSocket.Request.UserAddress))
        myWebSockets = webSocket
        myWebSockets.OnClosed = OnWebSocketClosed

        msg = "O ultimo item recebido foi " + str(Volts) + " na hora " + str(tempo)
        if myWebSockets is not None:
            myWebSockets.SendTextMessage(msg)
            myWebSockets.SendTextMessage(dumps(graphData.__dict__))

mws2 = MicroWebSrv2()
wsMod = MicroWebSrv2.LoadModule('WebSockets')
wsMod.OnWebSocketAccepted = OnWebSocketAccepted
mws2.SetEmbeddedConfig()
mws2.NotFoundURL = '/'
mws2.StartManaged()


def sendADC(state):
    """Enviar valores ADC para a página web"""
    global Volts, tempo, graphData
    value = 0
    for n in range(16):
        value = value + adc.read()
    value = value >> 4
    Volts = (value * 3.3) / 4095
    tempo = str(getTime())

    graphData.append([tempo, Volts])
    msg = "O ultimo item recebido foi " + str(Volts) + " na hora " + str(tempo)
    if myWebSockets is not None:
        myWebSockets.SendTextMessage(msg)
        myWebSockets.SendTextMessage(dumps(graphData.__dict__))

def sendLed():
    rLed.duty(2.5*4095/3.3 - adc.read())
    gLed.duty(adc.read())

but = Button(23, callback=sendADC)

class graph():
    def __init__(self):
        self.lista = [['Hora', 'Voltagem']]

    def append(self, other):
        self.lista.append(other)

graphData = graph()

state = True
def loop():
    global last
    now = ticks_ms()
    but.proc()
    if now - last >= 600000:
        last = now
        sendADC(True)
    sendLed()
        
sendADC(True)
try:
    last = ticks_ms()
    while mws2.IsRunning:
        loop()
except KeyboardInterrupt:
    pass

mws2.Stop()