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


class ImplementsTests(unittest.TestCase):

  def test_can_decorate_class(self):
    a = Assert()

    class IType(object):
      def xxx(self):
        pass
      def yyy(self):
        pass
      def zzz(self):
        pass

    @implements(IType)
    class ImplGood(object):
      def xxx(self):
        pass
      def yyy(self):
        pass
      def zzz(self):
        pass

    instance = ImplGood()
    a.not_null(instance, "Failed to create instance of decorated class")

  def test_cannot_decorate_class_without_correct_impl(self):
    a = Assert()

    class IType(object):
      def xxx(self):
        pass
      def yyy(self):
        pass
      def zzz(self):
        pass

    failed = False
    try:
      @implements(IType)
      class ImplGood(object):
        def xxx(self):
          pass
    except ImplementsException:
      e = exception()
      a.true(e.signature["xxx"], "Didn't find existing method")
      a.false(e.signature["yyy"], "Found missing method 'yyy'")
      a.false(e.signature["zzz"], "Found missing method 'zzz'")
      a.equals(len(e.signature.keys()), 3, "Found some other crazy thing on class")
      failed = True

    a.true(failed, "Could decorate an invalid class")

  def test_cannot_decorate_class_without_correct_props(self):
    a = Assert()

    class IType(object):
      prop1 = None
      prop2 = None
      def xxx(self):
        pass

    @implements(IType)
    class ImplGood(object):
      prop1 = "X"
      prop2 = "Y"
      def __init__(self):
        self.prop1 = p1
        self.prop2 = p2
      def xxx(self):
        pass

    failed = False
    try:
      @implements(IType)
      class ImplBad(object):
        prop2 = ""
        def xxx(self):
          pass
    except ImplementsException:
      e = exception()
      print("%r", e.signature)
      a.false(e.signature["prop1"], "Didn't detect missing property")
      a.true(e.signature["prop2"], "Didn't detect existing property")
      a.equals(len(e.signature.keys()), 3, "Found some other crazy thing on class")
      failed = True

    a.true(failed, "Could decorate an invalid class")


if __name__ == "__main__":
  unittest.main()
