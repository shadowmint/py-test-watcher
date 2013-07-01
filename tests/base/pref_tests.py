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
import os
from app.model import *
from nark import *
from base.test_harness import TestHarness


class PrefTests(unittest.TestCase):

  def setup(self):
    self.harness = TestHarness("PrefTests.sqlite")
    self.db = self.harness.db
    return  Prefs()

  def teardown(self):
    self.db.disconnect()
    self.harness.clean()

  def test_can_create_instance(self):
    a = Assert()
    i = self.setup()
    a.not_null(i, "Unable to create instance")
    self.teardown()

  def test_can_insert(self):
    a = Assert()
    i = self.setup()
    i.add("Key", "Value")
    self.teardown()

  def test_can_get_by_name(self):
    a = Assert()
    i = self.setup()
    i.add("Key", "Value")
    record = i.get("Key")
    a.equals(record.value, "Value", "Failed to query db")
    self.teardown()

  def test_can_delete_record(self):
    a = Assert()
    i = self.setup()

    i.add("Key", "Value")
    found = i.has("Key")
    a.true(found, "Failed to found record")

    i.delete("Key")
    found = i.has("Key")
    a.false(found, "Found missing record")

    self.teardown()

  def test_can_update_record(self):
    a = Assert()
    i = self.setup()

    i.add("Key1", "Value")
    i.add("Key1", "Value2")
    i.add("Key1", "Value3")

    p = i.get("Key1")
    a.equals(p.value, "Value3", "Update didn't work")

    i.delete("Key1")
    found = i.has("Key1")
    a.false(found, "Multiple insert did not do an update")

    self.teardown()


if __name__ == "__main__":
  unittest.main()
