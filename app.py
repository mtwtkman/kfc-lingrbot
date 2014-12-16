# -*- coding: utf-8 -*-

from flask import Flask, request
from datetime import datetime, date

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    data = request.json
    if data['status'] == 'ok' and 'KFC' in data['events'][0]['message']['text']:
      return 'もうちょっと我慢しろ'
    else:
      pass

  elif request.method == 'GET':
    return 'toriniku'


if __name__ == '__main__':
  app.run()
