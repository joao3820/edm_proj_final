# pylint: disable=global-statement, unused-argument
from MicroWebSrv2 import MicroWebSrv2
from machine import Pin, ADC
from utime import ticks_ms
from api import getTime

adc = ADC(Pin(32))
but = Pin(23, Pin.IN, Pin.PULL_UP)
Readings = [["Time","Voltage"]]
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

myWebSockets = None

def OnWebSocketClosed(webSocket):
  global myWebSockets
  myWebSockets = None

def OnWebSocketAccepted(microWebSrv2, webSocket):
  global myWebSockets
  if myWebSockets is None:
    print('WebSocket from {0}'.format(webSocket.Request.UserAddress))
    myWebSockets = webSocket
    myWebSockets.OnClosed = OnWebSocketClosed

mws2 = MicroWebSrv2()
wsMod = MicroWebSrv2.LoadModule('WebSockets')
wsMod.OnWebSocketAccepted = OnWebSocketAccepted
mws2.SetEmbeddedConfig()
mws2.NotFoundURL = '/'
mws2.StartManaged()

state = True
def loop():
  global last, Readings
  now = ticks_ms()
  if now - last >= 3000:
    last = now
    value = 0
    for n in range(16):
      value = value + adc.read()
    value = value >> 4
    Volts = (value * 3.3) / 4095
    Point = []
    Point.append(getTime())
    Point.append(Volts)
    Readings.append(Point)
    if myWebSockets is not None:
      myWebSockets.SendTextMessage(str(Readings))

try:
  last = ticks_ms()
  while mws2.IsRunning:
    loop()
except KeyboardInterrupt:
  pass

mws2.Stop()