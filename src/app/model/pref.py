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
from .base import Base
from nark import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Sequence
from sqlalchemy import *
from sqlalchemy.orm import *
import base
import app


class Pref(Base):

    __tablename__ = 'prefs'

    id = Column(Integer, Sequence('pref_id_seq'), primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    def __init__(self, key, value):
      self.key = key
      self.value = value

    def __repr__(self):
        return "<Record('%s = %s')>" % (self.key, self.value)


@resolve(app.scope)
class Prefs(object):
  """ Container for the prefs objects """

  def __init__(self, db=base.IDb):
    self.db = db

  def session(self):
    self.db.connect()
    return self.db.session
    
  def add(self, key, value):
    session = self.session()
    if self.has(key):
      record = self.get(key)
      record.value = value
    else:
      pref = Pref(key, value)
      session.add(pref)
    session.commit()

  def delete(self, key):
    if self.has(key):
      session = self.session()
      record = self.get(key)
      session.delete(record)
      session.commit()

  def has(self, key):
    session = self.session()
    return session.query(exists().where(Pref.key == key)).scalar()

  def get(self, key):
    session = self.session()
    return session.query(Pref).filter_by(key=key).first()
