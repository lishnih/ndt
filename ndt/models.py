#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-01

import string, md5
from datetime import datetime
from random import choice

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relationship
from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


size = 24


class Group(Base):                      # rev. 20120415
    __tablename__ = 'groups'
    id        = Column(Integer, primary_key=True)
    name      = Column(String)
    description = Column(String)
    homedir   = Column(String)


class UserRole(Base):                   # rev. 20120415
    __tablename__ = 'user_roles'
    id        = Column(Integer, primary_key=True)
    _users_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
    _groups_id = Column(Integer, ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'))


class User(Base):                       # rev. 20120415
    __tablename__ = 'users'
    id        = Column(Integer, primary_key=True)
    _groups_id = Column(Integer, ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'))

    name      = Column(String)
    password  = Column(String)
    blowfish  = Column(String)
    email     = Column(String)
    created   = Column(Integer, default=datetime.utcnow)    # Время создания задания
    updated   = Column(Integer, onupdate=datetime.utcnow)   # Время обновления задания

#     groups    = relationship(Group, secondary=UserRole, backref='users')
    groups    = relationship(Group, backref='users')

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        self.set_password(self.password)
        self.new_blowfish()

    def set_password(self, unhashedpass=''):
        self.password = md5.new(unhashedpass).hexdigest()

    def new_blowfish(self):
        self.blowfish = ''.join([choice(string.letters + string.digits) for i in range(size)])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Пользователь '{}'>".format(self.name)


class Db(Base):                         # rev. 20120419
    __tablename__ = 'dbs'
    id        = Column(Integer, primary_key=True)
    _groups_id = Column(Integer, ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'))

    group = relationship(Group, backref=backref('groups', cascade='all, delete, delete-orphan'))

    name      = Column(String)
    enabled   = Column(Integer)
    connect_on = Column(String)
    url       = Column(String)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<БД '{}'>".format(self.name)


class Option(Base):                     # rev. 20120415
    __tablename__ = 'options'
    id        = Column(Integer, primary_key=True)
    _users_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))

    user = relationship(User, backref=backref('users', cascade='all, delete, delete-orphan'))

    name      = Column(String)
    enabled   = Column(Integer)
    section   = Column(String)
    option    = Column(String)
    value     = Column(String)
    type      = Column(String)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        self.name = u"{}.{}".format(section, option)
        self.type = str(type(self.value)).replace("<type '", '').replace("'>", '')

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"<Опция '{}'>".format(self.name)
