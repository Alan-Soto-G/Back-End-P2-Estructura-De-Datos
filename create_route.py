import json
import os
import random
from pathlib import Path

from model.graph import Graph
from model import requirements
from database.id_generator import IDManager
from model.management import get_user_map  # función para obtener el mapa del usuario

# Rutas de archivos
USER_ROUTES_PATH = os.path.join("database", "user_routes.json")

def build_graph_from_map(user_map):
    """
    Construye un objeto Graph a partir de la información del mapa (points y edges).
    Adicionalmente, inyecta un método get_node para acceso a la información del nodo.
    """
    g = Graph()
    # Creamos un diccionario para obtener la info del nodo por id.
    node_info = {}
    for point in user_map["points"]:
        node_info[point["id"]] = point
        g.add_node(point["id"], node=point["id"], description=point["description"], risk_level=point["risk_level"])
    # Inyectamos get_node para que retorne un objeto similar con atributo risk_level
    g.get_node = lambda node: type("Node", (), node_info[node])
    # Agregar las aristas
    for edge in user_map["edges"]:
        n1 = edge["from"]
        n2 = edge["to"]
        weight = edge["distance_meters"]
        directed = edge.get("directed", False)
        g.add_edge(n1, n2, weight, directed)
    return g

def create_route_for_method(route_tuple, method_name):
    """
    Dado un route_tuple (o similar) obtenida de alguno de los métodos de requirements,
    genera un objeto ruta siguiendo la estructura especificada.
    
    Se asume que route_tuple para las rutas es de la forma (points, avg_risk, distance).
    """
    if not route_tuple:
        return None
    points, avg_risk, distance = route_tuple
    duration = (distance / 1000) * (60 / 15)  # (distance/1000)*4
    return {
        "route_id": None,  # Se asigna posteriormente
        "name": "Ruta generada",
        "popularity": random.randint(1, 5),
        "difficulty": avg_risk,
        "points": points,
        "distance_meters": distance,
        "duration_minutes": duration,
        "method": method_name
    }

def create_min_distance_route(min_distance_dict):
    """
    Crea una 'ruta' a partir del dict de distancias obtenido por min_distances_from.
    Se asigna null en campos que no apliquen.
    """
    return {
        "route_id": None,
        "name": "Ruta generada",
        "popularity": random.randint(1, 5),
        "difficulty": None,
        "points": None,
        "distance_meters": None,
        "duration_minutes": None,
        "min_distances": min_distance_dict,
        "method": "min_distances_from"
    }

def save_routes_for_user(user_id, new_routes):
    """
    Guarda las rutas para el usuario en database/user_routes.json.
    Si no existe la llave del usuario se crea, de lo contrario se añaden al array existente.
    """
    # Cargar archivo
    if os.path.exists(USER_ROUTES_PATH):
        with open(USER_ROUTES_PATH, "r") as file:
            data = json.load(file)
    else:
        data = {"users": {}}
    
    user_key = str(user_id)
    if user_key not in data["users"]:
        data["users"][user_key] = []
    
    data["users"][user_key].extend(new_routes)
    
    with open(USER_ROUTES_PATH, "w") as file:
        json.dump(data, file, indent=4)

def create(user_id, start, end, experience, risk_level, user_distance):
    """
    Función que genera las rutas utilizando los métodos auxiliares de requirements.
    Se actualiza el archivo database/ids.json para el correcto manejo del id de ruta y
    se almacena en database/user_routes.json.
    Los métodos utilizados son:
      - route_according_to_experience
      - safest_route
      - route_according_to_distance_and_difficulty
      - proposed_routes
      - min_distances_from
    """
    # Obtener mapa del usuario y construir grafo
    user_map = get_user_map(user_id)
    if not user_map:
        print("Mapa del usuario no encontrado.")
        return False

    g = build_graph_from_map(user_map)

    routes_generated = []

    # 1. route_according_to_experience
    route_exp = requirements.route_according_to_experience(start, end, g, experience)
    if route_exp[0] is not None:
        new_route = create_route_for_method(route_exp, "route_according_to_experience")
        routes_generated.append(new_route)

    # 2. safest_route
    route_safe = requirements.safest_route(start, end, g)
    if route_safe[0] is not None:
        new_route = create_route_for_method(route_safe, "safest_route")
        routes_generated.append(new_route)

    # 3. route_according_to_distance_and_difficulty
    route_distance = requirements.route_according_to_distance_and_difficulty(start, end, user_distance, g, risk_level)
    if route_distance[0] is not None:
        new_route = create_route_for_method(route_distance, "route_according_to_distance_and_difficulty")
        routes_generated.append(new_route)

    # 4. proposed_routes
    proposals = requirements.proposed_routes(start, end, user_distance, g, risk_level, experience)
    if proposals:
        for proposal in proposals:
            new_route = create_route_for_method(proposal, "proposed_routes")
            routes_generated.append(new_route)
    
    # 5. min_distances_from (se retorna un dict, se guarda aparte en la ruta)
    min_distances = requirements.min_distances_from(start, g)
    if min_distances:
        new_route = create_min_distance_route(min_distances)
        routes_generated.append(new_route)

    if not routes_generated:
        print("No se generaron rutas.")
        return False

    # Actualizar id de ruta con IDManager (actualiza el archivo database/ids.json)
    id_manager = IDManager()
    for route in routes_generated:
        new_id = id_manager.get_new_route_id(user_id)
        route["route_id"] = new_id

    # Guardar las rutas en database/user_routes.json
    save_routes_for_user(user_id, routes_generated)
    return True