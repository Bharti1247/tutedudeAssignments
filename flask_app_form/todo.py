from flask import Flask, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import quote_plus

passDB = quote_plus("MongoDB@1247")

app = Flask(__name__)

MONGO_URI = f"mongodb+srv://mongo:{passDB}@testcluster.8btdbnj.mongodb.net/?retryWrites=true&w=majority&appName=testCluster"

client = MongoClient(MONGO_URI)
db = client["todo_db"]
todo_collection = db["todo_items"]

@app.route('/submittodoitem', methods=['POST', 'GET'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    if not item_name or not item_description:
        return "Missing data", 400

    todo_data = {
        "name": item_name,
        "description": item_description
    }

    result = todo_collection.insert_one(todo_data)
    
    return jsonify({
        "message": "Data inserted successfully",
        "id": str(result.inserted_id)
    }), 201

if __name__ == '__main__':
    app.run(debug=True)

