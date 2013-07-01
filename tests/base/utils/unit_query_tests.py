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
from pau.utils.unit_query import *
import os
from pau.model import *
from nark import *


class UnitQueryTests(unittest.TestCase):

  # Path for this query
  # path = "/Users/doug/Library/Application Support/Steam/SteamApps/common/Planetary Annihilation/PA.app/Contents/Resources/"
  path = "media"

  def test_can_parse_units(self):
    assets = Assets(self.path)
    a = Assert()

    valid, invalid = load_units(assets)

    for i in invalid.keys():
      print("Failed: %s" % invalid[i])

    for u in valid.keys():
      unit = valid[u]
      print("\nUnit: %s" % u)
      for k in unit.keys():
        print("- %s ---> %r" % (k, unit[k]))

    #a.equals(len(invalid), 0, "Some units couldn't be loaded")


if __name__ == "__main__":
  unittest.main()
