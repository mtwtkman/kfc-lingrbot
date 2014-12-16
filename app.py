# -*- coding: utf-8 -*-

from flask import Flask, request
from datetime import date, datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    data = request.json
    if data['status'] == 'ok' and 'KFC' in data['events'][0]['message']['text']:
      return tori()
    else:
      pass

  elif request.method == 'GET':
    return 'toriniku'

def tori():
  if datetime.now().day is 28:
    return '今日はとりの日パックだからはよ行って来い'
  else:
    year, month, day = datetime.now().year, datetime.now().month, datetime.now().day
    if datetime.now().day < 28:
      left_days = date(year, month, 28) - date(year, month, day)
    else:
      if month is 12:
        new_year = year + 1
        new_month = 1
      else:
        month += 1
      left_days = date(new_year, new_month, 28) - date(year, month, day)

    if left_days.days-1 > 20:
      degree = 'だし結構'
    elif left_days.days-1 > 5:
      degree = 'なんだけどしばらく'
    else:
      degree = 'なんだからもうちょっと'
    return 'とりの日パックまであと{}日{}我慢しろ'.format(left_days.days-1, degree)


if __name__ == '__main__':
  app.run(debug=True)
