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
import unittest
from nark import *

class RunTests(unittest.TestCase):

  def test_run_command(self):
    run("ls", "-al")

  def test_run_successful_command_with_steal(self):
    a = Assert()
    ran, output = run("ls", capture_output=True)
    a.true(ran, "Wrong return code")
    a.not_equal(output, "", "Didn't get content")

  def test_run_bad_command_with_steal(self):
    a = Assert()
    ran, output = run("ls", "-al", "DSFSDFSDF/SFSDFS", capture_output=True)
    a.false(ran, "Wrong return code")
    a.not_equal(output, "", "Didn't get content")

  def test_can_run_command(self):
    a = Assert()
    has_ls = run("ls", check_only=True)
    has_xddsds = run("xddsds", check_only=True)
    a.true(has_ls, "Didn't find ls")
    a.false(has_xddsds, "Found stupid program")


if __name__ == "__main__":
  unittest.main()
