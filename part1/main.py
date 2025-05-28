import connect
from models import Author, Quote

#connect(db="quotes_db", host="your_full_mongo_uri")  # заміни на свій URI

def find_by_author(name):
    author = Author.objects(fullname=name).first()
    if not author:
        print("Автор не знайдений.")
        return
    quotes = Quote.objects(author=author)
    for q in quotes:
        print(q.quote)

def find_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for q in quotes:
        print(q.quote)

def find_by_tags(tags_str):
    tags = tags_str.split(',')
    quotes = Quote.objects(tags__in=tags)
    for q in quotes:
        print(q.quote)

def main():
    print("Команди:\nname:<author>\ntag:<tag>\ntags:<tag1,tag2>\nexit")
    while True:
        command = input(">>> ").strip()
        if command == "exit":
            break
        elif command.startswith("name:"):
            find_by_author(command[5:].strip())
        elif command.startswith("tag:"):
            find_by_tag(command[4:].strip())
        elif command.startswith("tags:"):
            find_by_tags(command[5:].strip())
        else:
            print("Невідома команда")

if __name__ == "__main__":
    main()
