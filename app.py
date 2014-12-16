from flask import Flask, request
import json

from tori import tori

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    data = request.json
    if data['status'] == ok and data['events']:
      return data['events'][0]['message']['text']
    else:
      pass
  elif request.method == 'GET':
    return 'toriniku'

if __name__ == '__main__':
  app.run()
