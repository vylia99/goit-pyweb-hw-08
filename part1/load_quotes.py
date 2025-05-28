import json
import connect
from models import Quote, Author


with open("quotes.json", encoding="utf-8") as file:
    quotes = json.load(file)

for q in quotes:
    author = Author.objects(fullname=q["author"]).first()
    if author:
        quote = Quote(
            tags=q["tags"],
            author=author,
            quote=q["quote"]
        )
        quote.save()
