# -*- coding: utf-8 -*-

from app import db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, index=True)
  rooms = db.relationship('Room', backref='user', lazy='dynamic')

  def __repr__(self):
    return '<User %r>' % self.username

class Room(db.Model):
  __tablename__ = 'rooms'
  id = db.Column(db.Integer, primary_key=True)
  roomname = db.Column(db.String(80), unique=True)
  count = db.Column(db.Integer)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

  def __repr__(self):
    return '<Room %r>' % self.roomname
