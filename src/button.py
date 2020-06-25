from machine import Pin

class Button:
  def __init__(self, pin, callback=None, active_high=False, pull_resistor=True):
    self.active_high = active_high
    self.callback = callback
    if not pull_resistor:
      self.but = Pin(pin, Pin.IN)
    else:
      self.but = Pin(pin, Pin.IN, Pin.PULL_UP if not active_high else Pin.PULL_DOWN)
    self.last = self.state()

  def logic(self, value):
    return value if self.active_high else not value

  def state(self):
    return self.logic(self.but.value())

  def proc(self):
    state = self.state()
    if self.last != state:
      self.last = state
      if self.callback is not None:
        self.callback(state)