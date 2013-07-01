# Copyright 2013 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from nark import *
from app import conf
import app.model


class Utils(object):
  
  def __init__(self):
    self.prefs = app.model.Prefs()
    self.flash_service = app.model.Flash()

  def get_preference(self, key):
    """ Get a preference by key """
    try:
      rtn = Dynamic()
      rtn.result = False
      rtn.value = ""
      if self.prefs.has(key):
        rtn.result = True
        rtn.value = self.prefs.get(key).value
    except Exception:
      e = exception()
      self.flash_service.error("Failed to get preference: %r" % e)
    return rtn

  def set_preference(self, value):
    """ Get preference value """
    key = str(value["key"])
    value = str(value["value"])
    self.prefs.add(key, value)
    self.flash_service.success("Set '%s' to value: '%s'" % (key, value))

  def flash(self, value):
    """  Return the next flash message, if any """
    rtn = Dynamic({"result" : False, "level" : False})
    if self.flash_service.any():
      msg = self.flash_service.get()
      rtn.result = msg.message
      if msg.level == app.model.FlashTypes.FAILURE:
        rtn.level = "FAILURE"
      elif msg.level == app.model.FlashTypes.SUCCESS:
        rtn.level = "SUCCESS"
      elif msg.level == app.model.FlashTypes.NOTICE:
        rtn.level = "NOTICE"
    return rtn


# Logging
log = Logging.get()
