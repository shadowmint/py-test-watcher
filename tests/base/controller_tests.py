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
from nark import *


class Dummy(object):
  def __init__(self):
    self.items = []

  def listen(self, key, callback):
    self.items.append(key)


class PrefTests(unittest.TestCase):

  def setup(self):
    self.dummy = Dummy()
    i = pau.Controller(self.dummy)
    return i

  def test_can_create_instance(self):
    a = Assert()
    i = self.setup()
    a.not_null(i, "Unable to create instance")

  def test_can_load_module(self):
    a = Assert()
    i = self.setup()
    import controllers
    i.load(controllers)

    a.equals(len(self.dummy.items), 6, "Failed to load targets")
    a.contains(self.dummy.items, "One.one", "Loaded targets were not named correctly")
    a.contains(self.dummy.items, "Two.one", "Loaded targets were not named correctly")
    a.contains(self.dummy.items, "Three.two", "Loaded targets were not named correctly")


if __name__ == "__main__":
  unittest.main()
