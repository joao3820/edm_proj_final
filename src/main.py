# pylint: disable=global-statement, unused-argument
from MicroWebSrv2 import MicroWebSrv2
from machine import Pin

but = Pin(23, Pin.IN, Pin.PULL_UP)

myWebSockets = None

def OnWebSocketClosed(webSocket):
  global myWebSockets
  myWebSockets = None

def OnWebSocketAccepted(microWebSrv2, webSocket):
  global myWebSockets
  if myWebSockets is None:
    print('WebSocket from {0}'.format(webSocket.Request.UserAddress))
    myWebSockets = webSocket
    myWebSockets.OnTextMessage = OnWebSocketTextMsg
    myWebSockets.OnClosed = OnWebSocketClosed

mws2 = MicroWebSrv2()
wsMod = MicroWebSrv2.LoadModule('WebSockets')
wsMod.OnWebSocketAccepted = OnWebSocketAccepted
mws2.SetEmbeddedConfig()
mws2.NotFoundURL = '/'
mws2.StartManaged()

state = True
def loop():
  global state
  if but.value() != state:
    state = not state
    msg = 'Button ' + ('OFF' if state else 'ON')
    print(msg)
    if myWebSockets is not None:
      myWebSockets.SendTextMessage(msg)

try:
  while mws2.IsRunning:
    loop()
except KeyboardInterrupt:
  pass

mws2.Stop()