from flask import Flask, request
import json

from tori import tori

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    return request.json['message']['text']
    if 'KFC' in request.json['message']['text']:
      return 'torinohi'
    else:
      pass
  elif request.method == 'GET':
    return 'toriniku'

if __name__ == '__main__':
  app.run()
