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
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_POSTGRESQL_VIOLET_URL') if os.getenv('IS_HEROKU') else 'postgresql://boku:@localhost/toridb'

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
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

    if left_days.days-1 > 20:
      degree = 'far'
    elif left_days.days-1 > 5:
      degree = 'middle'
    else:
      degree = 'near'
    return 'とりの日パックまであと{}日なんだけど{}'.format(left_days.days, random.choice(kfc_msg[degree]))

if __name__ == '__main__':
  app.run()
