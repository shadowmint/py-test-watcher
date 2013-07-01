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

import os
import re
import time


class FileWatcher(object):
  """ Looks for any changes in the path for files match pattern since the given timestamp.

      If there is any file more recent than since, the action is invoked,
      and since is updated to be the current timestamp.
  """

  def __init__(self, path=os.getcwd(), since=0, pattern=".*", action=None):
    self.path = path
    self.since = since
    self.pattern = pattern
    self.action = action

  def __last_update(self):
    """ Return the timestamp for the newest file matching pattern """
    rtn = 0
    for root,dirs,files in os.walk(self.path):
      for filename in files:
        path = os.path.join(root, filename)
        if re.match(self.pattern, filename):
          stats = os.stat(path)
          mtime = stats.st_mtime
          if mtime > rtn:
            rtn = mtime
            if rtn > self.since:
              break
    return rtn

  def run(self):
    rtn = False
    ltime = self.since
    ftime = self.__last_update()
    if ftime > ltime:
      print("Performed action")
      if self.action is not None:
        self.action()
      self.since = time.time()
      rtn = True
    return rtn

