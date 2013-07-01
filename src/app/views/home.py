from __future__ import absolute_import
from nark import *
from base import *
from app import conf 
import app.model
import app
import os
from datetime import datetime


@resolve(app.scope)
class Home(object):
  
  def __init__(self, session=ISession):
    self.session = session
    self.flash_service = app.model.Flash()
    self.prefs = app.model.Prefs()
    log.info("Found new session")
    self.session.watcher = FileWatcher()
    self.session.watcher.pattern = ".*\.py"
    self.session.watcher.action = self.actually_run_tests
    self.can_growl = run("growlnotify", check_only=True)
    self.last_result = True
    if not self.can_growl:
      log.warn("growlnofity isn't installed. Can't growl. :(")

  def select_test_watch_path(self, value):
    path = self.session.webkit.select_path()
    self.prefs.add(conf.tests.watch, path)
    self.flash_service.notice("Selected watch path: %s" % path)

  def select_test_path(self, value):
    path = self.session.webkit.select_path()
    self.prefs.add(conf.tests.location, path)
    self.flash_service.notice("Selected path: %s" % path)

  def select_test_runner(self, value):
    path = self.session.webkit.select_file()
    self.prefs.add(conf.tests.runner, path)
    self.flash_service.notice("Selected runner: %s" % path)

  def run_tests(self, value):
    self.path = self.prefs.get(conf.tests.location).value
    self.runner = self.prefs.get(conf.tests.runner).value
    self.session.watcher.path = self.prefs.get(conf.tests.watch).value
    self.session.watcher.run()  # Updates rtn if it ran
    return self.rtn

  def actually_run_tests(self):
    rtn = Dynamic()
    try: 
      log.info("File changes detected, actually ran tests")
      os.chdir(self.path)
      rtn.success, rtn.value = run(self.runner, capture_output=True)
      if self.can_growl:
        if rtn.success != self.last_result:
          self.last_result = rtn.success
          if not rtn.success:
            run("growlnotify", "-s", "-m", "Fail. FAil. FAIL. Fail. FAiled.\nYOUR TESTS FAILED.", "--image", self.session.assets.resolve("img/fail.png"))
          else:
            run("growlnotify", "-s", "-m", "Tests are happy again.\nGood job :)", "--image", self.session.assets.resolve("img/success.png"))
    except:
      e = exception()
      rtn.success = False
      rtn.value = str(e)
    rtn.last_update = "%s" % datetime.now()
    self.rtn = rtn

log = Logging.get()

