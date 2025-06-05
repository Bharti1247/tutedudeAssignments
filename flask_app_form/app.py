from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from urllib.parse import quote_plus

passDB = quote_plus("MongoDB@1247")

app = Flask(__name__)

MONGO_URI = f"mongodb+srv://mongo:{passDB}@testcluster.8btdbnj.mongodb.net/?retryWrites=true&w=majority&appName=testCluster"

client = MongoClient(MONGO_URI)
db = client["testdb"]                
collection = db["testcollection"] 

@app.route('/', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        userID = request.form.get('userID')
        password = request.form.get('password')
        if not userID or not password:
            error = "Both fields are required."
        else:
            try:
                collection.insert_one({"userID": userID, "password": password})
                return redirect(url_for('success'))
            except Exception as e:
                error = f"Error inserting into database: {e}"
    return render_template('form.html', error=error)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
