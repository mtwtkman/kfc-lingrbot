# -*- coding: utf-8 -*-

from flask import Flask, request
from datetime import date, datetime, timedelta
import pytz
from kfc_msg import kfc_msg
from calendar import monthrange
import re, random

app = Flask(__name__)
app.debug = True

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
