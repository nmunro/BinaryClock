#!/usr/bin/env python

import unicornhat as UH
import datetime
import time
import json
import os

class Clock():
  def __init__(self):
    self.prefs_file = "prefs.json"
    self.prefs = {}

    print("Clock online")
    self.__load_preferences()
    UH.brightness(self.prefs['brightness'])
    self.t = None

  def __load_preferences(self):
    if os.path.exists("prefs.json"):
      with open(self.prefs_file) as f:
        self.prefs = json.load(f)

  def __save_preferences(self):
    with open(self.prefs_file, "w") as f:
      f.write(json.dumps(self.prefs, sort_keys=True, indent=4, separators=(',', ':')))

  def __convert_to_binary(self, num):
    obj = { 32: 0, 16: 0, 8: 0, 4: 0, 2: 0, 1: 0 }

    for key in reversed(sorted(obj.keys())):
      if (num - key) >= 0:
        obj[key] = 1
        num -= key

    return obj

  def update_led(self, a, b, num):
    mapping = { 1: 32, 2: 16, 3: 8, 4: 4, 5: 2, 6: 1 }

    for x in range(1, 7):
      for y in range(a, b):
        if num[mapping[x]]:
          UH.set_pixel(x, y, self.prefs['on']['red'], self.prefs['on']['green'], self.prefs['on']['blue'])
        else:
          UH.set_pixel(x, y, self.prefs['off']['red'], self.prefs['off']['green'], self.prefs['off']['blue'])

  def set_hour(self):
    num = self.__convert_to_binary(self.t.hour)
    self.update_led(0, 2, num)

  def set_min(self):
    num = self.__convert_to_binary(self.t.minute)
    self.update_led(3, 5, num)

  def set_sec(self):
    num = self.__convert_to_binary(self.t.second)
    self.update_led(6, 8, num)

  def clear(self):
    UH.off()

  def update(self):
    while True:
      self.t = datetime.datetime.now()
      self.set_hour()
      self.set_min()
      self.set_sec()
      UH.show()

clock = Clock()
clock.update()
