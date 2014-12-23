# -*- coding: utf-8 -*-

# config{{{
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta
import pytz
from calendar import monthrange
import re, random, os
from kfc_msg import kfc_msg

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_POSTGRESQL_VIOLET_URL') if os.getenv('IS_HEROKU') else os.getenv('POSTGRESQL_TORI')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

from models import User, Room

# }}}

@app.route('/', methods=['GET', 'POST']) # {{{
def index():
  #signal()
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
      username = message_data['nickname']
      roomname = message_data['room']
      pattern = re.compile(r'[KＫ][･・]?[FＦ][･・]?[CＣ][!！]?')
      if re.search(pattern, text):
        user = User.query.filter_by(username=username).first()
        if user is None:
          user = User(username=username)
          room = Room(roomname=roomname, count=1, user=user)
          db.session.add_all([user, room])
        else:
          # ここ時限にしようかな
          if user.rooms.filter_by(roomname=roomname).first().count is 10:
            user.rooms.filter_by(roomname=roomname).first().count = 1
            db.session.add(user)
            return '{} さん、しつこい'.format(username)
          user.rooms.filter_by(roomname=roomname).first().count += 1
          db.session.add(user)
        return tori()
  elif request.method == 'GET':
    return 'toriniku'
# }}}

''' signal(){{{
def signal():
  today = datetime.now(pytz.timezone('Asia/Tokyo'))

  tori_day = 28
  tori_day_signal = (0, 6, 12, 15, 18, 20)

  before_day = 27
  before_day_signal = (0, 6, 12, 15, 23)

  if today.day is tori_day and today.minute is 0:
    if today.hour in tori_day_signal:
      return '今日は記念すべきとりの日です。満を持して行きましょう。'
  elif today.day is before_day and today.minute is 0:
    if today.hour in before_day_signal:
      return '明日は待ちに待ったとりの日です。開店ダッシュしましょう。'
}}} '''

def tori(): # {{{
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

    return 'とりの日パックまであと{}日なんだけど{}'.format(left_days.days, random.choice(kfc_msg))
# }}}

if __name__ == '__main__':
  app.run()
