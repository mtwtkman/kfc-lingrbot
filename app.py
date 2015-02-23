# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta
import pytz
from calendar import monthrange
import re, random, os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_POSTGRESQL_VIOLET_URL') if os.getenv('IS_HEROKU') else os.getenv('POSTGRESQL_TORI')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

# models {{{
class KFC(db.Model):
    __tablename__ = 'kfc'
    id = db.Column(db.Integer, primary_key=True)
    ptn_id = db.Column(db.Integer, unique=True)
    pattern = db.Column(db.String(256), unique=True)
    created_by = db.Column(db.String(256))

    def __repr__(self):
        return '<KFC Pattern %r>' % self.pattern

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    rooms = db.relationship('Room', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    roomneme = db.Column(db.String(256), unique=True)
    counter = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Room %r>' % self.roomneme
# }}}

@app.route('/', methods=['GET', 'POST']) # {{{
def index():
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
            nickname = message_data['nickname']
            room = message_data['room']
            # pattern{{{
            kfc_hit = re.compile(r'[KＫ][･・]?[FＦ][･・]?[CＣ][!！]?')
            make_pattern = re.compile(r'(^!kfc)\s(.+$)')
            modify_pattern = re.compile(r'(^!kfc!)\s([0-9]+)\s(.+)?')
            remove_pattern = re.compile(r'(^!kfc!!)\s([0-9]+)$')
            search_pattern = re.compile(r'(^!kfc\?)\s([0-9]+)')
            help_pattern = re.compile(r'^!kfc-help$')
            # }}}
            if re.search(kfc_hit, text):
                return tori()
            elif re.search(make_pattern, text):
                pattern = re.search(make_pattern, text).group(2)
                if KFC.query.filter_by(pattern=pattern).first():
                    return '重複してますよ。'
                ptn_id_list = sorted([i.ptn_id for i in KFC.query.filter(KFC.ptn_id>0).all()])
                ptn_id = max(ptn_id_list) + 1
                print(ptn_id)
                for i in range(1, ptn_id):
                    if ptn_id_list[i-1] is not i:
                        ptn_id = i
                        break
                print(ptn_id)
                kfc = KFC(ptn_id=ptn_id, pattern=pattern, created_by=nickname)
                db.session.add(kfc)
                db.session.commit()
                return '{} さんが "{}" を登録しました。(id: {})'.format(nickname, pattern, ptn_id)
            elif re.search(modify_pattern, text):
                [_, ptn_id, new_ptn] = [i for i in re.search(modify_pattern, text).groups()]
                if KFC.query.filter_by(pattern=new_ptn).first():
                    return '重複してますよ。'
                target = KFC.query.filter_by(ptn_id=int(ptn_id)).first()
                if target:
                    target.pattern = new_ptn
                    return 'id:{}を{}さんが変更しました。' .format(ptn_id, nickname)
            elif re.search(remove_pattern, text):
                ptn_id = int(re.search(remove_pattern, text).group(2))
                target = KFC.query.filter_by(ptn_id=ptn_id).first()
                if target:
                    db.session.delete(target)
                    db.session.commit()
                    return '{}さんが作成したid:{}\n"{}"を{}さんが削除しました。'.format(target.created_by, ptn_id, target.pattern, nickname)
                else:
                    return '登録のないidです。'
            elif re.search(search_pattern, text):
                ptn_id = int(re.search(search_pattern, text).group(2))
                target = KFC.query.filter_by(ptn_id=int(ptn_id)).first()
                if target:
                    return 'id:{}は{}さんが作成しました。\ntext: {}'.format(ptn_id, target.created_by, target.pattern)
                else:
                    return '登録のないidです。'

            elif re.search(help_pattern, text):
                return '\n'.join(['とりの日:', '  KFCを含むメッセージ', '作成:', '  !kfc メッセージ',
                                  '変更:', '  !kfc! id メッセージ', '削除:', '  !kfc!! id',
                                  '検索:', '  !kfc? id']).strip()
    elif request.method == 'GET':
        return 'toriniku'
# }}}

@app.route('/pattern') # {{{
def pattern():
    patterns = {k.ptn_id: {'pattern': k.pattern, 'created_by': k.created_by} for k in KFC.query.all()}
    return render_template('pattern.html', patterns=patterns)
# }}}

def tori(): # {{{
    kfc_msg = [k.pattern for k in KFC.query.all()]
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
        return 'とりの日パックまであと{}日{}'.format(left_days.days, random.choice(kfc_msg))
# }}}

if __name__ == '__main__':
    app.run()
