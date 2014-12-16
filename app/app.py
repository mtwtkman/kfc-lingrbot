from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    return 'receive'
  elif request.method == 'GET':
    return 'hoge'

if __name__ == '__main__':
  app.run(debug=True)
