# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import KFC

import os
engine = create_engine(os.getenv('HEROKU_POSTGRESQL_VIOLET_URL') if os.getenv('IS_HEROKU') else os.getenv('POSTGRESQL_TORI'))
Session = sessionmaker(bind=engine)
session = Session()

kfc_msg = ('なんだけどある程度我慢を覚えろよ', 'なんだけど唐揚げでも食ってろ', 'なんだけどお経でも読んで落ち着いてください',
           'なんだけどこれも全て私の責任です', 'なんだけど空腹は最高の調味料というじゃないですか', 'なんだけどてんや行こうぜ',
           'なんだけどしばらく我慢しろ', 'なんだけど君は我慢できるかな?', 'なんだけど自暴自棄になるのだけは勘弁な',
           'なんだけど大人の対応を頼むよ', 'なんだけどこれ以上誰も傷つけたくない…', 'なんだけど"止まない雨はない"ってね…',
           'なんだけどもうちょっと我慢しろ', 'なんだけどいい子で待っててね', 'なんだけど早く一緒に食べたいね',
           'なんだけど待ちきれないかな？じゃあクソして寝ろ', 'なんだけどそれも定かではない', 'なんだけどちゃんと野菜食ってるか?',
)

messages = [KFC(ptn_id=int(i+1), pattern=msg, created_by='boku') for i, msg in enumerate(kfc_msg)]
session.add_all(messages)
session.commit()
