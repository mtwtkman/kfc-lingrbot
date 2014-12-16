from flask import Flask, request
#from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen
#from datetime import datetime, date
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    msg = ''
    data = request.json
    if data['status'] == 'ok' and data['events']:
      msg = data['events'][0]['message']['text']
    return msg

  elif request.method == 'GET':
    return 'toriniku'

if __name__ == '__main__':
  app.run()
