import json
import connect
from models import Author

with open("authors.json", encoding="utf-8") as file:
    authors = json.load(file)

for a in authors:
    author = Author(
        fullname=a["fullname"],
        born_date=a["born_date"],
        born_location=a["born_location"],
        description=a["description"]
    )
    author.save()

