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

import app
import os
import app.config
from app.model import *
from base import *
from nark import *


@resolve(app.config.scope)
class TestHarness(object):

  def __init__(self, db_url, config=IConfig):
    self.config = config
    self.config.db = "sqlite:///%s" % db_url
    self.config.db_debug = False

    # Set assets to current folder
    self.session = app.scope.resolve(ISession)
    self.session.assets = Assets()
    a = self.session.assets
    self.db_path = a.new(db_url)

    # Open db connection and load schema
    self.db = app.scope.resolve(IDb)
    self.db.connect()
    self.db.rebuild()

  def clean(self):
    try:
      os.remove(self.db_path)
    except:
      e = exception()
      print(e)
      pass
