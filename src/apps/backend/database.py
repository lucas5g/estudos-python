from peewee import SqliteDatabase, Model, CharField, DateTimeField

db = SqliteDatabase('src/apps/backend/meu-chat.db')

class Chat(Model):
    name = CharField()
    history = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    class Meta:
	    database = db # This model uses the "people.db" database.

     
db.connect()
db.create_tables([Chat])

