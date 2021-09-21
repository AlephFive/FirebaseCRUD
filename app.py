#some parts used https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run
#https://medium.com/google-cloud/building-a-flask-python-crud-api-with-cloud-firestore-firebase-and-deploying-on-cloud-run-29a10c502877

# Required imports
import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
sticky_notes_ref = db.collection('sticky_notes')



#HOMEPAGE
@app.route('/')
def home():
    return render_template('index.html')


#CREATE A STICKY
@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    print("REQ: ", request.json)
    try:
        id = request.json['id']
        print(id)
        sticky_notes_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"

#READ STICKY NOTES
@app.route('/read', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        if id:
            note = sticky_notes_ref.document(id).get()
            return jsonify(note.to_dict()), 200
        else:
            #no id
            return jsonify({"success": False}),200
    except Exception as e:
        return f"An Error Occured: {e}"

#MODIFY STICKY
@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        sticky_notes_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

#DELETE STICKY
@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        id = request.args.get('id')
        sticky_notes_ref.document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__ == '__main__':
    app.run(debug=True)