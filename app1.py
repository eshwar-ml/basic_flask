from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return  conn

# books_list = [
#     {
#         "id":0,
#         "author":"Chinua Achebe",
#         "language":"English",
#         "title":"Things Fall Apart",
#     },
#         {
#         "id":1,
#         "author":"Hans Christian",
#         "language":"Danish",
#         "title":"Fairy tales",
#     },
#         {
#         "id":2,
#         "author":"FF",
#         "language":"English",
#         "title":"The Mysterious Case"
#     },
#         {
#         "id":3,
#         "author":"Samuel Beckett",
#         "language":"English, French",
#         "title":"Molly, Malone Dies, The Unnamable, The Trilogy",
#     },
#         {
#         "id":4,
#         "author":"Giovanni Boccanccio",
#         "language":"Italian",
#         "title":"The Decameron"
#     },
#         {
#         "id":5,
#         "author":"Jorge Luis Borges",
#         "language":"Spanish",
#         "title":"Ficciones"
#     },
# ]

@app.route("/books", methods=["GET","POST"])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == "POST":

        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author, language, title) 
                VALUES(?, ?, ?)"""
        cursor = conn.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully" , 201
        # iD = [max(zip(books_list.values(), books_list.keys()))[0] +1]

        # new_obj = {
        #     'id':iD,
        #     'author':new_author,
        #     'language':new_lang,
        #     'title':new_title
        # }
        # books_list.append(new_obj)
        # return jsonify(books_list), 201


@app.route('/book/<int:id>', methods=['GET','PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404
        
    if request.method == 'PUT':
        sql = """UPDATE book
                SET title=?,
                    author=?,
                    language=?
                WHERE id=?"""
        # for book in books_list:
        #     if book['id'] == id:
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        updated_book = {
                'id':id,
                'author': author,
                'language': language,
                'title': title
                 }
        conn.execute(sql, (author, language, title, id))
        conn.commit()
        return jsonify(updated_book)
    
    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        # for index, book in enumerate(books_list):
        #     if book['id'] == id:
        #         books_list.pop(index)
        return "The book with id: {} has been deleted.".format(id), 200


if __name__ == '__main__':
    app.run()