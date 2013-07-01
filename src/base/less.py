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
import time
import os
from datetime import datetime, timedelta
from nark import Logging, run, enum, Assets
from nark.process import Worker
from os.path import join


class Less(object):
  """ Less css compiler 

      lessc isn't installed?
      install instructions: http://lesscss.org/
  """

  def watch(self, path):
    """ Watch the given path as long as the app is running """

    # Check and warn
    if not run("lessc", check_only=True):
      log.warn("lessc is not installed. Less files were not updated")
      return

    l = LessWatcher(path)
    l.start()

  def execute(self, path):
    """ Convert all .less files in the given path to .css """

    # Check and warn
    if not run("lessc", check_only=True):
      log.warn("lessc is not installed. Less files were not updated")
      return

    # Look for oldest css file
    assets = Assets(path)
    updated = False
    oldest = 0
    reason = ""
    for f in os.listdir(path):
      f = f.lower()
      if f[-5:] == ".less":
        fullpath = join(path, f)
        output_path = fullpath[:-5] + ".css"
        if not assets.exists(output_path):
          updated = True
          reason = "missing css file"
          break
        else:
          opath = assets.resolve(output_path)
          utime = os.path.getmtime(opath)
          if utime > oldest:
            oldest = utime
            oldest_name = opath

    # Look for changes to any less files
    for root, dirnames, filenames in os.walk(path):
      for f in filenames:
        f = f.lower()
        if f[-5:] == ".less":
          fullpath = join(root, f)
          otime = os.path.getmtime(fullpath)
          if otime > oldest:
            updated = True
            reason = "less file updated"
            break

    # Found some? Ok, process the target dir
    if updated:
      for f in os.listdir(path):
        f = f.lower()
        if f[-5:] == ".less":
          fullpath = join(path, f)
          output_path = fullpath[:-5] + ".css"
          run("lessc", fullpath, output_path)
          log.info("css rebuild: %s" % reason)


# Event keys for the less watcher
LessWatcherActions = enum("PING", "PONG")


class LessWatcher(Worker):
  """ Creates a process that watches for changes to a file and compiles on demand """

  def __init__(self, path):
    self.updater = Less()
    self.path = path

  def remote_update(self):
    interval = datetime.now() - self.last_update
    if interval > timedelta(seconds=2):
      log.info("Remote timeout. Quiting less watcher...")
      self.api.stop()
    else:
      self.updater.execute(self.path)
      self.api.trigger(LessWatcherActions.PING)
      time.sleep(1)

  def ping(self):
    self.api.trigger(LessWatcherActions.PONG)

  def pong(self):
    self.last_update = datetime.now()

  def remote(self, data):
    self.api.listen(LessWatcherActions.PONG, self.pong)
    self.last_update = datetime.now()
    while self.api.alive():
      if not self.api.poll():
        break
      self.remote_update()
      time.sleep(0.1)  # Don't spam
  
  def local(self, data):
    self.api.listen(LessWatcherActions.PING, self.ping)
    self.api.event_loop(wait=False)


# Logging
log = Logging.get()
