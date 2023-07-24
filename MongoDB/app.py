from connect import mongo_user, mongodb_pass, domain, db_name
from pymongo import MongoClient
from main import Author, Quote

client = MongoClient(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority
""", ssl=True)


def find_by_name(*args):
    print("Searching for name:", args)

    try:
        author = Author.objects(fullname=args).get()
        quotes = Quote.objects(author=author)
        quotes_list = []
        for q in quotes:
            quotes_list.append(q.quote)
        return quotes_list
    except Exception as e:
        print("Error during name search:", e)
        return []


def find_by_tag(*args):
    quotes = Quote.objects(*args)
    quotes_list = []
    for q in quotes:
        quotes_list.append(q.quote)
    return quotes_list


def find_by_tags(*args):
    quotes = Quote.objects(__raw__={*args})
    quotes_list = []
    for q in quotes:
        quotes_list.append(q.quote)
    return quotes_list


commands = {
    "name": find_by_name,
    "tag": find_by_tag,
    "tags": find_by_tags
}


def parse(command):
    func, arguments = command.split(":")
    return func, arguments


def print_quotes(quotes):
    for q in quotes:
        print(q)
    if not quotes:
        print("Quotes not found")


def main():
    while True:
        command = input()
        if command == "exit":
            return
        data = parse(command)
        try:
            print_quotes(data[0](data[1]))
        except:
            print("Quotes not found")


if '__main__' == __name__:
    main()