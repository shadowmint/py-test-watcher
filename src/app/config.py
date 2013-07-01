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
import base
import os


@implements(base.IConfig)
class Config():
  def __init__(self):

    # The path for the database
    self.db = "sqlite:///db.sqlite3"

    # Do we want to dump db debug info?
    self.db_debug = False

    # Current base path
    self.root = os.getcwd()


# Special scope just for the config options, so other services can depend on them.
scope = Scope()
scope.register(Config)
