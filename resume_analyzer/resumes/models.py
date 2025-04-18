import mongoengine as me
from datetime import datetime


class Resume(me.Document):
    user_id = me.IntField(required=True)
    file_path = me.StringField(required=True)
    parsed_text = me.StringField()
    created_at = me.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'resumes'}
