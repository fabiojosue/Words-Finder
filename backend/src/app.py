from crypt import methods
from flask import Flask, request, json, jsonify
from flask_cors import CORS
import controller

app = Flask(__name__)
CORS(app)

app.config['HDFS_URI'] = 'hdfs://172.17.0.01:9000/tmp/csv/'
app.config['IMPALA_URI'] = '172.17.0.1:21050'

#conexiones
# mongo = PyMongo(app)

#endpoints

@app.route('/book', methods=['POST'])
def createBook():
    book = request.files['book']
    book.save('./staticFiles/currentBookTest.pdf')
    return controller.saveHDFS('./staticFiles/currentBookTest.pdf')

@app.route('/words', methods=['GET','DELETE'])
def countWords():
     if request.method == 'POST':
         return 
     else:
         return controller.test()

@app.route('/words', methods=['DELETE'])
def deleteBook():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)