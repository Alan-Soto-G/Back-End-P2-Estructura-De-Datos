from . import graph
import json
from database.id_generator import IDManager
PATH_USERS="database/users.json"
PATH_ROUTES="database/user_routes.json"
PATH_TEMP_ROUTES="database/temp_user_routes.json"
PATH_MAPS="database/user_map.json" 

id_manager = IDManager()

def edit_point (point_id, user_id, new_data):
    """
    Edit a point in the user's map.
    """
    user_id_str = str(user_id)

    with open(PATH_MAPS, "r") as file:
        data = json.load(file)
    
    # Buscar y actualizar el punto
    for point in data["users"][user_id_str]["points"]:
        if point["id"] == point_id:
            point.update(new_data)
            break

    with open(PATH_MAPS, "w") as file:
        json.dump(data, file, indent=4)

def save_routes(g: graph.Graph, user_id):
    user_id_str = str(user_id)

    # Cargar archivo temporal
    with open(PATH_TEMP_ROUTES, "r") as file:
        data_temp = json.load(file)

    # Cargar archivo principal
    with open(PATH_ROUTES, "r") as file:
        data = json.load(file)

    # Asegurar que la clave 'users' existe
    if "users" not in data:
        data["users"] = {}

    if user_id_str not in data["users"]:
        data["users"][user_id_str] = {}

    # Extraer rutas del temporal
    rutas_temp = data_temp.get("users", {}).get(user_id_str, {})

    # Concatenar las rutas (sobrescribe si ya existe una ruta con la misma clave)
    data["users"][user_id_str].update(rutas_temp)

    # Guardar archivo principal actualizado
    with open(PATH_ROUTES, "w") as file:
        json.dump(data, file, indent=4)


def delete_route (g:graph.Graph, route_id, user_id, option):
    """
    Delete a route from the user's routes.
    """
    user_id_str = str(user_id)
    condition = PATH_ROUTES if option == 1 else PATH_TEMP_ROUTES

    with open(condition, "r") as file:
        data = json.load(file)

    # delete route if it exists
    if route_id in data["users"][user_id_str]:
        del data["users"][user_id_str][route_id]

    with open(condition, "w") as file:
        json.dump(data, file, indent=4)

def delete_route_due_to_a_point (point_id, user_id):

    user_id_str = str(user_id)

    with open(PATH_ROUTES, "r") as file:
        data = json.load(file)

    # Eliminar rutas que usan el punto
    user_routes = data["users"].get(user_id_str, {})
    routes_to_delete = [
        route_id for route_id, route in user_routes.items()
        if point_id in route.get("path", [])
    ]
    
    for route_id in routes_to_delete:
        del user_routes[route_id]

    with open(PATH_ROUTES, "w") as file:
        json.dump(data, file, indent=4)

def add_user (user_data):
    """
    Add a new user to the users.json file.
    """
    with open(PATH_USERS, "r") as file:
        data = json.load(file)

    for user in data["users"].values():
        if user["username"] == user_data["username"]:
            return {"success": False, "message": "El nombre de usuario ya está en uso."}

    user_id_str = str(id_manager.create_new_user())

    new_user = {
        "name": user_data["name"],
        "username": user_data["username"],
        "password": user_data["password"],
        "birth_date": None,
        "avatar": None,
        "registration_date": user_data["registration_date"],
        "biography": "No bio yet.",
        "experience": user_data["experience"]
    }
    
    data["users"][user_id_str] = new_user

    with open(PATH_USERS, "w") as file:
        json.dump(data, file, indent=4)

    # Create a new map for the user
    with open("database/map_predefined.json", "r") as file:
        map_data = json.load(file)
    
    with open(PATH_MAPS, "r") as file:
        map_data_users = json.load(file)

    map_data_users["users"][user_id_str] = {
        "points": map_data["points"],
        "edges": map_data["edges"]
    }

    with open(PATH_MAPS, "w") as file:
        json.dump(map_data_users, file, indent=4)    

    return {"success": True, "message": "Usuario registrado exitosamente", "user_id": user_id_str}

def delete_user (user_id):
    """
    Delete a user from the users.json file.
    """
    user_id_str = str(user_id)
    with open(PATH_USERS, "r") as file:
        data = json.load(file)

    data["users"].pop(user_id_str)

    with open(PATH_USERS, "w") as file:
        json.dump(data, file, indent=4)

    # delete user routes and maps
    for path in [PATH_ROUTES, PATH_TEMP_ROUTES, PATH_MAPS]:
        with open(path, "r") as file:
            file_data = json.load(file)
        file_data["users"].pop(user_id_str, None)
        with open(path, "w") as file:
            json.dump(file_data, file, indent=4)

def update_user (user_id, user_data):
    """
    Update user data in the users.json file.
    """
    user_id_str = str(user_id)
    with open(PATH_USERS, "r") as file:
        data = json.load(file)

    data["users"][user_id_str].update(user_data)

    with open(PATH_USERS, "w") as file:
        json.dump(data, file, indent=4)

def login (username, password):
    """
    Check if the user exists and the password is correct.
    """
    with open(PATH_USERS, "r") as file:
        data = json.load(file)

    for user_id_str, user_data in data["users"].items():
        if user_data["username"] == username and user_data["password"] == password:
            return int(user_id_str), user_data

    return None, None

def get_user_map (user_id):
    """
    Get the user's map data.
    """
    user_id_str = str(user_id)

    with open(PATH_MAPS, "r") as file:
        data = json.load(file)

    user_data = data["users"].get(user_id_str, None)

    if user_data:
        return {
            "points": user_data["points"],
            "edges": user_data["edges"]
        }
    return None

def get_user (user_id):
    """
    Get the user's data.
    """
    user_id_str = str(user_id)

    with open(PATH_USERS, "r") as file:
        data = json.load(file)

    user_data = data["users"].get(user_id_str, None)

    if user_data:
        return {
            "name": user_data["name"],
            "username": user_data["username"],
            "password": user_data["password"],
            "birth_date": user_data["birth_date"],
            "avatar": user_data["avatar"],
            "registration_date": user_data["registration_date"],
            "biography": user_data["biography"],
            "experience": user_data["experience"]
        }
    return None

def get_user_routes(user_id):
    """
    Retorna todas las rutas del usuario a partir de su id.
    """
    user_id_str = str(user_id)
    try:
        with open("database/user_routes.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    return data.get("users", {}).get(user_id_str, [])