from peewee import (
    Model,
    SqliteDatabase,
    PrimaryKeyField,
    TextField,
    DateTimeField,
    SQL,
)

db = SqliteDatabase("estudos.db")


class Chat(Model):
    id = PrimaryKeyField()
    messages = TextField()
    created_at = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )  # Data e hora de criação
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = db


db.connect()

db.create_tables([Chat])

if __name__ == "main":

    messages = [{"rule": "user", "content": "Ola"}]
