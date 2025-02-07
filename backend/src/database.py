from flask import Flask, request,jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import uuid

class Firebase_Database:
    
    def __init__(self)->None:
        self.cred = credentials.Certificate("../firebase_config.json")
        firebase_admin.initialize_app(self.cred)
        self.db=firestore.client()
        self.app= Flask(__name__)
        CORS(self.app)
    
    def start(self):
        @self.app.route('/add_user', methods=['POST'])
        def add_user(self):
            data=request.json
            user_ref=self.db.collection('users').document(data[id])
            user_ref.set(data)
            return jsonify({"message":"User Added"}),201
        
        @self.app.route('/get_user', methods=['GET'])
        def get_user(self):
            users=self.db.collection('users').stream()
            userlist=[{**doc.to_dict(),"id":doc.id} for doc in users]
            return jsonify(userlist), 200
        
        @self.app.route('/add_signuture', methods=['POST'])
        def add_signuture(self):
            data= request.json
            
            if 'name' not in data:
                return jsonify({"error":{'Name Not Found!'}}),400
            if  'surname' not in data:
                return jsonify({"error":{'Surname Not Found!'}}),400
            if 'email' not in data:
                return jsonify({"error":{'E-Mail Not Found!'}}),400
            if 'message' not in data:
                return jsonify({"error":{'Message Not Found!'}}),400
            
            signature_id=str(uuid.uuid4())
            
            self.db.collection('signatures').document(signature_id).set(
                {
                    'name':data['name'],
                    'surname':data['surname'],
                    'email':data['email'],
                    'message':data['message'],
                    'timestamp':firestore.SERVER_TIMESTAMP
                }
            )
            
            return jsonify({"message":"The signature was successfully registered.", "id":signature_id}),201
        
        @self.app.route('/get_signuture', methods=['GET'])
        def get_signutures(self):
            signutures=self.db.collection('signatures').stream()
            signlist=[{**doc.to_dict(),'id':doc.id} for doc in signutures]
            return jsonify({signlist})
    
if __name__=='__main__':
    fd=Firebase_Database()
    fd.start()