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

import unittest
import bootstrap
import pau
import os
from pau.model import *
from nark import *
from pau.views import Home


class HomeTests(unittest.TestCase):

  # db for this test
  db_name = "HomeTests.sqlite"

  def setup(self):
    """ Setup db and return instance """
    self.config = pau.IConfig
    self.session = pau.ISession
    pau.resolve(self)

    self.session.assets = Assets()
    self.config.db = self.db_name
    self.config.db_debug = False

    self.db = pau.IDb
    pau.resolve(self)

    self.prefs = Prefs()
    pau.resolve(self.prefs)

    # Instance
    i = Home()
    pau.resolve(i)
    return i

  def teardown(self):
    self.db.reset()
    try:
      os.remove(self.db_name)
    except:
      pass

  def test_can_create_instance(self):
    a = Assert()
    i = self.setup()
    a.not_null(i, "Unable to create instance")
    self.teardown()

  def test_has_setup_fails(self):
    a = Assert()
    i = self.setup()
    rtn = i.has_setup("", "")
    a.false(rtn["result"], "Failed to not find preferences")
    self.teardown()

  def test_has_setup_passes(self):
    a = Assert()
    i = self.setup()
    self.prefs.add(pau.Preferences.LOCATION, "VALUE")
    rtn = i.has_setup("", "")
    a.true(rtn["result"], "Failed to find preferences")
    self.teardown()

  def test_preferences(self):
    a = Assert()
    i = self.setup()
    self.prefs.add(pau.Preferences.LOCATION, "VALUE")
    rtn = i.preference("", "LOCATION")
    a.equals(rtn["result"], "VALUE", "Failed to find preference by key")
    self.teardown()

  def test_flash(self):
    a = Assert()
    i = self.setup()

    i.flash_service.notice("Hello World")
    i.flash_service.success("Hello Again")

    rtn = i.flash("", "")
    a.equals(rtn["result"], "Hello World", "Failed to return oldest message")

    rtn = i.flash("", "")
    a.equals(rtn["result"], "Hello Again", "Failed to return second message")

    rtn = i.flash("", "")
    a.false(rtn["result"], "Invalid return when no messages")

    self.teardown()


if __name__ == "__main__":
  unittest.main()
