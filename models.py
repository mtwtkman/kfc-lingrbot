from app import db

class KFC(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  room = db.Column(db.String(80), unique=True)
  count = db.Column(db.Integer)

  def __init__(self, room, count):
    self.room = room
    self.count = count

  def __repr__(self):
    return '<KFC %r>' % self.room
