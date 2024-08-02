from peewee import SqliteDatabase, Model, CharField, DateTimeField

db = SqliteDatabase('src/backend/meu-chat.db')

class Chat(Model):
    name = CharField()
    history = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    class Meta:
	    database = db # This model uses the "people.db" database.

     
db.connect()
db.create_tables([Chat])


Chat(name='test', history=[], created_at="2022", updated_at="2022").save()