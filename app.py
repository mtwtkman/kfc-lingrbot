# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import TextField, SubmitField

from datetime import datetime, timedelta
import pytz
from calendar import monthrange
import re
import random
import os
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_POSTGRESQL_VIOLET_URL') if os.getenv('IS_HEROKU') else os.getenv('POSTGRESQL_TORI')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = ''.join([random.choice(string.ascii_letters+string.digits) for i in range(50)])

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


# forms {{{
class EditForm(Form):
    pattern = TextField('text')
    edit = SubmitField('submit')
# }}}


@app.route('/', methods=['GET', 'POST'])  # {{{
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
            # room = message_data['room']
            # pattern{{{
            kfc_hit = re.compile(r'[KＫ][･・]?[FＦ][･・]?[CＣ][!！]?')
            marukame_hit = re.compile(r'^!kfc-udon$')
            create_pattern = re.compile(r'(^!kfc-c(reate)?)\s(.+$)')
            read_patternn = re.compile(r'(^!kfc-r(ead)?)\s([0-9]+)$')
            update_pattern = re.compile(r'(^!kfc-u(pdate)?)\s([0-9]+)\s(.+)?')
            delete_pattern = re.compile(r'(^!kfc-d(elete)?)\s([0-9]+)$')
            help_pattern = re.compile(r'^!kfc-h(elp)?$')
            # }}}
            if re.search(kfc_hit, text):
                return tori()
            elif re.search(marukame_hit, text):
                return marukame()
            elif re.search(create_pattern, text):
                pattern = re.search(create_pattern, text).group(3)
                if KFC.query.filter_by(pattern=pattern).first():
                    return '重複してますよ。'
                ptn_id_list = sorted([i.ptn_id for i in KFC.query.filter(KFC.ptn_id>0).all()])
                ptn_id = max(ptn_id_list) + 1
                for i in range(1, ptn_id):
                    if ptn_id_list[i-1] is not i:
                        ptn_id = i
                        break
                kfc = KFC(ptn_id=ptn_id, pattern=pattern, created_by=nickname)
                db.session.add(kfc)
                db.session.commit()
                return '{nickname} さんが "{pattern}" を登録しました。(id: {ptn_id})\n出力例: とりの日パックまであとn日{pattern}'.format(nickname=nickname, pattern=pattern, ptn_id=ptn_id)
            elif re.search(read_patternn, text):
                ptn_id = int(re.search(read_patternn, text).group(3))
                target = KFC.query.filter_by(ptn_id=int(ptn_id)).first()
                if target:
                    return 'id:{ptn_id}は{created_by}さんが作成しました。\n出力例: とりの日パックまであとn日{pattern}'.format(ptn_id=ptn_id, created_by=target.created_by, pattern=target.pattern)
                else:
                    return '登録のないidです。'
            elif re.search(update_pattern, text):
                [_, _, ptn_id, new_ptn] = [i for i in re.search(update_pattern, text).groups()]
                if KFC.query.filter_by(pattern=new_ptn).first():
                    return '重複してますよ。'
                target = KFC.query.filter_by(ptn_id=int(ptn_id)).first()
                if target:
                    target.pattern = new_ptn
                    return '{nickname}さんがid:{ptn_id}を変更しました。\n出力例: とりの日パックまであとn日{new_ptn}' .format(nickname=nickname, ptn_id=ptn_id, new_ptn=new_ptn)
                else:
                    return '登録のないidです。'
            elif re.search(delete_pattern, text):
                ptn_id = int(re.search(delete_pattern, text).group(3))
                target = KFC.query.filter_by(ptn_id=ptn_id).first()
                print(target)
                if target:
                    db.session.delete(target)
                    db.session.commit()
                    return '{created_by}さんが作成したid:{ptn_id}\n"{pattern}"を{nickname}さんが削除しました。'.format(created_by=target.created_by, ptn_id=ptn_id, pattern=target.pattern, nickname=nickname)
                else:
                    return '登録のないidです。'
            elif re.search(help_pattern, text):
                return '\n'.join(['作成:', '!kfc-c(reate) <text>',
                                  '検索:', '!kfc-r(ead) <id>',
                                  '変更:', '!kfc-u(pdate) <id> <text>',
                                  '削除:', '!kfc-d(elete) <id>',
                                  'パターン一覧:', 'http://toriniku.herokuapp.com/pattern'])
    elif request.method == 'GET':
        return 'toriniku'
# }}}


@app.route('/pattern')  # {{{
def pattern():
    # form = EditForm()
    patterns = {k.ptn_id: {'pattern': k.pattern, 'created_by': k.created_by} for k in KFC.query.all()}
    return render_template('pattern.html', patterns=patterns)
# }}}


def tori():  # {{{
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


def marukame():  # {{{
    today = datetime.now(pytz.timezone('Asia/Tokyo'))
    if today.day is 1:
        return '今日は丸亀製麺の釜揚げうどんが半額ですよ！！！急いで！！！'
    else:
        year, month, day = today.year, today.month, today.day
        last_day = monthrange(year, month)[1]
        left_days = timedelta(last_day - day)
        return 'ところで、物の本によると丸亀製麺の釜揚げうどん半額まであと{}日なんだってね'.format(left_days.days)
# }}}

if __name__ == '__main__':
    app.run()
