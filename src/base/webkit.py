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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from nark import *
from .isession import ISession
import json
import sys
import app


print(app)
@resolve(app.scope)
class Webkit(object):
  """ A simply wrapper around PyQt to render content in a webkit frame """

  def __init__(self, base, path, session=ISession):
    self.base = base
    self.path = path
    self.session = session
    self.assets = self.session.assets
    self.__handlers = {}

  def listen(self, id, callback):
    """ Listen to for browser events.

        The callback should be in the form:

        def callback(id, data):
          # ...
          return {}

        ie. It always takes a parsed json object at the argument,
        and returns a dictionary to be serialized as json.

        To invoke an event from the browser, call:

          bridge.trigger("id", JSON.stringify({"My" : "Object"}))

        You may want to define a convenience function that does
        this directly on objects.
    """
    if id not in self.__handlers.keys():
      self.__handlers[id] = []
    self.__handlers[id].append(callback)

  def trigger(self, id, value):
    """ Trigger an event from an id + json block """
    if not id in self.__handlers.keys():
      log.warn("Invalid event id from browser: '%s' is not bound" % id)
    else:
      data = None
      try:
        data = json.loads(value)
        if isinstance(data, dict):
          data = Dynamic(data)
      except ValueError:
        e = exception()
        log.warn("Invalid JSON string from browser: '%s'" % value)
        log.warn("Parser failed with: %s" % str(e))
      if data is not None:
        rtn = []
        for callback in self.__handlers[id]:
          try:
            value = callback(data)
            if value is None:
              value = {}
            elif isinstance(value, Dynamic):
              value = dict(iter(value))
            rtn.append(value)
          except Exception:
            e = exception()
            log.warn("Failed while running '%s': %r" % (id, e))
        if len(rtn) == 1:
          return rtn[0]
        else:
          return rtn
    return {} 

  def ajax(self, url):
    """ Load a file via ajax """
    parts = url.split("/")
    filename = self.assets.resolve(*parts)
    with open(filename, 'r') as fp:
      data = fp.read()
    return data

  def select_path(self):
    """ Show a 'select directory' dialog """
    file = str(QFileDialog.getExistingDirectory(self.window, "Select Directory"))
    return file

  def select_file(self):
    """ Show a 'select file' dialog """
    file = str(QFileDialog.getOpenFileName(self.window, "Select File"))
    return file

  def run(self):
    """ Run the webkit ui until it terminates """
    self.app = QApplication(sys.argv)
    window = Window(self, self.base, self.path)
    window.show()
    self.window = window
    self.app.exec_()


class Bridge(QObject):
  """ Callable bridge from webkit """

  def __init__(self, widget, parent):
    super(Bridge, self).__init__(widget)
    self.__parent = parent

  @pyqtSlot(str, str, result=str)
  def trigger(self, id, value):
    rtn = self.__parent.trigger(str(id), str(value))
    raw = json.dumps(rtn)
    return raw

  @pyqtSlot(str, result=str)
  def _ajax(self, url):
    raw = self.__parent.ajax(str(url))
    return raw

  @pyqtSlot()
  def quit(self):
    QApplication.quit()


class Window(QWidget):

  def __init__(self, parent, base, path):
    super(Window, self).__init__()
    self.setAutoFillBackground(True)
    self.setBackgroundRole(QPalette.Highlight)

    # Create view
    self.view = QWebView(self)
    layout = QVBoxLayout(self)
    layout.setMargin(0)
    layout.addWidget(self.view)

    # Create bridge
    self.bridge = Bridge(self, parent)
    self.base = base

    # Bind js whenever required
    view = self.view
    def bind_bridge():
      view.page().mainFrame().addToJavaScriptWindowObject("bridge", self.bridge)
    view.connect(view.page().mainFrame(), SIGNAL("javaScriptWindowObjectCleared()"), bind_bridge)
    bind_bridge()

    # Read html for start page
    with open(path, "r") as fp:
      html = fp.read()

    # Set base url path for browser
    baseUrl = QUrl.fromLocalFile(self.base)
    self.view.setHtml(html, baseUrl)


# Logging
log = Logging.get()
