# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta
import pytz
from calendar import monthrange
import re, random, os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_POSTGRESQL_VIOLET_URL') if os.getenv('IS_HEROKU') else os.getenv('POSTGRESQL_TORI')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

# models {{{
class KFC(db.Model):
  __tablename__ = 'kfc'
  id = db.Column(db.Integer, primary_key=True)
  pattern = db.Column(db.String(256), unique=True)
  created_by = db.Column(db.String(256))

  def __repr__(self):
    return '<KFC Pattern %r>' % self.pattern

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(256), unique=True)
  rooms = db.relationship('Room', backref='user', lazy='dynamic')

  def __repr__(self):
    return '<User %r>' % self.username

class Room(db.Model):
  __tablename__ = 'rooms'
  id = db.Column(db.Integer, primary_key=True)
  roomneme = db.Column(db.String(256), unique=True)
  counter = db.Column(db.Integer)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def __repr__(self):
    return '<Room %r>' % self.roomneme
# }}}

@app.route('/', methods=['GET', 'POST']) # {{{
def index():
  if request.method == 'POST':
    ''' Lingr API {{{
    {"status":"ok",
     "counter":208,
     "events":[
      {"event_id":208,
       "message":
        {"id":82,
         "room":"myroom",
         "public_session_id":"UBDH84",
         "icon_url":"http://example.com/myicon.png",
         "type":"user",
         "speaker_id":"kenn",
         "nickname":"Kenn Ejima",
         "text":"yay!",
         "timestamp":"2011-02-12T08:13:51Z",
         "local_id":"pending-UBDH84-1"}}]}
    }}} '''

    data = request.json
    if data['status'] == 'ok':
      message_data = request.json['events'][0]['message']
      text = message_data['text']
      nickname = message_data['nickname']
      room = message_data['room']
      kfc_hit = re.compile(r'[KＫ][･・]?[FＦ][･・]?[CＣ][!！]?')
      make_pattern = re.compile(r'(^!kfc)\s(.*$)')
      delete_pattern = re.compile(r'^!kfc!!$')
      if re.search(kfc_hit, text):
        ''' kfc count{{{
        user = User.query.filter_by(username=username).first()
        if user is None:
          user = User(username=username)
          room = Room(roomname=roomname, count=1, user=user)
          db.session.add_all([user, room])
        else:
          room = user.rooms.filter_by(roomname=roomname).first()
          if room is None:
            user.rooms.roomname = roomname
            user.rooms.count = 0
          elif room.count is 5:
            room.count = 0
            db.session.add(user)
            #return '{} さん、しつこい'.format(username)
          else:
            room.count += 1
          db.session.add(user)
        }}} '''
        return tori()
      elif re.search(make_pattern, text):
        pattern = re.search(make_pattern, text).group(2)
        kfc = KFC(pattern=pattern, created_by=nickname)
        db.session.add(kfc)
        return '{} さんが "{}" を登録しました。'.format(nickname, pattern)
      elif re.search(delete_pattern, text):
        target = KFC.query.filter(KFC.id>18).order_by('id desc').first()
        if target is not None:
          db.session.delete(target)
          return '"{}" を削除しました。'.format(target.pattern)
  elif request.method == 'GET':
    return 'toriniku'
# }}}

@app.route('/pattern')
def pattern():
  patterns = {k.id: {'pattern': k.pattern, 'created_by': k.created_by} for k in KFC.query.all()}
  return render_template('pattern.html', patterns=patterns)

def tori(): # {{{
  kfc_msg = [k.pattern for k in KFC.query.all()]
  today = datetime.now(pytz.timezone('Asia/Tokyo'))
  if today.day is 28:
    return '今日はとりの日パックだからはよ行って来い'
  else:
    year, month, day = today.year, today.month, today.day
    if today.day < 28:
      left_days = timedelta(28 - day)
    else:
      last_day = monthrange(year, month)[1]
      left_days = timedelta(last_day - day + 28)

    return 'とりの日パックまであと{}日{}'.format(left_days.days, random.choice(kfc_msg))
# }}}

if __name__ == '__main__':
  app.run()
