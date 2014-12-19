# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import date, datetime, timedelta
import pytz
from calendar import monthrange
import re, random, os

from kfc_msg import kfc_msg

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_POSTGRESQL_VIOLET_URL') if os.getenv('IS_HEROKU') else os.getenv('POSTGRES_TORI')

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
  signal()

  if request.method == 'POST':
    data = request.json

    pattern = re.compile(r'[KＫ][･・]?[FＦ][･・]?[CＣ][!！]?')

    if data['status'] == 'ok':
        if re.search(pattern, data['events'][0]['message']['text']):
          return tori()
    else:
      pass
  elif request.method == 'GET':
    return 'toriniku'

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

def tori():
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

if __name__ == '__main__':
  app.run()
