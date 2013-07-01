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
from base import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Sequence
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
import app


# Possible message types
FlashTypes = enum(NOTICE=1, SUCCESS=2, FAILURE=3)


class FlashMsg(Base):

    __tablename__ = 'flash_msg'

    id = Column(Integer, Sequence('flash_msg_id_seq'), primary_key=True)
    created_on = Column(DateTime, nullable=False)
    level = Column(Integer, nullable=False)
    message = Column(String, nullable=False)

    def __init__(self, level, message):
      self.level = level
      self.message = message
      self.created_on = datetime.datetime.utcnow()

    def __repr__(self):
        return "<Flash('%s (%s, created on: %s)')>" % (self.message, self.level, self.created_on)


@resolve(app.scope)
class Flash(object):
  """ Container for the prefs objects """

  def __init__(self, db=IDb):
    self.db = db

  def session(self):
    self.db.connect()
    return self.db.session

  def fail(self, message):
    """ Post a new message to tell the user about """
    session = self.session()
    record = FlashMsg(FlashTypes.FAILURE, message)
    session.add(record)
    session.commit()
    log.error("Flash! %s (FAILURE)" % message)

  def success(self, message):
    """ Post a new message to tell the user about """
    session = self.session()
    record = FlashMsg(FlashTypes.SUCCESS, message)
    session.add(record)
    session.commit()
    log.info("Flash! %s (SUCCESS)" % message)

  def notice(self, message):
    """ Post a new message to tell the user about """
    session = self.session()
    record = FlashMsg(FlashTypes.NOTICE, message)
    session.add(record)
    session.commit()
    log.info("Flash! %s (NOTICE)" % message)

  def get(self):
    """ Return the next pending flash message """
    session = self.session()
    if self.any():
      rtn = session.query(FlashMsg).order_by(FlashMsg.created_on).first()
      session.delete(rtn)
      session.commit()
      return rtn
    return None

  def any(self):
    """ Return true if any pending messages """
    session = self.session()
    return session.query(FlashMsg).count() > 0


# Logging
log = Logging.get()
