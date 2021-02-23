from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from api_constants import mongodb_password, database_name
# pylint: disable=E1101
app = Flask(__name__)



DB_URI = "mongodb+srv://david:{}@clustermongo.skqmh.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_password, database_name)

app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


class Book(db.Document):
    book_id = db.IntField()
    name = db.StringField()
    author = db.StringField()

    def to_json(self):
        #convert this document to JSON
        return {
            "book_id": self.book_id,
            "name": self.name,
            "author": self.author
        }
'''
Populate api
'''
@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    book1 = Book(book_id=1, name="A Game Of Thrones", author="LutherKing")
    book2 = Book(book_id=2, name="Attack On Titan", author="isayama")
    book1.save()
    book2.save()
    return make_response("", 201)

'''
books api
'''
@app.route('/api/books', methods=['GET', 'POST'])
def api_books():
    if request.method == "GET":
        books = []
        for book in Book.objects:
            books.append(book)
        return make_response(jsonify(books), 200)
    elif request.method == "POST":
        '''
        Sample Request Body
        {
            "book_id": 1,
            "name": "Attack On Titan",
            "author": "Jo Dan Tae"
        }
        '''
        content = request.json
        book = Book(book_id=content['book_id'],
        name=content['name'],
        author=content['author'])
        book.save()
        return make_response("", 200)
'''
per books api
'''
@app.route('/api/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(book_id):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

if __name__ == '__main__':
    app.run()
