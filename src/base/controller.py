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
import inspect


class Controller(object):
  """ Binds various webkit event handles """

  def __init__(self, webkit):
    self.webkit = webkit
    self.controllers = []

  def load(self, module):
    classes = inspect.getmembers(module, inspect.isclass) 
    for cls in classes:
      self.register(cls[1])

  def register(self, cls):
    instance = cls()
    self.controllers.append(instance)
    t_methods = inspect.getmembers(instance, predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x))
    for k in t_methods:
      name = "%s.%s" % (cls.__name__, k[0])
      self.webkit.listen(name, k[1])
