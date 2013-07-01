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
from .idb import IDb
from .iconfig import IConfig
from nark import *
from app.config import scope
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


@resolve(scope)
@implements(IDb)
class Db():

  def __init__(self, config=IConfig):
    self.config = config
    self.assets = Assets(self.config.root)
    self.engine = None

  def connect(self):
    """ Create the local database if required """
    if self.engine is None:
      engine = create_engine(self.config.db, echo=self.config.db_debug)
      session = sessionmaker(bind=engine)
      self.__session = session
      self.engine = engine
      self.session = self.__session()  # Instance

  def disconnect(self):
    """ Rebuild all the things """
    if self.engine is not None:
      self.session.close()
      self.engine = None

  def rebuild(self):
    """ For tests; build the schema immediately.
        Use alembic for production things.
    """
    from app.model.base import Base
    Base.metadata.create_all(self.engine)
    self.disconnect()
    self.connect()
