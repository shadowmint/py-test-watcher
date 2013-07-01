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
import time
from nark import *


class FileWatcherTests(unittest.TestCase):

  def test_can_create_instance(self):
    a = Assert()
    i = FileWatcher()
    a.not_null(i, "Unable to create instance")

  def test_runs_callback_if_not_lock_found(self):
    i = FileWatcher()

    self.ran = False
    def callback():
      print("Callback~")
      self.ran = True
    i.action = callback
    i.run()

  def test_matches_on_pattern_correctly(self):
    a = Assert()
    i = FileWatcher()

    i.pattern = ".*\.py"
    ran = i.run()
    a.true(ran, "Didn't find python files")

    i.pattern = ".*\.pyz"
    ran = i.run()
    a.false(ran, "Found missing .pyz files")

  def test_only_triggered_on_actual_filechanges(self):
    a = Assert()
    i = FileWatcher()
    assets = Assets()

    self.value = 0
    def callback():
      self.value += 1

    i.path = assets.resolve("data")
    i.pattern = ".*\.txt"
    i.action = callback

    ran = i.run()
    a.equals(self.value, 1, "Ran callback too many times")
    a.true(ran, "Didn't run required callback")

    ran = i.run()
    a.equals(self.value, 1, "Ran callback too many times")
    a.false(ran, "Bad return code for not running")

    time.sleep(1)  # At least one second resolution
    assets.touch("data", "sub2", "sub3", "junk3.txt")

    ran = i.run()
    a.equals(self.value, 2, "Ran callback too many times")
    a.true(ran, "Didn't run required callback")

  def test_less_watcher(self):
    # TODO: Watch all the .less files in the data directory
    #       and if any of them change, run a command on any
    #       less files in the given target path
    #
    # NB. Yep, that means you've got to pass the path to the
    #     action, depending on its argument signature.
    pass


if __name__ == "__main__":
  unittest.main()
