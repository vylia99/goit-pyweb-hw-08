from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    sent = BooleanField(default=False)
    phone = StringField()
    notes = StringField()
