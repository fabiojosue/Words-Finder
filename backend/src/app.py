from crypt import methods
from flask import Flask, request, json, jsonify
from flask_cors import CORS
import controller

app = Flask(__name__)

@app.route('/book', methods=['POST'])
def createBook():
    book = request.files['book']
    book.save('./staticFiles/currentBook.pdf')
    return controller.interactBook(request.form['words'].lower(),'./staticFiles/currentBook.pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5000)