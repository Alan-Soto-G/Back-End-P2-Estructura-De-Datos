from flask import Flask, request, jsonify
from flask_cors import CORS
from model import management

app = Flask(__name__)
CORS(app)

@app.route('/new-user', methods=['POST'])
def sign_in():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibió JSON'}), 400
    return management.add_user(data)

@app.route('/login-user', methods=['POST'])
def login():
    print("Login")
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibió JSON'}), 400
    
    user_id, user_data = management.login(data["username"], data["password"])
    if user_id is None:
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
    
    return jsonify(
        {
            "success": True,
            "user": {
                "user_id": user_id,
                "name": user_data["name"],
                "username": user_data["username"],
            }
        }
    ), 200

if __name__ == '__main__':
    app.run(debug=True)