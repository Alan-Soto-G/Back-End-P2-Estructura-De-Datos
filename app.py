from flask import Flask, request, jsonify
from flask_cors import CORS
from model import management
import create_route

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

@app.route('/user-map', methods=['POST'])
def get_user_map():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({'error': 'No se recibió JSON válido con "user_id"'}), 400

    result = management.get_user_map(data["user_id"])
    if result is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify(result), 200

@app.route('/get-user-data', methods=['POST'])
def get_user():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({'error': 'No se recibió JSON'}),400
    
    user = management.get_user(data["user_id"])
    if user is None:
        return jsonify({'error': 'Usuario no encontrado'}),404
    
    return jsonify(user),200

@app.route('/submit-route', methods=['POST'])
def create_routes():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibió JSON'}), 400

    result = create_route.create(
        data["user_id"], 
        data["start"],  
        data["end"],    
        data["experience"], 
        data["risk_level"], 
        data["user_distance"]
    )

    if result:
        return jsonify({'success': "Ruta creada con éxito"}), 200
    else:
        return jsonify({'error': 'No se pudo crear la ruta'}), 400

@app.route('/get-user-routes', methods=['POST'])
def get_user_routes():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({'error': 'No se recibió JSON válido con "user_id"'}), 400
    routes = management.get_user_routes(data["user_id"])
    return jsonify({"routes": routes}), 200

@app.route('/delete-node', methods=['POST'])
def delete_node_route():
    data = request.get_json()
    if not data or "user_id" not in data or "point_id" not in data:
        return jsonify({'error': 'Se requiere user_id y point_id'}), 400
    result = management.delete_node(data["user_id"], data["point_id"])
    if result:
        return jsonify({'success': 'Nodo y rutas asociadas eliminados'}), 200
    else:
        return jsonify({'error': 'No se pudo eliminar el nodo'}), 400
    
if __name__ == '__main__':
    app.run(debug=True)