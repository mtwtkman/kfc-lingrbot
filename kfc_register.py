from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import KFC

import os

engine = create_engine(os.getenv('POSTGRESQL_TORI'))
Session = sessionmaker(bind=engine)
session = Session()

kfc_msg = ('ある程度我慢を覚えろよ', '唐揚げでも食ってろ', 'お経でも読んで落ち着いてください',
           'これも全て私の責任です', '空腹は最高の調味料というじゃないですか', 'てんや行こうぜ',
           'しばらく我慢しろ', '君は我慢できるかな?', '自暴自棄になるのだけは勘弁な',
           '大人の対応を頼むよ', 'これ以上誰も傷つけたくない…', '`止まない雨はない`ってね…',
           'もうちょっと我慢しろ', 'いい子で待っててね', '早く一緒に食べたいね',
           '待ちきれないかな？じゃあクソして寝ろ', 'それも定かではない', 'ちゃんと野菜食ってるか?',
)

messages = [KFC(pattern=msg, created_by='boku') for msg in kfc_msg]
session.add_all(messages)
session.commit()
