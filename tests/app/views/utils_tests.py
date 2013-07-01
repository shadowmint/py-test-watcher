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
from pau.views import Utils


class UtilsTests(unittest.TestCase):

  # db for this test
  db_name = "UtilsTests.sqlite"

  def setup(self):
    """ Setup db and return instance """
    self.config = pau.IConfig
    self.session = pau.ISession
    pau.resolve(self)

    self.session.assets = Assets()
    self.config.db = self.db_name

    self.db = pau.IDb
    pau.resolve(self)

    self.prefs = pau.model.Prefs()
    self.controller = Utils()
    pau.resolve_children(self)

    # Instance
    return self.controller

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

  def test_reformat(self):
    a = Assert()
    i = self.setup()
    local_path = os.path.join(os.getcwd(), "path")
    self.prefs.add(pau.Preferences.LOCATION, local_path)
    i.reformat("", "")
    self.teardown()


if __name__ == "__main__":
  unittest.main()
